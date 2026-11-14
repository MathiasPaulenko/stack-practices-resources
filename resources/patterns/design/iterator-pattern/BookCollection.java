// Iterator pattern — Java.
// BookCollection implements Iterable<String> so the enhanced for-loop works,
// plus a reverse traversal via a custom Iterator. Run:
//   javac BookCollection.java && java BookCollection

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class BookCollection implements Iterable<String> {
    private final List<String> books = new ArrayList<>();

    public void add(String book) {
        books.add(book);
    }

    @Override
    public Iterator<String> iterator() {
        return books.iterator();
    }

    public Iterator<String> reverseIterator() {
        return new ReverseIterator<>(books);
    }

    public static void main(String[] args) {
        BookCollection collection = new BookCollection();
        collection.add("Design Patterns");
        collection.add("Clean Code");
        collection.add("Refactoring");

        System.out.println("Forward:");
        for (String book : collection) {
            System.out.println("  " + book);
        }

        System.out.println("Reverse:");
        Iterator<String> it = collection.reverseIterator();
        while (it.hasNext()) {
            System.out.println("  " + it.next());
        }
    }
}

class ReverseIterator<T> implements Iterator<T> {
    private final List<T> list;
    private int index;

    public ReverseIterator(List<T> list) {
        this.list = list;
        this.index = list.size() - 1;
    }

    @Override
    public boolean hasNext() {
        return index >= 0;
    }

    @Override
    public T next() {
        return list.get(index--);
    }
}
