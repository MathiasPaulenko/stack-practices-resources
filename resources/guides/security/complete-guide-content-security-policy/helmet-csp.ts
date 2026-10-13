import helmet from 'helmet';

/**
 * Helmet builds the CSP header from a directives object.
 * Directive functions receive (req, res) so the per-request nonce
 * can be read from res.locals.
 *
 * The empty array for upgradeInsecureRequests is intentional — it is
 * how helmet emits a valueless directive.
 */
export const helmetCsp = helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: [
      "'self'",
      (req, res) => `'nonce-${(res as { locals: { nonce?: string } }).locals.nonce}'`,
      "'strict-dynamic'",
    ],
    styleSrc: [
      "'self'",
      (req, res) => `'nonce-${(res as { locals: { nonce?: string } }).locals.nonce}'`,
    ],
    imgSrc: ["'self'", 'data:', 'https:'],
    fontSrc: ["'self'", 'https://cdn.example.com'],
    connectSrc: ["'self'", 'https://api.example.com', 'wss://ws.example.com'],
    frameAncestors: ["'none'"],
    baseUri: ["'none'"],
    formAction: ["'self'"],
    objectSrc: ["'none'"],
    upgradeInsecureRequests: [],
  },
});
