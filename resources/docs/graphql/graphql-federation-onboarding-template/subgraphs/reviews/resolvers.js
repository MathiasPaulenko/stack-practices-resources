// Reviews subgraph resolvers.
// The Product fields here are the extension: the gateway reaches them
// through _entities on this subgraph after products resolves the key.
export const resolvers = {
  Query: {
    reviews: (_, { productId, first, after }, context) => {
      return context.dataSources.reviewDb.findByProduct(productId, { first, after });
    },
  },
  Product: {
    reviews: (parent, _, context) => {
      return context.dataSources.reviewDb.findByProduct(parent.id);
    },
    averageRating: (parent, _, context) => {
      return context.dataSources.reviewDb.getAverageRating(parent.id);
    },
    reviewCount: (parent, _, context) => {
      return context.dataSources.reviewDb.getCount(parent.id);
    },
  },
  Review: {
    __resolveReference: (reference, context) => {
      return context.dataSources.reviewDb.findById(reference.id);
    },
  },
};
