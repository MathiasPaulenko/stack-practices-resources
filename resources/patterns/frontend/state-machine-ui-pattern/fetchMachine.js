// fetchMachine.js — XState machine for data fetching
import { createMachine, assign } from 'xstate';

const fetchMachine = createMachine({
  id: 'fetch',
  initial: 'idle',
  context: {
    data: null,
    error: null,
    retries: 0,
  },
  states: {
    idle: {
      on: {
        FETCH: 'loading',
      },
    },
    loading: {
      invoke: {
        src: 'fetchData',
        onDone: {
          target: 'success',
          actions: assign({ data: (_, event) => event.data, error: null }),
        },
        onError: {
          target: 'error',
          actions: assign({
            error: (_, event) => event.data.message,
            retries: (context) => context.retries + 1,
          }),
        },
      },
      on: {
        CANCEL: 'idle',
      },
    },
    success: {
      on: {
        REFETCH: 'loading',
        RESET: 'idle',
      },
    },
    error: {
      on: {
        RETRY: {
          target: 'loading',
          cond: (context) => context.retries < 3,
        },
        RESET: 'idle',
      },
    },
  },
});

export default fetchMachine;
