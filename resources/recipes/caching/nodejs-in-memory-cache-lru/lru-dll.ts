// lru-dll.ts — LRU cache backed by a Map plus a doubly linked list.
// O(1) get, set, move-to-head and evict-from-tail at any capacity.

interface LRUNode<K, V> {
  key: K;
  value: V;
  prev: LRUNode<K, V> | null;
  next: LRUNode<K, V> | null;
}

export class LRUCache<K, V> {
  private index = new Map<K, LRUNode<K, V>>();
  private head: LRUNode<K, V> | null = null;
  private tail: LRUNode<K, V> | null = null;

  constructor(private readonly capacity: number) {
    if (capacity <= 0) {
      throw new Error("Capacity must be positive");
    }
  }

  get(key: K): V | undefined {
    const node = this.index.get(key);
    if (!node) return undefined;
    this.moveToHead(node);
    return node.value;
  }

  set(key: K, value: V): void {
    const existing = this.index.get(key);
    if (existing) {
      existing.value = value;
      this.moveToHead(existing);
      return;
    }

    const node: LRUNode<K, V> = { key, value, prev: null, next: this.head };
    if (this.head) this.head.prev = node;
    this.head = node;
    if (!this.tail) this.tail = node;
    this.index.set(key, node);

    if (this.index.size > this.capacity) {
      this.evictTail();
    }
  }

  delete(key: K): boolean {
    const node = this.index.get(key);
    if (!node) return false;
    this.unlink(node);
    this.index.delete(key);
    return true;
  }

  has(key: K): boolean {
    return this.index.has(key);
  }

  clear(): void {
    this.index.clear();
    this.head = null;
    this.tail = null;
  }

  get size(): number {
    return this.index.size;
  }

  *entries(): IterableIterator<[K, V]> {
    let node = this.head;
    while (node) {
      yield [node.key, node.value];
      node = node.next;
    }
  }

  private moveToHead(node: LRUNode<K, V>): void {
    if (node === this.head) return;
    this.unlink(node);
    node.prev = null;
    node.next = this.head;
    if (this.head) this.head.prev = node;
    this.head = node;
  }

  private unlink(node: LRUNode<K, V>): void {
    if (node.prev) node.prev.next = node.next;
    if (node.next) node.next.prev = node.prev;
    if (node === this.tail) this.tail = node.prev;
  }

  private evictTail(): void {
    if (!this.tail) return;
    this.index.delete(this.tail.key);
    this.tail = this.tail.prev;
    if (this.tail) {
      this.tail.next = null;
    } else {
      this.head = null;
    }
  }
}
