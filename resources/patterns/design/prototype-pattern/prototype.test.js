const { test } = require('node:test');
const assert = require('node:assert/strict');
const { ProductConfig, PrototypeRegistry } = require('./prototype.js');

const makeRegistry = () => {
  const registry = new PrototypeRegistry();
  registry.register('pro', new ProductConfig('Pro', 29.99, 'software', { tier: 'pro' }, ['pro', 'priority']));
  return registry;
};

test('clone is a new object with equal state', () => {
  const original = new ProductConfig('Pro', 29.99, 'software', { tier: 'pro' }, ['pro']);
  const clone = original.clone();
  assert.notEqual(clone, original);
  assert.equal(clone.name, original.name);
  assert.deepEqual(clone.attributes, original.attributes);
});

test('clone preserves the class (unlike structuredClone)', () => {
  const clone = new ProductConfig('P', 1, 'c').clone();
  assert.ok(clone instanceof ProductConfig);
  assert.equal(typeof clone.addTag, 'function');
});

test('clone is deep: nested structures are independent', () => {
  const original = new ProductConfig('Pro', 29.99, 'software', { tier: 'pro' }, ['pro']);
  const clone = original.clone();
  clone.attributes.discount = '20%';
  clone.tags.push('custom');
  assert.equal(original.attributes.discount, undefined);
  assert.equal(original.tags.includes('custom'), false);
});

test('registry returns independent clones', () => {
  const registry = makeRegistry();
  const a = registry.get('pro');
  const b = registry.get('pro');
  a.addTag('mutated');
  assert.equal(b.tags.includes('mutated'), false);
});

test('registered prototype is not mutated by clones', () => {
  const registry = makeRegistry();
  const custom = registry.get('pro');
  custom.name = 'Custom';
  custom.attributes = {};
  const fresh = registry.get('pro');
  assert.equal(fresh.name, 'Pro');
  assert.deepEqual(fresh.attributes, { tier: 'pro' });
});

test('unknown key returns undefined', () => {
  assert.equal(makeRegistry().get('missing'), undefined);
});

test('register rejects non-clonable', () => {
  const registry = new PrototypeRegistry();
  assert.throws(() => registry.register('bad', {}), TypeError);
});
