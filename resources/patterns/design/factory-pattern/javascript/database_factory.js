// Factory Pattern: registry-based factory for database connections.
class PostgresConnection {
  constructor({ host, port, database }) {
    this.dsn = `postgresql://${host}:${port}/${database}`;
  }
  connect() {
    return `pg.connect(${this.dsn})`;
  }
  query(sql) {
    return `pg.query(${sql})`;
  }
}

class MySQLConnection {
  constructor({ host, port, database }) {
    this.dsn = `mysql://${host}:${port}/${database}`;
  }
  connect() {
    return `mysql.connect(${this.dsn})`;
  }
  query(sql) {
    return `mysql.query(${sql})`;
  }
}

class DatabaseFactory {
  static registry = new Map();

  static register(type, creator) {
    this.registry.set(type, creator);
  }

  static create(type, config) {
    const creator = this.registry.get(type);
    if (!creator) throw new Error(`Unknown DB type: ${type}`);
    return creator(config);
  }
}

DatabaseFactory.register("postgres", (cfg) => new PostgresConnection(cfg));
DatabaseFactory.register("mysql", (cfg) => new MySQLConnection(cfg));

const db = DatabaseFactory.create("postgres", {
  host: "localhost",
  port: 5432,
  database: "myapp",
});
console.log(db.connect());
console.log(db.query("SELECT * FROM users"));
