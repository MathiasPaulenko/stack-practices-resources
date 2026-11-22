// benchmark.js — compare the Map-only trick vs Map+linked list eviction cost.
// Run: node benchmark.js   (transpile the .ts files first, or use tsx/ts-node)

const { MapLRUCache } = require('./lru-map');
const { LRUCache } = require('./lru-dll');

const SIZES = [100, 1_000, 10_000, 50_000];
const OPS = 20_000;

for (const size of SIZES) {
  for (const [name, Ctor] of [
    ['Map-only', MapLRUCache],
    ['Map+DLL ', LRUCache],
  ]) {
    const cache = new Ctor(size);
    for (let i = 0; i < size; i++) cache.set(`k${i}`, i);

    const t0 = performance.now();
    // churn: writes beyond capacity force an eviction each time
    for (let i = 0; i < OPS; i++) cache.set(`new${i}`, i);
    const ms = (performance.now() - t0).toFixed(1);
    console.log(`${name} cap=${String(size).padEnd(6)} ${OPS} evicting sets: ${ms} ms`);
  }
}
