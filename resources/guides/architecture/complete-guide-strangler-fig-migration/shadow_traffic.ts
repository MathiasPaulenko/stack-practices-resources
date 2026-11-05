// router/ShadowTraffic.ts — Send traffic to both systems, compare results
import type { HttpRequest, HttpResponse, SystemAdapter } from './strangler_router';

interface ComparisonRecord {
  path: string;
  method: string;
  legacyStatus: number;
  newStatus: number | 'error';
  legacyTime: number;
  newTime: number | null;
  match: boolean;
}

interface ComparisonLogger {
  log(record: ComparisonRecord): void;
}

class ShadowTraffic {
  constructor(
    private readonly legacySystem: SystemAdapter,
    private readonly newSystem: SystemAdapter,
    private readonly comparisonLogger: ComparisonLogger,
  ) {}

  async route(request: HttpRequest): Promise<HttpResponse> {
    // Send to both systems in parallel
    const [legacyResponse, newResponse] = await Promise.allSettled([
      this.legacySystem.handle(request),
      this.newSystem.handle(request),
    ]);

    // Return legacy response to client
    if (legacyResponse.status === 'fulfilled') {
      this.comparisonLogger.log({
        path: request.path,
        method: request.method,
        legacyStatus: legacyResponse.value.status,
        newStatus: newResponse.status === 'fulfilled'
          ? newResponse.value.status
          : 'error',
        legacyTime: legacyResponse.value.responseTime,
        newTime: newResponse.status === 'fulfilled'
          ? newResponse.value.responseTime
          : null,
        match: this.responsesMatch(
          legacyResponse.value,
          newResponse.status === 'fulfilled' ? newResponse.value : null,
        ),
      });

      return legacyResponse.value;
    }

    throw new Error('Legacy system failed');
  }

  private responsesMatch(legacy: HttpResponse, newResp: HttpResponse | null): boolean {
    if (!newResp) return false;
    if (legacy.status !== newResp.status) return false;
    // Compare normalized key fields — full-body equality fails on
    // timestamps, generated IDs, and field ordering.
    const legacyKey = { id: legacy.body.id, total: legacy.body.total, status: legacy.body.status };
    const newKey = { id: newResp.body.id, total: newResp.body.total, status: newResp.body.status };
    return JSON.stringify(legacyKey) === JSON.stringify(newKey);
  }
}

export { ShadowTraffic };
