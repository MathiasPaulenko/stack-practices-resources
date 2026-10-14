# Encryption at Rest — Companion Files

Runnable TypeScript modules for the guide
[Encryption at Rest: AES-256, KMS, Envelope Encryption](https://stackpractices.com/guides/complete-guide-encryption-at-rest/).

## Files

| File | What it does |
| --- | --- |
| `aes-gcm.ts` | AES-256-GCM `encrypt`/`decrypt` with random 96-bit IVs and a 128-bit auth tag. The `EncryptedData` shape carries `keyVersion` for rotation. |
| `kms-client.ts` | `KmsClient` interface plus an AWS KMS implementation (`@aws-sdk/client-kms`). The KEK never leaves the KMS. |
| `envelope-encryption.ts` | `EnvelopeEncryption` — generates a per-operation DEK, encrypts data locally, wraps the DEK through the KMS, and zeroes it from memory. |
| `encrypted-field.ts` | `EncryptedField` + `UserRepository` — transparent column-level encryption so ciphertext is all the database ever sees. |
| `key-rotation.ts` | `KeyRotationService` — batch re-encryption of records from an old `key_version` to the new one. |

## Run

```bash
npm install @aws-sdk/client-kms
npx tsc --strict --noEmit *.ts
```

`aes-gcm.ts` and `envelope-encryption.ts` work with any `KmsClient`
implementation — write a local mock (a static 32-byte master key behind the
same interface) to exercise the flow without AWS credentials.

## Notes

- Never reuse an IV with the same key in GCM — it breaks confidentiality and leaks the auth subkey.
- Keep `keyVersion` next to each ciphertext; rotation jobs depend on it.
- `key-rotation.ts` leaves the `encrypt`/`decrypt` wiring as an exercise — plug in `EnvelopeEncryption` with the old and new DEK versions.
