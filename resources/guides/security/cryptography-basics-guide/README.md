# Cryptography Basics — Companion Code

Runnable examples for the [Cryptography Basics guide](https://stackpractices.com/guides/cryptography-basics-guide/) on StackPractices.

| File | Language | What it shows |
|------|----------|---------------|
| `aes-gcm-encrypt.py` | Python | AES-256-GCM with unique nonces and AAD |
| `password-hashing.py` | Python | Argon2id + bcrypt hashing and verification |
| `hmac-verify.py` | Python | HMAC-SHA256 sign/verify with constant-time compare |
| `rsa-sign-verify.py` | Python | RSA-PSS and Ed25519 signatures |
| `envelope-kms.js` | JavaScript | Envelope encryption with AWS KMS + local runnable demo |

## Setup

```bash
pip install cryptography argon2-cffi bcrypt   # Python examples
npm install @aws-sdk/client-kms               # envelope-kms.js (KMS calls need AWS creds)
```

`envelope-kms.js` includes a self-contained local demo (wrap/unwrap with a local KEK) that runs without AWS credentials; swap the demo section for the KMS calls in production.
