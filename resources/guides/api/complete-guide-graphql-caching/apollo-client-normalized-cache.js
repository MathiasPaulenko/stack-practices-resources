// Apollo Client normalized cache with mutation updates.
import { ApolloClient, InMemoryCache, gql } from "@apollo/client";

export const GET_PRODUCTS = gql`
  query GetProducts {
    products {
      id
      name
      price
    }
  }
`;

export const CREATE_PRODUCT = gql`
  mutation CreateProduct($input: CreateProductInput!) {
    createProduct(input: $input) {
      product {
        id
        name
        price
      }
    }
  }
`;

export const client = new ApolloClient({
  cache: new InMemoryCache({
    typePolicies: {
      Product: { keyFields: ["id"] },
    },
  }),
});

/**
 * Update the cache after creating a product, without refetching.
 * @param {object} cache - Apollo cache instance.
 * @param {{ data: { createProduct: { product: object } } }} result - Mutation result.
 */
export function updateCacheAfterCreate(cache, { data }) {
  const newProduct = data.createProduct.product;
  cache.modify({
    fields: {
      products(existing = []) {
        cache.writeFragment({
          data: newProduct,
          fragment: gql`fragment NewProduct on Product { id name price }`,
        });
        return [...existing, newProduct];
      },
    },
  });
}
