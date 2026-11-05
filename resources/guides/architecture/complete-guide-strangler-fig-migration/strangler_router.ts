// router/StranglerRouter.ts — Route requests between legacy and new systems
interface HttpRequest {
  path: string;
  method: string;
  headers: Record<string, string | undefined>;
  body?: unknown;
}

interface HttpResponse {
  status: number;
  body: Record<string, unknown>;
  responseTime: number;
}

interface SystemAdapter {
  handle(request: HttpRequest): Promise<HttpResponse>;
}

interface RoutingRule {
  path?: RegExp;
  method?: string;
  flagName: string;
}

interface FlagContext {
  userId?: string;
  environment?: string;
}

interface FeatureFlagService {
  isEnabled(flagName: string, context: FlagContext): Promise<boolean>;
}

class StranglerRouter {
  constructor(
    private readonly legacySystem: SystemAdapter,
    private readonly newSystem: SystemAdapter,
    private readonly routingRules: RoutingRule[],
    private readonly featureFlags: FeatureFlagService,
  ) {}

  async route(request: HttpRequest): Promise<HttpResponse> {
    const rule = this.matchRule(request);

    if (!rule) {
      // No matching rule — route to legacy
      return this.legacySystem.handle(request);
    }

    // Check feature flag for gradual rollout — MUST await: isEnabled
    // returns Promise<boolean>, and an un-awaited Promise is always truthy,
    // which silently routes 100% of matching traffic to the new system.
    const useNewSystem = await this.featureFlags.isEnabled(
      rule.flagName,
      { userId: request.headers['x-user-id'] },
    );

    if (useNewSystem) {
      try {
        return await this.newSystem.handle(request);
      } catch (error) {
        // Fallback to legacy on new system failure — log every fallback,
        // silent fallback hides regressions during canary.
        console.error('New system failed, falling back to legacy:', error);
        return this.legacySystem.handle(request);
      }
    }

    return this.legacySystem.handle(request);
  }

  private matchRule(request: HttpRequest): RoutingRule | null {
    for (const rule of this.routingRules) {
      if (this.matches(request, rule)) {
        return rule;
      }
    }
    return null;
  }

  private matches(request: HttpRequest, rule: RoutingRule): boolean {
    if (rule.path && !request.path.match(rule.path)) return false;
    if (rule.method && request.method !== rule.method) return false;
    return true;
  }
}

export { StranglerRouter };
export type { HttpRequest, HttpResponse, SystemAdapter, RoutingRule };
