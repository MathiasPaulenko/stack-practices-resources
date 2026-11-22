import threading

class DatabaseConnectionPool:
    _instances = {}
    _lock = threading.Lock()

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        print(f"Created pool for tenant {tenant_id}")

    @classmethod
    def get_instance(cls, tenant_id: str):
        # Double-checked locking: the fast path avoids the lock once
        # the instance exists.
        if tenant_id not in cls._instances:
            with cls._lock:
                if tenant_id not in cls._instances:
                    cls._instances[tenant_id] = cls(tenant_id)
        return cls._instances[tenant_id]

    def query(self, sql: str):
        return f"[{self.tenant_id}] Result for: {sql}"


# Usage
pool_a = DatabaseConnectionPool.get_instance("tenant-a")
pool_b = DatabaseConnectionPool.get_instance("tenant-b")
pool_a2 = DatabaseConnectionPool.get_instance("tenant-a")

print(pool_a is pool_a2)  # True — same instance
print(pool_a is pool_b)   # False — different instance
