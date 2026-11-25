import math
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Document:
    id: str
    text: str

@dataclass
class SearchResult:
    id: str
    score: float

def bm25_search(
    query: str, documents: List[Document], top_k: int = 10
) -> List[SearchResult]:
    """Simplified BM25 keyword search."""
    query_terms = query.lower().split()
    scores: Dict[str, float] = {}
    doc_count = len(documents)
    avg_len = sum(len(d.text.split()) for d in documents) / max(doc_count, 1)

    k1, b = 1.5, 0.75

    for doc in documents:
        doc_terms = doc.text.lower().split()
        doc_len = len(doc_terms)
        score = 0.0

        for term in query_terms:
            tf = doc_terms.count(term)
            df = sum(1 for d in documents if term in d.text.lower())
            idf = math.log((doc_count - df + 0.5) / (df + 0.5) + 1)
            score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_len))

        if score > 0:
            scores[doc.id] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [SearchResult(id=did, score=score) for did, score in ranked]


def vector_search(
    query_embedding: List[float],
    doc_embeddings: Dict[str, List[float]],
    top_k: int = 10,
) -> List[SearchResult]:
    """Cosine similarity vector search."""
    def cosine(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b + 1e-10)

    scores = {
        did: cosine(query_embedding, emb)
        for did, emb in doc_embeddings.items()
    }
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [SearchResult(id=did, score=score) for did, score in ranked]


def reciprocal_rank_fusion(
    result_lists: List[List[SearchResult]],
    k: int = 60,
    top_k: int = 10,
) -> List[SearchResult]:
    """Fuse multiple ranked lists using RRF."""
    fused: Dict[str, float] = {}

    for results in result_lists:
        for rank, result in enumerate(results):
            fused[result.id] = fused.get(result.id, 0) + 1.0 / (k + rank + 1)

    ranked = sorted(fused.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [SearchResult(id=did, score=score) for did, score in ranked]


# Usage
documents = [
    Document("d1", "Python async programming with asyncio"),
    Document("d2", "JavaScript event loop and promises"),
    Document("d3", "Concurrent task execution in Python"),
    Document("d4", "Node.js worker threads for CPU tasks"),
]

query = "python async tasks"

bm25_results = bm25_search(query, documents, top_k=5)

query_emb = [0.12, 0.85, 0.33, 0.41]
doc_embeddings = {
    "d1": [0.11, 0.82, 0.30, 0.45],
    "d2": [0.05, 0.20, 0.71, 0.10],
    "d3": [0.13, 0.79, 0.35, 0.38],
    "d4": [0.02, 0.15, 0.60, 0.05],
}
vector_results = vector_search(query_emb, doc_embeddings, top_k=5)

hybrid_results = reciprocal_rank_fusion(
    [bm25_results, vector_results], k=60, top_k=5
)

for r in hybrid_results:
    print(f"{r.id}: {r.score:.4f}")
