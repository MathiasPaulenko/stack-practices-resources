"""MVVM Pattern — Python implementation with TodoApp.

Model: TodoRepository (data + business logic)
ViewModel: TodoViewModel (observable state + commands)
View: TodoConsoleView (declarative rendering, subscribes to VM)
"""
from dataclasses import dataclass
from typing import List, Callable


@dataclass
class TodoItem:
    id: int
    text: str
    done: bool = False


# --- Model ---
class TodoRepository:
    def __init__(self):
        self._items: List[TodoItem] = []
        self._next_id = 1

    def add(self, text: str) -> TodoItem:
        item = TodoItem(id=self._next_id, text=text)
        self._items.append(item)
        self._next_id += 1
        return item

    def toggle(self, item_id: int) -> None:
        for item in self._items:
            if item.id == item_id:
                item.done = not item.done

    def remove(self, item_id: int) -> None:
        self._items = [i for i in self._items if i.id != item_id]

    def all(self) -> List[TodoItem]:
        return list(self._items)

    def clear_completed(self) -> None:
        self._items = [i for i in self._items if not i.done]


# --- ViewModel ---
class TodoViewModel:
    def __init__(self, repository: TodoRepository):
        self._repo = repository
        self._listeners: List[Callable] = []

    def add_todo(self, text: str) -> None:
        if not text.strip():
            return
        self._repo.add(text.strip())
        self._notify()

    def toggle(self, item_id: int) -> None:
        self._repo.toggle(item_id)
        self._notify()

    def remove(self, item_id: int) -> None:
        self._repo.remove(item_id)
        self._notify()

    def clear_completed(self) -> None:
        self._repo.clear_completed()
        self._notify()

    @property
    def items(self) -> List[TodoItem]:
        return self._repo.all()

    @property
    def completed_count(self) -> int:
        return sum(1 for item in self.items if item.done)

    @property
    def pending_count(self) -> int:
        return sum(1 for item in self.items if not item.done)

    @property
    def total_count(self) -> int:
        return len(self.items)

    def subscribe(self, listener: Callable) -> None:
        self._listeners.append(listener)

    def _notify(self) -> None:
        for listener in self._listeners:
            listener()


# --- View (Console) ---
class TodoConsoleView:
    def __init__(self, view_model: TodoViewModel):
        self.vm = view_model
        self.vm.subscribe(self.render)

    def render(self) -> None:
        print("\n--- Todo List ---")
        for item in self.vm.items:
            status = "[x]" if item.done else "[ ]"
            print(f"  {status} {item.id}: {item.text}")
        print(f"\n  Total: {self.vm.total_count} | Completed: {self.vm.completed_count} | Pending: {self.vm.pending_count}")

    def on_add(self, text: str) -> None:
        self.vm.add_todo(text)

    def on_toggle(self, item_id: int) -> None:
        self.vm.toggle(item_id)

    def on_remove(self, item_id: int) -> None:
        self.vm.remove(item_id)


# --- Usage ---
if __name__ == "__main__":
    repo = TodoRepository()
    vm = TodoViewModel(repo)
    view = TodoConsoleView(vm)

    view.on_add("Buy groceries")
    view.on_add("Walk the dog")
    view.on_add("Write blog post")
    view.on_toggle(1)
    view.on_remove(2)
