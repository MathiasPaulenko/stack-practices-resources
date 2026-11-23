"""Using PostgreSQL logical replication for CDC-based outbox relay.
This avoids polling and provides near-real-time event publishing."""

import psycopg2
from psycopg2.extras import LogicalReplicationConnection

class CDCOutboxRelay:
    def __init__(self, dsn: str, slot_name: str = 'outbox_slot'):
        self.conn = psycopg2.connect(
            dsn,
            connection_factory=LogicalReplicationConnection,
        )
        self.slot_name = slot_name

    def start(self):
        cur = self.conn.cursor()
        try:
            cur.create_replication_slot(self.slot_name, output_plugin='wal2json')
        except psycopg2.errors.DuplicateObject:
            pass  # Slot already exists

        cur.start_replication(
            slot_name=self.slot_name,
            options={'table-names': 'public.outbox_events'},
        )

        def process_msg(msg):
            import json
            changes = json.loads(msg.payload)
            for change in changes.get('change', []):
                if change['table'] == 'outbox_events' and change['kind'] == 'insert':
                    row = {col['name']: col['value'] for col in change['columnvalues']}
                    publish_to_kafka(row)
            msg.cursor.send_feedback(flush_lsn=msg.data_start)

        cur.consume_stream(process_msg)
