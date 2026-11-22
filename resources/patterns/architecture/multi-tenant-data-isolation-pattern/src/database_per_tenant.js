const { Pool } = require("pg");

const tenantPools = new Map();

function getTenantPool(tenantId) {
    if (!tenantPools.has(tenantId)) {
        const pool = new Pool({
            host: "localhost",
            port: 5432,
            user: "saas_app",
            password: process.env.DB_PASSWORD,
            database: `tenant_${tenantId}`,
            max: 10,
        });
        tenantPools.set(tenantId, pool);
    }
    return tenantPools.get(tenantId);
}

async function getDocuments(tenantId) {
    const pool = getTenantPool(tenantId);
    const result = await pool.query(
        "SELECT id, title, content FROM documents ORDER BY id"
    );
    return result.rows;
}

async function createDocument(tenantId, title, content) {
    const pool = getTenantPool(tenantId);
    const result = await pool.query(
        "INSERT INTO documents (title, content) VALUES ($1, $2) RETURNING id",
        [title, content]
    );
    return result.rows[0];
}

// Usage — in a real service, close pools on shutdown and evict
// pools for tenants deleted or migrated elsewhere.
async function main() {
    const acmeDocs = await getDocuments("acme");
    console.log("Acme docs:", acmeDocs.length);

    const doc = await createDocument("globex", "Q3 Report", "Confidential");
    console.log("Created doc:", doc.id);
}

main().catch(console.error);
