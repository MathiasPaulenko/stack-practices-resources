// Express app wired exactly like the guide's "Server Configuration > Express.js" section.
import express from "express";
import helmet from "helmet";

export function createApp() {
  const app = express();

  app.use(
    helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", "https://cdn.jsdelivr.net"],
          styleSrc: ["'self'", "https://fonts.googleapis.com"],
          fontSrc: ["'self'", "https://fonts.gstatic.com"],
          imgSrc: ["'self'", "data:", "https:"],
          connectSrc: ["'self'", "https://api.example.com"],
          frameAncestors: ["'none'"],
          baseUri: ["'self'"],
          formAction: ["'self'"],
          objectSrc: ["'none'"],
        },
      },
      strictTransportSecurity: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true,
      },
      xFrameOptions: { action: "deny" },
      referrerPolicy: { policy: "strict-origin-when-cross-origin" },
      crossOriginOpenerPolicy: { policy: "same-origin" },
      crossOriginResourcePolicy: { policy: "same-origin" },
    })
  );

  app.use(express.json({ type: ["application/json", "application/csp-report", "application/reports+json"] }));

  app.get("/", (_req, res) => {
    res.type("html").send("<h1>secure headers demo</h1>");
  });

  app.get("/api/data", (_req, res) => {
    res.json({ ok: true });
  });

  // Legacy report-uri endpoint: single violation as application/csp-report
  app.post("/csp-report", (req, res) => {
    console.log("CSP violation (legacy):", req.body["csp-report"]);
    res.status(204).end();
  });

  // Reporting API endpoint: batched violations as application/reports+json
  app.post("/csp", (req, res) => {
    for (const report of req.body) {
      console.log("CSP violation:", report.body);
    }
    res.status(204).end();
  });

  return app;
}
