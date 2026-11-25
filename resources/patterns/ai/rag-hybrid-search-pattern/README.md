# RAG Hybrid Search Pattern — Runnable Examples

Companion to the StackPractices [RAG Hybrid Search Pattern](https://stackpractices.com/patterns/rag-hybrid-search-pattern/).

The three programs run keyword search, cosine-similarity search, and Reciprocal Rank Fusion against a tiny in-memory corpus. The vectors are fixed sample values, not embeddings from a model. No database, network access, or API key is needed.

## Run

| File | Requirement | Command |
| --- | --- | --- |
| `src/hybrid_search.py` | Python 3.10+ | `python src/hybrid_search.py` |
| `src/hybrid-search.js` | Node.js 18+ | `node src/hybrid-search.js` |
| `src/HybridSearch.java` | Java 17+ | `javac src/HybridSearch.java && java -cp src HybridSearch` |

For a real RAG system, replace the sample BM25 and vector-search functions with your search engine's retrievers. Keep the returned lists ranked, then pass them to `reciprocalRankFusion`.
