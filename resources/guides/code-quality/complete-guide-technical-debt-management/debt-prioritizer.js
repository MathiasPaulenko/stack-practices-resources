// debt-prioritizer.js — Score debt items by impact, interest, and effort.
// Runnable with plain Node.js: node debt-prioritizer.js

const IMPACT_WEIGHT = {
  critical: 100,
  high: 60,
  medium: 30,
  low: 10,
};

// Score = impact weight + accrued interest − effort cost.
// interestRate is "extra days per sprint if unpaid"; ageInDays converts
// staleness into accumulated interest. Effort gets a 0.5 cost factor.
function scoreDebt(item) {
  return (
    IMPACT_WEIGHT[item.impact] +
    (item.interestRate * item.ageInDays) / 30 -
    item.effort * 0.5
  );
}

function prioritizeDebt(items) {
  return [...items].sort((a, b) => scoreDebt(b) - scoreDebt(a));
}

// --- Demo: the register from the guide ---

const register = [
  {
    id: 'TD-001',
    title: 'Monolithic auth module',
    impact: 'high',
    effort: 5,
    interestRate: 2.5,
    ageInDays: 90,
  },
  {
    id: 'TD-002',
    title: 'No integration tests for payment flow',
    impact: 'critical',
    effort: 3,
    interestRate: 4,
    ageInDays: 60,
  },
  {
    id: 'TD-003',
    title: 'jQuery in legacy admin panel',
    impact: 'low',
    effort: 10,
    interestRate: 0.5,
    ageInDays: 180,
  },
  {
    id: 'TD-004',
    title: 'Runtime past end-of-life on payment service',
    impact: 'high',
    effort: 2,
    interestRate: 3,
    ageInDays: 45,
  },
];

const ranked = prioritizeDebt(register);
for (const item of ranked) {
  console.log(
    `${item.id}  score=${scoreDebt(item).toFixed(1).padStart(7)}  ` +
      `${item.impact.padEnd(8)}  ${item.title}`,
  );
}
