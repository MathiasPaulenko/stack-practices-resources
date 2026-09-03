# Companion de Arquitectura RabbitMQ

Implementaciones de tipos de exchange, patrones de consumer, clustering y monitoreo de RabbitMQ con tests.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `python_exchanges.py` | Python | Demos de exchanges direct, topic, fanout y headers con pika |
| `python_consumer_patterns.py` | Python | Patrones work queue, pub/sub y RPC |
| `python_clustering.py` | Python | Declaración de quorum queue, DLX queue y priority queue |
| `python_monitoring.py` | Python | Stats de colas y checking de alertas via Management API |
| `javascript_rabbitmq.js` | JavaScript | Demos de exchanges con amqplib (Node.js) |
| `docker-compose.yml` | Docker | Cluster RabbitMQ de 2 nodos con management plugin |
| `rabbitmq.conf` | Config | Configuración de RabbitMQ tipo producción |
| `test_exchanges.py` | Python | Tests pytest para tipos de exchange y DLX |
| `test_consumer_patterns.py` | Python | Tests pytest para work queue, confirms, prioridad, TTL |

## Inicio Rápido

### Docker (Cluster RabbitMQ)

```bash
docker-compose up -d
# RabbitMQ disponible en localhost:5672
# Management UI en http://localhost:15672 (admin/admin_pass)
```

### Python

```bash
pip install -r requirements.txt
python python_exchanges.py
python python_consumer_patterns.py
python python_clustering.py
python python_monitoring.py
pytest test_exchanges.py test_consumer_patterns.py -v
```

### JavaScript

```bash
npm install
node javascript_rabbitmq.js
```

## Features Clave

- Los 4 tipos de exchange (direct, topic, fanout, headers)
- Patrones de consumer (work queue, pub/sub, RPC)
- Quorum queues con consenso Raft
- Dead letter exchange con TTL y rechazo
- Priority queues
- Publisher confirms
- Monitoreo via Management API
- Cluster de 2 nodos con docker-compose
- rabbitmq.conf tipo producción
