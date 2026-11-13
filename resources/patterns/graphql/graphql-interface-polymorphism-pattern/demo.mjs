// Demo: a feed query that returns three concrete types through the Node
// interface, plus a Relay-style node(id) lookup. Run: npm install && node demo.mjs
import { buildSchema, graphqlSync } from 'graphql';
import { typeDefs } from './schema.mjs';
import { fieldResolver, typeResolver } from './resolvers.mjs';

const schema = buildSchema(typeDefs);
const run = (source) =>
  graphqlSync({ schema, source, fieldResolver, typeResolver });

const feed = run(/* GraphQL */ `
  query {
    feed {
      __typename
      id
      createdAt
      ... on Post {
        title
        tags
      }
      ... on Comment {
        body
      }
      ... on User {
        name
      }
    }
  }
`);
if (feed.errors) {
  console.error(feed.errors);
  process.exit(1);
}
for (const item of feed.data.feed) {
  const extra = item.title ?? item.body ?? item.name;
  console.log(`${item.__typename.padEnd(8)} ${item.id} -> ${extra}`);
}

// Relay-style lookup: base64("Post:p1").
const gid = Buffer.from('Post:p1').toString('base64');
const node = run(
  `query { node(id: "${gid}") { __typename id ... on Post { title } } }`
);
console.log('node(%s) ->', gid, JSON.stringify(node.data.node));
