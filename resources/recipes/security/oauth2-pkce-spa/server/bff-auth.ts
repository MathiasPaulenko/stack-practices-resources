// server/bff-auth.ts (Express backend — Node crypto is correct here)
import express from 'express';
import crypto from 'crypto';
import cookieParser from 'cookie-parser';

const base64URLEncode = (buffer: Buffer): string => buffer.toString('base64url');

const app = express();
app.use(cookieParser());

const TOKEN_ENDPOINT = 'https://auth.example.com/oauth/token';
const REVOCATION_ENDPOINT = 'https://auth.example.com/oauth/revoke';
const AUTHORIZATION_ENDPOINT = 'https://auth.example.com/oauth/authorize';
const REDIRECT_URI = 'https://app.example.com/auth/callback';
const CLIENT_ID = 'your-client-id';

app.get('/auth/login', (req, res) => {
  const verifier = base64URLEncode(crypto.randomBytes(32));
  const challenge = base64URLEncode(
    crypto.createHash('sha256').update(verifier).digest()
  );

  res.cookie('pkce_verifier', verifier, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 300_000, // 5 min
  });

  const state = base64URLEncode(crypto.randomBytes(16));
  res.cookie('oauth_state', state, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 300_000,
  });

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    scope: 'openid profile email',
    state,
    code_challenge: challenge,
    code_challenge_method: 'S256',
  });

  res.redirect(`${AUTHORIZATION_ENDPOINT}?${params}`);
});

app.get('/auth/callback', async (req, res) => {
  const { code, state } = req.query;
  const expectedState = req.cookies['oauth_state'];
  const codeVerifier = req.cookies['pkce_verifier'];

  if (!code || !codeVerifier || state !== expectedState) {
    return res.status(400).send('Invalid state or missing code');
  }

  const response = await fetch(TOKEN_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: CLIENT_ID,
      redirect_uri: REDIRECT_URI,
      code: code as string,
      code_verifier: codeVerifier,
    }),
  });

  const tokens = await response.json();

  // Store access token in httpOnly cookie
  res.cookie('access_token', tokens.access_token, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: tokens.expires_in * 1000,
  });

  // Store refresh token separately with stricter settings
  res.cookie('refresh_token', tokens.refresh_token, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
  });

  res.clearCookie('pkce_verifier');
  res.clearCookie('oauth_state');

  res.redirect('/');
});

app.get('/auth/logout', async (req, res) => {
  const refreshToken = req.cookies['refresh_token'];
  if (refreshToken) {
    // Revoke the token at the authorization server
    await fetch(REVOCATION_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        token: refreshToken,
        token_type_hint: 'refresh_token',
      }),
    });
  }
  res.clearCookie('access_token');
  res.clearCookie('refresh_token');
  res.redirect('/');
});

app.listen(3001, () => {
  console.log('BFF auth server running on port 3001');
});
