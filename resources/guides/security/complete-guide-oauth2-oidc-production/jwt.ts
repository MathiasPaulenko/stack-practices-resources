// auth/jwt.ts — Validate JWT access tokens against JWKS
import jwt from 'jsonwebtoken';
import jwksClient from 'jwks-rsa';
import type { NextFunction, Request, Response } from 'express';

export interface JwtPayload {
  sub: string;
  scope?: string;
  email?: string;
  iss?: string;
  aud?: string | string[];
  exp?: number;
  iat?: number;
}

export const client = jwksClient({
  jwksUri: 'https://auth.example.com/.well-known/jwks.json',
  cache: true,
  cacheMaxAge: 600000, // 10 min — short enough for key rotation, long enough to avoid hammering the JWKS endpoint
});

export function getKey(header: jwt.JwtHeader, callback: jwt.SigningKeyCallback) {
  client.getSigningKey(header.kid, (err, key) => {
    if (err) return callback(err);
    callback(null, key.getPublicKey());
  });
}

export function verifyAccessToken(token: string): Promise<JwtPayload> {
  return new Promise((resolve, reject) => {
    jwt.verify(token, getKey, {
      algorithms: ['RS256'],
      audience: 'my-api',
      issuer: 'https://auth.example.com/',
      clockTolerance: 30, // tolerate up to 30s of client clock skew on exp/nbf
    }, (err, decoded) => {
      if (err) return reject(err);
      resolve(decoded as JwtPayload);
    });
  });
}

// Middleware — authenticate every request, then inject identity
export async function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing bearer token' });
  }

  const token = authHeader.split(' ')[1];

  try {
    const payload = await verifyAccessToken(token);

    // jwt.verify already enforced signature, exp, nbf, iss, aud
    (req as unknown as { user: unknown }).user = {
      id: payload.sub,
      scopes: payload.scope?.split(' ') || [],
      email: payload.email,
    };

    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
