// Queue-Based Load Leveling Pattern - In-memory producer (no BullMQ dependency)

class Task {
  constructor(id, type, payload, options = {}) {
    this.id = id;
    this.type = type;
    this.payload = payload;
    this.attempts = 0;
    this.maxRetries = options.maxRetries || 3;
    this.createdAt = Date.now();
    this.priority = options.priority || 0;
  }
}

class DeadLetterQueue {
  constructor() {
    this.messages = [];
  }

  push(task, error) {
    this.messages.push({ task, error, failedAt: Date.now() });
  }

  drain() {
    const items = this.messages.slice();
    this.messages = [];
    return items;
  }

  get length() {
    return this.messages.length;
  }
}

class LoadLevelingQueue {
  constructor(options = {}) {
    this.queue = [];
    this.maxLength = options.maxLength || 1000;
    this.messageTtl = options.messageTtl || 3600000;
    this.processedCount = 0;
    this.rejectedCount = 0;
    this.dlq = new DeadLetterQueue();
  }

  enqueue(task) {
    if (this.queue.length >= this.maxLength) {
      this.rejectedCount++;
      return false;
    }
    this.queue.push(task);
    return true;
  }

  dequeue() {
    if (this.queue.length === 0) return null;
    const task = this.queue.shift();
    if (Date.now() - task.createdAt > this.messageTtl) {
      this.dlq.push(task, 'TTL expired');
      return null;
    }
    return task;
  }

  fail(task, error) {
    task.attempts++;
    if (task.attempts >= task.maxRetries) {
      this.dlq.push(task, error);
    } else {
      this.queue.push(task);
    }
  }

  get depth() {
    return this.queue.length;
  }

  get rejected() {
    return this.rejectedCount;
  }

  get dlqDepth() {
    return this.dlq.length;
  }

  drainDlq() {
    return this.dlq.drain();
  }
}

class TaskProducer {
  constructor(queue) {
    this.queue = queue;
  }

  send(task) {
    return this.queue.enqueue(task);
  }

  sendBatch(tasks) {
    return tasks.map((t) => this.queue.enqueue(t));
  }
}

module.exports = { Task, DeadLetterQueue, LoadLevelingQueue, TaskProducer };
