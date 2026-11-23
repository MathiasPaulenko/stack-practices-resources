import { describe, it, expect } from "vitest";
import request from "supertest";
import jwt from "jsonwebtoken";
import { createApp } from "./app.js";

const SECRET = "test-secret";
const app = createApp();

describe("GET /api/health", () => {
  it("returns 200 with healthy status", async () => {
    const response = await request(app).get("/api/health");
    expect(response.status).toBe(200);
    expect(response.body.status).toBe("healthy");
  });
});

describe("POST /api/users", () => {
  it("creates a user with valid data", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({ email: "alice@example.com", name: "Alice" });
    expect(response.status).toBe(201);
    expect(response.body.email).toBe("alice@example.com");
  });

  it("returns 400 when email is missing", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({ name: "Alice" });
    expect(response.status).toBe(400);
    expect(response.body.error).toContain("email");
  });
});

describe("GET /api/users with pagination", () => {
  it("returns first page by default", async () => {
    const response = await request(app).get("/api/users");
    expect(response.body.data).toHaveLength(10);
    expect(response.body.total).toBe(25);
  });

  it("returns correct page when specified", async () => {
    const response = await request(app).get("/api/users?page=2&limit=5");
    expect(response.body.data[0].id).toBe(6);
  });
});

describe("GET /api/profile with auth", () => {
  it("returns 401 without token", async () => {
    const response = await request(app).get("/api/profile");
    expect(response.status).toBe(401);
  });

  it("returns user data with valid token", async () => {
    const token = jwt.sign({ userId: 42, email: "alice@example.com" }, SECRET);
    const response = await request(app)
      .get("/api/profile")
      .set("Authorization", `Bearer ${token}`);
    expect(response.status).toBe(200);
    expect(response.body.userId).toBe(42);
  });

  it("returns 401 with expired token", async () => {
    const token = jwt.sign({ userId: 42 }, SECRET, { expiresIn: "0s" });
    const response = await request(app)
      .get("/api/profile")
      .set("Authorization", `Bearer ${token}`);
    expect(response.status).toBe(401);
  });
});

describe("Cookie-based sessions", () => {
  it("maintains cookies across requests", async () => {
    const agent = request.agent(app);
    await agent.post("/api/login").expect(200);
    const response = await agent.get("/api/dashboard");
    expect(response.status).toBe(200);
  });
});

describe("Error handling", () => {
  it("returns 500 with error message", async () => {
    const response = await request(app).get("/api/error");
    expect(response.status).toBe(500);
    expect(response.body.error).toBe("Something went wrong");
  });
});
