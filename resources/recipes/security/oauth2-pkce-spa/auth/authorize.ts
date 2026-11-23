// auth/authorize.ts
import { generatePKCE, generateRandomString } from './pkce';

export function buildAuthorizationUrl(params: {
  authorizationEndpoint: string;
  clientId: string;
  redirectUri: string;
  scope: string;
  state: string;
  codeChallenge: string;
}) {
  const url = new URL(params.authorizationEndpoint);
  url.searchParams.set('response_type', 'code');
  url.searchParams.set('client_id', params.clientId);
  url.searchParams.set('redirect_uri', params.redirectUri);
  url.searchParams.set('scope', params.scope);
  url.searchParams.set('state', params.state);
  url.searchParams.set('code_challenge', params.codeChallenge);
  url.searchParams.set('code_challenge_method', 'S256');
  return url.toString();
}

// Usage: call on "Sign in" click
export async function startLogin(config: {
  authorizationEndpoint: string;
  clientId: string;
  redirectUri: string;
  scope: string;
}) {
  const { codeVerifier, codeChallenge } = await generatePKCE();
  sessionStorage.setItem('pkce_verifier', codeVerifier);

  const state = generateRandomString(16);
  sessionStorage.setItem('oauth_state', state);

  window.location.href = buildAuthorizationUrl({
    authorizationEndpoint: config.authorizationEndpoint,
    clientId: config.clientId,
    redirectUri: config.redirectUri,
    scope: config.scope,
    state,
    codeChallenge,
  });
}
