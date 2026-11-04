// auth/callback.ts — Exchange authorization code for tokens
import { timingSafeEqual } from 'crypto';
import type { Request, Response } from 'express';
import { env } from './env.js';

// Session shape expected by this handler
interface OAuthSession {
  oauthState?: string;
  pkceVerifier?: string;
  accessToken?: string;
  idToken?: string;
  refreshToken?: string;
  expiresAt?: number;
  [key: string]: unknown;
}

export async function oauthCallback(req: Request, res: Response) {
  const session = req.session as unknown as OAuthSession;
  const { code, state } = req.query;

  // Constant-time state validation to prevent CSRF
  const expected = Buffer.from(session.oauthState ?? '', 'utf8');
  const received = Buffer.from(String(state ?? ''), 'utf8');
  if (expected.length !== received.length || !timingSafeEqual(expected, received)) {
    return res.status(400).send('Invalid state parameter');
  }

  const tokenResponse = await fetch('https://auth.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: env('OAUTH_CLIENT_ID'),
      client_secret: env('OAUTH_CLIENT_SECRET'), // omit for public clients
      code: String(code),
      redirect_uri: 'https://app.example.com/callback',
      code_verifier: session.pkceVerifier ?? '',
    }),
  });

  if (!tokenResponse.ok) {
    // Typical causes: redirect_uri mismatch, reused code, expired code (~30-60s TTL)
    return res.status(400).send('Token exchange failed');
  }

  const tokens = await tokenResponse.json() as {
    access_token: string; id_token?: string; refresh_token?: string; expires_in: number;
  };

  session.accessToken = tokens.access_token;
  session.idToken = tokens.id_token;
  session.refreshToken = tokens.refresh_token;
  session.expiresAt = Date.now() + tokens.expires_in * 1000;
  delete session.pkceVerifier; // single-use: discard after a successful exchange

  res.redirect('/dashboard');
}
