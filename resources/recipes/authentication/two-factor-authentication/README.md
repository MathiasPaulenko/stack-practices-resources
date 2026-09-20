# Two-Factor Authentication (TOTP) — Companion Resources

Runnable companion for the recipe **[Two-Factor Authentication](https://stackpractices.com/recipes/two-factor-authentication/)** on StackPractices.

## Files

| File | Purpose |
|---|---|
| `totp_service.py` | Python service: `enroll()` → `confirm()` → `verify()` with AES-encrypted secret storage, hashed single-use backup codes, and a 5-attempts-per-5-minutes rate limit. |
| `totp-service.js` | Node equivalent using `otplib` + AES-256-GCM encryption via `crypto`. Same enroll → confirm → verify contract. |
| `test_totp.py` | pytest suite covering the recipe's four scenarios: enrollment round-trip, window boundary, rate limiting, single-use backup codes. |

## Quick start — Python

```bash
pip install pyotp qrcode pillow cryptography pytest
export TOTP_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
pytest test_totp.py -v
```

```python
from totp_service import TOTPService

svc = TOTPService(issuer="MyApp")
out = svc.enroll("u_4812", "user@example.com")
# → show out["qr_png_b64"] as <img src="data:image/png;base64,...">
result = svc.confirm("u_4812", "123456")   # first code from the app
if result["enabled"]:
    print(result["backup_codes"])          # show ONCE, user saves them

# at every login:
ok = svc.verify("u_4812", "654321")
```

## Quick start — Node

```bash
npm install otplib qrcode
export TOTP_ENCRYPTION_KEY=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
```

```javascript
const { TOTPService } = require('./totp-service');
const svc = new TOTPService('MyApp');

const { qrDataUrl } = await svc.enroll('u_4812', 'user@example.com');
// render qrDataUrl in an <img> — the user scans it
const { enabled, backupCodes } = svc.confirm('u_4812', '123456');
// login-time:
const ok = svc.verify('u_4812', '654321');
```

## Notes

- **Never enable on enroll.** `confirm()` requires one valid code before `enabled=true` — otherwise a user who scans wrong locks themselves out.
- **Encryption key**: `TOTP_ENCRYPTION_KEY` env var (Fernet key for Python, 32-byte hex for Node). In production, source it from KMS/Vault, not a file.
- **Backup codes are single-use**: stored as SHA-256 hashes, burned on successful verify. Show them to the user exactly once.
- **Rate limit is in-memory here** for clarity — move the attempt counter to Redis for multi-instance deployments (same 5-per-5-min policy).
- The Python version uses Fernet (AES-128-CBC + HMAC) for brevity; the Node version uses AES-256-GCM. Either is fine — what matters is that secrets are never plaintext at rest.
