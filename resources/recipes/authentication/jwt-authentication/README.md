# JWT Authentication

Companion files for the recipe [JWT Authentication](https://stackpractices.com/recipes/jwt-authentication/).

Runnable token flows — sign/verify, access + refresh rotation, revocation — in the three languages the recipe covers.

## Contents

| File | What it does |
| ---- | ------------ |
| `jwt_demo.py` | End-to-end demo: issue, verify, refresh, revoke (PyJWT) |
| `jwt_demo.js` | Same flow in Node.js (`jsonwebtoken`) |
| `JwtUtil.java` | Sign/verify with the modern JJWT 0.12+ API |
| `generate_keys.sh` | Creates `private.pem`/`public.pem` for RS256 experiments |
| `requirements.txt` | Python dependency (`PyJWT>=2.8`) |
| `package.json` | Node dependency (`jsonwebtoken`) |

## Run it

```bash
# Python
pip install -r requirements.txt
python jwt_demo.py

# Node
npm install
node jwt_demo.js

# RS256 keys for the recipe's asymmetric variant
./generate_keys.sh
```

Expected output from `jwt_demo.py`: the access token verifies, a refresh issues a new access token, the revoked refresh token is rejected, and the token-type check rejects an access token passed as refresh.

## Notes

- `SECRET` values here are dev placeholders — never commit real secrets; load them from env vars.
- The refresh/blocklist stores are in-memory maps so the demo runs without Redis; the recipe shows the Redis-backed variant.
- `JwtUtil.java` needs the JJWT 0.12.x artifacts on the classpath (see the comment at the top of the file).
