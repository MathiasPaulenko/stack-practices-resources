# Data Mesh Guide — Companion Examples

Companion files for the guide [Data Mesh Architecture](https://stackpractices.com/guides/data-mesh-guide/).

## Contents

| File | Purpose |
|------|---------|
| `data-product.yaml` | Machine-readable data product spec for `orders.fact_order_events` — the YAML shown in the guide |
| `schemas/order_event.avsc` | Avro schema registered in Schema Registry for the order events topic |
| `validate_product.py` | Consistency check between spec and schema (stdlib-only; pyyaml optional) |
| `requirements.txt` | Optional deps — pyyaml for spec validation, confluent-kafka for the publisher |

## Quick start

```bash
python validate_product.py
# OK — data product spec and Avro schema are consistent
```

The validator checks that the Avro schema parses, that every field the publisher
code emits exists in the schema, that PII fields are documented, and (with
pyyaml installed) that the spec carries the fields the catalog requires:
`owner`, `schema`, `quality` SLAs and `access.pii_fields`.

## The contract in the guide

- **Publisher side** — the Orders team produces `OrderEvent` records to Kafka
  through `AvroProducer` with this `.avsc` registered in Schema Registry.
  Incompatible changes are rejected at publish time.
- **Consumer side** — analytics reads the Delta Lake table written by the
  platform and joins `orders.fact_order_events` with
  `payments.fact_payment_events` in its own Spark job.
- **Governance** — `pii_fields` in the spec drives automatic masking;
  `customer_email` is nullable in the schema so masked reads stay valid.
