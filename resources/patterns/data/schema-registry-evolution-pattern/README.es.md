# Patrón Schema Registry Evolution — Recursos complementarios

Archivos ejecutables del patrón [Schema Registry Evolution](https://stackpractices.com/es/patterns/schema-registry-evolution-pattern/) en StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `customer-v1.avsc` | Esquema Avro v1 de `customer-events` (id, email, enum status, created_at). |
| `customer-v2.avsc` | v2 compatible hacia atrás: nuevo símbolo `suspended` en el enum más campos opcionales `phone` y `country` con defaults. |
| `customer.proto` | La misma evolución expresada en Protobuf (campos `optional`, nuevo valor de enum). |
| `register_schema.py` | Registra ambas versiones Avro en un subject vía la API REST de Schema Registry. |
| `compatibility.py` | Configura la compatibilidad del subject (`BACKWARD`/`FORWARD`/`FULL`) y comprueba en seco un esquema nuevo contra la última versión — la llamada que conectas a CI. |
| `avro_producer.py` | `SerializingProducer` que publica un evento de cliente v2 con `AvroSerializer`. |
| `avro_consumer.py` | `DeserializingConsumer` que resuelve el schema id del wire format y muestra cómo los consumers de v1 reciben los defaults de los campos v2. |
| `CustomerProducer.java` | El mismo flujo de producer con `KafkaAvroSerializer` y una clase `Customer` generada. |

## Uso

Necesitas Kafka + Schema Registry corriendo (por ejemplo `docker compose up` con el stack de Confluent), y luego:

```bash
pip install requests confluent-kafka
python register_schema.py          # registra v1 y v2
python compatibility.py            # configura BACKWARD y valida v2 contra él
python avro_producer.py            # publica un evento v2
python avro_consumer.py            # consume con el esquema resuelto del registry
```

El ejemplo Java necesita las clases generadas `Customer`/`Status` — constrúyelas desde `customer-v2.avsc` con `avro-tools` o el plugin Avro de Maven/Gradle.
