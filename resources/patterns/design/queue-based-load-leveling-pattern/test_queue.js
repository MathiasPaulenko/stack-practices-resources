// Tests for the Queue-Based Load Leveling Pattern (JavaScript, in-memory)

const { Task, LoadLevelingQueue, TaskProducer } = require('./queue_producer');
const { TaskConsumer, routeTask } = require('./queue_consumer');

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    passed++;
    console.log(`PASS: ${message}`);
  } else {
    failed++;
    console.log(`FAIL: ${message}`);
  }
}

function makeTask(id = 't1', type = 'send-email', payload = null) {
  return new Task(id, type, payload || { to: 'a@b.com', body: 'hello world test email' });
}

// Test 1: Enqueue and dequeue
(function testEnqueueDequeue() {
  const q = new LoadLevelingQueue({ maxLength: 10 });
  const t = makeTask();
  assert(q.enqueue(t) === true, 'Enqueue returns true');
  const got = q.dequeue();
  assert(got !== null, 'Dequeue returns task');
  assert(got.id === 't1', 'Dequeued task has correct id');
})();

// Test 2: Depth limit rejects overflow
(function testDepthLimit() {
  const q = new LoadLevelingQueue({ maxLength: 3 });
  for (let i = 0; i < 3; i++) assert(q.enqueue(makeTask(`t${i}`)) === true, `Enqueue ${i} succeeds`);
  assert(q.enqueue(makeTask('overflow')) === false, 'Overflow enqueue returns false');
  assert(q.rejected === 1, 'Rejected count is 1');
  assert(q.depth === 3, 'Queue depth is 3');
})();

// Test 3: TTL expires to DLQ
(function testTtl() {
  const q = new LoadLevelingQueue({ maxLength: 10, messageTtl: 50 });
  q.enqueue(makeTask());
  setTimeout(() => {
    const result = q.dequeue();
    assert(result === null, 'TTL-expired task returns null on dequeue');
    assert(q.dlqDepth === 1, 'Expired task moved to DLQ');
  }, 100);
})();

// Test 4: Fail moves to DLQ after max retries
(function testFailToDlq() {
  const q = new LoadLevelingQueue({ maxLength: 10 });
  const t = makeTask();
  t.maxRetries = 2;
  q.enqueue(t);
  const got = q.dequeue();
  q.fail(got, 'error 1');
  const got2 = q.dequeue();
  q.fail(got2, 'error 2');
  assert(q.dlqDepth === 1, 'Task moved to DLQ after max retries');
})();

// Test 5: Fail requeues before max retries
(function testFailRequeue() {
  const q = new LoadLevelingQueue({ maxLength: 10 });
  const t = makeTask();
  t.maxRetries = 3;
  q.enqueue(t);
  const got = q.dequeue();
  q.fail(got, 'error 1');
  assert(q.depth === 1, 'Task requeued before max retries');
})();

// Test 6: Producer batch
(function testProducerBatch() {
  const q = new LoadLevelingQueue({ maxLength: 100 });
  const p = new TaskProducer(q);
  const tasks = [];
  for (let i = 0; i < 10; i++) tasks.push(makeTask(`batch-${i}`));
  const results = p.sendBatch(tasks);
  assert(results.every((r) => r === true), 'Batch enqueue all succeed');
  assert(q.depth === 10, 'Queue depth is 10 after batch');
})();

// Test 7: Consumer processes tasks
(function testConsumerProcesses() {
  const q = new LoadLevelingQueue({ maxLength: 100 });
  const processed = [];
  const customHandlers = { 'send-email': (data) => { processed.push(data.to); } };
  const c = new TaskConsumer(q, customHandlers, 1);
  for (let i = 0; i < 5; i++) q.enqueue(makeTask(`c-${i}`));
  c.start();
  setTimeout(() => {
    c.stop();
    assert(processed.length === 5, 'Consumer processed all 5 tasks');
    assert(c.processed === 5, 'Consumer processedCount is 5');
  }, 200);
})();

// Test 8: Consumer handles failures
(function testConsumerFailures() {
  const q = new LoadLevelingQueue({ maxLength: 100 });
  const failHandlers = { 'send-email': () => { throw new Error('boom'); } };
  const c = new TaskConsumer(q, failHandlers, 1);
  const t = makeTask('fail-me');
  t.maxRetries = 1;
  q.enqueue(t);
  c.start();
  setTimeout(() => {
    c.stop();
    assert(q.dlqDepth === 1, 'Failed task moved to DLQ');
  }, 200);
})();

// Test 9: Route task email
(function testRouteEmail() {
  const t = makeTask('e1', 'send-email', { to: 'a@b.com' });
  const result = routeTask(t);
  assert(result.status === 'sent', 'Route email returns sent');
})();

// Test 10: Route task report
(function testRouteReport() {
  const t = makeTask('r1', 'generate-report', { type: 'monthly' });
  const result = routeTask(t);
  assert(result.status === 'completed', 'Route report returns completed');
})();

// Test 11: Route unknown type throws
(function testRouteUnknown() {
  const t = makeTask('x1', 'unknown-type');
  try {
    routeTask(t);
    assert(false, 'Should have thrown for unknown type');
  } catch (e) {
    assert(e.message.includes('Unknown task type'), 'Unknown type throws error');
  }
})();

// Test 12: DLQ drain
(function testDlqDrain() {
  const q = new LoadLevelingQueue({ maxLength: 10, messageTtl: 50 });
  q.enqueue(makeTask());
  q.enqueue(makeTask('t2'));
  setTimeout(() => {
    q.dequeue();
    q.dequeue();
    assert(q.dlqDepth === 2, 'DLQ has 2 messages');
    const drained = q.drainDlq();
    assert(drained.length === 2, 'Drain returns 2 messages');
    assert(q.dlqDepth === 0, 'DLQ empty after drain');
  }, 100);
})();

// Test 13: Queue depth after partial consume
(function testPartialConsume() {
  const q = new LoadLevelingQueue({ maxLength: 100 });
  for (let i = 0; i < 10; i++) q.enqueue(makeTask(`d-${i}`));
  for (let i = 0; i < 3; i++) q.dequeue();
  assert(q.depth === 7, 'Queue depth is 7 after consuming 3');
})();

// Test 14: Rejected count tracks overflows
(function testRejectedCount() {
  const q = new LoadLevelingQueue({ maxLength: 2 });
  q.enqueue(makeTask('a'));
  q.enqueue(makeTask('b'));
  q.enqueue(makeTask('c'));
  q.enqueue(makeTask('d'));
  assert(q.rejected === 2, 'Rejected count is 2');
})();

// Test 15: Consumer getStats
(function testGetStats() {
  const q = new LoadLevelingQueue({ maxLength: 100 });
  const c = new TaskConsumer(q, { 'send-email': () => {} }, 1);
  c.processed = 5;
  c.failed = 2;
  const stats = c.getStats();
  assert(stats.processed === 5, 'getStats returns processed=5');
  assert(stats.failed === 2, 'getStats returns failed=2');
})();

// Wait for async tests to complete
setTimeout(() => {
  console.log();
  if (failed === 0) {
    console.log(`=== All ${passed} tests passed ===`);
  } else {
    console.log(`=== ${passed} passed, ${failed} failed ===`);
  }
}, 500);
