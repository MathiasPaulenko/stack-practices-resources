const crypto = require("crypto");

class CacheEntry {
  constructor(embedding, model, createdAt) {
    this.embedding = embedding;
    this.model = model;
    this.createdAt = createdAt;
    this.accessCount = 0;
  }
}

class EmbeddingCache {
  constructor(ttlSeconds = 86400 * 30) {
    this.cache = new Map();
    this.ttl = ttlSeconds;
    this.hits = 0;
    this.misses = 0;
  }

  _makeKey(text, model) {
    const hash = crypto.createHash("sha256").update(text, "utf8").digest("hex");
    return `${model}:${hash}`;
  }

  get(text, model) {
    const key = this._makeKey(text, model);
    const entry = this.cache.get(key);

    if (!entry) {
      this.misses++;
      return null;
    }

    if (Date.now() / 1000 - entry.createdAt > this.ttl) {
      this.cache.delete(key);
      this.misses++;
      return null;
    }

    entry.accessCount++;
    this.hits++;
    return entry.embedding;
  }

  set(text, model, embedding) {
    const key = this._makeKey(text, model);
    this.cache.set(key, new CacheEntry(embedding, model, Date.now() / 1000));
  }

  getOrCompute(text, model, embedFn) {
    const cached = this.get(text, model);
    if (cached) return cached;

    const embedding = embedFn(text, model);
    this.set(text, model, embedding);
    return embedding;
  }

  batchGetOrCompute(texts, model, batchEmbedFn) {
    const results = new Array(texts.length).fill(null);
    const uncachedIndices = [];

    for (let i = 0; i < texts.length; i++) {
      const cached = this.get(texts[i], model);
      if (cached) {
        results[i] = cached;
      } else {
        uncachedIndices.push(i);
      }
    }

    if (uncachedIndices.length > 0) {
      const uncachedTexts = uncachedIndices.map(i => texts[i]);
      const newEmbeddings = batchEmbedFn(uncachedTexts, model);

      uncachedIndices.forEach((idx, j) => {
        results[idx] = newEmbeddings[j];
        this.set(texts[idx], model, newEmbeddings[j]);
      });
    }

    return results;
  }

  stats() {
    return {
      hits: this.hits,
      misses: this.misses,
      size: this.cache.size,
      hitRate: this.hits / Math.max(this.hits + this.misses, 1),
    };
  }

  invalidateModel(model) {
    let count = 0;
    for (const key of this.cache.keys()) {
      if (key.startsWith(`${model}:`)) {
        this.cache.delete(key);
        count++;
      }
    }
    return count;
  }
}

// Mock embedding function
function mockEmbed(text, model) {
  console.log(`  [API CALL] Embedding '${text.slice(0, 30)}...' with ${model}`);
  return [text.length * 0.01, (text.charCodeAt(0) % 100) / 100, 0.5];
}

function mockBatchEmbed(texts, model) {
  console.log(`  [BATCH API CALL] Embedding ${texts.length} texts with ${model}`);
  return texts.map(t => mockEmbed(t, model));
}

// Usage
const cache = new EmbeddingCache(3600);

const documents = [
  "Python async programming guide",
  "JavaScript event loop explained",
  "Python async programming guide",
  "Database indexing strategies",
  "JavaScript event loop explained",
];

console.log("=== Single embeddings ===");
for (const doc of documents) {
  const emb = cache.getOrCompute(doc, "text-embedding-3-small", mockEmbed);
  console.log(`  Result: [${emb.slice(0, 2).map(n => n.toFixed(4))}...]`);
}

console.log(`\nCache stats:`, cache.stats());

console.log("\n=== Batch embeddings ===");
const cache2 = new EmbeddingCache();
const newDocs = ["New document one", "New document two", "Python async programming guide"];
cache2.batchGetOrCompute(newDocs, "text-embedding-3-small", mockBatchEmbed);
console.log(`Cache stats:`, cache2.stats());
