"""Registry Pattern: central map of named instances and lazy factories.

Run: python registry.py
"""
from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")


class Registry:
    _store: Dict[str, Any] = {}
    _factories: Dict[str, Callable[[], Any]] = {}

    @classmethod
    def register(cls, name: str, instance: Any) -> None:
        cls._store[name] = instance

    @classmethod
    def register_factory(cls, name: str, factory: Callable[[], Any]) -> None:
        cls._factories[name] = factory

    @classmethod
    def get(cls, name: str) -> Any:
        if name in cls._store:
            return cls._store[name]
        if name in cls._factories:
            instance = cls._factories[name]()
            cls._store[name] = instance
            return instance
        raise KeyError(f"No registration found for: {name}")

    @classmethod
    def has(cls, name: str) -> bool:
        return name in cls._store or name in cls._factories

    @classmethod
    def reset(cls) -> None:
        """Clear everything — call this between tests to avoid state leakage."""
        cls._store.clear()
        cls._factories.clear()


class DatabaseConnection:
    def query(self, sql: str) -> str:
        return f"Result: {sql}"


class CacheClient:
    def get(self, key: str) -> str:
        return f"cached-{key}"


if __name__ == "__main__":
    Registry.register("db", DatabaseConnection())
    Registry.register_factory("cache", lambda: CacheClient())

    db = Registry.get("db")
    cache = Registry.get("cache")  # factory runs here, then the instance is cached

    print(db.query("SELECT 1"))
    print(cache.get("users"))
    print("has db:", Registry.has("db"))
    print("same cache instance:", Registry.get("cache") is cache)

    try:
        Registry.get("missing")
    except KeyError as exc:
        print("KeyError:", exc)
