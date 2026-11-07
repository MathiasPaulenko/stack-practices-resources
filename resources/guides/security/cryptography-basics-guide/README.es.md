# Bases de Criptografía — Código Companion

Ejemplos ejecutables de la [guía Bases de Criptografía](https://stackpractices.com/es/guides/cryptography-basics-guide/) en StackPractices.

| Archivo | Lenguaje | Qué muestra |
|---------|----------|-------------|
| `aes-gcm-encrypt.py` | Python | AES-256-GCM con nonces únicos y AAD |
| `password-hashing.py` | Python | Hashing y verificación con Argon2id + bcrypt |
| `hmac-verify.py` | Python | Firma/verificación HMAC-SHA256 con comparación de tiempo constante |
| `rsa-sign-verify.py` | Python | Firmas RSA-PSS y Ed25519 |
| `envelope-kms.js` | JavaScript | Cifrado de sobre con AWS KMS + demo local ejecutable |

## Instalación

```bash
pip install cryptography argon2-cffi bcrypt   # ejemplos Python
npm install @aws-sdk/client-kms               # envelope-kms.js (las llamadas KMS necesitan credenciales AWS)
```

`envelope-kms.js` incluye una demo local autocontenida (wrap/unwrap con una KEK local) que corre sin credenciales de AWS; en producción sustituye la sección demo por las llamadas KMS.
