# Encripción en Reposo — Recursos Complementarios

Código complementario para [Encripción en Reposo para Bases de Datos y Almacenamiento](https://stackpractices.com/es/recipes/encryption-at-rest/).

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `encrypt_field.py` | Python 3.12+ | Encripción de sobre con AWS KMS usando AES-256-GCM |
| `field_encryption.js` | Node 20+ | Encripción a nivel de aplicación con derivación HKDF |
| `aes_gcm.go` | Go 1.22+ | AES-256-GCM con binding de contexto (AAD) |
| `pgcrypto_schema.sql` | PostgreSQL 16+ | Schema para encripción searchable con blind index |
| `multi_tenant.py` | Python 3.12+ | Encripción de sobre multi-tenant con keys KMS por tenant |
| `searchable_encryption.py` | Python 3.12+ | Encripción searchable con blind index HMAC |
| `key_rotation.py` | Python 3.12+ | Rotación de keys sin downtime con re-encripción AWS KMS |

## Requisitos

### Python

```bash
pip install boto3 cryptography>=43.0
```

### Node.js

Sin dependencias externas — usa el módulo `crypto` built-in.

### Go

Sin dependencias externas — usa la standard library `crypto/aes` y `crypto/cipher`.

### PostgreSQL

Requiere la extensión `pgcrypto` (incluida en PostgreSQL contrib).

## Ejecución

### Python (encripción de sobre)

```bash
export KMS_KEY_ID=alias/aws/ebs
python encrypt_field.py
```

### Node.js (encripción de campos)

```bash
node field_encryption.js
```

### Go (AES-256-GCM)

```bash
go run aes_gcm.go
```

### PostgreSQL (schema de encripción searchable)

```bash
psql -d mydb -f pgcrypto_schema.sql
```

## Licencia

MIT — ver el repositorio principal para detalles.
