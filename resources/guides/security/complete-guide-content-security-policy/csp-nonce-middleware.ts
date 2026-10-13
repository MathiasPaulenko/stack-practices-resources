import crypto from 'node:crypto';
import type { NextFunction, Request, Response } from 'express';

/**
 * Generates a cryptographic nonce per request and sets the CSP header.
 * The nonce is stored on res.locals.nonce so templates can stamp it on
 * <script> and <style> tags.
 *
 * Rules that make nonces safe:
 * 1. Use a CSPRNG (crypto.randomBytes), never a timestamp or counter.
 * 2. One nonce per response — never reuse across requests or users.
 * 3. Do not cache nonced HTML as shared output, or vary the nonce with it.
 */
export function cspNonceMiddleware(req: Request, res: Response, next: NextFunction) {
  const nonce = crypto.randomBytes(16).toString('base64');

  res.locals.nonce = nonce;

  res.setHeader('Content-Security-Policy', [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'`,
    `style-src 'self' 'nonce-${nonce}'`,
    `img-src 'self' data: https:`,
    `font-src 'self'`,
    `connect-src 'self'`,
    `frame-ancestors 'none'`,
    `base-uri 'none'`,
    `form-action 'self'`,
    `object-src 'none'`,
    `upgrade-insecure-requests`,
  ].join('; '));

  next();
}

/**
 * Same policy sent as Report-Only first — deploy this variant during the
 * discovery phase, collect violations, fix them, then switch to the
 * enforcing middleware above.
 */
export function cspReportOnlyMiddleware(req: Request, res: Response, next: NextFunction) {
  const nonce = crypto.randomBytes(16).toString('base64');

  res.locals.nonce = nonce;

  res.setHeader('Content-Security-Policy-Report-Only', [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'`,
    `style-src 'self' 'nonce-${nonce}'`,
    `img-src 'self' data: https:`,
    `font-src 'self'`,
    `connect-src 'self'`,
    `frame-ancestors 'none'`,
    `base-uri 'none'`,
    `form-action 'self'`,
    `report-uri /api/csp-reports`,
    `report-to csp-endpoint`,
  ].join('; '));

  next();
}
