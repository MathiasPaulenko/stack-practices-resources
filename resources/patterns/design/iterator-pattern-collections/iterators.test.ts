// Test suite for the custom-collection iterators — node:test, no deps.
// Run: npx tsx --test iterators.test.ts   (or: node --test --import tsx iterators.test.ts)

import { test } from 'node:test';
import assert from 'node:assert/strict';

// Re-declare the minimal surface the tests exercise (keeps this file
// self-contained — the full classes live in iterators.ts).

interface Iterator<T> {
  next(): T | null;
  hasNext(): boolean;
  reset(): void;
}

class TreeNode<T> {
  children: TreeNode<T>[] = [];
  constructor(public value: T) {}
  addChild(child: TreeNode<T>): void { this.children.push(child); }
}

class PreOrderIterator<T> implements Iterator<T> {
  private stack: TreeNode<T>[] = [];
  constructor(root: TreeNode<T>) { this.stack.push(root); }
  next(): T | null {
    if (!this.hasNext()) return null;
    const node = this.stack.pop()!;
    for (let i = node.children.length - 1; i >= 0; i--) this.stack.push(node.children[i]);
    return node.value;
  }
  hasNext(): boolean { return this.stack.length > 0; }
  reset(): void { this.stack = []; }
}

class LevelOrderIterator<T> implements Iterator<T> {
  private queue: TreeNode<T>[] = [];
  private head = 0;
  constructor(root: TreeNode<T>) { this.queue.push(root); }
  next(): T | null {
    if (!this.hasNext()) return null;
    const node = this.queue[this.head++];
    this.queue.push(...node.children);
    return node.value;
  }
  hasNext(): boolean { return this.head < this.queue.length; }
  reset(): void { this.queue = []; this.head = 0; }
}

class PostOrderIterator<T> implements Iterator<T> {
  private out: T[] = [];
  private head = 0;
  constructor(root: TreeNode<T>) {
    const visit = (n: TreeNode<T>) => {
      for (const c of n.children) visit(c);
      this.out.push(n.value);
    };
    visit(root);
  }
  next(): T | null { return this.hasNext() ? this.out[this.head++] : null; }
  hasNext(): boolean { return this.head < this.out.length; }
  reset(): void { this.head = 0; }
}

function collect<T>(it: Iterator<T>): T[] {
  const out: T[] = [];
  while (it.hasNext()) out.push(it.next()!);
  return out;
}

function tree() {
  const root = new TreeNode('root');
  const a = new TreeNode('a');
  const b = new TreeNode('b');
  root.addChild(a);
  root.addChild(b);
  a.addChild(new TreeNode('c'));
  return root;
}

test('pre-order yields root, then left subtree, then right', () => {
  assert.deepEqual(collect(new PreOrderIterator(tree())), ['root', 'a', 'c', 'b']);
});

test('level-order yields breadth-first sequence', () => {
  assert.deepEqual(collect(new LevelOrderIterator(tree())), ['root', 'a', 'b', 'c']);
});

test('post-order yields children before their parent', () => {
  assert.deepEqual(collect(new PostOrderIterator(tree())), ['c', 'a', 'b', 'root']);
});

test('single-node tree yields exactly one value', () => {
  const it = new PreOrderIterator(new TreeNode('root'));
  assert.equal(it.next(), 'root');
  assert.equal(it.hasNext(), false);
  assert.equal(it.next(), null);
});

test('hasNext() is idempotent — it does not consume elements', () => {
  const it = new LevelOrderIterator(tree());
  assert.equal(it.hasNext(), true);
  assert.equal(it.hasNext(), true);
  assert.equal(it.next(), 'root');
});

test('next() after exhaustion returns null, not an exception', () => {
  const it = new PreOrderIterator(tree());
  collect(it);
  assert.equal(it.next(), null);
});
