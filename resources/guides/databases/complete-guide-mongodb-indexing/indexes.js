// Index creation by query pattern - from the guide.
// Run with a live MongoDB: mongosh --file indexes.js

// Single field + unique
db.users.createIndex({ email: 1 }, { unique: true });

// Compound ordered by ESR: Equality, Sort, Range
db.users.createIndex({ status: 1, createdAt: -1, age: 1 });

// Covered query: filter + projection live in the index
db.users.createIndex({ email: 1, status: 1, lastLogin: -1 });

// Partial: only documents matching the predicate (replaces deprecated sparse)
db.users.createIndex(
  { email: 1 },
  { partialFilterExpression: { status: "active" } }
);

// TTL: documents expire 24h after createdAt (sweeper ~60s, not a hard deadline)
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 });

// Text: basic keyword search (use Atlas Search for fuzzy/faceted)
db.articles.createIndex(
  { title: "text", body: "text" },
  { weights: { title: 10, body: 1 }, default_language: "english" }
);

// Geospatial
db.stores.createIndex({ location: "2dsphere" });

// Wildcard: dynamic attributes pattern
db.products.createIndex({ "attributes.$**": 1 });

// Hashed: even shard-key distribution (equality only, no ranges)
db.users.createIndex({ _id: "hashed" });
