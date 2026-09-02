test('fetchPages yields data', async () => {
  const pages = [];
  // Mock fetch globally
  global.fetch = jest.fn().mockResolvedValue({
    json: async () => [{ price: 10 }, { price: 20 }]
  });

  const { fetchPages } = require('./javascript_async_generator');
  for await (const page of fetchPages("https://api.example.com/items", 30, 10)) {
    pages.push(page);
    if (pages.length >= 3) break;
  }
  expect(pages).toHaveLength(3);
  expect(pages.every(p => Array.isArray(p))).toBe(true);
});

test('fetchPages stops on empty data', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    json: async () => []
  });

  const { fetchPages } = require('./javascript_async_generator');
  const pages = [];
  for await (const page of fetchPages("https://api.example.com/items", 100)) {
    pages.push(page);
  }
  expect(pages).toHaveLength(0);
});

test('early exit calls gen.return()', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    json: async () => [{ price: 10 }]
  });

  const { fetchPages } = require('./javascript_async_generator');
  const gen = fetchPages("https://api.example.com/items", 10000);
  try {
    for await (const page of gen) {
      expect(page).toHaveLength(1);
      break;
    }
  } finally {
    await gen.return();
  }
});
