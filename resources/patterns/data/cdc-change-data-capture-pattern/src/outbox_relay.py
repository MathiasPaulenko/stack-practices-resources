"""Transactional outbox relay — publishes outbox rows to Kafka.

Reads unprocessed rows with FOR UPDATE SKIP LOCKED so multiple relay
instances can run safely in parallel.

Requires: kafka-python, psycopg2-binary
"""
import json
import logging
import time

import psycopg2
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutboxRelay:
    def __init__(self, db_conn_str, kafka_servers):
        self.db = psycopg2.connect(db_conn_str)
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def relay(self):
        while True:
            with self.db.cursor() as cur:
                cur.execute("""
                    SELECT id, aggregate_type, aggregate_id, event_type, payload
                    FROM outbox
                    WHERE processed_at IS NULL
                    ORDER BY created_at
                    LIMIT 100
                    FOR UPDATE SKIP LOCKED
                """)
                rows = cur.fetchall()

                for row in rows:
                    event_id, agg_type, agg_id, event_type, payload = row
                    topic = f"events.{agg_type.lower()}"
                    self.producer.send(topic, key=agg_id, value={
                        'eventId': str(event_id),
                        'eventType': event_type,
                        'aggregateId': agg_id,
                        'payload': payload
                    })
                    cur.execute(
                        "UPDATE outbox SET processed_at = NOW() WHERE id = %s",
                        (event_id,)
                    )

                self.db.commit()

            if not rows:
                time.sleep(0.5)


if __name__ == '__main__':
    relay = OutboxRelay(
        db_conn_str='postgresql://postgres:postgres@localhost:5432/shopdb',
        kafka_servers=['localhost:9092']
    )
    relay.relay()
