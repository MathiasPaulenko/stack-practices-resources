# Merge JSON Files in JavaScript — Runnable Node.js Examples

Companion code for [Merge JSON Files in JavaScript](https://stackpractices.com/recipes/merge-json-files-javascript/) on StackPractices.

## Contents

- `src/mergeJson.js` — hardened `deepMerge`: `null`-safe, filters `__proto__`/`constructor`/`prototype`, never mutates inputs. `node src/mergeJson.js`
- `src/mergeJsonDir.js` — sorted directory merge with per-file parse-error collection. `node src/mergeJsonDir.js ./config`
- `src/mergeRecords.js` — array concat + dedupe by stable key via `Map`. `node src/mergeRecords.js`

## Notes

- Sort the file list before merging: `readdirSync` order is platform-dependent and "last file wins" must be deterministic.
- For files too large for memory, stream-concat arrays with `JSONStream` (see the recipe); object deep-merge cannot stream.
- Validate merged output with AJV before shipping it in a build step.
