// Async task cancellation demo for Node.js (AbortController / AbortSignal).
//
// Run: node node_cancel.mjs
// The task auto-cancels after 2 seconds; watch the cleanup path fire.

async function longRunningTask(signal, taskId) {
  try {
    for (let i = 0; i < 1000; i++) {
      if (signal.aborted) {
        throw new DOMException('Task cancelled', 'AbortError');
      }
      await sleep(100, signal);
      console.log(`Task ${taskId}: processing item ${i}`);
    }
  } catch (err) {
    if (err.name === 'AbortError') {
      console.log(`Task ${taskId}: cancelled, cleaning up...`);
      await cleanupResources(taskId);
      throw err;
    }
    throw err;
  }
}

function sleep(ms, signal) {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(new DOMException('Aborted', 'AbortError'));
      return;
    }
    const onAbort = () => {
      clearTimeout(timer);
      reject(new DOMException('Aborted', 'AbortError'));
    };
    const timer = setTimeout(() => {
      signal?.removeEventListener('abort', onAbort);
      resolve();
    }, ms);
    signal?.addEventListener('abort', onAbort, { once: true });
  });
}

async function cleanupResources(taskId) {
  console.log(`Task ${taskId}: closing connections...`);
  await sleep(50); // signal is optional: cleanup runs even without one
  console.log(`Task ${taskId}: cleanup complete`);
}

async function fetchWithTimeout(url, options = {}, timeout = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    return await response.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      console.error(`Request to ${url} timed out after ${timeout}ms`);
      return null;
    }
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }
}

const controller = new AbortController();
const task = longRunningTask(controller.signal, 'worker-1');

setTimeout(() => controller.abort(), 2000);

try {
  await task;
} catch (err) {
  if (err.name === 'AbortError') {
    console.log('Task cancelled successfully');
  } else {
    throw err;
  }
}
