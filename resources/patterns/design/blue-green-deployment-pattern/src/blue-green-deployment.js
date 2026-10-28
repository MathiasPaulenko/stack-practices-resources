class Environment {
  constructor(color) {
    this.color = color;
    this.version = "";
    this.status = "inactive";
    this.health = false;
    this.instanceCount = 0;
  }
}

class BlueGreenDeployment {
  constructor() {
    this.blue = new Environment("blue");
    this.blue.version = "1.0.0"; this.blue.status = "active"; this.blue.health = true; this.blue.instanceCount = 3;
    this.green = new Environment("green");
    this.active = this.blue;
    this.inactive = this.green;
    this.history = [];
  }

  _switch() {
    [this.active, this.inactive] = [this.inactive, this.active];
    this.active.status = "active";
    this.inactive.status = "inactive";
  }

  async deploy(newVersion, smokeTests = []) {
    console.log(`\n=== Blue-Green Deploy: v${newVersion} ===`);
    const target = this.inactive;
    console.log(`  Deploying to ${target.color} (inactive)`);
    target.status = "deploying"; target.version = newVersion; target.instanceCount = 3;
    await new Promise(r => setTimeout(r, 100));
    console.log(`  Deployed v${newVersion} to ${target.color}`);

    target.status = "testing";
    for (const test of smokeTests) {
      if (!await test()) {
        target.health = false; target.status = "inactive";
        console.log(`  Smoke tests FAILED on ${target.color}`);
        return { success: false, activeColor: this.active.color, version: this.active.version, message: "Smoke tests failed" };
      }
    }
    target.health = true;
    console.log(`  Smoke tests passed on ${target.color}`);

    this._switch();
    console.log(`  Switched: ${this.active.color} (v${this.active.version}) is now active`);
    this.history.push({ version: newVersion, active: this.active.color });
    return { success: true, activeColor: this.active.color, version: newVersion, message: "Deployment successful" };
  }

  rollback() {
    console.log(`\n=== Rollback ===`);
    if (this.inactive.health && this.inactive.version) {
      this._switch();
      console.log(`  Rolled back to ${this.active.color} (v${this.active.version})`);
      return { success: true, activeColor: this.active.color, version: this.active.version, rollback: true };
    }
    return { success: false, activeColor: this.active.color, version: this.active.version, message: "No healthy env" };
  }

  status() {
    return {
      active: { color: this.active.color, version: this.active.version, instances: this.active.instanceCount },
      inactive: { color: this.inactive.color, version: this.inactive.version, health: this.inactive.health },
      history: this.history,
    };
  }
}

// Usage
(async () => {
  const bg = new BlueGreenDeployment();
  console.log("Initial:", bg.status());

  const result = await bg.deploy("2.0.0", [
    async () => { console.log("    Test: API response"); return true; },
    async () => { console.log("    Test: DB connection"); return true; },
  ]);
  console.log("Result:", result);
  console.log("State:", bg.status());

  console.log("\n=== Rolling back ===");
  console.log("Rollback:", bg.rollback());
  console.log("Final:", bg.status());
})();
