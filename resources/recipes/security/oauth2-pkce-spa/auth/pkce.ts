// auth/pkce.ts — runs in the browser via the Web Crypto API
export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  id_token?: string;
  expires_in: number;
}

export function generateRandomString(length: number): string {
  const bytes = crypto.getRandomValues(new Uint8Array(length));
  return base64URLEncode(bytes);
}

export async function generatePKCE() {
  const codeVerifier = generateRandomString(32);
  const digest = await crypto.subtle.digest(
    'SHA-256',
    new TextEncoder().encode(codeVerifier)
  );
  const codeChallenge = base64URLEncode(new Uint8Array(digest));
  return { codeVerifier, codeChallenge };
}

export function base64URLEncode(buffer: Uint8Array): string {
  return btoa(String.fromCharCode(...buffer))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}
