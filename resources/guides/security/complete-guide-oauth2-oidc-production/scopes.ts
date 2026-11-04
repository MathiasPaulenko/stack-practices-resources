// auth/scopes.ts — Check scopes for API endpoints
import type { NextFunction, Request, Response } from 'express';

interface ScopedRequest extends Request {
  user?: { id: string; scopes: string[]; email?: string };
}

export function requireScope(scope: string) {
  return (req: ScopedRequest, res: Response, next: NextFunction) => {
    if (!req.user?.scopes.includes(scope)) {
      // RFC 6750: insufficient_scope is a 403, not a 401
      return res.status(403).json({
        error: 'insufficient_scope',
        required: scope,
      });
    }
    next();
  };
}
