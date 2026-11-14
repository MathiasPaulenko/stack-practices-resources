// Tests for the tree iterators. Run: npx tsx --test tree-iterators.test.ts
// (or: node --experimental-strip-types --test tree-iterators.test.ts)

import { test } from "node:test";
import assert from "node:assert/strict";
import { BFSIterator, InOrderIterator, buildTree } from "./tree-iterators.ts";

test("in-order iterator yields sorted values", () => {
  const it = new InOrderIterator(buildTree());
  const out: (number | null)[] = [];
  while (it.hasNext()) out.push(it.next().value);
  assert.deepEqual(out, [1, 3, 4, 5, 6, 7, 8]);
});

test("BFS iterator yields level order", () => {
  const it = new BFSIterator(buildTree());
  const out: (number | null)[] = [];
  while (it.hasNext()) out.push(it.next().value);
  assert.deepEqual(out, [5, 3, 7, 1, 4, 6, 8]);
});

test("exhausted iterator reports done", () => {
  const it = new InOrderIterator(buildTree());
  while (it.hasNext()) it.next();
  assert.equal(it.hasNext(), false);
  assert.deepEqual(it.next(), { value: null, done: true });
});

test("hasNext is idempotent", () => {
  const it = new BFSIterator(buildTree());
  assert.equal(it.hasNext(), true);
  assert.equal(it.hasNext(), true);
  assert.equal(it.next().value, 5);
});

test("reset restores the traversal", () => {
  const it = new InOrderIterator(buildTree());
  it.next();
  it.next();
  it.reset();
  assert.equal(it.next().value, 1);
});
