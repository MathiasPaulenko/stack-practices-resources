// Tests for ambassador.js — companion to the Ambassador pattern.

const { test } = require("node:test");
const assert = require("node:assert/strict");
const {
  ServiceAmbassador,
  MonitoringAmbassador,
  RemoteError,
  CircuitOpenError,
} = require("./ambassador.js");

// Controllable remote + fake clock + recorded sleeps.
function fake(outcomes) {
  const f = {
    calls: 0,
    sleeps: [],
    now: [0],
    remote: async () => {
      f.calls++;
      const outcome = outcomes.shift();
      if (outcome instanceof Error) throw outcome;
      return outcome;
    },
    sleep: (ms) => {
      f.sleeps.push(ms);
      return Promise.resolve();
    },
    clock: () => f.now[0],
  };
  f.ambassador = (kw = {}) =>
    new ServiceAmbassador(f.remote, {
      sleep: f.sleep,
      clock: f.clock,
      jitterMs: 0,
      ...kw,
    });
  return f;
}

test("succeeds after retries", async () => {
  const f = fake([new RemoteError("503"), new RemoteError("503"), { id: 1 }]);
  assert.deepEqual(await f.ambassador({ baseDelayMs: 1 }).call(), { id: 1 });
  assert.equal(f.calls, 3);
});

test("exponential backoff delays", async () => {
  const f = fake([new RemoteError("x"), new RemoteError("x"), new RemoteError("x"), new RemoteError("x")]);
  await assert.rejects(f.ambassador({ retryCount: 4, baseDelayMs: 1000 }).call());
  // 1s, 2s, 4s — doubling each attempt, not linear
  assert.deepEqual(f.sleeps, [1000, 2000, 4000]);
});

test("gives up after max retries", async () => {
  const f = fake(Array(5).fill(new RemoteError("x")));
  await assert.rejects(f.ambassador({ retryCount: 3, baseDelayMs: 1 }).call());
  assert.equal(f.calls, 3); // never more than retryCount
});

test("circuit opens and fails fast", async () => {
  const f = fake(Array(10).fill(new RemoteError("x")));
  const a = f.ambassador({ retryCount: 1, failureThreshold: 3, baseDelayMs: 0 });
  for (let i = 0; i < 3; i++) {
    await assert.rejects(a.call(), RemoteError);
  }
  assert.equal(a.state, "open");
  const before = f.calls;
  await assert.rejects(a.call(), CircuitOpenError);
  assert.equal(f.calls, before); // no remote hit — failed fast
});

test("half-open trial then closed", async () => {
  const f = fake([...Array(3).fill(new RemoteError("x")), { ok: true }]);
  const a = f.ambassador({ retryCount: 1, failureThreshold: 3, resetAfterMs: 30000 });
  for (let i = 0; i < 3; i++) {
    await assert.rejects(a.call());
  }
  assert.equal(a.state, "open");
  f.now[0] = 31000; // cool-down elapsed
  assert.deepEqual(await a.call(), { ok: true });
  assert.equal(a.state, "closed");
});

test("failed half-open reopens immediately", async () => {
  const f = fake(Array(4).fill(new RemoteError("x")));
  const a = f.ambassador({ retryCount: 1, failureThreshold: 3, resetAfterMs: 30000 });
  for (let i = 0; i < 3; i++) {
    await assert.rejects(a.call());
  }
  f.now[0] = 31000;
  await assert.rejects(a.call(), RemoteError);
  assert.equal(a.state, "open"); // trial failed -> re-opened
});

test("monitoring counts final outcomes, not attempts", async () => {
  const f = fake([new RemoteError("x"), { ok: true }]);
  const monitored = new MonitoringAmbassador(f.ambassador({ baseDelayMs: 0 }));
  assert.deepEqual(await monitored.call(), { ok: true });
  const m = monitored.metrics();
  assert.equal(m.requests, 1); // the monitor sees the result, not the retry
  assert.equal(m.errors, 0);
});

test("monitoring counts errors", async () => {
  const f = fake(Array(3).fill(new RemoteError("x")));
  const monitored = new MonitoringAmbassador(f.ambassador({ retryCount: 3, baseDelayMs: 0 }));
  await assert.rejects(monitored.call());
  assert.equal(monitored.metrics().errors, 1);
});
