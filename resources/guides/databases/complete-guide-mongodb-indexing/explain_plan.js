// Explain-plan reading - the fields that tell the story.
// mongosh --file explain_plan.js

const explain = db.users
  .find({ status: "active", age: { $gt: 18 } })
  .explain("executionStats");

// What to check:
// winningPlan.stage: COLLSCAN (bad), IXSCAN (good), FETCH (doc reads), SORT (in-memory)
// totalKeysExamined ~ totalDocsExamined ~ nReturned -> healthy index
// totalDocsExamined >> nReturned -> index exists but doesn't serve this query
// no FETCH stage -> covered query
console.log({
  stage: explain.queryPlanner.winningPlan.stage,
  keys: explain.executionStats.totalKeysExamined,
  docs: explain.executionStats.totalDocsExamined,
  returned: explain.executionStats.nReturned,
  ms: explain.executionStats.executionTimeMillis,
});
