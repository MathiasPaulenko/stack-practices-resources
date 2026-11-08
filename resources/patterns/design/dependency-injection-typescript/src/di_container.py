"""DI container with explicit lifetimes — Python port of the article's
TypeScript container. Factories wire the graph; lifetimes decide caching."""

from enum import Enum


class Lifetime(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"


class Container:
    def __init__(self) -> None:
        self._registrations: dict[str, tuple] = {}
        self._singletons: dict[str, object] = {}

    def register(self, token: str, factory, lifetime: Lifetime = Lifetime.TRANSIENT) -> "Container":
        self._registrations[token] = (factory, lifetime)
        return self

    def resolve(self, token: str):
        if token not in self._registrations:
            raise KeyError(f"Nothing registered for {token}")
        factory, lifetime = self._registrations[token]

        if lifetime is Lifetime.SINGLETON:
            if token not in self._singletons:
                self._singletons[token] = factory(self)
            return self._singletons[token]
        return factory(self)

    def create_scope(self) -> "ScopedContainer":
        return ScopedContainer(self)


class ScopedContainer:
    def __init__(self, root: Container) -> None:
        self._root = root
        self._cache: dict[str, object] = {}

    def resolve(self, token: str):
        if token not in self._cache:
            self._cache[token] = self._root.resolve(token)
        return self._cache[token]


class Database:
    def query(self, _sql: str) -> list:
        return [{"id": 1, "name": "Alice"}]


class Logger:
    def info(self, msg: str) -> None:
        print(f"[info] {msg}")


class UserRepository:
    def __init__(self, db: Database, logger: Logger) -> None:
        self._db = db
        self._logger = logger

    def find_all(self) -> list:
        self._logger.info("fetching users")
        return self._db.query("SELECT * FROM users")


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def get_users(self) -> list:
        return self._repo.find_all()


if __name__ == "__main__":
    container = Container()
    container.register("db", lambda c: Database(), Lifetime.SINGLETON)
    container.register("logger", lambda c: Logger(), Lifetime.SINGLETON)
    container.register("repo", lambda c: UserRepository(c.resolve("db"), c.resolve("logger")))
    container.register("users", lambda c: UserService(c.resolve("repo")))

    service = container.resolve("users")
    print("users:", service.get_users())
    print("singleton shared:", container.resolve("db") is container.resolve("db"))
    print("transient fresh:", container.resolve("repo") is not container.resolve("repo"))

    scope_a, scope_b = container.create_scope(), container.create_scope()
    print("scoped same in scope:", scope_a.resolve("repo") is scope_a.resolve("repo"))
    print("scoped differs across scopes:", scope_a.resolve("repo") is not scope_b.resolve("repo"))
    print("singleton shared across scopes:", scope_a.resolve("db") is scope_b.resolve("db"))
