class OrderedOutboxRelay(OutboxRelay):
    """Publishes events ordered by aggregate_id using Kafka key-based partitioning."""

    def _process_batch(self) -> int:
        with self.engine.connect() as conn:
            # Group by aggregate_id to maintain ordering
            events = conn.execute(
                text("""SELECT id, aggregate_id, aggregate_type, event_type, payload, headers
                        FROM outbox_events
                        WHERE status = 'PENDING'
                        ORDER BY aggregate_id, created_at ASC
                        LIMIT :batch_size
                        FOR UPDATE SKIP LOCKED"""),
                {'batch_size': self.batch_size}
            ).fetchall()

            if not events:
                return 0

            for event in events:
                event_id, agg_id, agg_type, event_type, payload, headers = event

                # Use aggregate_id as Kafka key — same aggregate goes to same partition
                self.producer.produce(
                    topic=f'{agg_type.lower()}.events',
                    key=agg_id.encode('utf-8'),  # Key ensures ordering per aggregate
                    value=payload.encode('utf-8') if isinstance(payload, str) else json.dumps(payload).encode('utf-8'),
                )

                conn.execute(
                    text("""UPDATE outbox_events
                            SET status = 'PUBLISHED', published_at = NOW()
                            WHERE id = :id"""),
                    {'id': event_id}
                )

            self.producer.flush()
            conn.commit()
            return len(events)
