class ResilientOutboxRelay(OutboxRelay):
    def _process_batch(self) -> int:
        with self.engine.connect() as conn:
            # Include retry-eligible events
            events = conn.execute(
                text("""SELECT id, aggregate_id, aggregate_type, event_type, payload, headers, retry_count
                        FROM outbox_events
                        WHERE status = 'PENDING'
                          AND (next_retry_at IS NULL OR next_retry_at <= NOW())
                          AND retry_count < 5
                        ORDER BY created_at ASC
                        LIMIT :batch_size
                        FOR UPDATE SKIP LOCKED"""),
                {'batch_size': self.batch_size}
            ).fetchall()

            if not events:
                return 0

            for event in events:
                event_id, agg_id, agg_type, event_type, payload, headers, retry_count = event

                try:
                    self.producer.produce(
                        topic=f'{agg_type.lower()}.events',
                        key=agg_id.encode('utf-8'),
                        value=payload.encode('utf-8') if isinstance(payload, str) else json.dumps(payload).encode('utf-8'),
                    )
                    self.producer.flush(timeout=10)

                    conn.execute(
                        text("""UPDATE outbox_events
                                SET status = 'PUBLISHED', published_at = NOW()
                                WHERE id = :id"""),
                        {'id': event_id}
                    )

                except Exception as e:
                    logger.error(f"Failed to publish {event_id}: {e}")
                    backoff = min(30 * (2 ** retry_count), 3600)  # Exponential backoff, max 1 hour
                    conn.execute(
                        text("""UPDATE outbox_events
                                SET retry_count = retry_count + 1,
                                    next_retry_at = NOW() + :backoff * INTERVAL '1 second'
                                WHERE id = :id"""),
                        {'id': event_id, 'backoff': backoff}
                    )

                    if retry_count >= 4:
                        conn.execute(
                            text("""UPDATE outbox_events SET status = 'FAILED' WHERE id = :id"""),
                            {'id': event_id}
                        )
                        logger.error(f"Event {event_id} moved to FAILED status")

            conn.commit()
            return len(events)
