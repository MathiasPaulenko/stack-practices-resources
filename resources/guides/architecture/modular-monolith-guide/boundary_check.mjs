// Modular monolith boundary linter.
// Rule: a module may import another module's `api` package and `shared.kernel`.
// Nothing else may cross a module boundary — that's the whole architecture.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { join, relative, sep, dirname } from 'node:path';
import { tmpdir } from 'node:os';

const IMPORT_RE = /^import .*from ['"]([\w./-]+)['"]/;

function* walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.name.endsWith('.mjs') || e.name.endsWith('.js')) yield p;
  }
}

export function moduleOf(dotted) {
  const parts = dotted.split(/[./]/).filter(Boolean);
  if (parts[0] === 'shared' && parts[1] === 'kernel') return { type: 'kernel' };
  if (parts[0] === 'modules' && parts.length >= 3) {
    return { type: 'module', name: parts[1], kind: parts[2] === 'api' ? 'api' : 'internal' };
  }
  return { type: null };
}

// Resolve a relative import from the file's own directory to a modules/... path
function resolveImport(fromRel, spec) {
  if (!spec.startsWith('.')) return spec; // bare/absolute spec
  const base = dirname(fromRel).split(sep).join('/');
  const parts = (base + '/' + spec).split('/');
  const out = [];
  for (const p of parts) {
    if (p === '..') out.pop();
    else if (p !== '.') out.push(p);
  }
  return out.join('/');
}

export function checkBoundaries(root) {
  const violations = [];
  for (const file of walk(root)) {
    const rel = relative(root, file).split(sep).join('/');
    const src = moduleOf(rel.replace(/\.m?js$/, ''));
    if (!src.type || src.type === 'kernel') continue;
    const lines = readFileSync(file, 'utf-8').split('\n');
    lines.forEach((line, i) => {
      const m = line.trim().match(IMPORT_RE);
      if (!m) return;
      const dst = moduleOf(resolveImport(rel, m[1]).replace(/\.m?js$/, ''));
      if (dst.type === 'kernel' || dst.type !== 'module' || dst.name === src.name) return;
      if (dst.kind !== 'api') {
        violations.push({
          file: rel, line: i + 1, imp: m[1],
          reason: `${src.name} reaches into ${dst.name}'s internals (only '${dst.name}/api' is public)`,
        });
      }
    });
  }
  return violations;
}

export function report(violations) {
  if (!violations.length) return 'Boundaries intact: all cross-module imports go through public APIs.';
  return 'Boundary violations:\n' + violations.map(
    (v) => `  ${v.file}:${v.line}  import ${v.imp}  — ${v.reason}`
  ).join('\n');
}

function fixture(files) {
  const root = join(tmpdir(), `mm-${process.pid}-${Math.random().toString(36).slice(2)}`);
  for (const [rel, text] of Object.entries(files)) {
    const p = join(root, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, text);
  }
  return { root, cleanup: () => rmSync(root, { recursive: true, force: true }) };
}

test('ignores kernel and same-module imports', () => {
  const { root, cleanup } = fixture({
    'modules/orders/application/place_order.mjs':
      "import { DomainEvent } from '../../../shared/kernel/domain_event.mjs'\n" +
      "import { Order } from '../domain/order.mjs'\n",
  });
  try { assert.deepEqual(checkBoundaries(root), []); } finally { cleanup(); }
});

test('allows api imports', () => {
  const { root, cleanup } = fixture({
    'modules/orders/application/place_order.mjs':
      "import { CatalogApi } from '../../catalog/api/catalog_api.mjs'\n",
  });
  try { assert.deepEqual(checkBoundaries(root), []); } finally { cleanup(); }
});

test('flags internal imports', () => {
  const { root, cleanup } = fixture({
    'modules/orders/application/place_order.mjs':
      "import { ProductRepository } from '../../catalog/infrastructure/product_repository.mjs'\n",
  });
  try {
    const v = checkBoundaries(root);
    assert.equal(v.length, 1);
    assert.match(v[0].reason, /orders reaches into catalog's internals/);
  } finally { cleanup(); }
});

test('flags absolute-style internal imports too', () => {
  const { root, cleanup } = fixture({
    'modules/orders/application/place_order.mjs':
      "import { ProductRepository } from 'modules/catalog/infrastructure/product_repository.mjs'\n",
  });
  try {
    const v = checkBoundaries(root);
    assert.equal(v.length, 1);
  } finally { cleanup(); }
});
