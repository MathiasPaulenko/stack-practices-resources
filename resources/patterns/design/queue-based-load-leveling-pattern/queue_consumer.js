// Queue-Based Load Leveling Pattern - Consumer (in-memory, no BullMQ dependency)

const handlers = {
  'send-email': (data) => ({ status: 'sent', to: data.to }),
  'process-payment': (data) => ({ status: 'processed', amount: data.amount }),
  'generate-report': (data) => ({ status: 'completed', type: data.type }),
};

class TaskConsumer {
  constructor(queue, handlerMap, interval = 10) {
    this.queue = queue;
    this.handlers = handlerMap || handlers;
    this.interval = interval;
    this.running = false;
    this.processed = 0;
    this.failed = 0;
    this.timer = null;
  }

  start(concurrency = 1) {
    this.running = true;
    this._loop();
  }

  _loop() {
    if (!this.running) return;
    const task = this.queue.dequeue();
    if (task) {
      try {
        const handler = this.handlers[task.type];
        if (!handler) throw new Error(`Unknown task type: ${task.type}`);
        handler(task.payload);
        this.processed++;
      } catch (err) {
        this.failed++;
        this.queue.fail(task, err.message);
      }
    }
    this.timer = setTimeout(() => this._loop(), this.interval);
  }

  stop() {
    this.running = false;
    if (this.timer) clearTimeout(this.timer);
  }

  getStats() {
    return { processed: this.processed, failed: this.failed };
  }
}

function routeTask(task) {
  const handler = handlers[task.type];
  if (!handler) throw new Error(`Unknown task type: ${task.type}`);
  return handler(task.payload);
}

module.exports = { TaskConsumer, routeTask, handlers };
