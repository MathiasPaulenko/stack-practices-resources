// auth/oidc.ts — Validate OIDC ID token
import jwt from 'jsonwebtoken';
import { getKey } from './jwt.js';
import { env } from './env.js';

export interface OidcPayload {
  sub: string;
  iss: string;
  aud: string | string[];
  exp: number;
  iat: number;
  nonce?: string;
  email?: string;
  name?: string;
}

export function verifyIdToken(idToken: string, expectedNonce: string): Promise<OidcPayload> {
  return new Promise((resolve, reject) => {
    jwt.verify(idToken, getKey, {
      algorithms: ['RS256'],
      audience: env('OAUTH_CLIENT_ID'), // aud must be your client_id
      issuer: 'https://auth.example.com/',
    }, (err, decoded) => {
      if (err) return reject(err);

      const payload = decoded as OidcPayload;

      // Verify nonce to prevent replay attacks
      if (payload.nonce !== expectedNonce) {
        return reject(new Error('Nonce mismatch — possible replay attack'));
      }

      // Verify required OIDC claims (OIDC Core §2)
      if (!payload.sub) return reject(new Error('Missing sub claim'));
      if (!payload.iss) return reject(new Error('Missing iss claim'));
      if (!payload.aud) return reject(new Error('Missing aud claim'));
      if (!payload.exp) return reject(new Error('Missing exp claim'));
      if (!payload.iat) return reject(new Error('Missing iat claim'));

      resolve(payload);
    });
  });
}
