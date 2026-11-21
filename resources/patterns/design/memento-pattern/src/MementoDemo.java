import java.util.ArrayDeque;
import java.util.Deque;

// The caretaker holds Snapshot references but cannot inspect their state.
interface Snapshot {}

class TextEditor {
    private static final int SCHEMA_VERSION = 1;
    private String content = "";
    private int cursor = 0;

    private static final class EditorMemento implements Snapshot {
        private final String content;
        private final int cursor;
        private final int version;

        private EditorMemento(String content, int cursor, int version) {
            this.content = content;
            this.cursor = cursor;
            this.version = version;
        }
    }

    public void type(String text) {
        content = content.substring(0, cursor)
               + text
               + content.substring(cursor);
        cursor += text.length();
    }

    public void moveCursor(int position) {
        cursor = Math.max(0, Math.min(position, content.length()));
    }

    public Snapshot save() {
        return new EditorMemento(content, cursor, SCHEMA_VERSION);
    }

    public void restore(Snapshot snapshot) {
        if (!(snapshot instanceof EditorMemento)) {
            throw new IllegalArgumentException("Snapshot belongs to another originator");
        }
        EditorMemento m = (EditorMemento) snapshot;
        if (m.version != SCHEMA_VERSION) {
            throw new IllegalStateException("Unsupported memento version " + m.version);
        }
        content = m.content;
        cursor = m.cursor;
    }

    public String getContent() { return content; }
}

class History {
    private final Deque<Snapshot> stack = new ArrayDeque<>();
    private final int limit;

    History(int limit) { this.limit = limit; }

    public void push(Snapshot snapshot) {
        stack.push(snapshot);
        while (stack.size() > limit) stack.removeLast();
    }

    public Snapshot pop() {
        return stack.isEmpty() ? null : stack.pop();
    }
}

public class MementoDemo {
    public static void main(String[] args) {
        TextEditor editor = new TextEditor();
        History history = new History(50);

        history.push(editor.save());
        editor.type("Hello ");
        history.push(editor.save());
        editor.type("World!");
        System.out.println(editor.getContent()); // Hello World!

        editor.restore(history.pop());
        System.out.println(editor.getContent()); // Hello

        editor.restore(history.pop());
        System.out.println("'" + editor.getContent() + "'"); // ''

        editor.type("ab");
        editor.type("ef");
        editor.moveCursor(2);
        editor.type("cd");
        System.out.println(editor.getContent()); // abcdef
    }
}
