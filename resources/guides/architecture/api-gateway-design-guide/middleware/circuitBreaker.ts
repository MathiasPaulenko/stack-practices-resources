import { json, Middleware } from '../pipeline/types';

type State = 'closed' | 'open' | 'half-open';

interface CircuitBreakerConfig {
  failureThreshold: number; // consecutive failures before opening
  windowMs: number;         // how long the breaker stays open
  halfOpenProbes: number;   // probe requests allowed while half-open
  now?: () => number;
}

export function circuitBreakerMiddleware(config: CircuitBreakerConfig): Middleware {
  const now = config.now ?? (() => Date.now());
  let state: State = 'closed';
  let failures = 0;
  let openedAt = 0;
  let probesInFlight = 0;

  return async (_req, next) => {
    if (state === 'open') {
      if (now() - openedAt < config.windowMs) {
        return json(503, { error: 'Upstream unavailable', circuit: 'open' }, { 'retry-after': '30' });
      }
      state = 'half-open';
      probesInFlight = 0;
    }

    if (state === 'half-open') {
      if (probesInFlight >= config.halfOpenProbes) {
        return json(503, { error: 'Upstream recovering', circuit: 'half-open' });
      }
      probesInFlight += 1;
    }

    try {
      const response = await next();
      if (response.status >= 500) throw new Error(`upstream ${response.status}`);

      failures = 0;
      if (state === 'half-open') state = 'closed';
      return response;
    } catch (error) {
      failures += 1;
      if (state === 'half-open' || failures >= config.failureThreshold) {
        state = 'open';
        openedAt = now();
      }
      throw error;
    } finally {
      if (state === 'half-open') probesInFlight -= 1;
    }
  };
}
