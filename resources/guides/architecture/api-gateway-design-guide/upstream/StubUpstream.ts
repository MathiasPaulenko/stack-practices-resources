import { GatewayRequest, GatewayResponse } from '../pipeline/types';

// Test double for a backend service: lets a test script statuses and latencies.
export class StubUpstream {
  private queue: Array<{ status: number; body: unknown; delayMs?: number }> = [];

  enqueue(status: number, body: unknown, delayMs = 0) {
    this.queue.push({ status, body, delayMs });
  }

  handler = async (req: GatewayRequest): Promise<GatewayResponse> => {
    const next = this.queue.shift() ?? { status: 200, body: { path: req.path, echoed: true } };
    if (next.delayMs) await new Promise((r) => setTimeout(r, next.delayMs));
    return { status: next.status, headers: {}, body: next.body };
  };
}
