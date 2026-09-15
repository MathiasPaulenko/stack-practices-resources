# Encryption Key Rotation Runbook — Companion Resources

Companion files for the [Encryption Key Rotation Runbook](https://stackpractices.com/docs/encryption-key-rotation-runbook/) on StackPractices.com.

## What's included

| File | Language | Description |
|------|----------|-------------|
| `dual-key-config.yaml` | YAML | Dual-key migration configuration (batch size, parallelism, rate limit) |
| `migrate_keys.py` | Python | Batch re-encryption script: decrypt with old key, re-encrypt with new key |
| `verify_rotation.sh` | Bash | Post-rotation verification: key states, encrypt/decrypt test |
| `jwks-dual-key.json` | JSON | JWKS endpoint supporting dual JWT signing keys during rotation |

## Quick start

### 1. Configure dual-key mode

Edit `dual-key-config.yaml` with your KMS key ARNs:

```yaml
encryption:
  mode: dual-key
  current_key:
    kms_key_id: "arn:aws:kms:us-east-1:123:key/YOUR-OLD-KEY"
  new_key:
    kms_key_id: "arn:aws:kms:us-east-1:123:key/YOUR-NEW-KEY"
```

### 2. Run data migration

```bash
pip install boto3
python migrate_keys.py
```

### 3. Verify rotation

```bash
chmod +x verify_rotation.sh
./verify_rotation.sh
```

## Prerequisites

- AWS credentials with KMS decrypt/encrypt permissions
- Python 3.8+ with `boto3`
- `aws-cli` for verification script
- Database access configured in `migrate_keys.py`

## References

- [AWS KMS key rotation docs](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
- [NIST key management guidelines](https://csrc.nist.gov/projects/key-management)
- [OWASP cryptographic storage cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
