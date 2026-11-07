// Promise fan-out patterns: all (fail-fast) vs allSettled (isolated).
// Run: node fetch_all.mjs

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchItem(id, shouldFail = false) {
  await sleep(50);
  if (shouldFail) throw new Error(`item ${id} failed`);
  return `item-${id}`;
}

const ids = Array.from({ length: 10 }, (_, i) => i);

// allSettled: one failure doesn't cancel the rest — you get every outcome.
const settled = await Promise.allSettled(
  ids.map((id) => fetchItem(id, id === 4))
);
const ok = settled.filter((r) => r.status === "fulfilled").map((r) => r.value);
const failed = settled
  .filter((r) => r.status === "rejected")
  .map((r) => r.reason.message);

console.log(`${ok.length}/${ids.length} succeeded`);
console.log(`rejected: ${failed.join(", ")}`);

// Promise.all fails fast: a single rejection rejects the whole batch —
// pick it only when partial results are useless to the caller.
try {
  await Promise.all(ids.map((id) => fetchItem(id, id === 7)));
} catch (err) {
  console.log(`Promise.all bailed on first failure: ${err.message}`);
}
