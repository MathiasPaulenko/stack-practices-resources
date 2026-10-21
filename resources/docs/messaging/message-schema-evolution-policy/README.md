# Message Schema Evolution Policy — Companion Resources

Supporting files for the [Message Schema Evolution Policy](https://stackpractices.com/docs/message-schema-evolution-policy/) doc on StackPractices.

## Contents

| File | Description |
|------|-------------|
| `order-created-v1.avsc` | Original Avro schema (v1) used throughout the doc's examples. |
| `order-created-v2.avsc` | Backward-compatible v2: optional `currency`, deprecated `legacyPaymentMethod`, `paymentMethods` replacement array. |
| `order-created.proto` | Protobuf v2 with reserved field number, deprecated field, and repeated replacement — the policy rules applied. |
| `schema-compatibility-check.sh` | CI script: posts a candidate schema to the registry's compatibility endpoint and fails the build on `is_compatible: false`. |
| `consumer-migration-checklist.md` | Per-consumer checklist for the breaking change procedure (dual-write → migrate → grace period → delete). |

## Usage

Wire `schema-compatibility-check.sh` into your pipeline so every PR that touches a schema file is validated before merge:

```bash
./schema-compatibility-check.sh order-created-v2.avsc prod.orders.order-created.v1-value http://schema-registry:8081
```

## Source

- Doc: https://stackpractices.com/docs/message-schema-evolution-policy/
- Doc (ES): https://stackpractices.com/es/docs/message-schema-evolution-policy/
