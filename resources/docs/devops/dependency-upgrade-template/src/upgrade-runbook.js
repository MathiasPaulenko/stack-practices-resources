// Simulation of the five-phase dependency upgrade runbook.
// Two upgrades run through the same checklist: one succeeds end to end,
// one fails validation and exercises the rollback path.

const deps = [
  { name: "express", current: "4.18.2", target: "4.21.0", breaksTests: false },
  { name: "left-pad-classic", current: "1.0.0", target: "2.0.0", breaksTests: true },
];

function runPhase(label, steps) {
  console.log(`\n== ${label} ==`);
  for (const step of steps) console.log(`  [done] ${step}`);
}

function upgrade(dep) {
  console.log(`\n########## upgrade ${dep.name} ${dep.current} -> ${dep.target} ##########`);

  runPhase("1. Preparation", [
    "changelog reviewed for breaking changes",
    `branch created: deps/upgrade-${dep.name}-${dep.target}`,
    "CI green on main",
  ]);

  runPhase("2. Upgrade", [
    "version bumped in package.json",
    "npm install completed, no peer conflicts",
    `tests run: ${dep.breaksTests ? "2 FAILING" : "all passing"}`,
  ]);

  const stable = !dep.breaksTests;
  runPhase("3. Validation", [
    "coverage report reviewed",
    "no new warnings in logs",
    "npm audit: 0 high/critical",
    `result: ${stable ? "STABLE" : "UNSTABLE"}`,
  ]);

  if (!stable) {
    runPhase("4. Rollback", [
      "git checkout pre-upgrade-tag -- package.json package-lock.json",
      "npm ci restored last known good",
      "rollback executed in <15 min",
    ]);
    console.log(`  => ${dep.name} stays at ${dep.current}; upgrade rejected`);
    return;
  }

  runPhase("5. Merge & Monitor", [
    "PR opened with changelog summary",
    "staging soak: 24h clean",
    "production deploy in low-traffic window",
    "error rate flat after 48h",
  ]);
  console.log(`  => ${dep.name} is now ${dep.target}`);
}

for (const dep of deps) upgrade(dep);
