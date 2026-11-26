const { MongoClient } = require('mongodb');

async function seed() {
  if (process.env.NODE_ENV === 'production') {
    console.error('Refusing to seed production database');
    process.exit(1);
  }
  const client = new MongoClient(process.env.MONGODB_URI);
  await client.connect();
  const db = client.db('myapp');

  const users = db.collection('users');
  await users.deleteMany({ email: { $regex: '@example\.com$' } });
  await users.insertMany([
    { email: 'admin@example.com', name: 'Admin', role: 'admin', createdAt: new Date() },
    { email: 'user1@example.com', name: 'Alice', role: 'user', createdAt: new Date() }
  ]);

  const products = db.collection('products');
  await products.deleteMany({ sku: /^SKU-/ });
  await products.insertMany([
    {
      sku: 'SKU-001',
      name: 'Wireless Mouse',
      price: 29.99,
      reviews: [{ userId: 'user1@example.com', rating: 5, comment: 'Great mouse' }]
    }
  ]);

  await users.createIndex({ email: 1 }, { unique: true });
  await products.createIndex({ sku: 1 }, { unique: true });
  await client.close();
}

seed().catch(err => { console.error(err); process.exit(1); });
