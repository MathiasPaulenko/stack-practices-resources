# failover/database.py — PostgreSQL failover with connection switching
import psycopg2
import time
import threading

class DatabaseFailover:
    """Manages database connections with automatic failover.
    Primary: read-write. Standby: read-only, promoted on failover."""

    def __init__(self, primary_config, standby_configs):
        self.primary_config = primary_config
        self.standby_configs = standby_configs
        self._active_config = primary_config
        self._is_failover = False
        self._lock = threading.Lock()
        self._connection = None

    def _create_connection(self, config):
        return psycopg2.connect(
            host=config["host"],
            port=config.get("port", 5432),
            database=config["database"],
            user=config["user"],
            password=config["password"],
            connect_timeout=5
        )

    def get_connection(self):
        """Get a connection to the active database."""
        with self._lock:
            if self._connection and not self._connection.closed:
                try:
                    # Test the connection
                    self._connection.cursor().execute("SELECT 1")
                    return self._connection
                except Exception:
                    self._connection = None

            # Try active config
            try:
                self._connection = self._create_connection(self._active_config)
                return self._connection
            except Exception as e:
                print(f"Active DB unavailable: {e}")
                self._initiate_failover()
                self._connection = self._create_connection(self._active_config)
                return self._connection

    def _initiate_failover(self):
        """Try each standby in order."""
        for i, standby in enumerate(self.standby_configs):
            try:
                conn = self._create_connection(standby)
                conn.close()
                self._active_config = standby
                self._is_failover = True
                print(f"Failed over to standby {i}: {standby['host']}")
                return
            except Exception:
                continue

        raise Exception("All databases are unavailable")

    def execute(self, query, params=None):
        """Execute a query on the active database."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        conn.commit()
        return result

    @property
    def is_failover(self):
        with self._lock:
            return self._is_failover


if __name__ == "__main__":
    db = DatabaseFailover(
        primary_config={"host": "db-primary.internal", "database": "shop",
                        "user": "app", "password": "secret"},
        standby_configs=[
            {"host": "db-replica-1.internal", "database": "shop",
             "user": "app", "password": "secret"},
            {"host": "db-replica-2.internal", "database": "shop",
             "user": "app", "password": "secret"},
        ]
    )

    # Automatically fails over if primary is down
    users = db.execute("SELECT * FROM users LIMIT 10")
    print(users)
