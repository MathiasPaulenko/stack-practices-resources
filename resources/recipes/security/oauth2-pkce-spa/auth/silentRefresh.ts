// auth/silentRefresh.ts
import { generatePKCE, generateRandomString } from './pkce';
import type { TokenResponse } from './pkce';
import { buildAuthorizationUrl } from './authorize';
import { exchangeCodeForToken } from './tokenExchange';
import { getAccessToken, storeTokens } from './storage';

export async function silentRefresh(config: {
  authorizationEndpoint: string;
  tokenEndpoint: string;
  clientId: string;
  silentRedirectUri: string; // e.g. http://localhost:3000/silent-callback.html
  scope: string;
}): Promise<TokenResponse> {
  const { codeVerifier, codeChallenge } = await generatePKCE();
  const state = generateRandomString(16);

  return new Promise((resolve, reject) => {
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src =
      buildAuthorizationUrl({
        authorizationEndpoint: config.authorizationEndpoint,
        clientId: config.clientId,
        redirectUri: config.silentRedirectUri,
        scope: config.scope,
        state,
        codeChallenge,
      }) + '&prompt=none';

    const cleanup = () => {
      clearTimeout(timeout);
      window.removeEventListener('message', messageHandler);
      iframe.remove();
    };

    const messageHandler = async (event: MessageEvent) => {
      // The message comes from our own silent-callback page
      if (event.origin !== window.location.origin) return;
      const data = event.data;
      if (data?.type !== 'oauth-silent' || data.state !== state) return;

      cleanup();
      if (data.error || !data.code) {
        reject(new Error(data.error || 'No authorization code'));
        return;
      }
      try {
        const tokens = await exchangeCodeForToken({
          tokenEndpoint: config.tokenEndpoint,
          clientId: config.clientId,
          redirectUri: config.silentRedirectUri,
          code: data.code,
          codeVerifier,
        });
        resolve(tokens);
      } catch (err) {
        reject(err);
      }
    };

    const timeout = setTimeout(() => {
      cleanup();
      reject(new Error('Silent refresh timed out'));
    }, 10_000);

    window.addEventListener('message', messageHandler);
    document.body.appendChild(iframe);
  });
}

// Usage: call before the access token expires
export async function refreshIfNeeded(config: {
  authorizationEndpoint: string;
  tokenEndpoint: string;
  clientId: string;
  silentRedirectUri: string;
  scope: string;
}) {
  const token = getAccessToken();
  if (!token || isTokenExpired(token)) {
    try {
      const tokens = await silentRefresh(config);
      storeTokens(tokens);
    } catch {
      // Provider session is gone — fall back to interactive login
      window.location.href = '/login';
    }
  }
}

export function isTokenExpired(token: string): boolean {
  const payload = JSON.parse(atob(token.split('.')[1]));
  return Date.now() >= payload.exp * 1000 - 30_000; // 30s buffer
}
