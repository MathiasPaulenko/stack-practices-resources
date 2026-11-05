// router/RollbackManager.ts — Instant rollback to legacy
import type { FlagStore } from './feature_flags';

interface AlertingService {
  notify(alert: { severity: string; message: string; channel: string }): Promise<void>;
}

interface MetricsWindow {
  windowSeconds: number;
}

interface MetricsCollector {
  getErrorRate(flagName: string, window: MetricsWindow): Promise<number>;
  getP99Latency(flagName: string, window: MetricsWindow): Promise<number>;
}

class RollbackManager {
  constructor(
    private readonly flagStore: FlagStore,
    private readonly alerting: AlertingService,
  ) {}

  async rollback(flagName: string, reason: string): Promise<void> {
    await this.flagStore.update(flagName, {
      enabled: false,
      percentage: 0,
    });

    await this.alerting.notify({
      severity: 'critical',
      message: `Rolled back ${flagName}: ${reason}`,
      channel: '#migration-alerts',
    });
  }

  // Automatic rollback based on error rate.
  // Thresholds are decided before launch — 5% errors or 2s p99 are sane
  // defaults, tuned per endpoint.
  async monitor(flagName: string, metrics: MetricsCollector): Promise<void> {
    const window: MetricsWindow = { windowSeconds: 60 };
    const errorRate = await metrics.getErrorRate(flagName, window);
    const p99Latency = await metrics.getP99Latency(flagName, window);

    if (errorRate > 0.05) {
      await this.rollback(flagName, `Error rate ${errorRate} exceeded 5%`);
    } else if (p99Latency > 2000) {
      await this.rollback(flagName, `P99 latency ${p99Latency}ms exceeded 2000ms`);
    }
  }
}

export { RollbackManager };
export type { AlertingService, MetricsCollector, MetricsWindow };
