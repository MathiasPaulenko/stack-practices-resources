"""Full RAG pipeline: embed -> retrieve -> rerank -> assemble -> generate.

One class owns the index handle, embedder, and reranker; answer() runs the
whole query path. Two details that matter in production code that demos skip:

- The embedder and reranker are CPU-bound, so in an async service they run
  via asyncio.to_thread — otherwise they block the event loop for every
  concurrent request. The (sync) vector-store call goes through a thread too.
- Retrieval fetches top_k * 4 candidates so reranking has room to work.

What this version does NOT do: retries, timeouts, tracing, eval hooks.
Those aren't optional in production — instrument each stage separately
(embed / vector search / rerank / LLM) so p95 regressions point at a stage.
"""
import asyncio
import math
from typing import Any, Dict, List

CHAT_MODEL = "gpt-4o"  # check latest docs for current model names
TEMPERATURE = 0.3  # low temperature: factual answering, not creativity


def _default_embedder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer('all-MiniLM-L6-v2')


def _default_reranker():
    from sentence_transformers import CrossEncoder

    return CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')


def _default_llm_client():
    from openai import AsyncOpenAI

    return AsyncOpenAI()  # requires OPENAI_API_KEY


class RAGPipeline:
    def __init__(
        self,
        collection: Any,
        embedder: Any = None,
        reranker: Any = None,
        llm_client: Any = None,
        chat_model: str = CHAT_MODEL,
        max_context_tokens: int = 4000,
    ):
        """collection: a vector store with .query(query_embeddings=..., n_results=...)
        returning Chroma-shaped results (see vector_stores.py).
        embedder/reranker/llm_client default to the production models/clients
        but accept any object with the same interface — handy for tests.
        """
        self.collection = collection
        self.embedder = embedder if embedder is not None else _default_embedder()
        self.reranker = reranker if reranker is not None else _default_reranker()
        self.llm_client = llm_client if llm_client is not None else _default_llm_client()
        self.chat_model = chat_model
        self.max_context_tokens = max_context_tokens

    def _encode_query(self, query: str) -> List[float]:
        emb = self.embedder.encode(query)
        return emb.tolist() if hasattr(emb, "tolist") else list(emb)

    async def answer(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        # CPU-bound work goes through asyncio.to_thread so the event loop
        # stays free for concurrent requests.
        query_embedding = await asyncio.to_thread(self._encode_query, query)

        # Over-retrieve: reranking needs a wider candidate pool than top_k.
        results = await asyncio.to_thread(
            self.collection.query,
            query_embeddings=[query_embedding],
            n_results=top_k * 4,
        )

        documents = results["documents"][0]
        raw_metadatas = (results.get("metadatas") or [[]])[0] or []
        metadatas = [m or {} for m in raw_metadatas]
        # Pad defensively: a store may return fewer metadata entries than docs.
        metadatas += [{}] * (len(documents) - len(metadatas))

        pairs = [(query, doc) for doc in documents]
        scores = await asyncio.to_thread(self.reranker.predict, pairs)

        ranked = sorted(
            zip(documents, scores, metadatas),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        context_parts, sources = [], []
        for i, (doc, score, metadata) in enumerate(ranked):
            context_parts.append(f"[Source {i + 1}]: {doc}")
            sources.append({
                "source": metadata.get("source", "unknown"),
                "relevance_score": float(score),
            })

        messages = [
            {
                "role": "system",
                "content": (
                    "Answer based on the context. Cite source numbers. "
                    "If the context is insufficient, say you don't know."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{'\n\n'.join(context_parts)}\n\nQuestion: {query}",
            },
        ]

        response = await self.llm_client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=TEMPERATURE,
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": sources,
            "retrieved_count": len(ranked),
        }


if __name__ == "__main__":
    # Fully offline demo: stub embedder/reranker/LLM + in-memory collection.
    # No API keys, no model downloads — just to show the query path end to end.
    import hashlib

    DIM = 32

    class _HashEmbedder:
        """Deterministic bag-of-words embedder — demo only, not semantic."""

        def encode(self, text: str) -> List[float]:
            vec = [0.0] * DIM
            for tok in text.lower().split():
                h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
                vec[h % DIM] += 1.0
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            return [v / norm for v in vec]

    class _OverlapReranker:
        def predict(self, pairs):
            return [
                float(len(set(q.lower().split()) & set(d.lower().split())))
                for q, d in pairs
            ]

    class _FakeCompletions:
        async def create(self, model, messages, temperature):
            class _Message:
                content = "[demo] Based on the context, here is a stub answer."

            class _Choice:
                message = _Message()

            class _Response:
                choices = [_Choice()]

            return _Response()

    class _FakeChat:
        completions = _FakeCompletions()

    class _FakeLLM:
        chat = _FakeChat()

    class _MemoryCollection:
        """In-memory stand-in for a Chroma-shaped vector store."""

        def __init__(self, docs):
            self.docs = docs
            self.embedder = _HashEmbedder()

        def add(self, ids, documents, embeddings, metadatas):
            for i, d, e, m in zip(ids, documents, embeddings, metadatas):
                self.docs.append({"id": i, "text": d, "embedding": e, "metadata": m})

        def _dot(self, a, b):
            return sum(x * y for x, y in zip(a, b))

        def query(self, query_embeddings, n_results=10, where=None):
            qe = query_embeddings[0]
            ranked = sorted(self.docs, key=lambda d: -self._dot(qe, d["embedding"]))
            top = ranked[:n_results]
            return {
                "ids": [[d["id"] for d in top]],
                "documents": [[d["text"] for d in top]],
                "metadatas": [[d["metadata"] for d in top]],
                "distances": [[1.0 - self._dot(qe, d["embedding"]) for d in top]],
            }

    embedder = _HashEmbedder()
    texts = [
        "Refunds are issued to the original payment method within 5 days.",
        "SSO is configured under Admin > Security > Identity providers.",
        "The export API is limited to 100 requests per minute per key.",
    ]
    metas = [{"source": f"doc{i}.txt"} for i in range(len(texts))]

    collection = _MemoryCollection([])
    collection.add(
        ids=[f"doc_{i}" for i in range(len(texts))],
        documents=texts,
        embeddings=[embedder.encode(t) for t in texts],
        metadatas=metas,
    )

    rag = RAGPipeline(
        collection,
        embedder=embedder,
        reranker=_OverlapReranker(),
        llm_client=_FakeLLM(),
    )
    result = asyncio.run(rag.answer("How do refunds work?"))
    print(result["answer"])
    print("sources:", result["sources"])
