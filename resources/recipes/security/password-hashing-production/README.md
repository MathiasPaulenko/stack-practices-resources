# Password Hashing in Production — Examples

Runnable examples for the recipe [Password Hashing in Production](https://stackpractices.com/recipes/password-hashing-production/).

- `password_hash.py` — Argon2id with pepper, plus transparent MD5/SHA-256 → bcrypt migration on login. Requires `pip install argon2-cffi bcrypt`.
- `password-hash.mjs` — Argon2id + pepper + `needsRehash` upgrade. Requires `npm install argon2`.
- `PasswordHashing.java` — Argon2id parameters for Spring Security's `Argon2PasswordEncoder`.
