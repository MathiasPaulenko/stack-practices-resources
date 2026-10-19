export interface GatewayRequest {
  method: string;
  path: string;
  query: Record<string, string>;
  headers: Record<string, string>;
  body?: unknown;
}

export interface GatewayResponse {
  status: number;
  headers: Record<string, string>;
  body: unknown;
}

export type Upstream = (req: GatewayRequest) => Promise<GatewayResponse>;
export type NextFunction = () => Promise<GatewayResponse>;
export type Middleware = (req: GatewayRequest, next: NextFunction) => Promise<GatewayResponse>;

export function json(status: number, body: unknown, headers: Record<string, string> = {}): GatewayResponse {
  return { status, headers: { 'content-type': 'application/json', ...headers }, body };
}
