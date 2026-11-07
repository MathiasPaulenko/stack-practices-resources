import { describe, expect, it } from "vitest";
import request from "supertest";
import { createApp } from "../src/app.js";

const app = createApp();

describe("baseline security headers", () => {
  it("sets X-Content-Type-Options: nosniff", async () => {
    const res = await request(app).get("/");
    expect(res.headers["x-content-type-options"]).toBe("nosniff");
  });

  it("sets X-Frame-Options: DENY", async () => {
    const res = await request(app).get("/");
    expect(res.headers["x-frame-options"]).toBe("DENY");
  });

  it("sets the strict referrer policy", async () => {
    const res = await request(app).get("/");
    expect(res.headers["referrer-policy"]).toBe("strict-origin-when-cross-origin");
  });

  it("sets HSTS with preload and includeSubDomains", async () => {
    const res = await request(app).get("/");
    expect(res.headers["strict-transport-security"]).toBe(
      "max-age=31536000; includeSubDomains; preload"
    );
  });

  it("does not leak X-Powered-By", async () => {
    const res = await request(app).get("/");
    expect(res.headers["x-powered-by"]).toBeUndefined();
  });

  it("sets cross-origin isolation headers", async () => {
    const res = await request(app).get("/");
    expect(res.headers["cross-origin-opener-policy"]).toBe("same-origin");
    expect(res.headers["cross-origin-resource-policy"]).toBe("same-origin");
  });
});

describe("Content-Security-Policy", () => {
  it("declares the core directives", async () => {
    const res = await request(app).get("/");
    const csp = res.headers["content-security-policy"];
    expect(csp).toContain("default-src 'self'");
    expect(csp).toContain("frame-ancestors 'none'");
    expect(csp).toContain("object-src 'none'");
    expect(csp).toContain("base-uri 'self'");
    expect(csp).toContain("form-action 'self'");
  });

  it("allows the configured CDN and font origins", async () => {
    const res = await request(app).get("/");
    const csp = res.headers["content-security-policy"];
    expect(csp).toContain("script-src 'self' https://cdn.jsdelivr.net");
    expect(csp).toContain("style-src 'self' https://fonts.googleapis.com");
    expect(csp).toContain("font-src 'self' https://fonts.gstatic.com");
  });

  it("never includes unsafe-inline or unsafe-eval", async () => {
    const res = await request(app).get("/");
    const csp = res.headers["content-security-policy"];
    expect(csp).not.toContain("unsafe-inline");
    expect(csp).not.toContain("unsafe-eval");
  });

  it("applies the same policy to API responses", async () => {
    const res = await request(app).get("/api/data");
    expect(res.headers["content-security-policy"]).toBeTruthy();
    expect(res.headers["x-content-type-options"]).toBe("nosniff");
  });
});

describe("CSP violation report endpoints", () => {
  const legacyReport = {
    "csp-report": {
      "document-uri": "https://example.com/page",
      "violated-directive": "script-src",
      "blocked-uri": "inline",
    },
  };

  const modernReports = [
    {
      type: "csp-violation",
      url: "https://example.com/page",
      body: { directive: "script-src", blockedURL: "inline" },
    },
  ];

  it("accepts legacy application/csp-report payloads", async () => {
    const res = await request(app)
      .post("/csp-report")
      .set("Content-Type", "application/csp-report")
      .send(legacyReport);
    expect(res.status).toBe(204);
  });

  it("accepts Reporting API batches", async () => {
    const res = await request(app)
      .post("/csp")
      .set("Content-Type", "application/reports+json")
      .send(modernReports);
    expect(res.status).toBe(204);
  });
});
