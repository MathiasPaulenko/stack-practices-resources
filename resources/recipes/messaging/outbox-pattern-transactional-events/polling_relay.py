import json
import logging
import time
from confluent_kafka import Producer
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class OutboxRelay:
    def __init__(self, database_url: str, kafka_config: dict, batch_size: int = 100):
        self.engine = create_engine(database_url)
        self.producer = Producer(kafka_config)
        self.batch_size = batch_size
        self._running = True

    def run(self, poll_interval: float = 1.0):
        logger.info("Starting outbox relay...")
        while self._running:
            try:
                processed = self._process_batch()
                if processed == 0:
                    time.sleep(poll_interval)
            except Exception as e:
                logger.error(f"Relay error: {e}")
                time.sleep(5)

    def _process_batch(self) -> int:
        with self.engine.connect() as conn:
            # Select unpublished events with row-level locking
            events = conn.execute(
                text("""SELECT id, aggregate_id, aggregate_type, event_type, payload, headers
                        FROM outbox_events
                        WHERE status = 'PENDING'
                        ORDER BY created_at ASC
                        LIMIT :batch_size
                        FOR UPDATE SKIP LOCKED"""),
                {'batch_size': self.batch_size}
            ).fetchall()

            if not events:
                return 0

            for event in events:
                event_id, agg_id, agg_type, event_type, payload, headers = event

                topic = f'{agg_type.lower()}.events'
                key = agg_id.encode('utf-8')

                self.producer.produce(
                    topic=topic,
                    key=key,
                    value=payload.encode('utf-8') if isinstance(payload, str) else json.dumps(payload).encode('utf-8'),
                    headers=[(k, v.encode('utf-8')) for k, v in json.loads(headers).items()],
                    on_delivery=self._delivery_callback(event_id, conn),
                )

            self.producer.flush(timeout=10)
            conn.commit()
            return len(events)

    def _delivery_callback(self, event_id, conn):
        def callback(err, msg):
            if err:
                logger.error(f"Failed to publish event {event_id}: {err}")
                conn.execute(
                    text("""UPDATE outbox_events
                            SET retry_count = retry_count + 1,
                                next_retry_at = NOW() + INTERVAL '30 seconds'
                            WHERE id = :id"""),
                    {'id': event_id}
                )
            else:
                conn.execute(
                    text("""UPDATE outbox_events
                            SET status = 'PUBLISHED', published_at = NOW()
                            WHERE id = :id"""),
                    {'id': event_id}
                )
        return callback

    def stop(self):
        self._running = False

# Run the relay
relay = OutboxRelay(
    'postgresql://user:pass@localhost/myapp',
    {'bootstrap.servers': 'localhost:9092'},
    batch_size=100,
)
relay.run()
