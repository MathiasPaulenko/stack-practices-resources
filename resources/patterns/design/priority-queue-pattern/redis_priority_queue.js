// Priority Queue Pattern: Redis sorted set priority queue with a worker.
// Run: node redis_priority_queue.js
const Redis = require('ioredis');

class RedisPriorityQueue {
  constructor(redis, queueName) {
    this.redis = redis;
    this.queueName = queueName;
  }

  async enqueue(task, priority = 3) {
    const score = priority * 1000000000 + Date.now();
    const taskJson = JSON.stringify(task);
    await this.redis.zadd(this.queueName, score, taskJson);
  }

  async dequeue() {
    const result = await this.redis.zpopmin(this.queueName, 1);
    if (result.length === 0) return null;
    const [taskJson, score] = result;
    return { task: JSON.parse(taskJson), score: parseFloat(score) };
  }

  async peek() {
    const result = await this.redis.zrange(this.queueName, 0, 0, 'WITHSCORES');
    if (result.length === 0) return null;
    return { task: JSON.parse(result[0]), score: parseFloat(result[1]) };
  }

  async size() {
    return await this.redis.zcard(this.queueName);
  }
}

class PriorityWorker {
  constructor(redis, queueName, options = {}) {
    this.queue = new RedisPriorityQueue(redis, queueName);
    this.handlers = new Map();
    this.running = false;
    this.pollInterval = options.pollInterval || 100;
    this.concurrency = options.concurrency || 1;
  }

  registerHandler(taskType, handler) {
    this.handlers.set(taskType, handler);
  }

  async start() {
    this.running = true;
    const workers = Array(this.concurrency).fill().map(() => this.workerLoop());
    await Promise.all(workers);
  }

  async workerLoop() {
    while (this.running) {
      const item = await this.queue.dequeue();
      if (!item) {
        await this.sleep(this.pollInterval);
        continue;
      }
      const { task } = item;
      const handler = this.handlers.get(task.type);
      if (handler) {
        try {
          await handler(task.payload);
        } catch (err) {
          console.error(`Task ${task.id} failed:`, err);
        }
      }
    }
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  stop() {
    this.running = false;
  }
}

module.exports = { RedisPriorityQueue, PriorityWorker };
