// auth/refresh.ts — Refresh access tokens (with rotation)
import type { NextFunction, Request, Response } from 'express';
import { env } from './env.js';

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  id_token?: string;
  scope?: string;
}

export async function refreshAccessToken(refreshToken: string): Promise<TokenResponse> {
  const response = await fetch('https://auth.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      client_id: env('OAUTH_CLIENT_ID'),
      client_secret: env('OAUTH_CLIENT_SECRET'),
      refresh_token: refreshToken,
    }),
  });

  if (!response.ok) {
    const error = await response.json() as { error?: string; error_description?: string };
    // invalid_grant here usually means the refresh token was rotated or revoked — don't retry in a loop
    throw new Error(`Refresh failed: ${error.error_description ?? error.error}`);
  }

  return response.
