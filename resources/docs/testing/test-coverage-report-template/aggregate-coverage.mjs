#!/usr/bin/env node
// Aggregates a c8/istanbul coverage-summary.json into the
// "Coverage by Module" table used by the template.
//
// Usage:
//   npx vitest run --coverage --reporter=json-summary
//   node aggregate-coverage.mjs coverage/coverage-summary.json src/modules/

import { readFileSync } from 'node:fs';

const [file, moduleRoot = 'src/modules/'] = process.argv.slice(2);
const summary = JSON.parse(readFileSync(file, 'utf8'));

const rows = [];
let total = null;
for (const [key, value] of Object.entries(summary)) {
  if (key === 'total') {
    total = value;
    continue;
  }
  const module = key.slice(key.indexOf(moduleRoot) + moduleRoot.length).split('/')[0];
  rows.push({
    module,
    lines: value.lines.pct.toFixed(1),
    branches: value.branches.pct.toFixed(1),
    functions: value.functions.pct.toFixed(1),
  });
}

// merge entries for the same module directory
const byModule = new Map();
for (const row of rows) {
  const prev = byModule.get(row.module) ?? { n: 0, lines: 0, branches: 0, functions: 0 };
  byModule.set(row.module, {
    n: prev.n + 1,
    lines: prev.lines + Number(row.lines),
    branches: prev.branches + Number(row.branches),
    functions: prev.functions + Number(row.functions),
  });
}

console.log('| Module | Line Coverage | Branch Coverage | Function Coverage |');
console.log('|--------|--------------|-----------------|-------------------|');
for (const [module, agg] of [...byModule.entries()].sort()) {
  console.log(
    `| ${module} | ${(agg.lines / agg.n).toFixed(1)}% | ${(agg.branches / agg.n).toFixed(1)}% | ${(agg.functions / agg.n).toFixed(1)}% |`,
  );
}
if (total) {
  console.log(`| **Total** | **${total.lines.pct.toFixed(1)}%** | **${total.branches.pct.toFixed(1)}%** | **${total.functions.pct.toFixed(1)}%** |`);
}
