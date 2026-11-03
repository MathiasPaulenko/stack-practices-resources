"""Reconciliation checker — verifies a CDC consumer stays in sync.

Compares source row counts with the target index and re-syncs missing
documents. Run on a schedule (cron, Kubernetes CronJob).

Requires: psycopg2-binary, elasticsearch
"""
import logging

logger = logging.getLogger(__name__)


class Reconciliation:
    def __init__(self, source_db, target_es):
        self.source = source_db
        self.target = target_es

    def reconcile(self, table, index):
        # `table` is a trusted internal identifier (config), never user input
        with self.source.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            source_count = cur.fetchone()[0]

            cur.execute(f"SELECT id FROM {table} ORDER BY updated_at DESC LIMIT 100")
            recent_ids = [row[0] for row in cur.fetchall()]

        target_count = self.target.count(index=index)['count']

        if source_count != target_count:
            logger.warning(
                f"Count mismatch: source={source_count}, target={target_count}"
            )
            for doc_id in recent_ids:
                exists = self.target.exists(index=index, id=doc_id)
                if not exists:
                    logger.warning(f"Missing in target: id={doc_id}")
                    self.resync_record(table, index, doc_id)

    def resync_record(self, table, index, doc_id):
        with self.source.cursor() as cur:
            cur.execute(f"SELECT * FROM {table} WHERE id = %s", (doc_id,))
            row = cur.fetchone()
            if row:
                self.target.index(index=index, id=doc_id, document=dict(row))
                logger.info(f"Re-synced record {doc_id}")
