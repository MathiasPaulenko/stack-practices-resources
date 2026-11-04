// Index hygiene: usage stats, sizes, and the hide-before-drop pattern.
// mongosh --file index_audit.js

// Which indexes actually serve queries
db.users.aggregate([{ $indexStats: {} }]);

// Index inventory + sizes
db.users.getIndexes();
db.users.stats().indexSizes;

// Test a drop safely: invisible to planner, still maintained.
// If latency spikes, unhideIndex restores it instantly.
db.users.hideIndex("status_1");
// ... observe the workload ...
db.users.unhideIndex("status_1");

// Force an index when diagnosing plan choices
db.users.find({ status: "active" }).hint({ status: 1 });
