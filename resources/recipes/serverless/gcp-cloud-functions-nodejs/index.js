const functions = require('@google-cloud/functions-framework');
const express = require('express');
const cors = require('cors');
const { Firestore } = require('@google-cloud/firestore');
const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');

const app = express();
const firestore = new Firestore();
const secretClient = new SecretManagerServiceClient();
const projectId = process.env.GCP_PROJECT || 'my-project-id';

app.use(cors({
  origin: ['https://myapp.com', 'http://localhost:3000'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));
app.use(express.json());

let cachedApiKey = null;

async function getApiKey() {
  if (cachedApiKey) return cachedApiKey;
  const [version] = await secretClient.accessSecretVersion({
    name: `projects/${projectId}/secrets/api-key/versions/latest`,
  });
  cachedApiKey = version.payload.data.toString();
  return cachedApiKey;
}

async function getUserFromDb(userId) {
  const doc = await firestore.collection('users').doc(userId).get();
  if (!doc.exists) return null;
  return { id: doc.id, ...doc.data() };
}

async function createUser(data) {
  const docRef = await firestore.collection('users').add({
    ...data,
    createdAt: Firestore.FieldValue.serverTimestamp(),
  });
  return { id: docRef.id, ...data };
}

app.get('/users/:id', async (req, res) => {
  const user = await getUserFromDb(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

app.post('/users', async (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'name and email are required' });
  }
  const user = await createUser({ name, email });
  res.status(201).json(user);
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: err.message });
  }
  res.status(500).json({ error: 'Internal server error' });
});

functions.http('api', app);
