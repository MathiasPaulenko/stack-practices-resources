import { test } from 'node:test';
import assert from 'node:assert/strict';
import EventBus from './event_bus.js';

test('publish reaches all subscribers', () => {
  const bus = new EventBus();
  const hits = [];
  bus.subscribe('OrderPlaced', () => hits.push('a'));
  bus.subscribe('OrderPlaced', () => hits.push('b'));
  bus.publish('OrderPlaced', { id: 1 });
  assert.deepEqual(hits, ['a', 'b']);
});

test('unsubscribe stops delivery', () => {
  const bus = new EventBus();
  const hits = [];
  const unsub = bus.subscribe('Ping', (p) => hits.push(p.n));
  bus.publish('Ping', { n: 1 });
  unsub();
  bus.publish('Ping', { n: 2 });
  assert.deepEqual(hits, [1]);
});

test('only matching event types dispatch', () => {
  const bus = new EventBus();
  const hits = [];
  bus.subscribe('A', () => hits.push('a'));
  bus.publish('B', {});
  assert.deepEqual(hits, []);
});

test('failing handler does not block others', () => {
  const bus = new EventBus();
  const hits = [];
  const origError = console.error;
  console.error = () => {};
  try {
    bus.subscribe('E', () => { throw new Error('broken subscriber'); });
    bus.subscribe('E', () => hits.push('survivor'));
    bus.publish('E', {});
  } finally {
    console.error = origError;
  }
  assert.deepEqual(hits, ['survivor']);
});

test('handler can unsubscribe during dispatch', () => {
  const bus = new EventBus();
  const hits = [];
  let unsub;
  unsub = bus.subscribe('E', () => { hits.push('once'); unsub(); });
  bus.subscribe('E', () => hits.push('every'));
  bus.publish('E', {});
  bus.publish('E', {});
  assert.deepEqual(hits, ['once', 'every', 'every']);
});
