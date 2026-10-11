// Long-task chunking demo — run: node chunked_processing.js
// Splits heavy work so the event loop can breathe between chunks.

const heavyComputation = (n) => Math.sqrt(n) * Math.sin(n); // stand-in for real work

function processLargeArray(arr, chunkSize = 1000) {
  let index = 0;

  function processChunk() {
    const chunk = arr.slice(index, index + chunkSize);
    chunk.forEach(item => heavyComputation(item));
    index += chunkSize;
    console.log(`processed ${Math.min(index, arr.length)}/${arr.length}`);

    if (index < arr.length) {
      setTimeout(processChunk, 0); // yield to the event loop
    } else {
      console.log('done — every other timer and I/O callback still ran on time');
    }
  }

  processChunk();
}

processLargeArray(Array.from({ length: 5000 }, (_, i) => i));

// For contrast, the blocking version processes the whole array in one
// synchronous pass — every timer scheduled meanwhile arrives late.
