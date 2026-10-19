import { createHmac, timingSafeEqual } from 'node:crypto';
import { json, Middleware } from '../pipeline/types';

interface AuthConfig {
  jwtSecret: string;
  publicPaths: string[]; // path prefixes that skip auth
}

interface JwtPayload {
  sub: string;
  roles: string[];
  scopes: string[];
  exp: number;
}

function decodeAndVerify(token: string, secret: string): JwtPayload {
  const [header, payload, signature] = token.split('.');
  if (!header || !payload || !signature) throw new Error('malformed');

  const expected = createHmac('sha256', secret)
    .update(`${header}.${payload}`)
    .digest();
  const provided = Buffer.from(signature, 'base64url');
  if (expected.length !== provided.length || !timingSafeEqual(expected, provided)) {
    throw new Error('invalid-signature');
  }

  const claims = JSON.parse(Buffer.from(payload, 'base64url').toString()) as JwtPayload;
  if (claims.exp * 1000 < Date.now()) throw new Error('expired');
  return claims;
}

// Rejects before doing any work: public-path and missing-token checks run before verify.
export function authMiddleware(config: AuthConfig): Middleware {
  return async (req, next) => {
    if (config.publicPaths.some((p) => req.path.startsWith(p))) {
      return next();
    }

    const token = req.headers['authorization']?.replace('Bearer ', '');
    if (!token) {
      return json(401, { error: 'Missing authorization header' });
    }

    try {
      const claims = decodeAndVerify(token, config.jwtSecret);

      // Inject identity for upstream services — they trust these headers
      req.headers['x-user-id'] = claims.sub;
      req.headers['x-user-roles'] = claims.roles.join(',');
      req.headers['x-user-scopes'] = claims.scopes.join(',');

      return next();
    } catch (error) {
      const code = error instanceof Error && error.message === 'expired' ? 'Token expired' : 'Invalid token';
      return json(401, { error: code });
    }
  };
}

export function signTestToken(claims: Omit<JwtPayload, 'exp'>, secret: string, ttlSeconds = 300): string {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  const payload = Buffer.from(
    JSON.stringify({ ...claims, exp: Math.floor(Date.now() / 1000) + ttlSeconds })
  ).toString('base64url');
  const signature = createHmac('sha256', secret).update(`${header}.${payload}`).digest('base64url');
  return `${header}.${payload}.${signature}`;
}
