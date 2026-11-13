import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@as-integrations/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/use/ws';
import express from 'express';
import cors from 'cors';
import http from 'http';
import { typeDefs } from './schema.mjs';
import { resolvers, db } from './resolvers.mjs';

const schema = makeExecutableSchema({ typeDefs, resolvers });

// Demo context: a fixed user so publish calls work without a real auth layer.
// In production, verify the token from ctx.connectionParams / req headers.
const demoContext = { db, user: { id: 'u1' } };

export async function startServer(port = 4000) {
  const app = express();
  const httpServer = http.createServer(app);
  const wsServer = new WebSocketServer({ server: httpServer, path: '/graphql' });

  const serverCleanup = useServer(
    { schema, context: async () => demoContext },
    wsServer,
  );

  const apolloServer = new ApolloServer({
    schema,
    plugins: [
      // WS cleanup runs before the HTTP drain so the sockets close while the
      // http.Server is still alive
      {
        async serverWillStart() {
          return { async drainServer() { await serverCleanup.dispose(); } };
        },
      },
      ApolloServerPluginDrainHttpServer({ httpServer }),
    ],
  });

  await apolloServer.start();
  app.use('/graphql', cors(), express.json(), expressMiddleware(apolloServer, {
    context: async () => demoContext,
  }));

  await new Promise((resolve) => httpServer.listen(port, resolve));
  return {
    httpServer,
    stop: async () => {
      await apolloServer.stop();
      if (httpServer.listening) await new Promise((resolve) => httpServer.close(resolve));
    },
  };
}

if (process.argv[1] && process.argv[1].endsWith('server.mjs')) {
  const server = await startServer(4000);
  console.log('Ready at http://localhost:4000/graphql');
  process.on('SIGINT', async () => { await server.stop(); process.exit(0); });
}
