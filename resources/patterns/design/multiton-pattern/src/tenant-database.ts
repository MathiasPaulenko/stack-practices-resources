import { Pool } from "pg";

interface DBConfig {
  host: string;
  port: number;
}

// Multiton: singleton with key, one instance per key
class TenantDatabase {
  private static instances = new Map<string, TenantDatabase>();
  private pool: Pool;

  private constructor(private tenantId: string, config: DBConfig) {
    this.pool = new Pool({
      host: config.host,
      port: config.port,
      database: `tenant_${tenantId}`,
      max: 10,
    });
  }

  static getInstance(tenantId: string, config?: DBConfig): TenantDatabase {
    if (!this.instances.has(tenantId)) {
      if (!config) throw new Error(`Config required for new tenant: ${tenantId}`);
      this.instances.set(tenantId, new TenantDatabase(tenantId, config));
    }
    return this.instances.get(tenantId)!;
  }

  async query(sql: string, params: unknown[]) {
    return this.pool.query(sql, params);
  }

  static async closeAll(): Promise<void> {
    for (const instance of this.instances.values()) {
      await instance.pool.end();
    }
    this.instances.clear();
  }

  static getActiveTenants(): string[] {
    return [...this.instances.keys()];
  }
}

// Usage: one DB connection pool per tenant
const tenantA = TenantDatabase.getInstance("tenant-a", { host: "localhost", port: 5432 });
const tenantB = TenantDatabase.getInstance("tenant-b", { host: "localhost", port: 5432 });
const tenantA2 = TenantDatabase.getInstance("tenant-a"); // same instance

console.log(tenantA === tenantA2); // true
console.log(tenantA === tenantB);  // false
console.log(TenantDatabase.getActiveTenants()); // ["tenant-a", "tenant-b"]
