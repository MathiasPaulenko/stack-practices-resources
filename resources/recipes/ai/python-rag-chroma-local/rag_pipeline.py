"""Local RAG pipeline with ChromaDB and sentence-transformers.

Companion code for:
https://stackpractices.com/recipes/python-rag-chroma-local/

Usage:
    pip install -r requirements.txt
    export OPENAI_API_KEY=...   # only for the OpenAI pipeline
    python rag_pipeline.py          # runs the demo with OpenAI
    python rag_pipeline.py --ollama # fully local, needs Ollama running
"""

from dataclasses import dataclass

import chromadb


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(Chunk(
            id=f"chunk_{chunk_idx}",
            text=text[start:end],
            metadata={"chunk_index": chunk_idx, "char_start": start},
        ))
        start = end - overlap
        chunk_idx += 1

    return chunks


def chunk_documents(documents: list[dict]) -> list[Chunk]:
    """Chunk multiple documents with doc-prefixed chunk IDs."""
    all_chunks = []
    for doc_idx, doc in enumerate(documents):
        chunks = chunk_text(doc["text"])
        for chunk in chunks:
            chunk.id = f"doc_{doc_idx}_{chunk.id}"
            chunk.metadata.update({
                "source": doc.get("source", "unknown"),
                "title": doc.get("title", ""),
            })
        all_chunks.extend(chunks)
    return all_chunks


# ---------------------------------------------------------------------------
# Vector store
# ---------------------------------------------------------------------------

class LocalRAG:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Upsert chunks so re-ingesting a document overwrites its old chunks."""
        self.collection.upsert(
            ids=[c.id for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[c.metadata for c in chunks],
        )

    def query(self, query_text: str, n_results: int = 5) -> list[dict]:
        """Retrieve relevant chunks for a query."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
        )
        return [
            {"text": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def query_with_filter(
        self, query_text: str, n_results: int = 5, where: dict | None = None
    ) -> list[dict]:
        """Retrieve chunks restricted by metadata filter."""
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
        )


# ---------------------------------------------------------------------------
# Pipelines
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "Answer the question based on the provided context. "
    "If the context does not contain the answer, say "
    "'I don't have enough information to answer this.'"
)


class RAGPipeline:
    """RAG pipeline backed by the OpenAI chat API."""

    def __init__(self, persist_dir: str = "./chroma_db"):
        from openai import OpenAI

        self.rag = LocalRAG(persist_dir)
        self.llm = OpenAI()

    def ingest(self, documents: list[dict]) -> None:
        chunks = chunk_documents(documents)
        self.rag.add_chunks(chunks)
        print(f"Ingested {len(chunks)} chunks from {len(documents)} documents")

    def retrieve(self, query: str, n_results: int = 5) -> list[dict]:
        return self.rag.query(query, n_results)

    def build_context(self, context_chunks: list[dict]) -> str:
        return "\n\n".join(
            f"[Source: {c['metadata'].get('source', 'unknown')}]\n{c['text']}"
            for c in context_chunks
        )

    def generate(self, query: str, context_chunks: list[dict]) -> str:
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Context:\n{self.build_context(context_chunks)}\n\nQuestion: {query}",
                },
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content

    def ask(self, query: str, n_results: int = 5) -> dict:
        chunks = self.retrieve(query, n_results)
        return {
            "answer": self.generate(query, chunks),
            "sources": [
                {"source": c["metadata"].get("source"), "text": c["text"][:200]}
                for c in chunks
            ],
            "num_chunks": len(chunks),
        }


class LocalLLMRAG(RAGPipeline):
    """Fully local RAG pipeline using Ollama for generation."""

    def __init__(
        self,
        persist_dir: str = "./chroma_db",
        ollama_url: str = "http://localhost:11434",
        model: str = "llama3",
    ):
        self.rag = LocalRAG(persist_dir)
        self.ollama_url = ollama_url
        self.model = model

    def generate(self, query: str, context_chunks: list[dict]) -> str:
        import requests

        context = "\n\n".join(c["text"] for c in context_chunks)
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": (
                    f"{SYSTEM_PROMPT}\n\n"
                    f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
                ),
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["response"]


class RerankedRAG(RAGPipeline):
    """Adds cross-encoder reranking on top of vector retrieval."""

    def __init__(self, persist_dir: str = "./chroma_db"):
        from sentence_transformers import CrossEncoder

        super().__init__(persist_dir)
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def retrieve(
        self, query: str, n_results: int = 20, top_k: int = 5
    ) -> list[dict]:
        chunks = self.rag.query(query, n_results)
        pairs = [(query, c["text"]) for c in chunks]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
        return [c for c, _ in ranked[:top_k]]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

DEMO_DOCUMENTS = [
    {
        "title": "Redis Guide",
        "source": "redis-docs.md",
        "text": (
            "Redis is an in-memory data structure store. It supports strings, "
            "hashes, lists, sets, sorted sets, streams, and more. Redis is "
            "commonly used for caching, session management, real-time "
            "analytics, and message brokering."
        ),
    },
    {
        "title": "PostgreSQL Guide",
        "source": "postgres-docs.md",
        "text": (
            "PostgreSQL is a capable open-source relational database. It "
            "supports ACID compliance, JSON columns, full-text search, and "
            "geospatial data via PostGIS."
        ),
    },
]


def main() -> None:
    import sys

    if "--ollama" in sys.argv:
        pipeline = LocalLLMRAG()
        print("Using Ollama for generation (fully local).")
    else:
        pipeline = RAGPipeline()
        print("Using OpenAI for generation (needs OPENAI_API_KEY).")

    pipeline.ingest(DEMO_DOCUMENTS)

    result = pipeline.ask("What data structures does Redis support?")
    print("\nAnswer:", result["answer"])
    print("Sources:", [s["source"] for s in result["sources"]])


if __name__ == "__main__":
    main()
