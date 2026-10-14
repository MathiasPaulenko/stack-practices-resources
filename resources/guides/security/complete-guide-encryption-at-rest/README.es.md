# Cifrado en Reposo — Archivos complementarios

Módulos TypeScript ejecutables para la guía
[Cifrado en Reposo: AES-256, KMS y Cifrado Envolvente](https://stackpractices.com/es/guides/complete-guide-encryption-at-rest/).

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `aes-gcm.ts` | `encrypt`/`decrypt` con AES-256-GCM, IV aleatorio de 96 bits y etiqueta de autenticación de 128 bits. `EncryptedData` lleva `keyVersion` para la rotación. |
| `kms-client.ts` | Interfaz `KmsClient` más una implementación con AWS KMS (`@aws-sdk/client-kms`). La KEK nunca sale del KMS. |
| `envelope-encryption.ts` | `EnvelopeEncryption` — genera una DEK por operación, cifra los datos en local, envuelve la DEK vía el KMS y la borra de memoria. |
| `encrypted-field.ts` | `EncryptedField` + `UserRepository` — cifrado transparente a nivel de columna: la base de datos solo ve ciphertext. |
| `key-rotation.ts` | `KeyRotationService` — re-cifrado por lotes de registros de una `key_version` antigua a la nueva. |

## Ejecutar

```bash
npm install @aws-sdk/client-kms
npx tsc --strict --noEmit *.ts
```

`aes-gcm.ts` y `envelope-encryption.ts` funcionan con cualquier
implementación de `KmsClient`: escribe un mock local (una clave maestra
estática de 32 bytes tras la misma interfaz) para probar el flujo sin
credenciales de AWS.

## Notas

- Nunca reuses un IV con la misma clave en GCM: rompe la confidencialidad y filtra la subclave de autenticación.
- Guarda `keyVersion` junto a cada ciphertext; los trabajos de rotación dependen de él.
- `key-rotation.ts` deja el cableado de `encrypt`/`decrypt` como ejercicio: conecta `EnvelopeEncryption` con la versión de DEK vieja y la nueva.
