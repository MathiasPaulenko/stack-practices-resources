# Guía Completa de Apache Kafka en Producción — Companion

Companion ejecutable de la guía de StackPractices
[Guía Completa de Apache Kafka en Producción](https://stackpractices.com/es/guides/complete-guide-kafka-production/).

- `docker-compose.yml` — cluster KRaft de 3 brokers (sin ZooKeeper) con RF=3 como en producción
- `config/server-production.properties` — settings de broker de producción (RF=3, ISR=2, retención)
- `config/producer-tuning.py` / `consumer-tuning.py` — clientes kafka-python tuneados de la guía
- `scripts/create-topics.sh` — crea el topic `orders` con RF=3
- `scripts/check-health.sh` — checks de particiones under-replicated + consumer lag

## Ejecutar

```bash
docker compose up -d
./scripts/create-topics.sh
pip install kafka-python
python config/producer-tuning.py
```

Detén `kafka3` para ver el failover del leader de partición a una réplica ISR — el escenario de falla que cubre la guía.
