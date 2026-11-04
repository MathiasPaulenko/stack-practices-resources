// auth/introspect.ts — Ask the AS whether a token is active (RFC 7662)
import { env } from './env.js';

export async function introspectToken(token: string): Promise<boolean> {
  const response = await fetch('https://auth.example.com/oauth/introspect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      token,
      client_id: env('OAUTH_CLIENT_ID'),
      client_secret: env('OAUTH_CLIENT_SECRET'),
    }),
  });
  const data = await response.json() as { active?: boolean };
  return data.active === true; // cache briefly — introspecting every request adds latency
}
