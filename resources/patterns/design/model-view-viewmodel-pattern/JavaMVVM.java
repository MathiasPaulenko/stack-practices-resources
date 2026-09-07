import java.util.*;

// MVVM Pattern — Java implementation with TodoApp
// Model: TodoRepository (data + business logic)
// ViewModel: TodoViewModel (observable state + commands)
// View: TodoConsoleView (declarative rendering, subscribes to VM)

class TodoItem {
    private final int id;
    private final String text;
    private boolean done;

    public TodoItem(int id, String text) {
        this.id = id;
        this.text = text;
    }

    public int getId() { return id; }
    public String getText() { return text; }
    public boolean isDone() { return done; }
    public void setDone(boolean done) { this.done = done; }
}

// --- Model ---
class TodoRepository {
    private final List<TodoItem> items = new ArrayList<>();
    private int nextId = 1;

    public TodoItem add(String text) {
        if (text == null || text.trim().isEmpty()) return null;
        TodoItem item = new TodoItem(nextId++, text.trim());
        items.add(item);
        return item;
    }

    public void toggle(int id) {
        items.stream().filter(i -> i.getId() == id).findFirst()
            .ifPresent(i -> i.setDone(!i.isDone()));
    }

    public void remove(int id) {
        items.removeIf(i -> i.getId() == id);
    }

    public void clearCompleted() {
        items.removeIf(TodoItem::isDone);
    }

    public List<TodoItem> all() { return new ArrayList<>(items); }
}

// --- ViewModel ---
class TodoViewModel {
    private final TodoRepository repository;
    private final List<Runnable> listeners = new ArrayList<>();

    public TodoViewModel(TodoRepository repository) {
        this.repository = repository;
    }

    public void addTodo(String text) {
        repository.add(text);
        notifyListeners();
    }

    public void toggle(int id) {
        repository.toggle(id);
        notifyListeners();
    }

    public void remove(int id) {
        repository.remove(id);
        notifyListeners();
    }

    public void clearCompleted() {
        repository.clearCompleted();
        notifyListeners();
    }

    public List<TodoItem> getItems() { return repository.all(); }

    public int getCompletedCount() {
        return (int) repository.all().stream().filter(TodoItem::isDone).count();
    }

    public int getPendingCount() {
        return (int) repository.all().stream().filter(i -> !i.isDone()).count();
    }

    public int getTotalCount() { return repository.all().size(); }

    public void subscribe(Runnable listener) { listeners.add(listener); }

    private void notifyListeners() { listeners.forEach(Runnable::run); }
}

// --- View (Console) ---
class TodoConsoleView {
    private final TodoViewModel viewModel;

    public TodoConsoleView(TodoViewModel viewModel) {
        this.viewModel = viewModel;
        this.viewModel.subscribe(this::render);
    }

    public void render() {
        System.out.println("\n--- Todo List ---");
        for (TodoItem item : viewModel.getItems()) {
            System.out.println("  " + (item.isDone() ? "[x]" : "[ ]") + " " + item.getId() + ": " + item.getText());
        }
        System.out.println("\n  Total: " + viewModel.getTotalCount() +
            " | Completed: " + viewModel.getCompletedCount() +
            " | Pending: " + viewModel.getPendingCount());
    }

    public void onAdd(String text) { viewModel.addTodo(text); }
    public void onToggle(int id) { viewModel.toggle(id); }
    public void onRemove(int id) { viewModel.remove(id); }
}

// --- Usage ---
public class JavaMVVM {
    public static void main(String[] args) {
        TodoRepository repo = new TodoRepository();
        TodoViewModel vm = new TodoViewModel(repo);
        TodoConsoleView view = new TodoConsoleView(vm);

        view.onAdd("Buy groceries");
        view.onAdd("Walk the dog");
        view.onAdd("Write blog post");
        view.onToggle(1);
        view.onRemove(2);
    }
}
