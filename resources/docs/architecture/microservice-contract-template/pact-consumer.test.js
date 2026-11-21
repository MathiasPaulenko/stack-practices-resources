// Consumer-driven contract test with Pact.
// Requires: npm install @pact-foundation/pact
// Run with a Jest/Mocha runner; on success it writes a pact file to ./pacts.
const { Pact } = require("@pact-foundation/pact");
const path = require("path");

const provider = new Pact({
  consumer: "web-frontend",
  provider: "user-service",
  port: 8080,
  log: path.resolve(__dirname, "logs", "pact.log"),
  dir: path.resolve(__dirname, "pacts"),
});

describe("User Service Contract", () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it("returns a user by ID", async () => {
    await provider.addInteraction({
      uponReceiving: "a request for user 123",
      withRequest: {
        method: "GET",
        path: "/users/123",
        headers: { Accept: "application/json" },
      },
      willRespondWith: {
        status: 200,
        headers: { "Content-Type": "application/json" },
        body: {
          id: 123,
          name: "Alice",
          email: "alice@example.com",
        },
      },
    });

    const res = await fetch("http://localhost:8080/users/123", {
      headers: { Accept: "application/json" },
    });
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.id).toBe(123);
    expect(body.name).toBe("Alice");
  });
});
