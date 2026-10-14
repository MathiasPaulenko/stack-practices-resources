# HMAC Request Signing — Companion Files

Runnable sign/verify code for the recipe
[HMAC Request Signing for API Authentication (AWS Sig v4)](https://stackpractices.com/recipes/request-signing-hmac/):
per-language signing pairs, a full AWS Signature v4 signer, a webhook
verifier with nonce replay protection, and overlap-window key rotation.

## Files

| File | What it does |
| --- | --- |
| `sign_request.py` | Python sign/verify pair with `hmac.compare_digest`. Runs a self-contained round-trip demo. |
| `sign-request.js` | Node.js sign/verify pair. The verifier guards `crypto.timingSafeEqual` with a length check (it throws on mismatched lengths). |
| `RequestSigner.java` | Java signer returning both headers — the timestamp must travel with the request for verification to work. Includes a `main()` demo. |
| `sign-request.go` | Go `SignRequest`/`VerifyRequest` with a 5-minute freshness check and `hmac.Equal`. |
| `aws-sigv4.py` | Full AWS Signature v4 signer: canonical request, normalized+sorted query string, derived signing key chain, `Authorization` header. |
| `webhook-verify.js` | Express webhook verifier: timestamp freshness window + Redis `SET NX` nonce uniqueness + HMAC check. |
| `key-rotation.py` | `KeyRotation` dataclass — old and new secrets both verify during a 1-hour overlap. |

## Run

```bash
python sign_request.py       # sign + verify round-trip
python aws-sigv4.py          # prints a SigV4 Authorization header
python key-rotation.py       # shows both keys valid during overlap
node sign-request.js         # JS round-trip
go run sign-request.go       # compiles the Go pair

# Webhook verifier needs express + redis
npm install express redis && REDIS_URL=redis://localhost:6379 node webhook-verify.js

# Java
javac RequestSigner.java && java RequestSigner
```

## Notes

- `timingSafeEqual`/`hmac.Equal`/`compare_digest` are constant-time —
  but they throw when buffer lengths differ, so always guard length first.
- Sign the raw request body, not re-serialized JSON — key ordering and
  whitespace change the bytes and break the signature.
- The nonce store is what actually stops replay inside the timestamp
  window; without it a captured request replays until it goes stale.
- Prefer the AWS SDK/`botocore` signer over `aws-sigv4.py` in production —
  the file exists for interop testing and understanding the spec.
