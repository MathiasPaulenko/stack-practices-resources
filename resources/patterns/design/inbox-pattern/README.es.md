# Patrón Inbox — Recursos Complementarios

Scripts para implementar el Patrón Inbox con procesamiento idempotente de eventos, deduplicación y lógica de reintentos.

## Archivos

| Archivo | Lenguaje | Propósito |
|---------|----------|-----------|
| `inbox_processor.py` | Python | Inbox basado en SQLite con deduplicación y reintentos |
| `inbox_processor.js` | JavaScript | Inbox en Node.js con procesamiento async |

## Requisitos

### Python

```bash
pip install sqlite3  # Incluido en Python 3.x
```

### JavaScript

```bash
npm install sqlite3 sqlite
```

## Uso

### Python

```python
from inbox_processor import InboxProcessor

inbox = InboxProcessor("inbox.db")

# Recibir un evento de webhook
event = {"order_id": "ORD-001", "amount": 99.99, "event": "payment.received"}
is_new = inbox.receive(event)
print(f"Mensaje nuevo: {is_new}")  # True

# El duplicado es rechazado
is_new = inbox.receive(event)
print(f"Mensaje nuevo: {is_new}")  # False

# Procesar mensajes pendientes
inbox.process_pending(lambda p: f"Pago de ${p['amount']} procesado")
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
  console.log('Recibido:', await inbox.receive(event));  // true
  console.log('Duplicado:', await inbox.receive(event));  // false

  await inbox.processPending(async (p) => `Pago de $${p.amount} procesado`);
  console.log(await inbox.getStats());
}

main().catch(console.error);
```

## Fuente

- [Patrón Inbox](https://stackpractices.com/es/patterns/inbox-pattern/)
