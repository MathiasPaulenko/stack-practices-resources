/**
 * Eager Loading pattern - runnable single-file JavaScript example.
 *
 * Source: https://stackpractices.com/patterns/eager-loading-pattern/
 *
 * Run: node eager-loading.js  (requires Node >= 22.13 for node:sqlite)
 * Expected output: query counts for the naive N+1 loop (1 + N), the JOIN
 * variant (1), and the batch variant (2), then the loaded books.
 */

const { DatabaseSync } = require('node:sqlite');

class Author {
  constructor(id, name) {
    this.id = id;
    this.name = name;
  }
}

class Book {
  constructor(id, title, authorId) {
    this.id = id;
    this.title = title;
    this.authorId = authorId;
    this.author = null;
  }
}

// Wraps DatabaseSync and counts every prepared query that runs.
class CountingDb {
  constructor(db) {
    this.db = db;
    this.queries = 0;
  }

  prepare(sql) {
    const stmt = this.db.prepare(sql);
    const counting = this;
    return {
      all: (...args) => { counting.queries += 1; return stmt.all(...args); },
      get: (...args) => { counting.queries += 1; return stmt.get(...args); },
      run: (...args) => { counting.queries += 1; return stmt.run(...args); },
    };
  }
}

class BookRepository {
  constructor(db) {
    this.db = db;
  }

  // N+1 Problem (BAD): 1 query + 1 per book
  findAllWithAuthorsNaive() {
    const books = this.db.prepare('SELECT id, title, author_id FROM books').all()
      .map(r => new Book(r.id, r.title, r.author_id));
    for (const book of books) {
      const author = this.db.prepare('SELECT id, name FROM authors WHERE id = ?')
        .get(book.authorId);
      book.author = author ? new Author(author.id, author.name) : null;
    }
    return books;
  }

  // Eager Loading (GOOD): single JOIN query
  findAllWithAuthorsEager() {
    const rows = this.db.prepare(`
      SELECT b.id AS book_id, b.title, b.author_id,
             a.id AS author_id, a.name AS author_name
      FROM books b
      JOIN authors a ON b.author_id = a.id
    `).all();
    return rows.map(r => {
      const book = new Book(r.book_id, r.title, r.author_id);
      book.author = new Author(r.author_id, r.author_name);
      return book;
    });
  }

  // Batch loading: two queries, no JOIN
  findAllWithAuthorsBatch() {
    const books = this.db.prepare('SELECT id, title, author_id FROM books').all()
      .map(r => new Book(r.id, r.title, r.author_id));
    const authorIds = [...new Set(books.map(b => b.authorId))];
    const authors = this.db.prepare(
      `SELECT id, name FROM authors WHERE id IN (${authorIds.join(',')})`
    ).all();
    const authorMap = new Map(authors.map(a => [a.id, new Author(a.id, a.name)]));
    for (const book of books) {
      book.author = authorMap.get(book.authorId) || null;
    }
    return books;
  }
}

function seed(db, bookCount = 100) {
  db.exec(`
    CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author_id INTEGER);
    INSERT INTO authors (name) VALUES ('Alice'), ('Bob');
  `);
  const insert = db.prepare('INSERT INTO books (title, author_id) VALUES (?, ?)');
  for (let i = 1; i <= bookCount; i++) {
    insert.run(`Book ${i}`, 1 + (i % 2));
  }
}

const db = new DatabaseSync(':memory:');
seed(db);
const counting = new CountingDb(db);
const repo = new BookRepository(counting);

for (const [label, method] of [
  ['naive', () => repo.findAllWithAuthorsNaive()],
  ['eager JOIN', () => repo.findAllWithAuthorsEager()],
  ['batch', () => repo.findAllWithAuthorsBatch()],
]) {
  counting.queries = 0;
  const books = method();
  console.log(`${label.padStart(10)}: ${counting.queries} queries for ${books.length} books`);
}

const book = repo.findAllWithAuthorsEager()[0];
console.log(`${book.title} by ${book.author.name}`);
