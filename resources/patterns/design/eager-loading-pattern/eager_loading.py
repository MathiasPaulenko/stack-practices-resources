"""Eager Loading pattern - runnable single-file Python example.

Source: https://stackpractices.com/patterns/eager-loading-pattern/

Run: python eager_loading.py
Expected output: query counts for the naive N+1 loop (1 + N), the JOIN
variant (1), and the batch variant (2), then the loaded books.

The naive version counts every author lookup, so you can see the N+1
pattern instead of just reading about it.
"""

from dataclasses import dataclass
from typing import List, Optional
import sqlite3


@dataclass
class Author:
    id: int
    name: str


@dataclass
class Book:
    id: int
    title: str
    author_id: int
    author: Optional[Author] = None


class CountingConnection:
    """Wraps sqlite3.Connection and counts execute() calls."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self.queries = 0

    def execute(self, sql: str, params=()):
        self.queries += 1
        return self._conn.execute(sql, params)


class BookRepository:
    def __init__(self, conn: CountingConnection) -> None:
        self._conn = conn

    # N+1 Problem (BAD): 1 query + 1 per book
    def find_all_with_authors_naive(self) -> List[Book]:
        books = []
        for row in self._conn.execute("SELECT id, title, author_id FROM books"):
            book = Book(id=row["id"], title=row["title"], author_id=row["author_id"])
            author_row = self._conn.execute(
                "SELECT id, name FROM authors WHERE id = ?", (book.author_id,)
            ).fetchone()
            if author_row:
                book.author = Author(id=author_row["id"], name=author_row["name"])
            books.append(book)
        return books

    # Eager Loading (GOOD): single JOIN query
    def find_all_with_authors_eager(self) -> List[Book]:
        query = """
            SELECT b.id AS book_id, b.title, b.author_id,
                   a.id AS author_id, a.name AS author_name
            FROM books b
            JOIN authors a ON b.author_id = a.id
        """
        books = []
        for row in self._conn.execute(query):
            author = Author(id=row["author_id"], name=row["author_name"])
            book = Book(
                id=row["book_id"],
                title=row["title"],
                author_id=row["author_id"],
                author=author,
            )
            books.append(book)
        return books

    # Batch loading: two queries, no JOIN
    def find_all_with_authors_batch(self) -> List[Book]:
        books = []
        rows = self._conn.execute("SELECT id, title, author_id FROM books").fetchall()
        author_ids = [r["author_id"] for r in rows]

        placeholders = ",".join("?" * len(author_ids))
        authors = {
            r["id"]: Author(id=r["id"], name=r["name"])
            for r in self._conn.execute(
                f"SELECT id, name FROM authors WHERE id IN ({placeholders})",
                author_ids,
            )
        }

        for row in rows:
            books.append(
                Book(
                    id=row["id"],
                    title=row["title"],
                    author_id=row["author_id"],
                    author=authors.get(row["author_id"]),
                )
            )
        return books


def seed(conn: sqlite3.Connection, book_count: int = 100) -> None:
    conn.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute(
        "CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author_id INTEGER)"
    )
    conn.execute("INSERT INTO authors (name) VALUES ('Alice'), ('Bob')")
    for i in range(1, book_count + 1):
        conn.execute(
            "INSERT INTO books (title, author_id) VALUES (?, ?)",
            (f"Book {i}", 1 + i % 2),
        )


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    seed(conn)
    counting = CountingConnection(conn)
    repo = BookRepository(counting)

    for label, method in (
        ("naive", repo.find_all_with_authors_naive),
        ("eager JOIN", repo.find_all_with_authors_eager),
        ("batch", repo.find_all_with_authors_batch),
    ):
        counting.queries = 0
        books = method()
        print(f"{label:>10}: {counting.queries} queries for {len(books)} books")

    book = repo.find_all_with_authors_eager()[0]
    print(f"{book.title} by {book.author.name}")
