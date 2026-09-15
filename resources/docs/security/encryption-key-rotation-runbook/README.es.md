# Runbook de Rotación de Claves de Cifrado — Recursos Companion

Archivos companion del [Runbook de Rotación de Claves de Cifrado](https://stackpractices.com/es/docs/encryption-key-rotation-runbook/) en StackPractices.com.

## Qué incluye

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `dual-key-config.yaml` | YAML | Configuración de migración dual-key (tamaño de lote, paralelismo, rate limit) |
| `migrate_keys.py` | Python | Script de re-cifrado por lotes: descifra con clave vieja, re-cifra con nueva |
| `verify_rotation.sh` | Bash | Verificación post-rotación: estados de claves, test de cifrado/descifrado |
| `jwks-dual-key.json` | JSON | Endpoint JWKS con soporte dual para claves JWT durante rotación |

## Inicio rápido

### 1. Configurar modo dual-key

Edita `dual-key-config.yaml` con los ARNs de tus claves KMS:

```yaml
encryption:
  mode: dual-key
  current_key:
    kms_key_id: "arn:aws:kms:us-east-1:123:key/TU-CLAVE-VIEJA"
  new_key:
    kms_key_id: "arn:aws:kms:us-east-1:123:key/TU-CLAVE-NUEVA"
```

### 2. Ejecutar migración de datos

```bash
pip install boto3
python migrate_keys.py
```

### 3. Verificar rotación

```bash
chmod +x verify_rotation.sh
./verify_rotation.sh
```

## Prerrequisitos

- Credenciales de AWS con permisos KMS decrypt/encrypt
- Python 3.8+ con `boto3`
- `aws-cli` para el script de verificación
- Acceso a base de datos configurado en `migrate_keys.py`

## Referencias

- [Documentación de rotación de claves AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
- [Guías de gestión de claves NIST](https://csrc.nist.gov/projects/key-management)
- [OWASP cheat sheet de almacenamiento criptográfico](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
