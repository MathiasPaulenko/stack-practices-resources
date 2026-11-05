"""Rerankers: cross-encoders (self-hosted) and Cohere's hosted rerank API.

The retriever optimizes for recall — it fetches candidates cheaply and lets
some noise through. A reranker optimizes for precision: it scores each
(query, document) pair jointly and reorders the shortlist.

- Bi-encoders embed query and document independently (that's what powers
  first-stage retrieval). They never see the pair together.
- Cross-encoders feed the concatenated pair through a transformer — more
  accurate, but every candidate costs a forward pass, so they rerank a
  shortlist of 20-50, not a corpus.

Skip reranking when retrieval is already precise (small, clean corpus,
context precision > ~0.9 on your eval set) or when the latency budget is
tighter than the quality gain justifies.
"""
import asyncio
import os
from typing import Any, Dict, List, Optional

DEFAULT_CROSS_ENCODER = "cross-encoder/ms-marco-MiniLM-L-6-v2"
DEFAULT_COHERE_MODEL = "rerank-v5.0-fast"  # check Cohere docs for the latest model


class CrossEncoderReranker:
    """Self-hosted cross-encoder via sentence-transformers.

    CPU-bound: in an async service, call rerank_async() (or wrap predict()
    in asyncio.to_thread yourself) so the event loop stays free.
    """

    def __init__(self, model_name: str = DEFAULT_CROSS_ENCODER):
        from sentence_transformers import CrossEncoder

        self.model = CrossEncoder(model_name)

    def predict(self, pairs: List[tuple]) -> List[float]:
        """pairs: [(query, document), ...] -> relevance scores."""
        return [float(s) for s in self.model.predict(pairs)]

    async def rerank_async(self, query: str, documents: List[str],
                           top_k: int = 5) -> List[Dict[str, Any]]:
        pairs = [(query, doc) for doc in documents]
        scores = await asyncio.to_thread(self.model.predict, pairs)
        return _ranked(documents, scores, top_k)


def _ranked(documents: List[str], scores: List[float], top_k: int) -> List[Dict[str, Any]]:
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [{"text": doc, "score": float(score)} for doc, score in ranked[:top_k]]


async def rerank_results_async(
    query: str,
    documents: List[str],
    top_k: int = 5,
    reranker: Optional[CrossEncoderReranker] = None,
) -> List[Dict[str, Any]]:
    """Async convenience wrapper — predict() runs in a thread."""
    reranker = reranker or CrossEncoderReranker()
    return await reranker.rerank_async(query, documents, top_k=top_k)


def cohere_rerank(
    query: str,
    documents: List[str],
    top_k: int = 5,
    client: Any = None,
    model: str = DEFAULT_COHERE_MODEL,
) -> List[Dict[str, Any]]:
    """Hosted rerank via Cohere — removes the GPU/CPU requirement entirely.

    client: a cohere.Client instance; built from COHERE_API_KEY when omitted.
    """
    if client is None:
        api_key = os.environ.get("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY is not set — pass a cohere.Client or set the env var")
        import cohere

        client = cohere.Client(api_key)

    results = client.rerank(
        model=model,
        query=query,
        documents=documents,
        top_n=top_k,
    )
    return [
        {
            "text": documents[r.index],
            "score": float(r.relevance_score),
            "index": r.index,
        }
        for r in results.results
    ]


if __name__ == "__main__":
    # Offline demo of the ranking logic with a stub reranker — no model
    # download. For real use: CrossEncoderReranker() or cohere_rerank().
    class _StubReranker:
        def predict(self, pairs):
            # "score" = number of shared words between query and document
            return [
                float(len(set(q.lower().split()) & set(d.lower().split())))
                for q, d in pairs
            ]

    reranker = _StubReranker()
    query = "refund policy"
    docs = [
        "Our refund policy allows returns within 30 days.",
        "The weather in spring is mild.",
        "Refund exceptions apply to digital downloads.",
    ]
    pairs = [(query, d) for d in docs]
    print(_ranked(docs, reranker.predict(pairs), top_k=2))
