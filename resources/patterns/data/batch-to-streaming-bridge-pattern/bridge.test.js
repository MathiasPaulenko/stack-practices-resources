// Tests for bridge.js — batch-to-streaming bridge companion.

const { test } = require("node:test");
const assert = require("node:assert/strict");
const {
  BatchProducer,
  StreamingProducer,
  PartitionedLake,
  SpeedLayer,
  ServingLayer,
  UnifiedConsumer,
} = require("./bridge.js");

const WHEN = new Date("2026-08-19T14:00:00Z");

const row = (over = {}) => ({
  id: 1,
  email: "  ANA@Shop.com ",
  status: "active",
  created_at: WHEN,
  ...over,
});

const event = (over = {}) => ({
  after: {
    id: 1,
    email: "ana@shop.com",
    status: "banned",
    created_at: WHEN,
    ...over,
  },
});

test("shared schema normalizes both paths", () => {
  const b = BatchProducer.produce(row());
  const s = StreamingProducer.produce(event());
  assert.equal(b.email, "ana@shop.com");
  assert.equal(s.email, "ana@shop.com");
  assert.equal(b.source, "batch");
  assert.equal(s.source, "streaming");
  assert.equal(s.is_active, false); // derived from status
});

test("schema rejects invalid status", () => {
  assert.throws(() => BatchProducer.produce(row({ status: "ghost" })));
});

test("partition path includes hour", () => {
  const lake = new PartitionedLake();
  const key = lake.write(BatchProducer.produce(row()), WHEN);
  assert.equal(key, "customers/year=2026/month=08/day=19/hour=14");
});

test("serving layer prefers streaming over batch", () => {
  const lake = new PartitionedLake();
  lake.write(BatchProducer.produce(row()), WHEN);
  lake.write(StreamingProducer.produce(event()), WHEN);
  const winners = ServingLayer.latest(lake.readAll());
  assert.equal(winners.length, 1);
  assert.equal(winners[0].source, "streaming");
});

test("serving layer keeps batch when no streaming", () => {
  const lake = new PartitionedLake();
  lake.write(BatchProducer.produce(row({ id: 2, email: "bob@shop.com" })), WHEN);
  const winners = ServingLayer.latest(lake.readAll());
  assert.deepEqual(winners.map((r) => r.id), [2]);
});

test("unified view merges streaming over batch selectively", () => {
  const lake = new PartitionedLake();
  const speed = new SpeedLayer();
  lake.write(BatchProducer.produce(row({ email: "old@shop.com" })), WHEN);
  speed.put(StreamingProducer.produce(event({ email: "new@shop.com" })));

  const view = new UnifiedConsumer(lake, speed).getUnifiedView(1);
  assert.equal(view.email, "new@shop.com");
  assert.equal(view.status, "banned");
  assert.equal(view.source, "merged");
});

test("unified view returns null for unknown customer", () => {
  const consumer = new UnifiedConsumer(new PartitionedLake(), new SpeedLayer());
  assert.equal(consumer.getUnifiedView(999), null);
});
