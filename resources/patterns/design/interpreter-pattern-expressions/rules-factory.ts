/**
 * JSON rules -> expression tree factory.
 * This is how the interpreter ends up fed from a database: rules are stored
 * as JSON documents and mapped to expression classes by a whitelist factory.
 *
 * Shape: { "and": [cond, ...] } | { "or": [...] } | { "not": cond }
 *        | { ">": [left, right] } | { "==": [left, right] }
 *        | { "+": [a, b] } | { "-": [a, b] } | { "*": [a, b] } | { "/": [a, b] }
 *        | { "var": "name" } | number
 *
 * Run: npx tsx rules-factory.ts
 */

import {
  Expression,
  AndExpression,
  OrExpression,
  NotExpression,
  GreaterThanExpression,
  EqualsExpression,
  AddExpression,
  SubtractExpression,
  MultiplyExpression,
  DivideExpression,
  VariableExpression,
  NumberExpression,
} from "./rule-engine";

type RuleJson = Record<string, unknown> | number;

const ALLOWED_VARS = new Set(["cartValue", "isVIP", "status", "isAdmin", "price", "shipping"]);

function operand(node: unknown): Expression {
  if (typeof node === "number") return new NumberExpression(node);
  if (typeof node === "object" && node !== null) return toExpression(node as RuleJson);
  throw new Error(`invalid operand: ${JSON.stringify(node)}`);
}

function binary(
  node: Record<string, unknown>,
  op: string,
  build: (l: Expression, r: Expression) => Expression,
): Expression {
  const pair = node[op];
  if (!Array.isArray(pair) || pair.length !== 2) {
    throw new Error(`"${op}" expects [left, right]`);
  }
  return build(operand(pair[0]), operand(pair[1]));
}

export function toExpression(node: RuleJson): Expression {
  if (typeof node === "number") return new NumberExpression(node);

  if ("var" in node) {
    const name = node.var;
    if (typeof name !== "string" || !ALLOWED_VARS.has(name)) {
      throw new Error(`unknown variable: ${JSON.stringify(name)}`);
    }
    return new VariableExpression(name);
  }

  if ("and" in node) {
    const parts = node.and as unknown[];
    return parts.map(operand).reduce((a, b) => new AndExpression(a, b));
  }
  if ("or" in node) {
    const parts = node.or as unknown[];
    return parts.map(operand).reduce((a, b) => new OrExpression(a, b));
  }
  if ("not" in node) return new NotExpression(operand(node.not));

  if (">" in node) return binary(node, ">", (l, r) => new GreaterThanExpression(l, r));
  if ("==" in node) return binary(node, "==", (l, r) => new EqualsExpression(l, r));
  if ("+" in node) return binary(node, "+", (l, r) => new AddExpression(l, r));
  if ("-" in node) return binary(node, "-", (l, r) => new SubtractExpression(l, r));
  if ("*" in node) return binary(node, "*", (l, r) => new MultiplyExpression(l, r));
  if ("/" in node) return binary(node, "/", (l, r) => new DivideExpression(l, r));

  throw new Error(`unknown operator: ${JSON.stringify(node)}`);
}

// --- Demo: "20% off if cart > 100 AND user is VIP" stored as data -----------

const discountRule: RuleJson = {
  and: [{ ">": [{ var: "cartValue" }, 100] }, { var: "isVIP" }],
};

const ctx = { cartValue: 150, isVIP: true };
console.log("discount rule:", toExpression(discountRule).interpret(ctx)); // true
console.log("discount rule (not vip):", toExpression(discountRule).interpret({ cartValue: 150, isVIP: false })); // false

// Rejected at the boundary: variable not in the whitelist
try {
  toExpression({ ">": [{ var: "process.env" }, 0] });
} catch (e) {
  console.log("blocked:", (e as Error).message); // unknown variable: "process.env"
}
