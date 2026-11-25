class Document {
  constructor(id, text) {
    this.id = id;
    this.text = text;
  }
}

function bm25Search(query, documents, topK = 10) {
  const queryTerms = query.toLowerCase().split(" ");
  const scores = {};
  const docCount = documents.length;
  const avgLen = documents.reduce((s, d) => s + d.text.split(" ").length, 0) / Math.max(docCount, 1);
  const k1 = 1.5, b = 0.75;

  for (const doc of documents) {
    const docTerms = doc.text.toLowerCase().split(" ");
    const docLen = docTerms.length;
    let score = 0;

    for (const term of queryTerms) {
      const tf = docTerms.filter(t => t === term).length;
      const df = documents.filter(d => d.text.toLowerCase().includes(term)).length;
      const idf = Math.log((docCount - df + 0.5) / (df + 0.5) + 1);
      score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * docLen / avgLen));
    }

    if (score > 0) scores[doc.id] = score;
  }

  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topK)
    .map(([id, score]) => ({ id, score }));
}

function cosineSimilarity(a, b) {
  const dot = a.reduce((s, x, i) => s + x * b[i], 0);
  const normA = Math.sqrt(a.reduce((s, x) => s + x * x, 0));
  const normB = Math.sqrt(b.reduce((s, x) => s + x * x, 0));
  return dot / (normA * normB + 1e-10);
}

function vectorSearch(queryEmbedding, docEmbeddings, topK = 10) {
  const scores = {};
  for (const [id, emb] of Object.entries(docEmbeddings)) {
    scores[id] = cosineSimilarity(queryEmbedding, emb);
  }
  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topK)
    .map(([id, score]) => ({ id, score }));
}

function reciprocalRankFusion(resultLists, k = 60, topK = 10) {
  const fused = {};
  for (const results of resultLists) {
    results.forEach((result, rank) => {
      fused[result.id] = (fused[result.id] || 0) + 1 / (k + rank + 1);
    });
  }
  return Object.entries(fused)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topK)
    .map(([id, score]) => ({ id, score }));
}

// Usage
const docs = [
  new Document("d1", "Python async programming with asyncio"),
  new Document("d2", "JavaScript event loop and promises"),
  new Document("d3", "Concurrent task execution in Python"),
  new Document("d4", "Node.js worker threads for CPU tasks"),
];

const query = "python async tasks";
const bm25Results = bm25Search(query, docs, 5);

const queryEmb = [0.12, 0.85, 0.33, 0.41];
const docEmbs = {
  d1: [0.11, 0.82, 0.30, 0.45],
  d2: [0.05, 0.20, 0.71, 0.10],
  d3: [0.13, 0.79, 0.35, 0.38],
  d4: [0.02, 0.15, 0.60, 0.05],
};
const vectorResults = vectorSearch(queryEmb, docEmbs, 5);

const hybrid = reciprocalRankFusion([bm25Results, vectorResults], 60, 5);
console.log(hybrid);
