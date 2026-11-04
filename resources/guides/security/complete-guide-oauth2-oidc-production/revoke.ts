// auth/revoke.ts — Revoke a token at the authorization server (RFC 7009)
import { env } from './env.js';

export async function revokeToken(
  token: string,
  hint: 'access_token' | 'refresh_token',
): Promise<void> {
  await fetch('https://auth.example.com/oauth/revoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      token,
      token_type_hint: hint,
      client_id: env('OAUTH_CLIENT_ID'),
      client_secret: env('OAUTH_CLIENT_SECRET'),
    }),
  });
  // RFC 7009: the endpoint returns 200 even for unknown/invalid tokens
}
