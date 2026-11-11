// Meilisearch full-text search: index setup, typo-tolerant search, faceting.
// Requires: npm install meilisearch
// Start:    docker compose up -d meilisearch
// Run:      node meilisearch-search.js

import { MeiliSearch } from "meilisearch";

const client = new MeiliSearch({ host: "http://localhost:7700", apiKey: "masterKey" });
const index = client.index("articles");

async function setup() {
  await index.updateSettings({
    searchableAttributes: ["title", "content"],
    filterableAttributes: ["category"],
    rankingRules: ["words", "typo", "proximity", "attribute", "sort", "exactness"],
  });

  const task = await index.addDocuments([
    { id: 1, title: "Database optimization", content: "Indexing strategies for large tables", category: "db" },
    { id: 2, title: "Full-text search", content: "Tokenization, stemming, and relevance ranking", category: "search" },
    { id: 3, title: "Query tuning", content: "How to read EXPLAIN and fix slow queries", category: "db" },
  ]);

  await client.tasks.waitForTask(task.taskUid); // indexing is async
}

async function search(query, filter) {
  const res = await index.search(query, {
    attributesToHighlight: ["title", "content"],
    facets: ["category"],
    filter,
    limit: 20,
  });
  return res.hits;
}

const run = async () => {
  await setup();
  console.log("'datbase' (typo) ->");
  for (const hit of await search("datbase")) console.log("   ", hit.title);
  console.log("'query' filtered to category=db ->");
  for (const hit of await search("query", 'category = "db"')) console.log("   ", hit.title);
};

run().catch(console.error);
