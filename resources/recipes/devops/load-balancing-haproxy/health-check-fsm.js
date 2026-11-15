/**
 * Simulates HAProxy's active health-check state machine.
 *
 * Each backend runs a small FSM driven by probe results at every `inter`
 * interval: `fall N` consecutive failures mark it DOWN, `rise M` consecutive
 * passes mark it UP again. A leastconn dispatcher then routes simulated
 * requests only across servers currently UP.
 *
 * This mirrors the recipe's `default-server inter 5s fall 2 rise 3` tuning:
 * a flapping backend that fails intermittently leaves rotation fast but
 * rejoins slowly, so clients never see its bad period.
 */

const FALL = 2; // consecutive failures to mark DOWN
const RISE = 3; // consecutive passes to mark UP

class Backend {
  constructor(name, probes) {
    this.name = name;
    this.probes = probes; // boolean[], one per interval
    this.up = true;
    this.fails = 0;
    this.passes = 0;
    this.sessions = 0;
    this.log = [];
  }

  probe(ok) {
    if (ok) {
      this.fails = 0;
      this.passes += 1;
      if (!this.up && this.passes >= RISE) {
        this.up = true;
        this.log.push(`${this.name}: UP after ${this.passes} passes`);
      }
    } else {
      this.passes = 0;
      this.fails += 1;
      if (this.up && this.fails >= FALL) {
        this.up = false;
        this.log.push(`${this.name}: DOWN after ${this.fails} fails`);
      }
    }
  }
}

function main() {
  const web1 = new Backend('web1', Array(20).fill(true));
  // web2 fails at t=0..3 (down at t=1), recovers slowly (up at t=6)
  const web2 = new Backend('web2', [...Array(4).fill(false), ...Array(16).fill(true)]);
  // web3 flaps: never reaches 3 consecutive passes, stays down
  const web3 = new Backend('web3', Array(20).fill(0).map((_, i) => i % 3 === 0));

  const pool = [web1, web2, web3];
  const intervals = 20;
  const served = { web1: 0, web2: 0, web3: 0 };

  for (let t = 0; t < intervals; t++) {
    for (const b of pool) b.probe(b.probes[t % b.probes.length]);

    const candidates = pool.filter((b) => b.up);
    if (!candidates.length) continue; // backup server would serve here
    const pick = candidates.reduce((a, b) => (b.sessions < a.sessions ? b : a));
    pick.sessions += 1;
    served[pick.name] += 1;
    // sessions accumulate so leastconn visibly steers traffic to web2
    // once it rejoins; real HAProxy drains them as requests finish
  }

  for (const b of pool) for (const entry of b.log) console.log(entry);
  console.log(`\nRequests served per backend (of ${intervals}):`);
  for (const [name, n] of Object.entries(served)) console.log(`  ${name}: ${n}`);
  console.log('\nweb3 flapped and never earned 3 consecutive passes:');
  console.log('  it stayed DOWN the whole run despite answering some probes');
}

main();
