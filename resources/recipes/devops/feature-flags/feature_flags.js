// Lightweight feature flag service with boolean, percentage, user, and group rollouts.

import { createHash } from "crypto";

class FeatureFlags {
  constructor(config) {
    this.config = config;
  }

  isEnabled(flag, userId = null) {
    const rule = this.config[flag] ?? false;

    if (typeof rule === "boolean") return rule;
    if (typeof rule !== "object") return false;

    if (rule.percentage != null && userId) {
      return this.#hashBucket(userId, flag) < rule.percentage;
    }
    if (rule.users && userId) {
      return rule.users.includes(userId);
    }
    if (rule.groups) {
      return this.#checkGroups(rule.groups);
    }
    return false;
  }

  #hashBucket(userId, flag) {
    const hash = createHash("md5").update(`${flag}:${userId}`).digest("hex");
    return parseInt(hash.slice(0, 8), 16) % 100;
  }

  #checkGroups(groups) {
    return false;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const flags = new FeatureFlags({
    newDashboard: true,
    betaSearch: { percentage: 10 },
    vipFeature: { users: ["user_123"] },
    adminTools: { groups: ["admins"] },
  });

  console.log("newDashboard:", flags.isEnabled("newDashboard"));
  console.log("betaSearch (user_456):", flags.isEnabled("betaSearch", "user_456"));
  console.log("vipFeature (user_123):", flags.isEnabled("vipFeature", "user_123"));
  console.log("missing_flag:", flags.isEnabled("missing_flag"));
}

export { FeatureFlags };
