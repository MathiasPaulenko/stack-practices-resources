// cost-budget.js — per-identity cost budget backed by Redis
// Rate limiting by IP alone fails behind NAT/CGNAT and resets per instance.
// A shared Redis budget counts query cost per user/API key across all pods.
import { GraphQLError } from "graphql";

// In production create one ioredis/redis client and inject it.
export async function checkCostBudget(clientId, queryCost, redis, { limit = 5000, windowMs = 60_000 } = {}) {
  const key = `cost-budget:${clientId}`;
  const current = await redis.incrby(key, queryCost);
  if (current === queryCost) {
    await redis.pexpire(key, windowMs); // first write in this window → set TTL
  }
  if (current > limit) {
    throw new GraphQLError("Cost budget exceeded", {
      extensions: { code: "RATE_LIMITED" },
    });
  }
  return current;
}

// Apollo Server 4 plugin that drains the budget after validation has
// produced a cost estimate (pair with @escape.tech/graphql-armor-cost-limit
// or your own complexity estimator).
export function costBudgetPlugin(redis, estimateCost) {
  return {
    async requestDidStart() {
      return {
        async didResolveOperation(requestContext) {
          const clientId = requestContext.contextValue.user?.id ?? requestContext.request.http?.headers.get("x-forwarded-for") ?? "anonymous";
          const queryCost = estimateCost(requestContext.document);
          await checkCostBudget(clientId, queryCost, redis);
        },
      };
    },
  };
}
