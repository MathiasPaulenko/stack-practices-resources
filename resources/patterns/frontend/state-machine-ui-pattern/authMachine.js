// authMachine.js — guarded transitions with conditions
import { createMachine, assign } from 'xstate';

const authMachine = createMachine({
  id: 'auth',
  initial: 'unauthenticated',
  context: {
    user: null,
    token: null,
    loginAttempts: 0,
  },
  states: {
    unauthenticated: {
      on: {
        LOGIN: 'authenticating',
      },
    },
    authenticating: {
      invoke: {
        src: 'authenticate',
        onDone: {
          target: 'authenticated',
          actions: assign({
            user: (_, event) => event.data.user,
            token: (_, event) => event.data.token,
            loginAttempts: 0,
          }),
        },
        onError: {
          target: 'authError',
          actions: assign({
            loginAttempts: (ctx) => ctx.loginAttempts + 1,
          }),
        },
      },
    },
    authenticated: {
      on: {
        LOGOUT: {
          target: 'unauthenticated',
          actions: assign({ user: null, token: null }),
        },
      },
    },
    authError: {
      on: {
        RETRY: {
          target: 'authenticating',
          cond: (ctx) => ctx.loginAttempts < 3,
        },
        BACK: 'unauthenticated',
      },
    },
  },
});

export default authMachine;
