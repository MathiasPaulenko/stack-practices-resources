// Tests for the command undo/redo companion. Run: node --test test_command_history.ts

import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
  CommandHistory,
  CommandQueue,
  DeleteCommand,
  InsertCommand,
  MacroCommand,
  TextDocument,
  type AsyncCommand,
} from './command_history.ts';

test('execute applies commands in order', () => {
  const doc = new TextDocument();
  const history = new CommandHistory();
  history.execute(new InsertCommand(doc, 'Hello', 0));
  history.execute(new InsertCommand(doc, ' World', 5));
  assert.equal(doc.getContent(), 'Hello World');
});

test('undo reverses the last command', () => {
  const doc = new TextDocument();
  const history = new CommandHistory();
  history.execute(new InsertCommand(doc, 'Hello', 0));
  history.execute(new InsertCommand(doc, ' World', 5));
  history.undo();
  assert.equal(doc.getContent(), 'Hello');
});

test('redo replays an undone command', () => {
  const doc = new TextDocument();
  const history = new CommandHistory();
  history.execute(new InsertCommand(doc, 'Hello', 0));
  history.undo();
  history.redo();
  assert.equal(doc.getContent(), 'Hello');
});

test('a new command after undo clears the redo stack', () => {
  const doc = new TextDocument();
  const history = new CommandHistory();
  history.execute(new InsertCommand(doc, 'ab', 0));
  history.execute(new InsertCommand(doc, 'X', 1));
  history.undo();
  history.execute(new InsertCommand(doc, 'Y', 1));
  assert.equal(history.canRedo(), false);
  assert.equal(doc.getContent(), 'aYb');
});

test('DeleteCommand restores the deleted text on undo', () => {
  const doc = new TextDocument();
  const history = new CommandHistory();
  history.execute(new InsertCommand(doc, 'Hello World', 0));
  history.execute(new DeleteCommand(doc, 5, 6));
  assert.equal(doc.getContent(), 'Hello');
  history.undo();
  assert.equal(doc.getContent(), 'Hello World');
});

test('MacroCommand undoes its children in reverse order', () => {
  const doc = new TextDocument();
  const history = new CommandHistory();
  history.execute(
    new MacroCommand([
      new InsertCommand(doc, 'a', 0),
      new InsertCommand(doc, 'b', 1),
      new InsertCommand(doc, 'c', 2),
    ]),
  );
  assert.equal(doc.getContent(), 'abc');
  history.undo();
  assert.equal(doc.getContent(), '');
});

test('bounded history drops the oldest command', () => {
  const doc = new TextDocument();
  const history = new CommandHistory(2);
  history.execute(new InsertCommand(doc, 'a', 0));
  history.execute(new InsertCommand(doc, 'b', 1));
  history.execute(new InsertCommand(doc, 'c', 2));
  history.undo();
  history.undo();
  history.undo(); // nothing left — the oldest was dropped
  assert.equal(doc.getContent(), 'a'); // 'c' and 'b' undone, 'a' stays
});

test('undo on empty history is a no-op', () => {
  const doc = new TextDocument();
  const history = new CommandHistory();
  history.undo();
  assert.equal(doc.getContent(), '');
  assert.equal(history.canUndo(), false);
});

test('CommandQueue serializes async commands', async () => {
  const order: string[] = [];
  const cmd = (id: string, ms: number): AsyncCommand => ({
    getName: () => id,
    execute: async () => {
      await new Promise((r) => setTimeout(r, ms));
      order.push(`exec-${id}`);
    },
    undo: async () => {
      order.push(`undo-${id}`);
    },
  });

  const queue = new CommandQueue();
  await Promise.all([queue.execute(cmd('a', 20)), queue.execute(cmd('b', 1))]);
  assert.deepEqual(order, ['exec-a', 'exec-b']); // b waits for a despite being faster
});
