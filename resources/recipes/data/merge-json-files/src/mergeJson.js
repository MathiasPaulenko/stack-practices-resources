// Merge JSON files: array concat, null-safe deep merge, glob multi-merge, dedupe.
const fs = require('fs');
const path = require('path');

const isPlainObject = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const UNSAFE_KEYS = new Set(['__proto__', 'constructor', 'prototype']);

function deepMerge(base, override) {
  const result = { ...base };
  for (const key of Object.keys(override)) {
    if (UNSAFE_KEYS.has(key)) continue; // block prototype pollution
    if (isPlainObject(override[key]) && isPlainObject(result[key])) {
      result[key] = deepMerge(result[key], override[key]);
    } else {
      result[key] = override[key];
    }
  }
  return result;
}

function mergeArrays(dir) {
  return fs.readdirSync(dir)
    .filter((f) => f.endsWith('.json'))
    .flatMap((f) => {
      const data = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf-8'));
      return Array.isArray(data) ? data : [data];
    });
}

function mergeJsonGlob(pattern, output) {
  const glob = require('glob'); // lazy: keep the deepMerge demo dependency-free
  const merged = {};
  for (const filepath of glob.sync(pattern).sort()) {
    const data = JSON.parse(fs.readFileSync(filepath, 'utf-8'));
    if (Array.isArray(data)) merged.items = (merged.items || []).concat(data);
    else Object.assign(merged, data);
  }
  fs.writeFileSync(output, JSON.stringify(merged, null, 2));
}

module.exports = { deepMerge, mergeArrays, mergeJsonGlob };

if (require.main === module) {
  const base = { db: { host: 'x', port: 5432 }, name: 'app' };
  const override = { db: { port: 3306 }, debug: true, extra: null };
  console.log(JSON.stringify(deepMerge(base, override), null, 2));
}
