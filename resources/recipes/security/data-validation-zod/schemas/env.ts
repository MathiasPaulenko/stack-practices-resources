// Fail-fast environment validation at startup — Zod 4 API.
import { z } from 'zod';

export const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().int().positive().default(3000),
  DATABASE_URL: z.url(),
  REDIS_URL: z.url().optional(),
  JWT_SECRET: z.string().min(32, 'JWT secret: min 32 characters'),
  JWT_EXPIRES_IN: z.string().regex(/^\d+[smhd]$/, 'e.g. "1h" or "7d"'),
  CORS_ORIGINS: z.string()
    .transform((val) => val.split(','))
    .pipe(z.array(z.url())),
  RATE_LIMIT_MAX: z.coerce.number().int().positive().default(100),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

const parsed = EnvSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('Invalid environment configuration:');
  parsed.error.issues.forEach((issue) => {
    console.error(`  ${issue.path.join('.')}: ${issue.message}`);
  });
  process.exit(1);
}

export const env = parsed.data;
// env is fully typed: env.PORT is number, env.CORS_ORIGINS is string[]
