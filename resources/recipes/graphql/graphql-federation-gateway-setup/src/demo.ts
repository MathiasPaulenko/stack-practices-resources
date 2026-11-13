// demo.ts — starts both subgraphs + gateway, runs a federated query, prints the result.
// Run: npm start

import { startUsersService } from './users-service.js';
import { startPostsService } from './posts-service.js';
import { startGateway } from './gateway.js';

const FEDERATED_QUERY = /* GraphQL */ `
  query {
    posts {
      id
      title
      author {
        id
        name
        posts {
          id
          title
        }
      }
    }
  }
`;

async function main() {
  const users = await startUsersService();
  const posts = await startPostsService();
  const gateway = await startGateway();

  // Wait a beat for composition to finish.
  await new Promise((r) => setTimeout(r, 1500));

  const res = await fetch('http://localhost:4000/graphql', {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: 'Bearer alice-token' },
    body: JSON.stringify({ query: FEDERATED_QUERY }),
  });

  const body = await res.json();
  console.log('\n=== Federated query result ===');
  console.log(JSON.stringify(body, null, 2));

  const firstAuthor = body?.data?.posts?.[0]?.author;
  console.log(
    `\nauthor.name resolved via users subgraph _entities: ${
      firstAuthor?.name === 'Alice' ? 'OK' : 'FAIL'
    }`,
  );

  await gateway.stop();
  await users.stop();
  await posts.stop();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
