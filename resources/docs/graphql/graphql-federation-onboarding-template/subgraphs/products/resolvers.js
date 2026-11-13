import DataLoader from 'dataloader';

export const resolvers = {
  Query: {
    product: (_, { id }, context) => {
      return context.dataSources.productDb.findById(id);
    },
    products: (_, { first, after }, context) => {
      return context.dataSources.productDb.findMany({ first, after });
    },
    category: (_, { id }, context) => {
      return context.dataSources.categoryDb.findById(id);
    },
  },
  Mutation: {
    createProduct: (_, { input }, context) => {
      const product = context.dataSources.productDb.create(input);
      return { product };
    },
    updateProduct: (_, { input }, context) => {
      const product = context.dataSources.productDb.update(input);
      return { product };
    },
  },
  // Entity resolvers — called through _entities when the gateway
  // resolves a Product or Category by key from another subgraph.
  Product: {
    __resolveReference: (reference, context) => {
      // reference = { id: "123", __typename: "Product" }
      return context.loaders.productById.load(reference.id);
    },
  },
  Category: {
    __resolveReference: (reference, context) => {
      return context.loaders.categoryById.load(reference.id);
    },
  },
};

export function createLoaders(db) {
  return {
    productById: new DataLoader(async (ids) => {
      const products = await db.products.findMany({ where: { id: { in: ids } } });
      return ids.map(id => products.find(p => p.id === id) || null);
    }),
    categoryById: new DataLoader(async (ids) => {
      const categories = await db.categories.findMany({ where: { id: { in: ids } } });
      return ids.map(id => categories.find(c => c.id === id) || null);
    }),
  };
}
