// Tests for the memento companion. Run: node --test test_memento_history.ts

import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
  EditorHistory,
  FormEditor,
  FormHistory,
  GameState,
  TextEditor,
} from './memento_history.ts';

test('undo restores the previous snapshot', () => {
  const editor = new TextEditor();
  const history = new EditorHistory();
  history.backup(editor);
  editor.type('Hello');
  history.backup(editor);
  history.undo(editor);
  assert.equal(editor.getContent(), '');
});

test('redo replays forward after undo', () => {
  const editor = new TextEditor();
  const history = new EditorHistory();
  history.backup(editor);
  editor.type('Hello');
  history.backup(editor);
  history.undo(editor);
  history.redo(editor);
  assert.equal(editor.getContent(), 'Hello');
});

test('new backup after undo drops the redo branch', () => {
  const editor = new TextEditor();
  const history = new EditorHistory();
  history.backup(editor);
  editor.type('A');
  history.backup(editor);
  history.undo(editor);
  editor.type('B');
  history.backup(editor);
  history.redo(editor); // should be a no-op — nothing to redo
  assert.equal(editor.getContent(), 'B');
});

test('undo at the oldest snapshot is a no-op', () => {
  const editor = new TextEditor();
  const history = new EditorHistory();
  history.backup(editor);
  history.undo(editor);
  history.undo(editor); // already at index 0 — must not throw or corrupt
  assert.equal(editor.getContent(), '');
});

test('checkpoint is not mutated by later state changes', () => {
  const game = new GameState();
  game.addItem('sword');
  const checkpoint = game.createCheckpoint();
  game.addItem('shield');
  game.damage(50);
  game.loadCheckpoint(checkpoint);
  assert.equal(game.getHealth(), 100);
  assert.deepEqual(game.getInventory(), ['sword']);
});

test('getInventory returns a copy, not the live array', () => {
  const game = new GameState();
  game.addItem('sword');
  const checkpoint = game.createCheckpoint();
  const snapshotInventory = (checkpoint as { getInventory(): string[] }).getInventory();
  snapshotInventory.push('hacked-item');
  game.loadCheckpoint(checkpoint);
  assert.deepEqual(game.getInventory(), ['sword']);
});

test('form wizard restores the previous step', () => {
  const form = new FormEditor();
  const history = new FormHistory();
  form.setField('email', 'user@test.com');
  form.setStep(1);
  history.push(form.save());
  form.setField('name', 'Alice');
  form.setStep(2);
  history.push(form.save());
  form.setStep(3);

  const prev = history.pop();
  assert.ok(prev);
  form.restore(prev);
  assert.equal(form.getState().step, 2);
  assert.equal(form.getState().fields.name, 'Alice');
});

test('form snapshot does not share the fields map', () => {
  const form = new FormEditor();
  const history = new FormHistory();
  form.setField('email', 'a@b.c');
  history.push(form.save());
  form.setField('email', 'changed@b.c');
  const prev = history.pop();
  assert.ok(prev);
  form.restore(prev);
  assert.equal(form.getState().fields.email, 'a@b.c');
});
