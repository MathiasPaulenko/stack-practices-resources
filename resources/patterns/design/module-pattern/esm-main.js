import { increment, getCount } from './esm-counter.js';

increment();
increment();
console.log(getCount()); // 2
// `count` and `log` are not exported — unreachable here
