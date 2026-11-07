// Round-trip test: the node tree is plain data, so
// JSON.parse(JSON.stringify(tree)) must be structurally identical
// and render the same shape. Run: node serialization.test.mjs

import { readFileSync } from 'node:fs';
import { strict as assert } from 'node:assert';

const tree = JSON.parse(
  readFileSync(new URL('./form-tree.json', import.meta.url), 'utf-8')
);

// 1. Round-trip: data survives JSON intact
const roundTripped = JSON.parse(JSON.stringify(tree));
assert.deepStrictEqual(roundTripped, tree, 'tree must survive JSON round-trip');

// 2. Count nodes recursively — the composite invariant
function countNodes(node) {
  if (node.type === 'field') return { fields: 1, sections: 0 };
  return node.children.reduce(
    (acc, child) => {
      const sub = countNodes(child);
      return { fields: acc.fields + sub.fields, sections: acc.sections + sub.sections };
    },
    { fields: 0, sections: 1 }
  );
}

const { fields, sections } = countNodes(tree);
assert.equal(fields, 4, 'expected 4 field leaves');
assert.equal(sections, 3, 'expected 3 section composites');

// 3. Only composites carry children — the "safe" variant check
function assertSafe(node) {
  if (node.type === 'field') {
    assert.equal(node.children, undefined, 'leaf must not carry children');
    return;
  }
  assert.ok(Array.isArray(node.children), 'composite must carry children[]');
  node.children.forEach(assertSafe);
}
assert.doesNotThrow(() => assertSafe(tree));

console.log(`OK: ${sections} sections, ${fields} fields, round-trip + safety verified`);
