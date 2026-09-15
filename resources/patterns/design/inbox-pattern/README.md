# Inbox Pattern — Companion Resources

Scripts for implementing the Inbox Pattern with idempotent event processing, deduplication, and retry logic.

## Files

| File | Language | Purpose |
|------|----------|---------|
| `inbox_processor.py` | Python | SQLite-based inbox with deduplication and retry |
| `inbox_processor.js` | JavaScript | Node.js inbox with async processing |

## Requirements

### Python

```bash
pip install sqlite3  # Built into Python 3.x
```

### JavaScript

```bash
npm install sqlite3 sqlite
```

## Usage

### Python

```python
from inbox_processor import InboxProcessor

inbox = InboxProcessor("inbox.db")

# Receive a webhook event
event = {"order_id": "ORD-001", "amount": 99.99, "event": "payment.received"}
is_new = inbox.receive(event)
print(f"New message: {is_new}")  # True

# Duplicate is rejected
is_new = inbox.receive(event)
print(f"New message: {is_new}")  # False

# Process pending messages
inbox.process_pending(lambda p: f"Payment of ${p['amount']} processed")
print(inbox.get_stats())
```

### JavaScript

```javascript
const sqlite3 = require('sqlite3').verbose();
const { open } = require('sqlite');
const { InboxProcessor } = require('./inbox_processor');

async function main() {
  const db = await open({ filename: 'inbox.db', driver: sqlite3.Database });
  const inbox = new InboxProcessor(db);
  await inbox.init();

  const event = { order_id: 'ORD-001', amount: 99.99, event: 'payment.received' };
  console.log('Received:', await inbox.receive(event));  // true
  console.log('Duplicate:', await inbox.receive(event));  // false

  await inbox.processPending(async (p) => `Payment of $${p.amount} processed`);
  console.log(await inbox.getStats());
}

main().catch(console.error);
```

## Source

- [Inbox Pattern](https://stackpractices.com/patterns/inbox-pattern/)
