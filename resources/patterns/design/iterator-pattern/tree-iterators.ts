// Iterator pattern — TypeScript.
// Two traversal strategies over one binary tree: in-order (DFS with a
// stack) and breadth-first (queue). Both implement the same Iterator
// contract, so the client can't tell them apart.
// Run: npx tsx tree-iterators.ts  (or: npx ts-node, deno run)

interface Iterator<T> {
  next(): { value: T | null; done: boolean };
  hasNext(): boolean;
  reset(): void;
}

// Binary tree node
export class TreeNode<T> {
  constructor(
    public value: T,
    public left: TreeNode<T> | null = null,
    public right: TreeNode<T> | null = null
  ) {}
}

// In-order traversal (left, root, right)
export class InOrderIterator<T> implements Iterator<T> {
  private stack: TreeNode<T>[] = [];
  private readonly root: TreeNode<T>;

  constructor(root: TreeNode<T>) {
    this.root = root;
    this.pushLeft(root);
  }

  private pushLeft(node: TreeNode<T> | null) {
    while (node) {
      this.stack.push(node);
      node = node.left;
    }
  }

  hasNext(): boolean {
    return this.stack.length > 0;
  }

  next(): { value: T | null; done: boolean } {
    if (this.stack.length === 0) return { value: null, done: true };
    const node = this.stack.pop()!;
    this.pushLeft(node.right);
    return { value: node.value, done: false };
  }

  reset() {
    this.stack = [];
    this.pushLeft(this.root);
  }
}

// Breadth-first traversal (level order)
export class BFSIterator<T> implements Iterator<T> {
  private queue: TreeNode<T>[];
  private readonly root: TreeNode<T>;

  constructor(root: TreeNode<T>) {
    this.root = root;
    this.queue = [root];
  }

  hasNext(): boolean {
    return this.queue.length > 0;
  }

  next(): { value: T | null; done: boolean } {
    if (this.queue.length === 0) return { value: null, done: true };
    const node = this.queue.shift()!;
    if (node.left) this.queue.push(node.left);
    if (node.right) this.queue.push(node.right);
    return { value: node.value, done: false };
  }

  reset() {
    this.queue = [this.root];
  }
}

export function buildTree(): TreeNode<number> {
  return new TreeNode(
    5,
    new TreeNode(3, new TreeNode(1), new TreeNode(4)),
    new TreeNode(7, new TreeNode(6), new TreeNode(8))
  );
}

function collect<T>(it: Iterator<T>): (T | null)[] {
  const out: (T | null)[] = [];
  while (it.hasNext()) out.push(it.next().value);
  return out;
}

// Demo (skipped when imported by the test file)
const isMain =
  typeof process !== "undefined" &&
  process.argv[1] &&
  /tree-iterators\.ts$/.test(process.argv[1]);

if (isMain) {
  const tree = buildTree();
  console.log("In-order:", collect(new InOrderIterator(tree)).join(", "));
  console.log("BFS:     ", collect(new BFSIterator(tree)).join(", "));
}
