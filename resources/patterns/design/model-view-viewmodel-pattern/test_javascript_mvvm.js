// Unit tests for TodoViewModel — no View required.
// Run with: node test_javascript_mvvm.js

const assert = require('assert');
const { TodoRepository, TodoViewModel } = require('./javascript_mvvm');

function testAddTodoIncreasesCount() {
  const vm = new TodoViewModel(new TodoRepository());
  vm.addTodo('Buy groceries');
  assert.strictEqual(vm.totalCount, 1);
  assert.strictEqual(vm.items[0].text, 'Buy groceries');
  console.log('✓ testAddTodoIncreasesCount');
}

function testAddEmptyTextIgnored() {
  const vm = new TodoViewModel(new TodoRepository());
  vm.addTodo('  ');
  assert.strictEqual(vm.totalCount, 0);
  console.log('✓ testAddEmptyTextIgnored');
}

function testToggleMarksDone() {
  const vm = new TodoViewModel(new TodoRepository());
  vm.addTodo('Walk the dog');
  vm.toggle(1);
  assert.strictEqual(vm.items[0].done, true);
  assert.strictEqual(vm.completedCount, 1);
  console.log('✓ testToggleMarksDone');
}

function testToggleUnmarksDone() {
  const vm = new TodoViewModel(new TodoRepository());
  vm.addTodo('Walk the dog');
  vm.toggle(1);
  vm.toggle(1);
  assert.strictEqual(vm.items[0].done, false);
  assert.strictEqual(vm.completedCount, 0);
  console.log('✓ testToggleUnmarksDone');
}

function testRemoveDecreasesCount() {
  const vm = new TodoViewModel(new TodoRepository());
  vm.addTodo('Task A');
  vm.addTodo('Task B');
  vm.remove(1);
  assert.strictEqual(vm.totalCount, 1);
  assert.strictEqual(vm.items[0].text, 'Task B');
  console.log('✓ testRemoveDecreasesCount');
}

function testClearCompleted() {
  const vm = new TodoViewModel(new TodoRepository());
  vm.addTodo('Task A');
  vm.addTodo('Task B');
  vm.toggle(1);
  vm.clearCompleted();
  assert.strictEqual(vm.totalCount, 1);
  assert.strictEqual(vm.completedCount, 0);
  console.log('✓ testClearCompleted');
}

function testPendingCount() {
  const vm = new TodoViewModel(new TodoRepository());
  vm.addTodo('Task A');
  vm.addTodo('Task B');
  vm.toggle(1);
  assert.strictEqual(vm.pendingCount, 1);
  console.log('✓ testPendingCount');
}

function testSubscribeNotifiedOnChange() {
  const vm = new TodoViewModel(new TodoRepository());
  const notifications = [];
  vm.subscribe(() => notifications.push(true));
  vm.addTodo('Task A');
  vm.toggle(1);
  assert.strictEqual(notifications.length, 2);
  console.log('✓ testSubscribeNotifiedOnChange');
}

// Run all tests
console.log('Running TodoViewModel tests...\n');
testAddTodoIncreasesCount();
testAddEmptyTextIgnored();
testToggleMarksDone();
testToggleUnmarksDone();
testRemoveDecreasesCount();
testClearCompleted();
testPendingCount();
testSubscribeNotifiedOnChange();
console.log('\n✅ All 8 tests passed!');
