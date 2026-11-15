# Consumer Groups de Kafka (Python) — Código Companion

Demo ejecutable de consumer groups para la receta de StackPractices [Consumer Groups de Kafka con Python](https://stackpractices.com/es/recipes/kafka-python-consumer-groups/).

## Archivos

| Archivo | Propósito |
|---|---|
| `docker-compose.yml` | Kafka de un nodo en modo KRaft (sin Zookeeper) |
| `producer.py` | Envía 30 eventos `OrderCreated` con key `userId` |
| `consumer_worker.py` | Miembro del consumer group con logging de `on_assign`/`on_revoke`/`on_lost` |
| `requirements.txt` | Dependencia `confluent-kafka` |

## Ejecución

```bash
docker compose up -d          # levantar Kafka (KRaft, localhost:9092)
pip install -r requirements.txt

python consumer_worker.py worker-1   # terminal 1
python consumer_worker.py worker-2   # terminal 2 — mira los logs de rebalanceo
python producer.py                   # terminal 3 — envía 30 órdenes
```

Luego experimenta:

- Inicia un `worker-3` — cooperative-sticky mueve particiones incrementalmente sin detener el grupo.
- Ctrl+C a un worker — sus particiones se reasignan tras `session.timeout.ms`.
- Vuelve a correr `producer.py` mientras un worker está caído — al volver, se pone al día desde su último offset confirmado.

## Notas

- `KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092` solo funciona desde el host; los contenedores necesitan un segundo listener interno.
- El topic `orders` se auto-crea con un número de particiones por defecto. Para una demo de rebalanceo real, créalo con varias particiones antes: `docker exec kafka kafka-topics --create --topic orders --partitions 6 --bootstrap-server localhost:9092`.
- `consumer.commit(msg)` confirma por mensaje para claridad de la demo; confirma en lotes para throughput en producción.
