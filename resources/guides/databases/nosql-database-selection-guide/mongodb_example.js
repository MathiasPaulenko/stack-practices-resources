// MongoDB embedded document model from the NoSQL selection guide.
// Companion to https://stackpractices.com/guides/nosql-database-selection-guide/
// Run with: mongosh nosql_examples mongodb_example.js

// A product document with nested reviews and variants
db.products.insertOne({
  sku: "SHOE-001",
  name: "Trail Runner",
  price: 89.99,
  attributes: { color: "red", size: 42 },
  reviews: [
    { user_id: 42, rating: 5, comment: "Great grip!" }
  ],
  tags: ["running", "trail", "waterproof"]
});

// Flexible query with nested matching
db.products.find({ "reviews.rating": { $gte: 4 }, tags: "trail" });
