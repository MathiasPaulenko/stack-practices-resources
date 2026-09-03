# RabbitMQ Architecture Companion

Implementations of RabbitMQ exchange types, consumer patterns, clustering, and monitoring with tests.

## Files

| File | Language | Description |
|------|----------|-------------|
| `python_exchanges.py` | Python | Direct, topic, fanout, and headers exchange demos with pika |
| `python_consumer_patterns.py` | Python | Work queue, pub/sub, and RPC patterns |
| `python_clustering.py` | Python | Quorum queue, DLX queue, and priority queue declarations |
| `python_monitoring.py` | Python | Queue stats and alert checking via Management API |
| `javascript_rabbitmq.js` | JavaScript | Exchange demos with amqplib (Node.js) |
| `docker-compose.yml` | Docker | 2-node RabbitMQ cluster with management plugin |
| `rabbitmq.conf` | Config | Production-like RabbitMQ configuration |
| `test_exchanges.py` | Python | pytest tests for exchange types and DLX |
| `test_consumer_patterns.py` | Python | pytest tests for work queue, confirms, priority, TTL |

## Quick Start

### Docker (RabbitMQ cluster)

```bash
docker-compose up -d
# RabbitMQ available at localhost:5672
# Management UI at http://localhost:15672 (admin/admin_pass)
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

## Key Features

- All 4 exchange types (direct, topic, fanout, headers)
- Consumer patterns (work queue, pub/sub, RPC)
- Quorum queues with Raft consensus
- Dead letter exchange with TTL and rejection
- Priority queues
- Publisher confirmsss
- Monitoring via Management API
- 2-node cluster with docker-compose
- Production-like rabbitmq.conf
