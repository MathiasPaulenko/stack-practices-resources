# Encryption at Rest — Companion Resources

Companion code for [Implement Encryption at Rest for Databases and File Storage](https://stackpractices.com/recipes/encryption-at-rest/).

## Files

| File | Language | Description |
| --- | --- | --- |
| `encrypt_field.py` | Python 3.12+ | Envelope encryption with AWS KMS using AES-256-GCM |
| `field_encryption.js` | Node 20+ | Application-level encryption with HKDF key derivation |
| `aes_gcm.go` | Go 1.22+ | AES-256-GCM with context binding (AAD) |
| `pgcrypto_schema.sql` | PostgreSQL 16+ | Schema for searchable encryption with blind index |
| `multi_tenant.py` | Python 3.12+ | Multi-tenant envelope encryption with per-tenant KMS keys |
| `searchable_encryption.py` | Python 3.12+ | Searchable encryption with HMAC blind index |
| `key_rotation.py` | Python 3.12+ | Zero-downtime key rotation with AWS KMS re-encryption |

## Requirements

### Python

```bash
pip install boto3 cryptography>=43.0
```

### Node.js

No external dependencies — uses built-in `crypto` module.

### Go

No external dependencies — uses standard library `crypto/aes` and `crypto/cipher`.

### PostgreSQL

Requires the `pgcrypto` extension (included in PostgreSQL contrib).

## Running

### Python (envelope encryption)

```bash
export KMS_KEY_ID=alias/aws/ebs
python encrypt_field.py
```

### Node.js (field encryption)

```bash
node field_encryption.js
```

### Go (AES-256-GCM)

```bash
go run aes_gcm.go
```

### PostgreSQL (searchable encryption schema)

```bash
psql -d mydb -f pgcrypto_schema.sql
```

## License

MIT — see the main repository for details.
