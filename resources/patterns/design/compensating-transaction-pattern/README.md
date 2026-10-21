# Compensating Transaction Pattern

Runnable companion examples for the pattern:
[https://stackpractices.com/patterns/compensating-transaction-pattern/](https://stackpractices.com/patterns/compensating-transaction-pattern/)

## What's here

| File | Language | What it shows |
|------|----------|---------------|
| `python/compensating_transaction.py` | Python (stdlib only) | Full order saga: success path and a failing order that triggers reverse-order compensation across payment, inventory, and shipping |
| `javascript/compensating-transaction.js` | Node.js (no deps) | Async saga orchestrator; the reserve step fails and the payment is refunded by the compensation pass |
| `java/CompensatingTransactionDemo.java` | Java | Same orchestrator compiled as a real program — `javac` + `java`, `main` included |

## Run

```bash
python python/compensating_transaction.py
node javascript/compensating-transaction.js
javac java/CompensatingTransactionDemo.java -d java/ && java -cp java CompensatingTransactionDemo
```

Expected output (Python, order 2 — insufficient stock):

```text
=== ORDER 2 (Failure -> Compensation) ===
Executing step 1: charge_payment
  [Payment] Charged $999.99 for order ORD-002, txn=...
Executing step 2: reserve_inventory
  [Inventory] Insufficient stock for SKU-999
Step reserve_inventory failed! Running compensating transactions...
Compensating: charge_payment
  [Payment] Refunded $999.99 for order ORD-002
Result: FAILED
Payment refunded: refunded
```

## Key points

- Compensation is a **semantic undo**: refund, release, cancel — business operations, not `ROLLBACK`.
- Compensations run in **reverse order** of the completed steps.
- Make compensations **idempotent** — they may be retried.
- Production systems log the saga durably and queue failed compensations for retry + escalation.
