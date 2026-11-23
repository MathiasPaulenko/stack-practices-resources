// hooks/useAuth.ts
import { useState, useEffect, useCallback } from 'react';
import { generatePKCE, generateRandomString } from '../auth/pkce';
import type { TokenResponse } from '../auth/pkce';
import { buildAuthorizationUrl } from '../auth/authorize';
import { exchangeCodeForToken, handleCallback } from '../auth/tokenExchange';
import { getAccessToken, storeTokens } from '../auth/storage';
import { refreshIfNeeded } from '../auth/silentRefresh';

const CONFIG = {
  authorizationEndpoint: 'https://auth.example.com/oauth/authorize',
  tokenEndpoint: 'https://auth.example.com/oauth/token',
  clientId: 'your-client-id',
  redirectUri: 'http://localhost:3000/callback',
  silentRedirectUri: 'http://localhost:3000/silent-callback.html',
  scope: 'openid profile email',
};

interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  error: Error | null;
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    const init = async () => {
      try {
        if (window.location.pathname === '/callback') {
          const tokens = await handleCallback(CONFIG);
          storeTokens(tokens);
          window.history.replaceState({}, '', '/');
        }
        setState({
          isAuthenticated: Boolean(getAccessToken()),
          isLoading: false,
          error: null,
        });
      } catch (err) {
        setState({ isAuthenticated: false, isLoading: false, error: err as Error });
      }
    };
    init();
  }, []);

  const login = useCallback(async () => {
    const { codeVerifier, codeChallenge } = await generatePKCE();
    sessionStorage.setItem('pkce_verifier', codeVerifier);
    const state = generateRandomString(16);
    sessionStorage.setItem('oauth_state', state);
    window.location.href = buildAuthorizationUrl({
      authorizationEndpoint: CONFIG.authorizationEndpoint,
      clientId: CONFIG.clientId,
      redirectUri: CONFIG.redirectUri,
      scope: CONFIG.scope,
      state,
      codeChallenge,
    });
  }, []);

  const logout = useCallback(() => {
    sessionStorage.clear();
    setState({ isAuthenticated: false, isLoading: false, error: null });
  }, []);

  // Auto-refresh before the token expires
  useEffect(() => {
    const interval = setInterval(() => {
      refreshIfNeeded(CONFIG).catch(() => logout());
    }, 60_000);
    return () => clearInterval(interval);
  }, [logout]);

  return { ...state, login, logout };
}
