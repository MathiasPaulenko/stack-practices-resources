"""Lightweight DI container — companion to
https://stackpractices.com/recipes/dependency-injection/

Scoped lifetimes via context manager; no dependencies.
"""

from contextlib import contextmanager
from typing import TypeVar, Callable, Dict

T = TypeVar('T')


class DIContainer:
    def __init__(self):
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, object] = {}
        self._scoped: Dict[str, object] = {}

    def register_singleton(self, key: str, factory: Callable[[], T]) -> None:
        self._factories[key] = lambda: self._singletons.setdefault(key, factory())

    def register_scoped(self, key: str, factory: Callable[[], T]) -> None:
        self._factories[key] = lambda: self._scoped.setdefault(key, factory())

    def register_transient(self, key: str, factory: Callable[[], T]) -> None:
        self._factories[key] = factory

    def resolve(self, key: str) -> T:
        if key not in self._factories:
            raise KeyError(f'No service registered for: {key}')
        return self._factories[key]()

    def validate(self) -> None:
        """Fail fast: resolve every registered key once at startup."""
        for key in self._factories:
            self.resolve(key)

    @contextmanager
    def scope(self):
        """Context manager for scoped lifetime (one per request/test)."""
        self._scoped.clear()
        try:
            yield self
        finally:
            self._scoped.clear()


# --- Example wiring (composition root) ---
#
# container = DIContainer()
# container.register_singleton('db', lambda: create_engine('postgresql://localhost/app'))
# container.register_scoped('session', lambda: Session(container.resolve('db')))
# container.register_transient('user_service', lambda: UserService(container.resolve('session')))
# container.validate()
#
# with container.scope() as scoped:
#     service = scoped.resolve('user_service')
#     service.register('user@example.com', 'password')
