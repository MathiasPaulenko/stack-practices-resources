// JSON diff in two flavors: categorized report and RFC 6902 patch.
//
// Usage:
//   node diff-json.js old.json new.json          # recursive report (no deps)
//   node diff-json.js --patch old.json new.json  # RFC 6902 (needs fast-json-patch)
//
//   npm install fast-json-patch   # only for --patch mode

import { readFileSync } from 'node:fs';

function jsonDiff(oldObj, newObj, path = '', changes = {}) {
  if (JSON.stringify(oldObj) === JSON.stringify(newObj)) return changes;

  const bothObjects =
    oldObj && newObj && typeof oldObj === 'object' && typeof newObj === 'object';

  if (bothObjects && !Array.isArray(oldObj) && !Array.isArray(newObj)) {
    for (const key of new Set([...Object.keys(oldObj), ...Object.keys(newObj)])) {
      const p = `${path}/${key}`;
      if (!(key in oldObj)) changes[p] = { added: newObj[key] };
      else if (!(key in newObj)) changes[p] = { removed: oldObj[key] };
      else jsonDiff(oldObj[key], newObj[key], p, changes);
    }
  } else if (bothObjects && Array.isArray(oldObj) && Array.isArray(newObj)) {
    const common = Math.min(oldObj.length, newObj.length);
    for (let i = 0; i < common; i++) jsonDiff(oldObj[i], newObj[i], `${path}/${i}`, changes);
    for (let i = common; i < newObj.length; i++) changes[`${path}/${i}`] = { added: newObj[i] };
    for (let i = common; i < oldObj.length; i++) changes[`${path}/${i}`] = { removed: oldObj[i] };
  } else {
    changes[path || '/'] = { old: oldObj, new: newObj };
  }
  return changes;
}

const usePatch = process.argv[2] === '--patch';
const [oldPath, newPath] = usePatch ? process.argv.slice(3) : process.argv.slice(2);
const oldDoc = JSON.parse(readFileSync(oldPath, 'utf-8'));
const newDoc = JSON.parse(readFileSync(newPath, 'utf-8'));

if (usePatch) {
  const { compare } = await import('fast-json-patch');
  console.log(JSON.stringify(compare(oldDoc, newDoc), null, 2));
} else {
  const diff = jsonDiff(oldDoc, newDoc);
  const entries = Object.entries(diff);
  if (!entries.length) console.log('No differences found.');
  for (const [path, change] of entries) console.log(`${path.padEnd(30)} ->`, change);
}
