// Run: npx tsx ts_pipeline.ts   (or: ts-node)
// CSP-style pipeline in TypeScript using async generators as channels.

async function* generatorChannel(limit: number): AsyncGenerator<number> {
  for (let i = 0; i < limit; i++) {
    await new Promise((r) => setTimeout(r, 50)); // simulate production cost
    yield i;
  }
}

async function* squareChannel(
  source: AsyncIterable<number>
): AsyncGenerator<number> {
  for await (const n of source) {
    yield n * n;
  }
}

// Fan-out: N consumers pull from the same source and tag their results.
async function fanOut<T, R>(
  source: AsyncIterable<T>,
  workers: number,
  fn: (item: T, workerId: number) => Promise<R>
): Promise<R[]> {
  const it = source[Symbol.asyncIterator]();
  const results: R[] = [];
  await Promise.all(
    Array.from({ length: workers }, async (_, id) => {
      for (;;) {
        const { value, done } = await it.next();
        if (done) return;
        results.push(await fn(value, id));
      }
    })
  );
  return results;
}

async function main() {
  // Pipeline
  for await (const s of squareChannel(generatorChannel(5))) {
    console.log("square:", s);
  }

  // Fan-out over a shared source
  const out = await fanOut(generatorChannel(9), 3, async (n, id) => {
    await new Promise((r) => setTimeout(r, 30));
    console.log(`worker ${id}: job ${n}`);
    return n * 2;
  });
  console.log("results:", out);
}

main();
