"""Retrieval quality testing for RAG pipelines."""

from typing import List, Dict


def test_retrieval_quality(
    test_queries: List[str],
    vector_store,
    expected_sources: Dict[str, List[str]],
    top_k: int = 5,
) -> Dict:
    """Run retrieval queries and compute hit rate against expected sources."""
    results = []
    for query in test_queries:
        retrieved = vector_store.search(query, top_k=top_k)
        retrieved_sources = [r["metadata"]["source"] for r in retrieved]
        expected = expected_sources.get(query, [])

        hit = any(src in retrieved_sources for src in expected)

        results.append({
            "query": query,
            "hit": hit,
            "retrieved_sources": retrieved_sources,
            "expected_sources": expected,
        })

    hit_rate = sum(1 for r in results if r["hit"]) / len(results) if results else 0.0
    return {"hit_rate": hit_rate, "results": results}


if __name__ == "__main__":
    class MockStore:
        def search(self, query, top_k=5):
            return [{"metadata": {"source": "docs/api"}}]

    store = MockStore()
    queries = ["How do I authenticate?", "What is the rate limit?"]
    expected = {
        "How do I authenticate?": ["docs/auth"],
        "What is the rate limit?": ["docs/api"],
    }
    report = test_retrieval_quality(queries, store, expected)
    print(f"Hit rate: {report['hit_rate']:.2f}")
    for r in report["results"]:
        print(f"  {r['query']} -> hit={r['hit']}")
