# Seguridad de Webhooks — Entrega, Verificación y Protección

Ejemplos ejecutables que acompañan a la guía:
[https://stackpractices.com/es/guides/webhook-security-guide/](https://stackpractices.com/es/guides/webhook-security-guide/)

## Qué contiene

| Archivo | Lenguaje | Qué muestra |
|---------|----------|-------------|
| `python/webhook_security.py` | Python (solo stdlib) | Firma del productor + verificación del consumidor con ventana de timestamp y deduplicación; corre los cuatro casos: legítimo, replay, forjado, viejo |
| `javascript/stripe-verifier.js` | Node.js (solo node:crypto) | Esquema de firma `t,v1` de Stripe con `timingSafeEqual`; corre rechazos por payload alterado, firma forjada y timestamp viejo |

Sin dependencias — ambos ejemplos corren de forma autónoma.

## Ejecutar

```bash
python python/webhook_security.py
node javascript/stripe-verifier.js
```

Salida esperada (Python):

```text
legitimate delivery: ACCEPTED
replayed delivery:   REJECTED (duplicate)
forged signature:    REJECTED
stale timestamp:     REJECTED
```

## Puntos clave

- Firma y verifica los **bytes crudos del body** — nunca un objeto JSON re-serializado.
- Compara firmas con `hmac.compare_digest()` / `crypto.timingSafeEqual()`, no con `==`.
- Verificación de timestamp **y** deduplicación por ID de evento — cualquiera de las dos sola no basta.
- Devuelve `200` para duplicados para que el proveedor deje de reintentar.
