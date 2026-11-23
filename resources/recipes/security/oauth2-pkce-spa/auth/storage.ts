// auth/storage.ts — module-scoped, never on window or localStorage
import type { TokenResponse } from './pkce';

let accessToken: string | undefined;

export function storeTokens(tokens: TokenResponse) {
  accessToken = tokens.access_token;
  // Hand refresh tokens to a backend that stores them in an
  // httpOnly cookie — keeping them in JS storage invites XSS theft.
}

export function getAccessToken(): string | undefined {
  return accessToken;
}
