# Priority Queue Pattern — Companion Examples

Companion code for the [Priority Queue Pattern](https://stackpractices.com/patterns/priority-queue-pattern/) guide on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `priority_queue_heap.py` | Python | Heap-based priority queue with worker threads |
| `PriorityQueueScheduler.java` | Java | `PriorityBlockingQueue` with a thread pool |
| `redis_priority_queue.js` | JavaScript | Redis sorted set priority queue with a worker |
| `priority_queue_ts.ts` | TypeScript | Generic heap-based priority queue |
| `test_priority_queue.py` | Python | Unit tests for the Python implementation |

## Run

### Python

```bash
python priority_queue_heap.py
python -m pytest test_priority_queue.py -v
```

### Java

```bash
javac PriorityQueueScheduler.java
java PriorityQueueScheduler
```

### JavaScript (requires Redis)

```bash
npm install ioredis
node redis_priority_queue.js
```

### TypeScript

```bash
npm install -g typescript
tsc priority_queue_ts.ts
node priority_queue_ts.js
```

## License

MIT — see the main repository for details.
