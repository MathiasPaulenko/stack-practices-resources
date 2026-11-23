// auth/tokenExchange.ts
import type { TokenResponse } from './pkce';

export async function exchangeCodeForToken(params: {
  tokenEndpoint: string;
  clientId: string;
  redirectUri: string;
  code: string;
  codeVerifier: string;
}) {
  const response = await fetch(params.tokenEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: params.clientId,
      redirect_uri: params.redirectUri,
      code: params.code,
      code_verifier: params.codeVerifier,
    }),
  });

  if (!response.ok) {
    throw new Error(`Token exchange failed: ${response.statusText}`);
  }

  return response.json() as Promise<TokenResponse>;
}

// In the callback handler (/callback route)
export async function handleCallback(config: {
  tokenEndpoint: string;
  clientId: string;
  redirectUri: string;
}): Promise<TokenResponse> {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  const state = urlParams.get('state');

  if (state !== sessionStorage.getItem('oauth_state')) {
    throw new Error('Invalid state parameter');
  }

  const codeVerifier = sessionStorage.getItem('pkce_verifier');
  if (!code || !codeVerifier) {
    throw new Error('Missing authorization code or PKCE verifier');
  }

  const tokens = await exchangeCodeForToken({
    tokenEndpoint: config.tokenEndpoint,
    clientId: config.clientId,
    redirectUri: config.redirectUri,
    code,
    codeVerifier,
  });

  sessionStorage.removeItem('pkce_verifier');
  sessionStorage.removeItem('oauth_state');
  return tokens;
}
