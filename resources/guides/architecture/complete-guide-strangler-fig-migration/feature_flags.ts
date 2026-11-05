// flags/FeatureFlagService.ts — Control migration rollout
interface Flag {
  name: string;
  enabled?: boolean;
  rolloutStrategy: 'percentage' | 'user-list' | 'environment' | 'boolean';
  percentage?: number;
  userIds?: string[];
  environments?: string[];
}

interface FlagStore {
  get(flagName: string): Promise<Flag | undefined>;
  update(flagName: string, patch: Partial<Flag>): Promise<void>;
}

interface FlagContext {
  userId?: string;
  environment?: string;
}

class FeatureFlagService {
  constructor(private readonly flagStore: FlagStore) {}

  async isEnabled(flagName: string, context: FlagContext): Promise<boolean> {
    const flag = await this.flagStore.get(flagName);
    if (!flag) return false;

    switch (flag.rolloutStrategy) {
      case 'percentage':
        return this.percentageRollout(flag, context);

      case 'user-list':
        // ?. guards: a flag configured for 'percentage' has no userIds —
        // evaluating the wrong field crashes the router mid-request.
        return flag.userIds?.includes(context.userId ?? '') ?? false;

      case 'environment':
        return flag.environments?.includes(context.environment ?? '') ?? false;

      case 'boolean':
        return flag.enabled ?? false;

      default:
        return false;
    }
  }

  private percentageRollout(flag: Flag, context: FlagContext): boolean {
    const hash = this.hashString(context.userId || flag.name);
    const bucket = hash % 100;
    return bucket < (flag.percentage ?? 0);
  }

  // Stable bucketing: the same user must land in the same bucket on every
  // request, or they see inconsistent behavior within a session.
  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }
}

// Migration rollout config
const migrationFlags: Record<string, Flag> = {
  'use-new-user-service': {
    name: 'use-new-user-service',
    enabled: true,
    rolloutStrategy: 'percentage',
    percentage: 5, // Start with 5% of users
  },
  'use-new-order-service': {
    name: 'use-new-order-service',
    enabled: true,
    rolloutStrategy: 'user-list',
    userIds: ['test-user-1', 'test-user-2'],
  },
  'use-new-billing-service': {
    name: 'use-new-billing-service',
    enabled: false,
    rolloutStrategy: 'boolean',
  },
};

export { FeatureFlagService, migrationFlags };
export type { Flag, FlagStore, FlagContext };
