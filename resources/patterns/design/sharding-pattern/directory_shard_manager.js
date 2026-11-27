// Directory-based sharding: an explicit lookup table maps each entity ID
// to the shard that owns it. Adds one lookup hop in exchange for full
// control over placement — ideal for geographic sharding and live migration.

class DirectoryShardManager {
    constructor() {
        // Lookup table mapping entity IDs to shard assignments
        this.directory = new Map();
        this.shards = new Map();
    }

    registerShard(shardId, connection) {
        this.shards.set(shardId, connection);
    }

    assignToShard(entityId, shardId) {
        this.directory.set(entityId, shardId);
    }

    getShardForEntity(entityId) {
        const shardId = this.directory.get(entityId);
        if (!shardId) throw new Error(`No shard assigned for ${entityId}`);
        return this.shards.get(shardId);
    }

    async queryEntity(entityId, query, params) {
        const shard = this.getShardForEntity(entityId);
        return await shard.query(query, params);
    }

    // Migration: move an entity from one shard to another
    async migrateEntity(entityId, fromShardId, toShardId) {
        const fromShard = this.shards.get(fromShardId);
        const toShard = this.shards.get(toShardId);

        // 1. Read from source
        const data = await fromShard.query(
            'SELECT * FROM entities WHERE id = ?', [entityId]
        );

        // 2. Write to destination
        await toShard.query('INSERT INTO entities VALUES (?, ?, ?)', [
            data.id, data.name, data.metadata
        ]);

        // 3. Update directory
        this.directory.set(entityId, toShardId);

        // 4. Delete from source (after verification)
        await fromShard.query('DELETE FROM entities WHERE id = ?', [entityId]);
    }
}

// Usage with geographic sharding
const manager = new DirectoryShardManager();

manager.registerShard('us-east', usEastPool);
manager.registerShard('eu-west', euWestPool);
manager.registerShard('ap-south', apSouthPool);

// Assign users to shards based on location
manager.assignToShard('user-1001', 'us-east');
manager.assignToShard('user-1002', 'eu-west');
manager.assignToShard('user-1003', 'ap-south');

// Queries route to the correct shard automatically
const result = await manager.queryEntity('user-1001',
    'SELECT * FROM users WHERE id = ?', ['user-1001']
);
