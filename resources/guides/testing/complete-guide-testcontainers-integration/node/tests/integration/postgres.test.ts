// tests/integration/postgres.test.ts — Testcontainers in Node.js
import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import { PostgreSqlContainer, type StartedPostgreSqlContainer } from "@testcontainers/postgresql";
import { Client } from "pg";

describe("PostgreSQL integration", () => {
  let container: StartedPostgreSqlContainer;
  let client: Client;

  beforeAll(async () => {
    container = await new PostgreSqlContainer("postgres:16")
      .withDatabase("testdb")
      .withUsername("test")
      .withPassword("test")
      .start();

    client = new Client({
      host: container.getHost(),
      port: container.getMappedPort(5432),
      database: container.getDatabase(),
      user: container.getUsername(),
      password: container.getPassword(),
    });
    await client.connect();
  });

  afterAll(async () => {
    await client.end();
    await container.stop();
  });

  beforeEach(async () => {
    await client.query("DROP TABLE IF EXISTS users");
    await client.query(`
      CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL
      )
    `);
  });

  it("inserts and retrieves a user", async () => {
    const result = await client.query(
      "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id",
      ["alice@example.com", "Alice"]
    );
    expect(result.rows[0].id).toBeGreaterThan(0);

    const count = await client.query("SELECT COUNT(*) FROM users");
    expect(parseInt(count.rows[0].count)).toBe(1);
  });

  it("enforces unique email constraint", async () => {
    await client.query(
      "INSERT INTO users (email, name) VALUES ($1, $2)",
      ["bob@example.com", "Bob"]
    );

    await expect(
      client.query("INSERT INTO users (email, name) VALUES ($1, $2)", ["bob@example.com", "Bob2"])
    ).rejects.toThrow(/unique/i);
  });
});
