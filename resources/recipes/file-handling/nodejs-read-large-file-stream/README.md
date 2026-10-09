# Read Large Files in Node.js with Streams — Companion Resources

Companion files for [Read Large Files in Node.js with Streams](https://stackpractices.com/recipes/nodejs-read-large-file-stream/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `csv-to-jsonl.js` | Full pipeline: read CSV → parse with leftover buffer → filter → write JSONL via `stream/promises` |
| `memory-compare.js` | Heap-delta comparison: `fs.readFile` vs streaming line count on the same file |

## How to use

1. `node csv-to-jsonl.js` — generates `sample.csv` (10k rows) if none given, writes `output.jsonl`.
2. `node memory-compare.js big.log` — prints heap delta for both approaches. Generate a test file first: `node -e "require('fs').writeFileSync('big.log', 'x\n'.repeat(5e6))"`.

No dependencies — Node.js 18+ only.