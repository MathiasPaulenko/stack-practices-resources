import { describe, it, expect } from 'vitest';
import { resolvers, createLoaders } from '../subgraphs/products/resolvers.js';

// Minimal data-source doubles — swap for your real DB layer in tests.
const db = {
  products: [
    { id: '1', name: 'Widget', price: 9.99 },
    { id: '2', name: 'Gadget', price: 19.99 },
  ],
};

const testContext = {
  loaders: {
    productById: {
      load: async (id) => db.products.find(p => p.id === id) || null,
    },
  },
  dataSources: {
    productDb: {
      findById: async (id) => db.products.find(p => p.id === id) || null,
    },
  },
};

describe('Product entity resolver', () => {
  it('resolves a product by ID', async () => {
    const product = await resolvers.Product.__resolveReference(
      { id: '1', __typename: 'Product' },
      testContext
    );
    expect(product).toEqual({ id: '1', name: 'Widget', price: 9.99 });
  });

  it('returns null for a non-existent product', async () => {
    const product = await resolvers.Product.__resolveReference(
      { id: '999', __typename: 'Product' },
      testContext
    );
    expect(product).toBeNull();
  });
});

describe('createLoaders', () => {
  it('batches ids into a single findMany call and preserves order', async () => {
    const calls = [];
    const fakeDb = {
      products: {
        findMany: async ({ where }) => {
          calls.push(where.id.in);
          return db.products.filter(p => where.id.in.includes(p.id));
        },
      },
      categories: { findMany: async () => [] },
    };
    const loaders = createLoaders(fakeDb);
    const [a, b, missing] = await Promise.all([
      loaders.productById.load('1'),
      loaders.productById.load('2'),
      loaders.productById.load('999'),
    ]);
    expect(calls).toEqual([['1', '2', '999']]);
    expect(a.id).toBe('1');
    expect(b.id).toBe('2');
    expect(missing).toBeNull();
  });
});
