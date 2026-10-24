import hashlib
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class CacheEntry:
    embedding: List[float]
    model: str
    created_at: float
    access_count: int = 0

class EmbeddingCache:
    def __init__(self, ttl_seconds: float = 86400 * 30):
        self._cache: Dict[str, CacheEntry] = {}
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0

    def _make_key(self, text: str, model: str) -> str:
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return f"{model}:{content_hash}"

    def get(self, text: str, model: str) -> Optional[List[float]]:
        key = self._make_key(text, model)
        entry = self._cache.get(key)

        if entry is None:
            self.misses += 1
            return None

        if time.time() - entry.created_at > self.ttl:
            del self._cache[key]
            self.misses += 1
            return None

        entry.access_count += 1
        self.hits += 1
        return entry.embedding

    def set(self, text: str, model: str, embedding: List[float]) -> None:
        key = self._make_key(text, model)
        self._cache[key] = CacheEntry(
            embedding=embedding,
            model=model,
            created_at=time.time(),
        )

    def get_or_compute(
        self,
        text: str,
        model: str,
        embed_fn: callable,
    ) -> List[float]:
        cached = self.get(text, model)
        if cached is not None:
            return cached

        embedding = embed_fn(text, model)
        self.set(text, model, embedding)
        return embedding

    def batch_get_or_compute(
        self,
        texts: List[str],
        model: str,
        batch_embed_fn: callable,
    ) -> List[List[float]]:
        results: List[Optional[List[float]]] = [None] * len(texts)
        uncached_indices: List[int] = []

        for i, text in enumerate(texts):
            cached = self.get(text, model)
            if cached is not None:
                results[i] = cached
            else:
                uncached_indices.append(i)

        if uncached_indices:
            uncached_texts = [texts[i] for i in uncached_indices]
            new_embeddings = batch_embed_fn(uncached_texts, model)

            for idx, embedding in zip(uncached_indices, new_embeddings):
                results[idx] = embedding
                self.set(texts[idx], model, embedding)

        return [r for r in results if r is not None]

    def stats(self) -> Dict[str, int]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "size": len(self._cache),
            "hit_rate": self.hits / max(self.hits + self.misses, 1),
        }

    def invalidate_model(self, model: str) -> int:
        keys_to_remove = [k for k in self._cache if k.startswith(f"{model}:")]
        for k in keys_to_remove:
            del self._cache[k]
        return len(keys_to_remove)

# Mock embedding function
def mock_embed(text: str, model: str) -> List[float]:
    print(f"  [API CALL] Embedding '{text[:30]}...' with {model}")
    return [len(text) * 0.01, int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % 100 / 100, 0.5]

def mock_batch_embed(texts: List[str], model: str) -> List[List[float]]:
    print(f"  [BATCH API CALL] Embedding {len(texts)} texts with {model}")
    return [mock_embed(t, model) for t in texts]

# Usage
cache = EmbeddingCache(ttl_seconds=3600)

documents = [
    "Python async programming guide",
    "JavaScript event loop explained",
    "Python async programming guide",
    "Database indexing strategies",
    "JavaScript event loop explained",
]

print("=== Single embeddings ===")
for doc in documents:
    emb = cache.get_or_compute(doc, "text-embedding-3-small", mock_embed)
    print(f"  Result: {emb[:2]}...")

print(f"\nCache stats: {cache.stats()}")

print("\n=== Batch embeddings ===")
cache2 = EmbeddingCache()
new_docs = ["New document one", "New document two", "Python async programming guide"]
embs = cache2.batch_get_or_compute(new_docs, "text-embedding-3-small", mock_batch_embed)
print(f"Cache stats: {cache2.stats()}")

print("\n=== Model invalidation ===")
removed = cache.invalidate_model("text-embedding-3-small")
print(f"Removed {removed} entries")
print(f"Cache stats: {cache.stats()}")
