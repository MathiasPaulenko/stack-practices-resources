# Embedding Cache Pattern — Runnable Implementations

Companion to the StackPractices pattern [Embedding Cache Pattern](https://stackpractices.com/patterns/embedding-cache-pattern/).

An embedding cache keyed by `model:SHA-256(text)` with TTL expiry, batch get-or-compute, hit-rate stats, and per-model invalidation. Three equivalent implementations with a mock embed function so they run without API keys.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/embedding_cache.py` | Python 3.10+ (stdlib only) | `python src/embedding_cache.py` |
| `src/embedding-cache.js` | Node.js 18+ (stdlib only) | `node src/embedding-cache.js` |
| `src/EmbeddingCache.java` | Java 17+ | `javac src/EmbeddingCache.java && java -cp src EmbeddingCache` |

Each run embeds a small document list with repeats and prints cache stats — watch the hits climb and the API calls stop.
