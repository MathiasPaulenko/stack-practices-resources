# Webhook Security — Delivery, Verification, and Protection

Runnable companion examples for the guide:
[https://stackpractices.com/guides/webhook-security-guide/](https://stackpractices.com/guides/webhook-security-guide/)

## What's here

| File | Language | What it shows |
|------|----------|---------------|
| `python/webhook_security.py` | Python (stdlib only) | Producer signing + consumer verification with timestamp window and dedup; runs the four cases: legitimate, replay, forged, stale |
| `javascript/stripe-verifier.js` | Node.js (node:crypto only) | Stripe `t,v1` signature scheme with `timingSafeEqual`; runs tampered-payload, forged, and stale-timestamp rejections |

No dependencies required — both examples run standalone.

## Run

```bash
python python/webhook_security.py
node javascript/stripe-verifier.js
```

Expected output (Python):

```text
legitimate delivery: ACCEPTED
replayed delivery:   REJECTED (duplicate)
forged signature:    REJECTED
stale timestamp:     REJECTED
```

## Key points

- Sign and verify the **raw body bytes** — never a re-serialized JSON object.
- Compare signatures with `hmac.compare_digest()` / `crypto.timingSafeEqual()`, not `==`.
- Timestamp check **and** event-ID deduplication — either one alone is insufficient.
- Return `200` for duplicates so the provider stops retrying.
