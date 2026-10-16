// tests/integration/redis.test.ts — Redis with Testcontainers
import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import { RedisContainer, type StartedRedisContainer } from "@testcontainers/redis";
import Redis from "ioredis";

describe("Redis integration", () => {
  let container: StartedRedisContainer;
  let redis: Redis;

  beforeAll(async () => {
    container = await new RedisContainer("redis:7-alpine").start();
    redis = new Redis(container.getPort(), container.getHost());
  });

  afterAll(async () => {
    await redis.quit();
    await container.stop();
  });

  beforeEach(async () => {
    await redis.flushall();
  });

  it("sets and gets a string", async () => {
    await redis.set("key1", "value1");
    expect(await redis.get("key1")).toBe("value1");
  });

  it("performs hash operations", async () => {
    await redis.hset("user:1", "name", "Alice", "email", "alice@test.com");
    expect(await redis.hget("user:1", "name")).toBe("Alice");
    expect(await redis.hgetall("user:1")).toEqual({
      name: "Alice",
      email: "alice@test.com",
    });
  });
});
