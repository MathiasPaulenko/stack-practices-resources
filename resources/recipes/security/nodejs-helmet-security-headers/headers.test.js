const request = require("supertest");
const app = require("./app");

describe("Security Headers", () => {
  it("should set X-Content-Type-Options", async () => {
    const response = await request(app).get("/");
    expect(response.headers["x-content-type-options"]).toBe("nosniff");
  });

  it("should set X-Frame-Options", async () => {
    const response = await request(app).get("/");
    expect(response.headers["x-frame-options"]).toBe("DENY");
  });

  it("should set Strict-Transport-Security", async () => {
    const response = await request(app).get("/");
    expect(response.headers["strict-transport-security"]).toContain("max-age=31536000");
  });

  it("should set Content-Security-Policy", async () => {
    const response = await request(app).get("/");
    expect(response.headers["content-security-policy"]).toContain("default-src 'self'");
  });

  it("should remove X-Powered-By", async () => {
    const response = await request(app).get("/");
    expect(response.headers["x-powered-by"]).toBeUndefined();
  });
});
