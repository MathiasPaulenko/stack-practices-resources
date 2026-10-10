# Message Queue Load Leveling — ejemplos complementarios

Ejemplos ejecutables del patrón de StackPractices
[Message Queue Load Leveling](https://stackpractices.com/es/patterns/message-queue-load-leveling-pattern/):
el productor escribe a cualquier ritmo y el consumidor vacía la cola a ritmo controlado.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `celery_consumer.py` | Productor + tarea Celery sobre Redis — pico de 1.000 pedidos, el worker drena 1 cada 2 s |
| `requirements.txt` | Dependencia Python (`celery[redis]`) |
| `bullmq_worker.mjs` | Cola BullMQ + worker con `limiter` (máx 1 job / 2 s) sobre Redis |
| `package.json` | Dependencia Node (`bullmq`) y script de ejecución |
| `pom.xml` | Proyecto Maven para el ejemplo Java |
| `src/main/java/OrderProcessor.java` | Productor Spring AMQP + consumidor `@RabbitListener` con `concurrency=1` |

## Cómo ejecutar los ejemplos

### Python (Celery + Redis)

```bash
docker run -p 6379:6379 -d redis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
celery -A celery_consumer worker --concurrency=1 --loglevel=info   # terminal 1
python celery_consumer.py                                        # terminal 2
```

### Node.js (BullMQ + Redis)

```bash
docker run -p 6379:6379 -d redis
npm install
npm start
```

### Java (Spring AMQP + RabbitMQ)

```bash
docker run -p 5672:5672 -d rabbitmq
mvn compile exec:java -Dexec.mainClass="OrderProcessor"
```

## Notas

- Los ejemplos necesitan un broker en ejecución (Redis para Celery/BullMQ, RabbitMQ para Java).
- Observa la cola: el pico encola 1.000 jobs al instante mientras el worker los
  drena a su propio ritmo — esa diferencia de tasas es todo el patrón.
