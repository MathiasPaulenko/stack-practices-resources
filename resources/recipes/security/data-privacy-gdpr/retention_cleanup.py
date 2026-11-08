"""Data retention auto-deletion job (run via cron).

Deletes or anonymizes records past their retention period and writes an
audit entry. Retention rules must also cover database backups.
"""

import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

RETENTION_POLICIES = {
    'inactive_users': timedelta(days=730),    # 2 years
    'activity_logs': timedelta(days=365),     # 1 year
    'session_data': timedelta(days=30),       # 30 days
    'marketing_data': timedelta(days=540),    # 18 months
}


def run_retention_cleanup(db):
    """Delete or anonymize data past retention period."""
    now = datetime.now(timezone.utc)

    for data_type, retention in RETENTION_POLICIES.items():
        cutoff = now - retention
        deleted_count = 0

        if data_type == 'inactive_users':
            # Anonymize instead of delete to preserve order history
            deleted_count = db.execute("""
                UPDATE users
                SET email = NULL, name = 'Anonymized User',
                    phone = NULL, deleted_at = NOW()
                WHERE last_login < %s AND deleted_at IS NULL
            """, (cutoff,)).rowcount

        elif data_type == 'activity_logs':
            deleted_count = db.execute("""
                DELETE FROM activity_logs
                WHERE created_at < %s
            """, (cutoff,)).rowcount

        elif data_type == 'session_data':
            deleted_count = db.execute("""
                DELETE FROM sessions
                WHERE expires_at < %s
            """, (cutoff,)).rowcount

        logger.info(
            'Retention cleanup: %s - %d records processed',
            data_type, deleted_count,
        )

    # Log audit entry
    db.execute("""
        INSERT INTO audit_log (action, details, created_at)
        VALUES ('retention_cleanup', %s, NOW())
    """, (f'Completed at {now.isoformat()}',))
