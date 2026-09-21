// LinkedList implementing Symbol.iterator + generator-based alternative
// traversals — for...of, spread, destructuring all work out of the box.
//
// Run with ts-node / deno / bun:
//   npx ts-node linked-list.ts   or   deno run linked-list.ts

class LinkedListNode<T> {
  constructor(public value: T, public next: LinkedListNode<T> | null = null) {}
}

class LinkedList<T> implements Iterable<T> {
  private head: LinkedListNode<T> | null = null;
  private tail: LinkedListNode<T> | null = null;
  private size = 0;

  append(value: T) {
    const node = new LinkedListNode(value);
    if (!this.head) { this.head = node; this.tail = node; }
    else { this.tail!.next = node; this.tail = node; }
    this.size++;
  }

  get length() { return this.size; }

  [Symbol.iterator](): Iterator<T> {
    let current = this.head;
    return {
      next(): IteratorResult<T> {
        if (!current) return { done: true, value: undefined };
        const value = current.value;
        current = current.next;
        return { done: false, value };
      }
    };
  }

  *reverseIterator(): Generator<T> {
    const values: T[] = [];
    let current = this.head;
    while (current) { values.unshift(current.value); current = current.next; }
    for (const v of values) yield v;
  }

  *filterIterator(pred: (v: T) => boolean): Generator<T> {
    let current = this.head;
    while (current) {
      if (pred(current.value)) yield current.value;
      current = current.next;
    }
  }
}

// --- Demo ---
const list = new LinkedList<number>();
for (const n of [1, 2, 3, 4, 5]) list.append(n);

console.log('for...of: ', [...list]);
console.log('reverse:  ', [...list.reverseIterator()]);
console.log('evens:    ', [...list.filterIterator(x => x % 2 === 0)]);
console.log('spread:   ', [...list]);
