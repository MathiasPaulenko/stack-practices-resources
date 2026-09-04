// Apollo Client with persisted queries and GET for CDN cacheable requests.
import {
  ApolloClient,
  InMemoryCache,
  HttpLink,
} from "@apollo/client";
import { createPersistedQueryLink } from "@apollo/client/link/persisted-queries";
import { sha256 } from "crypto-hash";

const persistedQueryLink = createPersistedQueryLink({ sha256 });
const httpLink = new HttpLink({
  uri: "/graphql",
  useGETForQueries: true,
});

export const client = new ApolloClient({
  link: persistedQueryLink.concat(httpLink),
  cache: new InMemoryCache({
    typePolicies: {
      Product: { keyFields: ["id"] },
      Query: {
        fields: {
          products: {
            merge(existing = [], incoming) {
              return incoming;
            },
          },
        },
      },
    },
  }),
});
