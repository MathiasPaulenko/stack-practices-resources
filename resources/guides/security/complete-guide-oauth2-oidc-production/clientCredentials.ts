// auth/clientCredentials.ts — Machine-to-machine authentication
import type { TokenResponse } from './refresh.js';

export async function getClientCredentialsToken(
  clientId: string,
  clientSecret: string,
  scope: string,
): Promise<TokenResponse> {
  const response = await fetch('https://auth.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: clientId,
      client_secret: clientSecret,
      scope,
    }),
  });

  if (!response.ok) throw new Error('Client credentials grant failed');
  return response.json() as Promise<TokenResponse>;
}
