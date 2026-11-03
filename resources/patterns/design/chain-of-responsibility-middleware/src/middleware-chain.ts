// Chain of Responsibility — middleware pipeline (TypeScript)
// Compile: tsc middleware-chain.ts && node middleware-chain.js
// Or run directly: npx tsx middleware-chain.ts

interface RequestContext {
  headers: Record<string, string>;
  body: unknown;
  path: string;
  method: string;
  user?: { id: string; roles: string[] };
}

type NextFunction = () => void;

abstract class MiddlewareHandler {
  protected next: MiddlewareHandler | null = null;

  setNext(handler: MiddlewareHandler): MiddlewareHandler {
    this.next = handler;
    return handler;
  }

  handle(req: RequestContext, next: NextFunction): void {
    if (this.canHandle(req)) {
      this.process(req, () => {
        if (this.next) {
          this.next.handle(req, next);
        } else {
          next();
        }
      });
    } else if (this.next) {
      this.next.handle(req, next);
    } else {
      next();
    }
  }

  protected abstract canHandle(req: RequestContext): boolean;
  protected abstract process(req: RequestContext, next: NextFunction): void;
}

class AuthMiddleware extends MiddlewareHandler {
  protected canHandle(): boolean {
    return true;
  }

  protected process(req: RequestContext, next: NextFunction): void {
    const token = req.headers['authorization']?.replace('Bearer ', '');
    if (!token) {
      throw new Error('401 Unauthorized');
    }
    // Demo token check: real code verifies signature and expiry.
    req.user = { id: 'user123', roles: ['user'] };
    console.log('  auth        -> user', req.user.id);
    next();
  }
}

class RateLimitMiddleware extends MiddlewareHandler {
  private requests = new Map<string, number[]>();
  private readonly windowMs = 60_000;
  private readonly maxRequests = 100;

  protected canHandle(): boolean {
    return true;
  }

  protected process(req: RequestContext, next: NextFunction): void {
    const clientId = req.headers['x-client-id'] || req.user?.id || 'anonymous';
    const now = Date.now();
    const recent = (this.requests.get(clientId) || []).filter(
      (t) => now - t < this.windowMs,
    );
    if (recent.length >= this.maxRequests) {
      throw new Error('429 Rate limit exceeded');
    }
    recent.push(now);
    this.requests.set(clientId, recent);
    console.log(`  rate limit  -> ${recent.length}/${this.maxRequests} for ${clientId}`);
    next();
  }
}

class ValidationMiddleware extends MiddlewareHandler {
  protected canHandle(req: RequestContext): boolean {
    return req.method === 'POST' || req.method === 'PUT';
  }

  protected process(req: RequestContext, next: NextFunction): void {
    if (!req.body || typeof req.body !== 'object') {
      throw new Error('400 Invalid request body');
    }
    console.log('  validation  -> body ok');
    next();
  }
}

class LoggingMiddleware extends MiddlewareHandler {
  protected canHandle(): boolean {
    return true;
  }

  protected process(req: RequestContext, next: NextFunction): void {
    console.log(`  logging     -> ${new Date().toISOString()} ${req.method} ${req.path}`);
    next();
  }
}

// --- Demo -------------------------------------------------------------------

const auth = new AuthMiddleware();
const rateLimit = new RateLimitMiddleware();
const validation = new ValidationMiddleware();
const logging = new LoggingMiddleware();

auth.setNext(rateLimit).setNext(validation).setNext(logging);

function handleRequest(req: RequestContext): void {
  try {
    auth.handle(req, () => console.log(`  endpoint    -> 200 OK for ${req.path}`));
  } catch (err) {
    console.log('  chain error ->', (err as Error).message);
  }
}

console.log('Request 1: authenticated POST (passes every link)');
handleRequest({
  headers: { authorization: 'Bearer demo-token', 'x-client-id': 'cli-1' },
  body: { name: 'order' },
  path: '/orders',
  method: 'POST',
});

console.log('\nRequest 2: missing token (auth short-circuits)');
handleRequest({
  headers: {},
  body: { name: 'order' },
  path: '/orders',
  method: 'POST',
});

console.log('\nRequest 3: GET skips validation but crosses auth/rate-limit/logging');
handleRequest({
  headers: { authorization: 'Bearer demo-token' },
  path: '/orders',
  method: 'GET',
});
