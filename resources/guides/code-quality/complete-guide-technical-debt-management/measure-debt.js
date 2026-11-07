// measure-debt.js — Snapshot of debt metrics over time.
// Runnable with plain Node.js: node measure-debt.js [srcDir]
//
// Two metrics are self-contained (TODO markers, outdated deps).
// Coverage, duplication and complexity are read from the JSON reports
// of tools you already run (coverage-summary.json, jscpd), when present.

const { execSync } = require('node:child_process');
const { readFileSync, readdirSync, statSync, existsSync } = require('node:fs');
const { join, resolve } = require('node:path');

// Count TODO/FIXME/HACK markers across the source tree — portable,
// no grep dependency.
function countTodos(dir) {
  let count = 0;
  const pattern = /\b(TODO|FIXME|HACK|XXX)\b/;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.name.startsWith('.') || entry.name === 'node_modules') continue;
    if (entry.isDirectory()) {
      count += countTodos(full);
    } else if (/\.(ts|tsx|js|jsx)$/.test(entry.name)) {
      count += readFileSync(full, 'utf-8')
        .split('\n')
        .filter((l) => pattern.test(l)).length;
    }
  }
  return count;
}

// npm outdated exits non-zero when anything is outdated — that is not a
// failure, read the JSON it printed anyway.
function countOutdatedDeps(cwd) {
  try {
    const out = execSync('npm outdated --json', { encoding: 'utf-8', cwd });
    return Object.keys(JSON.parse(out || '{}')).length;
  } catch (err) {
    const stdout = err.stdout;
    return stdout ? Object.keys(JSON.parse(stdout)).length : 0;
  }
}

// line coverage % from an Istanbul coverage-summary.json, if present
function readCoverage(cwd) {
  const file = join(cwd, 'coverage', 'coverage-summary.json');
  if (!existsSync(file)) return null;
  const data = JSON.parse(readFileSync(file, 'utf-8'));
  return data.total?.lines?.pct ?? null;
}

// duplication % from a jscpd JSON report (jscpd-report.json), if present
function readDuplication(cwd) {
  const file = join(cwd, 'report', 'jscpd-report.json');
  if (!existsSync(file)) return null;
  const data = JSON.parse(readFileSync(file, 'utf-8'));
  return data.statistics?.total?.percentage ?? null;
}

const target = resolve(process.argv[2] || '.');

const metrics = {
  todoCount: countTodos(target),
  outdatedDependencies: countOutdatedDeps(target),
  testCoverage: readCoverage(target), // null → tool not run here
  duplicationPercentage: readDuplication(target), // null → tool not run here
};

console.log(JSON.stringify(metrics, null, 2));
