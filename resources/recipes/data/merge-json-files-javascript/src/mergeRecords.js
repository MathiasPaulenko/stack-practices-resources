// Concat arrays of records and dedupe by a stable key (last file wins the slot).
function mergeRecords(sources, key = "id") {
  const seen = new Map();
  for (const source of sources) {
    for (const item of source) {
      seen.set(item[key], item);
    }
  }
  return [...seen.values()];
}

module.exports = { mergeRecords };

if (require.main === module) {
  const a = [{ id: 1, v: "a" }, { id: 2, v: "a" }];
  const b = [{ id: 2, v: "b" }, { id: 3, v: "b" }];
  console.log(JSON.stringify(mergeRecords([a, b])));
}
