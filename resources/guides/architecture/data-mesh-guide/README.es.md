# Guía Data Mesh — Ejemplos Companion

Archivos companion de la guía [Arquitectura Data Mesh](https://stackpractices.com/es/guides/data-mesh-guide/).

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `data-product.yaml` | Spec legible por máquina del data product `orders.fact_order_events` — el YAML de la guía |
| `schemas/order_event.avsc` | Esquema Avro registrado en Schema Registry para el topic de eventos de pedidos |
| `validate_product.py` | Chequeo de consistencia entre spec y esquema (solo stdlib; pyyaml opcional) |
| `requirements.txt` | Dependencias opcionales — pyyaml para validar la spec, confluent-kafka para el publicador |

## Inicio rápido

```bash
python validate_product.py
# OK — data product spec and Avro schema are consistent
```

El validador comprueba que el esquema Avro parsea, que cada campo que emite el
publicador existe en el esquema, que los campos PII están documentados y (con
pyyaml instalado) que la spec lleva los campos que exige el catálogo:
`owner`, `schema`, SLAs de `quality` y `access.pii_fields`.

## El contrato en la guía

- **Lado publicador** — el equipo de Pedidos produce registros `OrderEvent` a
  Kafka vía `AvroProducer` con este `.avsc` registrado en Schema Registry.
  Los cambios incompatibles se rechazan al publicar.
- **Lado consumidor** — analytics lee la tabla Delta Lake que escribe la
  plataforma y une `orders.fact_order_events` con
  `payments.fact_payment_events` en su propio job de Spark.
- **Gobernanza** — `pii_fields` en la spec dispara el enmascarado automático;
  `customer_email` es nullable en el esquema para que las lecturas enmascaradas
  sigan siendo válidas.
