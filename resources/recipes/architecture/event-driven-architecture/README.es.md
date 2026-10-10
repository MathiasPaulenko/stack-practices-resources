# Arquitectura Event-Driven — ejemplos complementarios

Esta carpeta contiene ejemplos ejecutables de productores y consumidores
para la receta de StackPractices
[Diseñar Sistemas Event-Driven con Event Buses y Brokers](https://stackpractices.com/es/recipes/event-driven-architecture/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `kafka_publisher.py` | Productor Python que publica `OrderPlaced` en Kafka (`kafka-python`, `acks=all`) |
| `schema_registry_avro.py` | Productor serializado con Avro + Confluent Schema Registry y callback de entrega |
| `requirements.txt` | Dependencias de Python |
| `rabbitmq_consumer.mjs` | Consumidor Node.js con acks manuales y dead-lettering (`amqplib`) |
| `eventbridge_producer.mjs` | Publica en AWS EventBridge y consume desde su target SQS |
| `package.json` | Dependencias y scripts de Node |
| `eventbridge.tf` | Event bus + regla + targets de Terraform (SQS y Lambda) |
| `pom.xml` | Proyecto Maven para el ejemplo de Java |
| `src/main/java/OrderEventStore.java` | Event sourcing con Kafka Streams y state store consultable |

## Cómo ejecutar los ejemplos

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
python kafka_publisher.py      # requiere un broker Kafka en kafka:9092
python schema_registry_avro.py # además necesita Schema Registry en :8081
```

### Node.js

```bash
npm install
npm run rabbitmq    # requiere RabbitMQ en amqp://rabbitmq
npm run eventbridge # requiere credenciales AWS e INVENTORY_QUEUE_URL
```

### Java

```bash
mvn compile
mvn exec:java -Dexec.mainClass="OrderEventStore"
```

El `pom.xml` usa Java 17 y Kafka Streams 3.7.1. Los tipos de dominio
(`OrderEvent`, `OrderEventSerde`, `OrderStateSerde`, `getStreamsConfig`)
son stubs — conecta tu propia serialización y configuración del broker.

### Terraform

```bash
terraform init
terraform plan   # define primero aws_sqs_queue.inventory_queue y una Lambda
```

## Notas

- Todos los ejemplos esperan infraestructura en ejecución (broker Kafka,
  RabbitMQ, cuenta AWS). Son implementaciones de referencia para la
  receta, no despliegues listos para usar.
- `save_order()` / `reserveInventory()` quedan como stubs a propósito —
  conecta tu capa de persistencia o servicio de inventario.
