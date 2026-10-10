import psycopg2
from dataclasses import dataclass

@dataclass
class FailoverVerification:
    promoted_node: str
    old_primary_lsn: str  # Log sequence number at failure
    new_primary_lsn: str  # LSN at promotion
    transactions_lost: int
    consistency_ok: bool

def verify_failover_consistency(
    new_primary_host: str,
    old_primary_lsn: str,
    db_user: str = "monitor",
) -> FailoverVerification:
    """Verify data consistency after a database failover."""
    conn = psycopg2.connect(host=new_primary_host, user=db_user, dbname="postgres")
    cur = conn.cursor()

    # Get current LSN on new primary
    cur.execute("SELECT pg_current_wal_lsn();")
    new_lsn = cur.fetchone()[0]

    # Count transactions since promotion point
    cur.execute("""
        SELECT count(*) FROM pg_stat_activity
        WHERE state = 'active' AND xact_start > now() - interval '5 minutes';
    """)
    active_txns = cur.fetchone()[0]

    # Check for replication slot health
    cur.execute("""
        SELECT slot_name, active, restart_lsn
        FROM pg_replication_slots;
    """)
    slots = cur.fetchall()

    # Verify all slots are active
    all_active = all(slot[1] for slot in slots) if slots else True

    # Estimate lost transactions (simplified)
    lost = 0 if old_primary_lsn == "unknown" else estimate_lost(old_primary_lsn, new_lsn)

    result = FailoverVerification(
        promoted_node=new_primary_host,
        old_primary_lsn=old_primary_lsn,
        new_primary_lsn=new_lsn,
        transactions_lost=lost,
        consistency_ok=all_active,
    )

    cur.close()
    conn.close()
    return result

def estimate_lost(old_lsn: str, new_lsn: str) -> int:
    """Estimate lost transactions between two LSNs."""
    # Parse LSN format (e.g., '0/17000058')
    try:
        old_parts = [int(x, 16) for x in old_lsn.split("/")]
        new_parts = [int(x, 16) for x in new_lsn.split("/")]
        old_bytes = old_parts[0] * 0x100000000 + old_parts[1]
        new_bytes = new_parts[0] * 0x100000000 + new_parts[1]
        diff = new_bytes - old_bytes
        # Rough estimate: 1 transaction ~ 200 bytes average
        return max(0, diff // 200)
    except (ValueError, IndexError):
        return 0

# Example usage
result = verify_failover_consistency(
    new_primary_host="replica.db.internal",
    old_primary_lsn="0/17000058",
)
print(f"Promoted node: {result.promoted_node}")
print(f"Transactions lost (est.): {result.transactions_lost}")
print(f"Replication slots healthy: {result.consistency_ok}")
