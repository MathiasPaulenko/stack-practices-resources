// Configuration object built step by step — the most common real-world Builder use.

class DatabaseConfig {
  constructor(
    public readonly host: string,
    public readonly port: number,
    public readonly database: string,
    public readonly username: string,
    public readonly password: string,
    public readonly poolSize: number,
    public readonly timeout: number,
    public readonly ssl: boolean,
    public readonly retryAttempts: number
  ) {}
}

class DatabaseConfigBuilder {
  private host: string = 'localhost';
  private port: number = 5432;
  private database!: string;
  private username!: string;
  private password!: string;
  private poolSize: number = 10;
  private timeout: number = 5000;
  private ssl: boolean = false;
  private retryAttempts: number = 3;

  setHost(host: string): this { this.host = host; return this; }
  setPort(port: number): this { this.port = port; return this; }
  setDatabase(database: string): this { this.database = database; return this; }
  setCredentials(username: string, password: string): this {
    this.username = username;
    this.password = password;
    return this;
  }
  setPoolSize(size: number): this { this.poolSize = size; return this; }
  setTimeout(timeout: number): this { this.timeout = timeout; return this; }
  enableSsl(): this { this.ssl = true; return this; }
  setRetryAttempts(attempts: number): this { this.retryAttempts = attempts; return this; }

  build(): DatabaseConfig {
    if (!this.database) throw new Error('Database name is required');
    if (!this.username || !this.password) {
      throw new Error('Credentials are required');
    }
    return new DatabaseConfig(
      this.host, this.port, this.database, this.username,
      this.password, this.poolSize, this.timeout, this.ssl, this.retryAttempts
    );
  }
}

// Environment presets share the same builder and override only what differs.
function productionPreset(): DatabaseConfigBuilder {
  return new DatabaseConfigBuilder()
    .setHost('db.production.com')
    .setPoolSize(50)
    .enableSsl()
    .setTimeout(10000);
}

function developmentPreset(): DatabaseConfigBuilder {
  return new DatabaseConfigBuilder(); // localhost:5432, pool of 10, SSL off
}

// Load secrets from the environment — never hardcode them in builder calls.
const prodConfig = productionPreset()
  .setDatabase('myapp')
  .setCredentials(process.env.DB_USER ?? 'user', process.env.DB_PASSWORD ?? 'secret')
  .build();

const devConfig = developmentPreset()
  .setDatabase('myapp_dev')
  .setCredentials('dev', 'dev')
  .build();

console.log(prodConfig.host, prodConfig.poolSize, prodConfig.ssl); // db.production.com 50 true
console.log(devConfig.host, devConfig.poolSize, devConfig.ssl);    // localhost 10 false
