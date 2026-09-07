// MVVM Pattern — JavaScript implementation with TodoApp
// Model: TodoRepository (data + business logic)
// ViewModel: TodoViewModel (observable state + commands)
// View: TodoConsoleView (declarative rendering, subscribes to VM)

class TodoItem {
  constructor(id, text) {
    this.id = id;
    this.text = text;
    this.done = false;
  }
}

// --- Model ---
class TodoRepository {
  constructor() {
    this.items = [];
    this.nextId = 1;
  }

  add(text) {
    if (!text || !text.trim()) return null;
    const item = new TodoItem(this.nextId++, text.trim());
    this.items.push(item);
    return item;
  }

  toggle(id) {
    const item = this.items.find(i => i.id === id);
    if (item) item.done = !item.done;
  }

  remove(id) {
    this.items = this.items.filter(i => i.id !== id);
  }

  clearCompleted() {
    this.items = this.items.filter(i => !i.done);
  }

  all() {
    return [...this.items];
  }
}

// --- ViewModel ---
class TodoViewModel {
  constructor(repository) {
    this.repository = repository;
    this.listeners = [];
  }

  addTodo(text) {
    this.repository.add(text);
    this.notify();
  }

  toggle(id) {
    this.repository.toggle(id);
    this.notify();
  }

  remove(id) {
    this.repository.remove(id);
    this.notify();
  }

  clearCompleted() {
    this.repository.clearCompleted();
    this.notify();
  }

  get items() {
    return this.repository.all();
  }

  get completedCount() {
    return this.items.filter(i => i.done).length;
  }

  get pendingCount() {
    return this.items.filter(i => !i.done).length;
  }

  get totalCount() {
    return this.items.length;
  }

  subscribe(listener) {
    this.listeners.push(listener);
  }

  notify() {
    this.listeners.forEach(l => l());
  }
}

// --- View (Console) ---
class TodoConsoleView {
  constructor(viewModel) {
    this.viewModel = viewModel;
    this.viewModel.subscribe(() => this.render());
  }

  render() {
    console.log('\n--- Todo List ---');
    for (const item of this.viewModel.items) {
      console.log(`  ${item.done ? '[x]' : '[ ]'} ${item.id}: ${item.text}`);
    }
    console.log(`\n  Total: ${this.viewModel.totalCount} | Completed: ${this.viewModel.completedCount} | Pending: ${this.viewModel.pendingCount}`);
  }

  onAdd(text) {
    this.viewModel.addTodo(text);
  }

  onToggle(id) {
    this.viewModel.toggle(id);
  }

  onRemove(id) {
    this.viewModel.remove(id);
  }
}

// --- Usage ---
const repo = new TodoRepository();
const vm = new TodoViewModel(repo);
const view = new TodoConsoleView(vm);

view.onAdd('Buy groceries');
view.onAdd('Walk the dog');
view.onAdd('Write blog post');
view.onToggle(1);
view.onRemove(2);

module.exports = { TodoItem, TodoRepository, TodoViewModel, TodoConsoleView };
