import { json, Upstream, GatewayRequest, GatewayResponse } from '../pipeline/types';

export interface Route {
  prefix: string;
  upstream: Upstream;
  stripPrefix?: boolean;
}

// Stateless prefix routing — any instance reaches the same decision.
// First match wins, so register more specific prefixes first.
export function createRouter(routes: Route[]): Upstream {
  return async (req: GatewayRequest): Promise<GatewayResponse> => {
    const route = routes.find((r) => req.path.startsWith(r.prefix));
    if (!route) {
      return json(404, { error: `No route for ${req.path}` });
    }
    const upstreamReq = route.stripPrefix
      ? { ...req, path: req.path.slice(route.prefix.length) || '/' }
      : req;
    return route.upstream(upstreamReq);
  };
}
