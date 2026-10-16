// app.js — Express as a front controller.
// Run: npm install express && node app.js
// Test: curl -H "Authorization: Bearer valid" http://localhost:3000/user

const express = require('express');
const app = express();

// Shared preprocessing — every request passes through here
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

app.use((req, res, next) => {
  if (req.headers.authorization !== 'Bearer valid') {
    return res.status(401).send('Unauthorized');
  }
  next();
});

// Route handlers — the "commands"
app.get('/', (req, res) => res.send('Welcome to the home page'));
app.get('/user', (req, res) => res.send('User profile page'));

// Fallback dispatch
app.use((req, res) => res.status(404).send('Not Found'));

app.listen(3000, () => console.log('Front controller on :3000'));
