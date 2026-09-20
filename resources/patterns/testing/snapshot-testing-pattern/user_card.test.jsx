// Jest snapshot examples — runnable with `npm test` after `npm install`.
//
// Covers the three techniques from the pattern:
//   1. External snapshot  (.snap file in __snapshots__/)
//   2. Inline snapshot    (literal stored in this file)
//   3. Property matchers  (mask dynamic values)

function renderUserCard({ name, email, role }) {
  return {
    type: 'div',
    props: {
      className: `user-card ${role}`,
      children: [
        { type: 'h2', props: { children: name } },
        { type: 'p', props: { children: email } },
        { type: 'span', props: { children: role } },
      ],
    },
  };
}

function generateConfig({ environment, features }) {
  return {
    environment,
    features: features.sort(),
    generated: true,
  };
}

// 1. External snapshot — baseline written to __snapshots__/ on first run.
test('user card matches snapshot', () => {
  const card = renderUserCard({ name: 'Alice', email: 'alice@x.com', role: 'admin' });
  expect(card).toMatchSnapshot();
});

// 2. Inline snapshot — small output kept inside the test file for easy review.
test('generateConfig produces a stable shape', () => {
  const config = generateConfig({
    environment: 'production',
    features: ['auth', 'logging', 'monitoring'],
  });
  expect(config).toMatchInlineSnapshot(`
    Object {
      "environment": "production",
      "features": Array [
        "auth",
        "logging",
        "monitoring",
      ],
      "generated": true,
    }
  `);
});

// 3. Property matchers — dynamic fields masked so the snapshot stays deterministic.
function createOrder(items) {
  return {
    id: `ord_${Math.random().toString(36).slice(2, 10)}`,
    createdAt: new Date().toISOString(),
    items,
    status: 'pending',
  };
}

test('order response matches shape with dynamic fields masked', () => {
  const order = createOrder([{ productId: 1, quantity: 2 }]);

  expect(order).toMatchInlineSnapshot({
    id: expect.any(String),
    createdAt: expect.any(String),
  }, `
    Object {
      "createdAt": Any<String>,
      "id": Any<String>,
      "items": Array [
        Object {
          "productId": 1,
          "quantity": 2,
        },
      ],
      "status": "pending",
    }
  `);
});
