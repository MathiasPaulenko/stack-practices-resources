import type { ApolloServerPlugin } from '@apollo/server';
import type { QueryLog } from './instrumented.js';

interface QueryLogContext {
  queryLog: QueryLog;
}

// Reads the per-request QueryLog from contextValue right before the
// response is sent. The counter must live in the context (see server.ts).
export const queryLoggerPlugin: ApolloServerPlugin<QueryLogContext> = {
  async requestDidStart() {
    return {
      async willSendResponse({ contextValue, operationName }) {
        const { count, queries } = contextValue.queryLog;
        if (count > 5) {
          console.warn(
            `[N+1 SUSPECT] ${count} queries for operation: ` +
              `${operationName ?? 'anonymous'}\n` +
              queries.slice(0, 10).map((q, i) => `  ${i + 1}. ${q}`).join('\n')
          );
        }
      },
    };
  },
};
