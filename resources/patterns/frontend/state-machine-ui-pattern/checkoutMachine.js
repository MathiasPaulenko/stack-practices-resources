// checkoutMachine.js — checkout flow state machine
import { createMachine, assign } from 'xstate';

const checkoutMachine = createMachine({
  id: 'checkout',
  initial: 'cart',
  context: {
    cart: [],
    shippingAddress: null,
    paymentMethod: null,
    order: null,
    error: null,
  },
  states: {
    cart: {
      on: {
        NEXT: 'shipping',
        REMOVE_ITEM: {
          actions: assign({
            cart: (ctx, event) => ctx.cart.filter(item => item.id !== event.id),
          }),
        },
      },
    },
    shipping: {
      on: {
        NEXT: {
          target: 'payment',
          cond: (ctx) => ctx.shippingAddress !== null,
        },
        BACK: 'cart',
        SET_ADDRESS: {
          actions: assign({
            shippingAddress: (_, event) => event.address,
          }),
        },
      },
    },
    payment: {
      on: {
        NEXT: {
          target: 'review',
          cond: (ctx) => ctx.paymentMethod !== null,
        },
        BACK: 'shipping',
        SET_PAYMENT: {
          actions: assign({
            paymentMethod: (_, event) => event.method,
          }),
        },
      },
    },
    review: {
      on: {
        SUBMIT: 'processing',
        BACK: 'payment',
      },
    },
    processing: {
      invoke: {
        src: 'submitOrder',
        onDone: {
          target: 'confirmation',
          actions: assign({ order: (_, event) => event.data }),
        },
        onError: {
          target: 'error',
          actions: assign({ error: (_, event) => event.data.message }),
        },
      },
    },
    confirmation: {
      type: 'final',
    },
    error: {
      on: {
        RETRY: 'processing',
        BACK: 'review',
      },
    },
  },
});

export default checkoutMachine;
