// demo-server.js — minimal Express app showing the CSRF middleware in action.
// Run: CSRF_SECRET=dev-secret node demo-server.js
const express = require('express');
const cookieParser = require('cookie-parser');
const { csrfProtection } = require('./csrf-middleware');

const app = express();
app.use(express.json());
app.use(cookieParser());
app.use(csrfProtection());

app.get('/', (req, res) => {
  res.send(`<!doctype html>
<form id="f">
  <input name="amount" placeholder="amount" />
  <button>Transfer</button>
</form>
<pre id="out"></pre>
<script>
const token = document.cookie
  .split('; ')
  .find(r => r.startsWith('csrfToken='))
  ?.split('=')[1]
  .split('.')[0];
document.getElementById('f').onsubmit = async (e) => {
  e.preventDefault();
  const r = await fetch('/api/transfer', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': token },
    body: JSON.stringify({ amount: e.target.amount.value })
  });
  document.getElementById('out').textContent = r.status + ' ' + await r.text();
};
</script>`);
});

app.post('/api/transfer', (req, res) => {
  res.json({ ok: true, amount: req.body.amount });
});

app.listen(3000, () => console.log('http://localhost:3000'));
