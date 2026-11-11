"""Factory Pattern: registry-based factory for database connections.

Each product owns its config shape; the factory only routes. Plugins can
register new engines without modifying DatabaseFactory.
"""


class DatabaseConnection:
    def connect(self) -> str:
        raise NotImplementedError

    def query(self, sql: str) -> str:
        raise NotImplementedError


class PostgresConnection(DatabaseConnection):
    def __init__(self, host: str, port: int, database: str):
        self.dsn = f"postgresql://{host}:{port}/{database}"

    def connect(self) -> str:
        return f"pg.connect({self.dsn})"

    def query(self, sql: str) -> str:
        return f"pg.query({sql})"


class MySQLConnection(DatabaseConnection):
    def __init__(self, host: str, port: int, database: str):
        self.dsn = f"mysql://{host}:{port}/{database}"

    def connect(self) -> str:
        return f"mysql.connect({self.dsn})"

    def query(self, sql: str) -> str:
        return f"mysql.query({sql})"


class DatabaseFactory:
    _registry = {}

    @classmethod
    def register(cls, db_type: str, creator) -> None:
        cls._registry[db_type] = creator

    @classmethod
    def create(cls, db_type: str, config: dict) -> DatabaseConnection:
        try:
            return cls._registry[db_type](**config)
        except KeyError:
            raise ValueError(f"Unknown DB type: {db_type}")


DatabaseFactory.register("postgres", lambda **cfg: PostgresConnection(**cfg))
DatabaseFactory.register("mysql", lambda **cfg: MySQLConnection(**cfg))


if __name__ == "__main__":
    db = DatabaseFactory.create("postgres", {
        "host": "localhost",
        "port": 5432,
        "database": "myapp",
    })
    print(db.connect())
    print(db.query("SELECT * FROM users"))
