/**
 * LLM Router Pattern — runnable demo (Node 18+).
 *
 * Classifies queries by complexity (rules-based) and routes them to a tier
 * (small/medium/large). CascadeRouter adds quality-gated escalation.
 * Generate is mocked so the demo runs offline — swap `mockGenerate` for
 * real provider calls to use it for real.
 */

class ModelConfig {
  constructor(name, maxTokens, costPer1k, latencyMs) {
    this.name = name;
    this.maxTokens = maxTokens;
    this.costPer1k = costPer1k;
    this.latencyMs = latencyMs;
  }
}

const MODELS = {
  small:  new ModelConfig("gpt-4o-mini", 4096, 0.0006, 200),
  medium: new ModelConfig("gpt-4o",      8192, 0.005,  500),
  large:  new ModelConfig("o1",         16384, 0.015,  2000),
};

function classifyComplexity(text) {
  const lower = text.toLowerCase();
  const wordCount = text.split(" ").length;
  let score = 0;

  const complexPatterns = [
    /analyze|design|architect|compare|evaluate/,
    /debug|refactor|optimize|review/,
    /step.by.step|detailed|thorough/,
    /legal|medical|financial|security/,
  ];
  const simplePatterns = [
    /^\s*(what|who|when|where|is|are|can|do)\s/,
    /calculate|convert|format|translate/,
    /summarize|rewrite|paraphrase/,
  ];

  for (const p of complexPatterns) if (p.test(lower)) score += 2;
  for (const p of simplePatterns) if (p.test(lower)) score -= 2;

  if (wordCount > 100) score += 2;
  else if (wordCount < 20) score -= 1;

  if (score >= 2) return ["high", Math.min(0.5 + score * 0.15, 1.0)];
  if (score <= -2) return ["low", Math.min(0.5 - score * 0.15, 1.0)];
  return ["medium", 0.5];
}

function routeToModel(complexity) {
  return { low: "small", medium: "medium", high: "large" }[complexity] || "medium";
}

const TIER_RANK = { small: 0, medium: 1, large: 2 };
const LEVEL_RANK = { low: 0, medium: 1, high: 2 };

function mockGenerate(tier, model, prompt) {
  // A tier under the query's true level answers thin.
  const required = LEVEL_RANK[classifyComplexity(prompt)[0]];
  if (TIER_RANK[tier] < required) {
    return { model: model.name, content: `[${model.name}] I can't fully answer that.`, tokensUsed: 12, cost: 0 };
  }
  const tokens = Math.min(Math.max(60, prompt.split(" ").length * 2), model.maxTokens);
  return {
    model: model.name,
    content: `[${model.name}] Response to: ${prompt.slice(0, 50)}...`,
    tokensUsed: tokens,
    cost: (tokens / 1000) * model.costPer1k,
  };
}

class LLMRouter {
  constructor(models) {
    this.models = models;
    this.stats = { routed: 0, escalated: 0, totalCost: 0, baselineCost: 0 };
  }

  _charge(response) {
    this.stats.routed++;
    this.stats.totalCost += response.cost;
    this.stats.baselineCost += (response.tokensUsed / 1000) * this.models.large.costPer1k;
    return response;
  }

  handle(queryText) {
    const [complexity, confidence] = classifyComplexity(queryText);
    const key = routeToModel(complexity);
    console.log(`  [${complexity} @ ${confidence.toFixed(2)}] -> ${this.models[key].name}`);
    return this._charge(mockGenerate(key, this.models[key], queryText));
  }
}

class CascadeRouter extends LLMRouter {
  static TIERS = ["small", "medium", "large"];

  _qualityOk(response) {
    return response.tokensUsed >= 30 && !response.content.includes("I can't");
  }

  handle(queryText) {
    const [complexity, confidence] = classifyComplexity(queryText);
    let start = CascadeRouter.TIERS.indexOf(routeToModel(complexity));
    if (confidence < 0.7) start = Math.max(start - 1, 0); // unsure: start one tier lower, verify

    for (const tier of CascadeRouter.TIERS.slice(start)) {
      const response = mockGenerate(tier, this.models[tier], queryText);
      this._charge(response);
      if (this._qualityOk(response) || tier === "large") {
        console.log(`  [${complexity} @ ${confidence.toFixed(2)}] -> ${this.models[tier].name}`);
        return response;
      }
      this.stats.escalated++;
      console.log(`  [${complexity} @ ${confidence.toFixed(2)}] ${this.models[tier].name} thin -> escalate`);
    }
  }
}

const QUERIES = [
  "What is the capital of France?",
  "Analyze this contract for liability clauses and suggest revisions",
  "Convert 100 degrees Celsius to Fahrenheit",
  "Design a microservices architecture for an e-commerce platform with 10M users",
  "Translate 'good morning' to Spanish",
  "Should I refactor this function or leave it as is?", // borderline -> medium
];

function report(router) {
  const savings = 1 - router.stats.totalCost / Math.max(router.stats.baselineCost, 1e-9);
  console.log(`  ${router.stats.routed} calls | ${router.stats.escalated} escalations`
    + ` | cost $${router.stats.totalCost.toFixed(6)} vs always-large`
    + ` $${router.stats.baselineCost.toFixed(6)} | saved ${(savings * 100).toFixed(0)}%`);
}

console.log("== One-shot router ==");
const router = new LLMRouter(MODELS);
for (const q of QUERIES) router.handle(q);
report(router);

console.log("\n== Cascade router (verify + escalate) ==");
const cascade = new CascadeRouter(MODELS);
for (const q of QUERIES) cascade.handle(q);
report(cascade);
