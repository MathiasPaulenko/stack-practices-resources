// Iterator Pattern for Custom Collections — runnable TypeScript.
//
// Two traversals over one tree (pre-order DFS and level-order BFS with an
// index-based queue), plus an async paginated iterator.
//
// Run with ts-node / deno / bun:
//   npx ts-node iterators.ts   or   deno run iterators.ts

interface Iterator<T> {
  next(): T | null;
  hasNext(): boolean;
  reset(): void;
}

interface IterableCollection<T> {
  createIterator(): Iterator<T>;
}

class TreeNode<T> {
  children: TreeNode<T>[] = [];

  constructor(public value: T) {}

  addChild(child: TreeNode<T>): void {
    this.children.push(child);
  }
}

class PreOrderIterator<T> implements Iterator<T> {
  private stack: TreeNode<T>[] = [];

  constructor(root: TreeNode<T>) {
    this.stack.push(root);
  }

  next(): T | null {
    if (!this.hasNext()) return null;
    const node = this.stack.pop()!;
    for (let i = node.children.length - 1; i >= 0; i--) {
      this.stack.push(node.children[i]);
    }
    return node.value;
  }

  hasNext(): boolean {
    return this.stack.length > 0;
  }

  reset(): void {
    this.stack = [];
  }
}

// Index-based queue: O(1) per next() — no queue.shift() reindexing.
class LevelOrderIterator<T> implements Iterator<T> {
  private queue: TreeNode<T>[] = [];
  private head = 0;

  constructor(root: TreeNode<T>) {
    this.queue.push(root);
  }

  next(): T | null {
    if (!this.hasNext()) return null;
    const node = this.queue[this.head++];
    this.queue.push(...node.children);
    return node.value;
  }

  hasNext(): boolean {
    return this.head < this.queue.length;
  }

  reset(): void {
    this.queue = [];
    this.head = 0;
  }
}

class FileSystem implements IterableCollection<string> {
  private root = new TreeNode<string>('root');
  private nodes = new Map<string, TreeNode<string>>();

  constructor() {
    this.nodes.set('root', this.root);
  }

  addNode(parentPath: string, name: string): void {
    const parent = this.nodes.get(parentPath);
    if (!parent) throw new Error(`Unknown path: ${parentPath}`);
    const child = new TreeNode<string>(name);
    parent.addChild(child);
    this.nodes.set(name, child);
  }

  createIterator(type: 'pre-order' | 'level-order' = 'pre-order'): Iterator<string> {
    return type === 'level-order'
      ? new LevelOrderIterator(this.root)
      : new PreOrderIterator(this.root);
  }
}

interface AsyncIterator<T> {
  next(): Promise<T | null>;
  hasNext(): boolean;
}

class DatabaseQueryIterator implements AsyncIterator<Record<string, unknown>> {
  private currentPage: Record<string, unknown>[] = [];
  private pageIndex = 0;
  private offset = 0;
  private hasMore = true;

  constructor(
    private query: string,
    private pageSize: number = 100,
    private db: { query: (sql: string, params: unknown[]) => Promise<Record<string, unknown>[]> }
  ) {}

  async next(): Promise<Record<string, unknown> | null> {
    if (this.pageIndex >= this.currentPage.length) {
      if (!this.hasMore) return null;
      await this.loadNextPage();
    }
    if (this.pageIndex >= this.currentPage.length) return null;
    return this.currentPage[this.pageIndex++];
  }

  hasNext(): boolean {
    return this.hasMore || this.pageIndex < this.currentPage.length;
  }

  private async loadNextPage(): Promise<void> {
    this.currentPage = await this.db.query(
      `${this.query} LIMIT ${this.pageSize} OFFSET ${this.offset}`,
      []
    );
    this.offset += this.pageSize;
    this.pageIndex = 0;
    this.hasMore = this.currentPage.length === this.pageSize;
  }
}

// --- Demo ---
function collect<T>(it: Iterator<T>): T[] {
  const out: T[] = [];
  while (it.hasNext()) out.push(it.next()!);
  return out;
}

const fs = new FileSystem();
fs.addNode('root', 'src');
fs.addNode('root', 'dist');
fs.addNode('src', 'index.ts');

console.log('Pre-order:  ', collect(fs.createIterator('pre-order')));
console.log('Level-order:', collect(fs.createIterator('level-order')));

// Fake paginated db: two pages of 2 rows, then empty
const pages = [[{ id: 1 }, { id: 2 }], [{ id: 3 }], []];
let call = 0;
const fakeDb = {
  query: async () => pages[call++] ?? [],
};

async function demo() {
  const qit = new DatabaseQueryIterator('SELECT * FROM t', 2, fakeDb);
  const rows: Record<string, unknown>[] = [];
  while (qit.hasNext()) {
    const row = await qit.next();
    if (row) rows.push(row);
  }
  console.log('Paginated rows:', rows);
}

demo();
