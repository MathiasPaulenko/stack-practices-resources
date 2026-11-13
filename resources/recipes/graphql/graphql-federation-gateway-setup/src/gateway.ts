// gateway.ts — Apollo Gateway composing both subgraphs.

import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { ApolloGateway, IntrospectAndCompose } from '@apollo/gateway';

export interface GatewayContext {
  user: { id: string; role: string } | null;
}

async function verifyToken(token: string): Promise<GatewayContext['user']> {
  if (token === 'alice-token') return { id: '1', role: 'user' };
  if (token === 'admin-token') return { id: '9', role: 'admin' };
  return null;
}

export async function startGateway(port = 4000) {
  const gateway = new ApolloGateway({
    supergraphSdl: new IntrospectAndCompose({
      subgraphs: [
        { name: 'users', url: `http://localhost:4001/graphql` },
        { name: 'posts', url: `http://localhost:4002/graphql` },
      ],
    }),
  });

  const server = new ApolloServer<GatewayContext>({ gateway });

  const { url } = await startStandaloneServer(server, {
    listen: { port },
    context: async ({ req }) => {
      const token = req.headers.authorization?.replace('Bearer ', '');
      return { user: token ? await verifyToken(token) : null };
    },
  });

  console.log(`gateway at ${url}`);
  return server;
}
