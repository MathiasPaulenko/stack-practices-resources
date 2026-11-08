// Deep clone comparison: JSON round-trip vs structuredClone.
// The JSON path silently degrades types; structuredClone preserves them,
// including circular references.

function main() {
  const original = {
    name: "config",
    created: new Date("2026-01-01T00:00:00Z"),
    tags: new Set(["a", "b"]),
    nested: { level: 2 },
  };
  // circular reference: the object points back to itself
  original.selfRef = original;

  console.log("== json round-trip (loses types) ==");
  try {
    JSON.parse(JSON.stringify(original));
  } catch (err) {
    console.log(`JSON.stringify failed: ${err.constructor.name}: circular ref`);
  }

  const { selfRef, ...noCycles } = original;
  const jsonCopy = JSON.parse(JSON.stringify(noCycles));
  console.log("created type:", typeof jsonCopy.created, "(was Date)");
  console.log("tags is Set?", jsonCopy.tags instanceof Set, "(became {})");

  console.log("\n== structuredClone (preserves everything) ==");
  const clone = structuredClone(original);
  console.log("created is Date:", clone.created instanceof Date);
  console.log("tags is Set:", clone.tags instanceof Set);
  console.log("nested is a copy:", clone.nested !== original.nested);
  console.log("circular ref ok:", clone.selfRef === clone);

  clone.nested.level = 99;
  console.log("original untouched:", original.nested.level === 2);
}

main();
