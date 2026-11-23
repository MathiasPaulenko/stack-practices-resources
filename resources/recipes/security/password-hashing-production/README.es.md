# Hashing de Contraseñas en Producción — Ejemplos

Ejemplos ejecutables de la receta [Hashing de Contraseñas en Producción](https://stackpractices.com/es/recipes/password-hashing-production/).

- `password_hash.py` — Argon2id con pepper y migración transparente MD5/SHA-256 → bcrypt en login. Requiere `pip install argon2-cffi bcrypt`.
- `password-hash.mjs` — Argon2id + pepper + upgrade con `needsRehash`. Requiere `npm install argon2`.
- `PasswordHashing.java` — parámetros Argon2id para `Argon2PasswordEncoder` de Spring Security.
