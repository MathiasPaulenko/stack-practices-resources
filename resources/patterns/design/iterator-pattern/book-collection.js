// Iterator pattern — JavaScript.
// A BookCollection that speaks Symbol.iterator via a generator method,
// plus a reverse traversal helper. Run: node book-collection.js

class BookCollection {
  constructor() {
    this.books = [];
  }

  add(book) {
    this.books.push(book);
  }

  *[Symbol.iterator]() {
    for (const book of this.books) {
      yield book;
    }
  }

  *reverseIterator() {
    for (let i = this.books.length - 1; i >= 0; i--) {
      yield this.books[i];
    }
  }
}

const collection = new BookCollection();
collection.add("Design Patterns");
collection.add("Clean Code");
collection.add("Refactoring");

console.log("Forward:");
for (const book of collection) {
  console.log(`  ${book}`);
}

console.log("Reverse:");
for (const book of collection.reverseIterator()) {
  console.log(`  ${book}`);
}
