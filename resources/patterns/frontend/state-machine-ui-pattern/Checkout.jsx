// Checkout.jsx — multi-step checkout using the machine
import { useMachine } from '@xstate/react';
import checkoutMachine from '../machines/checkoutMachine';

function Checkout({ initialCart }) {
  const [state, send] = useMachine(checkoutMachine, {
    context: { cart: initialCart },
    services: {
      submitOrder: (context) =>
        fetch('/api/orders', {
          method: 'POST',
          body: JSON.stringify({
            cart: context.cart,
            shipping: context.shippingAddress,
            payment: context.paymentMethod,
          }),
        }).then(res => res.json()),
    },
  });

  if (state.matches('cart')) {
    return (
      <div>
        <h2>Your Cart</h2>
        {state.context.cart.map(item => (
          <div key={item.id}>
            {item.name} — ${item.price}
            <button onClick={() => send({ type: 'REMOVE_ITEM', id: item.id })}>
              Remove
            </button>
          </div>
        ))}
        <button onClick={() => send('NEXT')}>Continue to Shipping</button>
      </div>
    );
  }

  if (state.matches('shipping')) {
    return (
      <div>
        <h2>Shipping Address</h2>
        <AddressForm
          onSave={(address) => send({ type: 'SET_ADDRESS', address })}
        />
        <button onClick={() => send('BACK')}>Back to Cart</button>
        <button
          onClick={() => send('NEXT')}
          disabled={!state.context.shippingAddress}
        >
          Continue to Payment
        </button>
      </div>
    );
  }

  if (state.matches('payment')) {
    return (
      <div>
        <h2>Payment Method</h2>
        <PaymentForm
          onSave={(method) => send({ type: 'SET_PAYMENT', method })}
        />
        <button onClick={() => send('BACK')}>Back to Shipping</button>
        <button
          onClick={() => send('NEXT')}
          disabled={!state.context.paymentMethod}
        >
          Review Order
        </button>
      </div>
    );
  }

  if (state.matches('review')) {
    return (
      <div>
        <h2>Review Your Order</h2>
        <pre>{JSON.stringify(state.context, null, 2)}</pre>
        <button onClick={() => send('BACK')}>Back to Payment</button>
        <button onClick={() => send('SUBMIT')}>Place Order</button>
      </div>
    );
  }

  if (state.matches('processing')) {
    return <div className="spinner">Processing your order...</div>;
  }

  if (state.matches('confirmation')) {
    return (
      <div className="confirmation">
        <h2>Order Confirmed!</h2>
        <p>Order #{state.context.order.id}</p>
      </div>
    );
  }

  if (state.matches('error')) {
    return (
      <div className="error">
        <h2>Order Failed</h2>
        <p>{state.context.error}</p>
        <button onClick={() => send('RETRY')}>Try Again</button>
        <button onClick={() => send('BACK')}>Back to Review</button>
      </div>
    );
  }

  return null;
}
