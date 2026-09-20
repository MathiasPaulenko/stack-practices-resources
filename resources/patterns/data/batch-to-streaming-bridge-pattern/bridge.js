/**
 * Batch-to-Streaming Bridge — a shared lake for both pipelines.
 *
 * Simulates the Lambda-architecture bridge without infrastructure:
 * two producers (batch + streaming) write normalized records into a
 * partitioned "lake", a speed layer holds the freshest state per key,
 * and a serving layer deduplicates by id preferring streaming.
 *
 * Run the demo:   node bridge.js
 * Run the tests:  node --test bridge.test.js
 */

const VALID_STATUSES = new Set(["active", "inactive", "banned", "suspended"]);

function makeRecord({ id, email, status, is_active, created_at, source }) {
  if (!VALID_STATUSES.has(status)) {
    throw new Error(`invalid status: ${status}`);
  }
  if (source !== "batch" && source !== "streaming") {
    throw new Error(`invalid source: ${source}`);
  }
  return {
    id,
    email: email.toLowerCase().trim(),
    status,
    is_active,
    created_at,
    source,
    ingested_at: new Date(),
  };
}

// Normalizes a raw DB row into the shared record.
const BatchProducer = {
  produce: (row) =>
    makeRecord({
      id: row.id,
      email: row.email,
      status: row.status,
      is_active: row.status === "active",
      created_at: row.created_at,
      source: "batch",
    }),
};

// Normalizes a CDC envelope ('after' payload) into the shared record.
const StreamingProducer = {
  produce: (event) => {
    const after = event.after;
    return makeRecord({
      id: after.id,
      email: after.email,
      status: after.status,
      is_active: after.status === "active",
      created_at: after.created_at,
      source: "streaming",
    });
  },
};

// Stand-in for the S3 lake: files keyed by partition path.
// Both writers must produce the same layout, hour included.
class PartitionedLake {
  constructor(table = "customers") {
    this.table = table;
    this.files = new Map();
  }

  static partitionKey(table, when) {
    const p = (n) => String(n).padStart(2, "0");
    return (
      `${table}/year=${when.getUTCFullYear()}` +
      `/month=${p(when.getUTCMonth() + 1)}` +
      `/day=${p(when.getUTCDate())}/hour=${p(when.getUTCHours())}`
    );
  }

  write(record, when = new Date()) {
    const key = PartitionedLake.partitionKey(this.table, when);
    if (!this.files.has(key)) this.files.set(key, []);
    this.files.get(key).push(record);
    return key;
  }

  readAll() {
    return [...this.files.values()].flat();
  }
}

// Redis stand-in: latest streaming state per key.
class SpeedLayer {
  #state = new Map();

  put(record) {
    this.#state.set(record.id, {
      id: record.id,
      email: record.email,
      status: record.status,
      is_active: record.is_active,
    });
  }

  get(customerId) {
    return this.#state.get(customerId) ?? null;
  }
}

// Trino stand-in: ROW_NUMBER() dedup preferring streaming, then freshest.
class ServingLayer {
  static latest(records) {
    const rank = { streaming: 0, batch: 1 };
    const best = new Map();
    for (const r of records) {
      const cur = best.get(r.id);
      if (
        !cur ||
        rank[r.source] < rank[cur.source] ||
        (rank[r.source] === rank[cur.source] &&
          r.ingested_at > cur.ingested_at)
      ) {
        best.set(r.id, r);
      }
    }
    return [...best.values()];
  }
}

// History from the serving layer + fresh state from the speed layer.
class UnifiedConsumer {
  constructor(lake, speed) {
    this.lake = lake;
    this.speed = speed;
  }

  getUnifiedView(customerId) {
    const historical = ServingLayer.latest(this.lake.readAll()).find(
      (r) => r.id === customerId
    );
    const result = historical ? { ...historical } : {};

    const latest = this.speed.get(customerId);
    if (latest) {
      // Streaming overrides only the fields it actually carries
      for (const f of ["email", "status", "is_active"]) {
        if (f in latest) result[f] = latest[f];
      }
      result.source = "merged";
    }

    return Object.keys(result).length ? result : null;
  }
}

function demo() {
  const lake = new PartitionedLake();
  const speed = new SpeedLayer();
  const when = new Date("2026-08-19T14:00:00Z");

  lake.write(
    BatchProducer.produce({
      id: 1,
      email: "  ANA@Shop.com ",
      status: "active",
      created_at: when,
    }),
    when
  );

  const event = {
    after: {
      id: 1,
      email: "ana@shop.com",
      status: "banned",
      created_at: when,
    },
  };
  const rec = StreamingProducer.produce(event);
  lake.write(rec, when);
  speed.put(rec);

  console.log("partitions:", [...lake.files.keys()]);
  console.log(
    "serving dedup:",
    ServingLayer.latest(lake.readAll()).map((r) => r.source)
  );
  console.log("unified view:", new UnifiedConsumer(lake, speed).getUnifiedView(1));
}

if (require.main === module) {
  demo();
}

module.exports = {
  BatchProducer,
  StreamingProducer,
  PartitionedLake,
  SpeedLayer,
  ServingLayer,
  UnifiedConsumer,
};
