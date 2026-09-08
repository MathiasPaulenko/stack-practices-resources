// Semantic search with OpenAI embeddings and cosine similarity (plain JS).
const { OpenAI } = require('openai');

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function embed(text) {
  const res = await openai.embeddings.create({
    input: text,
    model: 'text-embedding-3-small',
  });
  return res.data[0].embedding;
}

function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}

async function semanticSearch(documents, query, k = 2) {
  const embeddings = await Promise.all(documents.map(embed));
  const q = await embed(query);
  return documents
    .map((doc, i) => ({ doc, score: cosine(q, embeddings[i]) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, k);
}

module.exports = { embed, cosine, semanticSearch };

if (require.main === module) {
  const docs = [
    'Python is great for data science and machine learning.',
    'JavaScript runs in browsers and on servers via Node.js.',
    'Rust offers memory safety without a garbage collector.',
  ];
  semanticSearch(docs, 'language for web development', 2).then((results) => {
    results.forEach((r, i) => console.log(`${i + 1}. ${r.doc} (score: ${r.score.toFixed(3)})`));
  });
}
