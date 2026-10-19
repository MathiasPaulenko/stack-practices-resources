import { GatewayRequest, GatewayResponse, Middleware, Upstream } from './types';

// Composes middleware around the router: earlier entries run first.
// Order matters — auth before rate limit before cache, like the guide's pipeline diagram.
export function createGateway(middlewares: Middleware[], upstream: Upstream): Upstream {
  return middlewares.reduceRight<Upstream>(
    (next, mw) => (req) => mw(req, () => next(req)),
    upstream
  );
}

export async function dispatch(gateway: Upstream, req: GatewayRequest): Promise<GatewayResponse> {
  return gateway(req);
}
