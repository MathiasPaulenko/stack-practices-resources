"""Hybrid retrieval: vector search + keyword search, fused into one ranking.

Plain vector search has a blind spot: exact-match queries. "Error code
E-4471" or a product SKU embeds into a vector far from the chunk containing
it, because embeddings capture meaning, not tokens. Hybrid search runs
keyword search (BM25 or equivalent) alongside vector search and merges the
rankings.

Two fusion strategies live here:

- HybridSearch: min-max score normalization + weighted sum (alpha).
  Simple but brittle — a bad result set still produces a 'best' score of
  1.0. Fine for prototyping and identifier-heavy tuning experiments.
- reciprocal_rank_fusion(): fuses rankings by rank position instead of raw
  scores — far less sensitive to score-scale differences between retrievers.
  This is the production-preferred approach (see the repo's
  rag-hybrid-search-pattern for a full RRF implementation).
"""
import math
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple


class HybridSearch:
    """Combines vector and keyword results with weighted score fusion.

    vector_store: anything with .query(query_embeddings=[...], n_results=...)
        returning Chroma-shaped results (see vector_stores.py).
    keyword_index: anything with .search(query, top_k=...) returning a list
        of {"id", "score", "text", "metadata"?} dicts (see SimpleKeywordIndex).
    alpha: 0 = keyword only, 1 = vector only.
    """

    def __init__(self, vector_store: Any, keyword_index: Any, alpha: float = 0.5):
        self.vector_store = vector_store
        self.keyword_index = keyword_index
        self.alpha = alpha

    def search(self, query: str, query_embedding: List[float], top_k: int = 10) -> List[dict]:
        # assumes query_embedding comes from the embedding step
        vector_results = self.vector_store.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2,
        )
        keyword_results = self.keyword_index.search(query, top_k=top_k * 2)

        vector_scores = self._normalize_scores(
            [1 - d for d in vector_results["distances"][0]]  # distance -> similarity
        )
        keyword_scores = self._normalize_scores([r["score"] for r in keyword_results])

        combined = {}

        for i, doc in enumerate(vector_results["documents"][0]):
            doc_id = vector_results["ids"][0][i]
            combined[doc_id] = {
                "id": doc_id,
                "text": doc,
                "metadata": vector_results["metadatas"][0][i] or {},
                "score": self.alpha * vector_scores[i],
            }

        for i, result in enumerate(keyword_results):
            doc_id = result["id"]
            contribution = (1 - self.alpha) * keyword_scores[i]
            if doc_id in combined:
                combined[doc_id]["score"] += contribution
            else:
                combined[doc_id] = {
                    "id": doc_id,
                    "text": result["text"],
                    "metadata": result.get("metadata", {}),
                    "score": contribution,
                }

        return sorted(combined.values(), key=lambda x: x["score"], reverse=True)[:top_k]

    def _normalize_scores(self, scores: List[float]) -> List[float]:
        if not scores:
            return []
        min_s, max_s = min(scores), max(scores)
        if max_s == min_s:
            return [1.0] * len(scores)
        return [(s - min_s) / (max_s - min_s) for s in scores]


def reciprocal_rank_fusion(rankings: List[List[str]], k: int = 60) -> List[Tuple[str, float]]:
    """Fuse ranked ID lists by position: score += 1 / (k + rank).

    k=60 is the standard constant from the original RRF paper. Pass one
    ranking per retriever (e.g. vector order, BM25 order); returns
    (doc_id, score) pairs sorted by fused score, best first.
    """
    scores: Dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


class SimpleKeywordIndex:
    """Minimal dependency-free keyword index (TF-IDF-ish overlap scoring).

    Stand-in for BM25 to make hybrid search runnable offline. For production
    use rank_bm25, Elasticsearch/OpenSearch, or your store's native keyword
    search (Weaviate BM25, pgvector + ts_rank, Pinecone sparse vectors).
    """

    def __init__(self):
        self._docs: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _tokens(text: str) -> List[str]:
        return [t for t in "".join(c if c.isalnum() else " " for c in text.lower()).split() if t]

    def add(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._docs[doc_id] = {
            "text": text,
            "tokens": Counter(self._tokens(text)),
            "metadata": metadata or {},
        }

    def add_many(self, ids: List[str], texts: List[str],
                 metadatas: Optional[List[Dict[str, Any]]] = None) -> None:
        metadatas = metadatas or [{}] * len(ids)
        for doc_id, text, meta in zip(ids, texts, metadatas):
            self.add(doc_id, text, meta)

    def search(self, query: str, top_k: int = 10) -> List[dict]:
        if not self._docs:
            return []

        n_docs = len(self._docs)
        df = Counter()
        for doc in self._docs.values():
            for tok in doc["tokens"]:
                df[tok] += 1

        results = []
        for doc_id, doc in self._docs.items():
            score = 0.0
            for tok in set(self._tokens(query)):
                if tok not in doc["tokens"]:
                    continue
                # Smoothed IDF so rare terms dominate, plus raw term frequency.
                idf = math.log((n_docs + 1) / (df[tok] + 0.5)) + 1.0
                score += doc["tokens"][tok] * idf
            if score > 0:
                results.append({
                    "id": doc_id,
                    "text": doc["text"],
                    "score": score,
                    "metadata": doc["metadata"],
                })

        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]


if __name__ == "__main__":
    # Offline demo: fake vector results + real SimpleKeywordIndex.
    class _FakeVectorStore:
        """Returns a fixed Chroma-shaped result for demo purposes."""

        def query(self, query_embeddings, n_results=10, where=None):
            return {
                "ids": [["v1", "v2", "v3"]],
                "documents": [["vector hit one", "vector hit two", "vector hit three"]],
                "metadatas": [[{"source": "a"}, {"source": "b"}, {"source": "c"}]],
                "distances": [[0.1, 0.4, 0.9]],
            }

    index = SimpleKeywordIndex()
    index.add_many(
        ids=["k1", "k2", "v2"],
        texts=["keyword match here", "unrelated words", "vector hit two plus keyword"],
        metadatas=[{"source": "a"}, {"source": "b"}, {"source": "b"}],
    )

    hybrid = HybridSearch(_FakeVectorStore(), index, alpha=0.5)
    for r in hybrid.search("keyword match", query_embedding=[0.1] * 8, top_k=3):
        print(f"{r['id']:>4}  score={r['score']:.3f}  {r['text'][:40]}")

    # RRF example: fuse the two rankings by position.
    fused = reciprocal_rank_fusion([["v2", "v1", "v3"], ["k1", "v2", "k2"]])
    print("rrf:", fused)
