// ETag-based optimistic locking for HTTP APIs with Express.
//
// Run: npm install express

const crypto = require('crypto');
const express = require('express');

const app = express();
app.use(express.json());

// Mock store
const products = new Map();

function generateETag(resource) {
  const hash = crypto.createHash('md5');
  hash.update(JSON.stringify(resource));
  return `"${hash.digest('hex')}"`;
}

app.get('/products/:id', (req, res) => {
  const product = products.get(req.params.id);
  if (!product) return res.status(404).json({ error: 'Not found' });
  res.set('ETag', generateETag(product));
  res.json(product);
});

app.put('/products/:id', (req, res) => {
  const ifMatch = req.headers['if-match'];
  if (!ifMatch) {
    return res.status(428).json({ error: 'If-Match header required' });
  }

  const product = products.get(req.params.id);
  if (!product) return res.status(404).json({ error: 'Not found' });

  const currentETag = generateETag(product);
  if (ifMatch !== currentETag) {
    return res.status(412).json({
      error: 'Precondition failed: resource has been modified',
      currentETag,
    });
  }

  const updated = { ...product, ...req.body, version: product.version + 1 };
  products.set(req.params.id, updated);
  res.set('ETag', generateETag(updated));
  res.json(updated);
});

if (require.main === module) {
  app.listen(3000, () => console.log('Listening on :3000'));
}
