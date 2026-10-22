import java.util.*;

/**
 * Eager Loading pattern - runnable single-file Java example.
 *
 * Source: https://stackpractices.com/patterns/eager-loading-pattern/
 *
 * Run: javac EagerLoadingDemo.java && java EagerLoadingDemo
 * Expected output: query counts for the naive N+1 loop (1 + N), the JOIN
 * variant (1), and the batch variant (2).
 *
 * The article version talks JDBC (java.sql). This file swaps the database
 * for an in-memory table that counts "queries" so it compiles and runs
 * with plain javac — the repository logic is the same either way.
 */
public class EagerLoadingDemo {

    static class Author {
        final int id;
        final String name;
        Author(int id, String name) { this.id = id; this.name = name; }
        @Override public String toString() { return name; }
    }

    static class Book {
        final int id;
        final String title;
        final int authorId;
        Author author;
        Book(int id, String title, int authorId) {
            this.id = id; this.title = title; this.authorId = authorId;
        }
        @Override public String toString() { return title + " by " + author; }
    }

    /** In-memory stand-in for a database. Every lookup counts as one query. */
    static class FakeDb {
        int queries;
        private final List<Author> authors = new ArrayList<>();
        private final List<Book> books = new ArrayList<>();

        void seed(int bookCount) {
            authors.add(new Author(1, "Alice"));
            authors.add(new Author(2, "Bob"));
            for (int i = 1; i <= bookCount; i++) {
                books.add(new Book(i, "Book " + i, 1 + (i % 2)));
            }
        }

        List<Book> selectBooks() {
            queries++;
            return new ArrayList<>(books);
        }

        Author selectAuthorById(int id) {
            queries++;
            return authors.stream().filter(a -> a.id == id).findFirst().orElse(null);
        }

        List<Author> selectAuthorsIn(Set<Integer> ids) {
            queries++;
            List<Author> result = new ArrayList<>();
            for (Author a : authors) {
                if (ids.contains(a.id)) result.add(a);
            }
            return result;
        }

        List<Map.Entry<Book, Author>> selectBooksJoinAuthors() {
            queries++;
            List<Map.Entry<Book, Author>> rows = new ArrayList<>();
            for (Book b : books) {
                Author a = authors.stream()
                    .filter(x -> x.id == b.authorId).findFirst().orElse(null);
                rows.add(Map.entry(b, a));
            }
            return rows;
        }
    }

    static class BookRepository {
        private final FakeDb db;
        BookRepository(FakeDb db) { this.db = db; }

        // N+1 Problem (BAD): 1 query + 1 per book
        List<Book> findAllWithAuthorsNaive() {
            List<Book> books = db.selectBooks();
            for (Book book : books) {
                book.author = db.selectAuthorById(book.authorId);
            }
            return books;
        }

        // Eager Loading (GOOD): single JOIN-equivalent query
        List<Book> findAllWithAuthorsEager() {
            List<Book> books = new ArrayList<>();
            for (Map.Entry<Book, Author> row : db.selectBooksJoinAuthors()) {
                Book book = row.getKey();
                book.author = row.getValue();
                books.add(book);
            }
            return books;
        }

        // Batch loading: two queries, no JOIN
        List<Book> findAllWithAuthorsBatch() {
            List<Book> books = db.selectBooks();
            Set<Integer> authorIds = new HashSet<>();
            for (Book b : books) authorIds.add(b.authorId);
            Map<Integer, Author> authorMap = new HashMap<>();
            for (Author a : db.selectAuthorsIn(authorIds)) authorMap.put(a.id, a);
            for (Book book : books) book.author = authorMap.get(book.authorId);
            return books;
        }
    }

    public static void main(String[] args) {
        FakeDb db = new FakeDb();
        db.seed(100);
        BookRepository repo = new BookRepository(db);

        db.queries = 0;
        List<Book> naive = repo.findAllWithAuthorsNaive();
        System.out.printf("%10s: %d queries for %d books%n", "naive", db.queries, naive.size());

        db.queries = 0;
        List<Book> eager = repo.findAllWithAuthorsEager();
        System.out.printf("%10s: %d queries for %d books%n", "eager JOIN", db.queries, eager.size());

        db.queries = 0;
        List<Book> batch = repo.findAllWithAuthorsBatch();
        System.out.printf("%10s: %d queries for %d books%n", "batch", db.queries, batch.size());

        System.out.println(eager.get(0));
    }
}
