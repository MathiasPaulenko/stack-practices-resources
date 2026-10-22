// MongoDB per-operation consistency knobs.
// writeConcern = how many nodes must confirm the write.
// readConcern  = what a query is allowed to see.
// readPreference = which node serves the read.

// CP-leaning: linearizable read of a majority-committed write.
// During a partition that costs availability: if no majority is
// reachable, the write waits and eventually fails with wtimeout.
db.accounts.find({ _id: accountId })
  .readConcern('linearizable');

db.accounts.updateOne(
  { _id: accountId },
  { $inc: { balance: -100 } },
  { writeConcern: { w: 'majority', wtimeout: 5000 } }
);

// AP-leaning: read from a secondary, accept staleness.
// During a partition the secondary keeps answering, so the app
// stays up and may serve data a few seconds old.
db.events.find({ userId: userId })
  .readConcern('local')
  .readPreference('secondaryPreferred');

// Session reads: cheap read-your-writes for the current session.
const session = db.getMongo().startSession({ causalConsistency: true });
session.getDatabase('app').profiles.find({ _id: userId });
