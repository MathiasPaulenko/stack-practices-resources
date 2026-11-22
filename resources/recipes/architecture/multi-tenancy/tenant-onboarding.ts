class TenantOnboardingService {
  constructor(
    private db: Database,
    private cache: TenantCache,
    private config: TenantConfigService
  ) {}

  async onboard(tenantId: string, plan: string): Promise<void> {
    // Utility statements can't take $1 params, and identifiers can't be
    // parameterized at all — sanitize before interpolating
    const safeId = tenantId.replace(/[^a-z0-9_]/gi, '');
    if (!safeId) throw new Error('invalid tenant id');

    // 1. Create database schema or dedicated database
    if (plan === 'enterprise') {
      await this.db.query(`CREATE DATABASE tenant_${safeId}`);
      const password = generatePassword();
      await this.db.query(
        `CREATE USER tenant_${safeId} WITH PASSWORD '${password.replace(/'/g, "''")}'`
      );
    } else {
      await this.db.query(`CREATE SCHEMA IF NOT EXISTS tenant_${safeId}`);
    }

    // 2. Run migrations
    await this.runMigrations(safeId);

    // 3. Seed default data
    await this.seedDefaults(safeId);

    // 4. Configure feature flags
    await this.config.setFlags(safeId, getDefaultFlags(plan));

    // 5. Set resource quotas
    await this.config.setQuotas(safeId, getQuotas(plan));

    // 6. Warm cache
    await this.cache.set(safeId, 'status', 'active', 3600);
  }

  async offboard(tenantId: string): Promise<void> {
    const safeId = tenantId.replace(/[^a-z0-9_]/gi, '');

    // 1. Mark tenant as inactive
    await this.db.query('UPDATE tenants SET status = $1 WHERE id = $2', ['inactive', safeId]);

    // 2. Export tenant data (GDPR compliance)
    await this.exportTenantData(safeId);

    // 3. Drop schema or database
    await this.db.query(`DROP SCHEMA IF EXISTS tenant_${safeId} CASCADE`);

    // 4. Invalidate cache
    await this.cache.invalidate_tenant(safeId);

    // 5. Remove configuration
    await this.config.removeAll(safeId);
  }

  private async runMigrations(tenantId: string): Promise<void> {
    const migrations = await this.db.query('SELECT * FROM migrations ORDER BY version');
    for (const migration of migrations.rows) {
      await this.db.query(`SET search_path TO tenant_${tenantId}; ${migration.sql}`);
    }
  }

  private async seedDefaults(tenantId: string): Promise<void> {
    await this.db.query(
      `INSERT INTO tenant_${tenantId}.settings (key, value) VALUES ('timezone', 'UTC'), ('locale', 'en-US')`
    );
  }
}
