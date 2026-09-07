"""Unit tests for TodoViewModel — no View required."""
import pytest
from python_mvvm import TodoRepository, TodoViewModel


@pytest.fixture
def vm():
    repo = TodoRepository()
    return TodoViewModel(repo)


def test_add_todo_increases_count(vm):
    vm.add_todo("Buy groceries")
    assert vm.total_count == 1
    assert vm.items[0].text == "Buy groceries"


def test_add_empty_text_ignored(vm):
    vm.add_todo("  ")
    assert vm.total_count == 0


def test_toggle_marks_done(vm):
    vm.add_todo("Walk the dog")
    vm.toggle(1)
    assert vm.items[0].done is True
    assert vm.completed_count == 1


def test_toggle_unmarks_done(vm):
    vm.add_todo("Walk the dog")
    vm.toggle(1)
    vm.toggle(1)
    assert vm.items[0].done is False
    assert vm.completed_count == 0


def test_remove_decreases_count(vm):
    vm.add_todo("Task A")
    vm.add_todo("Task B")
    vm.remove(1)
    assert vm.total_count == 1
    assert vm.items[0].text == "Task B"


def test_clear_completed(vm):
    vm.add_todo("Task A")
    vm.add_todo("Task B")
    vm.toggle(1)
    vm.clear_completed()
    assert vm.total_count == 1
    assert vm.completed_count == 0


def test_pending_count(vm):
    vm.add_todo("Task A")
    vm.add_todo("Task B")
    vm.toggle(1)
    assert vm.pending_count == 1


def test_subscribe_notified_on_change(vm):
    notifications = []
    vm.subscribe(lambda: notifications.append(True))
    vm.add_todo("Task A")
    vm.toggle(1)
    assert len(notifications) == 2
