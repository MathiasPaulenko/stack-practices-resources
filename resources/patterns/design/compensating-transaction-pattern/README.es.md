# Patrón Compensating Transaction

Ejemplos ejecutables que acompañan al patrón:
[https://stackpractices.com/es/patterns/compensating-transaction-pattern/](https://stackpractices.com/es/patterns/compensating-transaction-pattern/)

## Qué contiene

| Archivo | Lenguaje | Qué muestra |
|---------|----------|-------------|
| `python/compensating_transaction.py` | Python (solo stdlib) | Saga de orden completa: camino exitoso y una orden que falla disparando compensación en orden inverso sobre pago, inventario y envío |
| `javascript/compensating-transaction.js` | Node.js (sin deps) | Orquestador de saga asíncrono; el paso de reserva falla y el pago se reembolsa en el pase de compensación |
| `java/CompensatingTransactionDemo.java` | Java | El mismo orquestador compilado como programa real — `javac` + `java`, `main` incluido |

## Ejecutar

```bash
python python/compensating_transaction.py
node javascript/compensating-transaction.js
javac java/CompensatingTransactionDemo.java -d java/ && java -cp java CompensatingTransactionDemo
```

Salida esperada (Python, orden 2 — stock insuficiente):

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

## Puntos clave

- La compensación es un **deshacer semántico**: reembolsar, liberar, cancelar — operaciones de negocio, no `ROLLBACK`.
- Las compensaciones corren en **orden inverso** a los pasos completados.
- Haz las compensaciones **idempotentes** — pueden reintentarse.
- En producción el log de saga es durable y las compensaciones fallidas se encolan para reintento + escalado.
