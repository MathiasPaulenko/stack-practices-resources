class TransactionalOutboxRelay:
    """Publishes each batch inside one Kafka transaction to avoid partial publishes."""

    def __init__(self, database_url: str, kafka_config: dict, batch_size: int = 100):
        self.engine = create_engine(database_url)
        self.kafka_config = {**kafka_config, 'transactional.id': 'outbox-relay-txn'}
        self.producer = Producer(self.kafka_config)
        self.producer.init_transactions()
        self.batch_size = batch_size

    def process_batch(self) -> int:
        with self.engine.connect() as conn:
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

            # One transaction per batch, not per event — per-event txns kill throughput
            self.producer.begin_transaction()
            try:
                for event in events:
                    event_id, agg_id, agg_type, event_type, payload, headers = event
                    self.producer.produce(
                        topic=f'{agg_type.lower()}.events',
                        key=agg_id.encode('utf-8'),
                        value=payload.encode('utf-8') if isinstance(payload, str) else json.dumps(payload).encode('utf-8'),
                    )
                self.producer.commit_transaction()
            except Exception as e:
                logger.error(f"Kafka transaction failed: {e}")
                self.producer.abort_transaction()
                return 0

            # Mark the batch published after the Kafka commit succeeds
            for event in events:
                conn.execute(
                    text("""UPDATE outbox_events
                            SET status = 'PUBLISHED', published_at = NOW()
                            WHERE id = :id"""),
                    {'id': event[0]}
                )
            conn.commit()
            return len(events)
