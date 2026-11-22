import { test } from 'node:test';
import assert from 'node:assert/strict';
import { makeUserStore } from './user_store.mjs';

const alice = () => ({ email: 'alice@example.com', name: 'Alice', role: 'user', credits: 100 });
const bob = () => ({ email: 'bob@example.com', name: 'Bob', role: 'user', credits: 50 });

test('create + read + update + soft delete round-trip', () => {
  const s = makeUserStore();
  const u = s.create(alice());
  assert.equal(s.findById(u._id).name, 'Alice');

  s.findByIdAndUpdate(u._id, { role: 'admin' });
  assert.equal(s.findById(u._id).role, 'admin');

  s.softDelete(u._id);
  assert.equal(s.findById(u._id), null); // hidden from normal queries
  assert.equal(s.findById(u._id, { includeDeleted: true }).role, 'admin');
});

test('validators reject bad documents and keep errors readable', () => {
  const s = makeUserStore();
  assert.throws(() => s.create({ email: 'not-an-email', name: 'X' }), /email/);
  assert.throws(() => s.create({ email: 'a@b.co', name: 'X' }), /name/);
  assert.equal(s.countDocuments(), 0);
});

test('transaction commits both writes', () => {
  const s = makeUserStore();
  const a = s.create(alice());
  const b = s.create(bob());

  s.withTransaction([
    () => s.findByIdAndUpdate(a._id, { credits: a.credits - 30 }),
    () => s.findByIdAndUpdate(b._id, { credits: b.credits + 30 }),
  ]);

  assert.equal(s.findById(a._id).credits, 70);
  assert.equal(s.findById(b._id).credits, 80);
});

test('transaction rolls back all writes on failure', () => {
  const s = makeUserStore();
  const a = s.create(alice());
  const b = s.create(bob());

  assert.throws(() =>
    s.withTransaction([
      () => s.findByIdAndUpdate(a._id, { credits: 0 }),
      () => { throw new Error('downstream write failed'); },
    ])
  );

  assert.equal(s.findById(a._id).credits, 100); // unchanged
  assert.equal(s.findById(b._id).credits, 50); // unchanged
});
