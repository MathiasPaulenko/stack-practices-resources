// Composition root: the single file that knows about PostgreSQL, Express,
// and SMTP. Everything else stays technology-agnostic.

import express from "express";
import { Pool } from "pg";
import {
  PostgresUserRepository,
  SmtpEmailService,
} from "./adapters";
import { UserRegistrationService } from "./user-registration-service";

const app = express();
app.use(express.json());

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const userRepository = new PostgresUserRepository(pool);
const emailService = new SmtpEmailService();

const registrationService = new UserRegistrationService(
  userRepository,
  emailService
);

// Express route (driving adapter over HTTP)
app.post("/users", async (req, res) => {
  try {
    const user = await registrationService.register(
      req.body.email,
      req.body.name
    );
    res.status(201).json(user);
  } catch (err) {
    res.status(400).json({ error: (err as Error).message });
  }
});

app.listen(3000);
