# Relay processes events per tenant
events = conn.execute(
    text("""SELECT * FROM outbox_events
            WHERE status = 'PENDING' AND tenant_id = :tenant
            ORDER BY created_at ASC LIMIT 100 FOR UPDATE SKIP LOCKED"""),
    {'tenant': tenant_id}
).fetchall()
