/**
 * Rule engine built on the Interpreter pattern.
 * Expressions are composable trees evaluated against a context object.
 *
 * Run: npx tsx rule-engine.ts
 */

export interface Expression {
  interpret(context: Record<string, unknown>): boolean | number | unknown;
}

// --- Terminal expressions -------------------------------------------------

export class VariableExpression implements Expression {
  constructor(private name: string) {}

  interpret(context: Record<string, unknown>): unknown {
    return context[this.name];
  }
}

export class NumberExpression implements Expression {
  constructor(private value: number) {}

  interpret(): number {
    return this.value;
  }
}

// --- Non-terminal expressions ----------------------------------------------

export class GreaterThanExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): boolean {
    const l = this.left.interpret(context) as number;
    const r = this.right.interpret(context) as number;
    return l > r;
  }
}

export class AndExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): boolean {
    // short-circuit: skip the right side when the left already decides
    if (!this.left.interpret(context)) return false;
    return this.right.interpret(context) as boolean;
  }
}

export class OrExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): boolean {
    if (this.left.interpret(context)) return true;
    return this.right.interpret(context) as boolean;
  }
}

export class NotExpression implements Expression {
  constructor(private expr: Expression) {}

  interpret(context: Record<string, unknown>): boolean {
    return !(this.expr.interpret(context) as boolean);
  }
}

export class EqualsExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): boolean {
    return this.left.interpret(context) === this.right.interpret(context);
  }
}

export class AddExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): number {
    return (
      (this.left.interpret(context) as number) +
      (this.right.interpret(context) as number)
    );
  }
}

export class SubtractExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): number {
    return (
      (this.left.interpret(context) as number) -
      (this.right.interpret(context) as number)
    );
  }
}

export class MultiplyExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): number {
    return (
      (this.left.interpret(context) as number) *
      (this.right.interpret(context) as number)
    );
  }
}

export class DivideExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Record<string, unknown>): number {
    const r = this.right.interpret(context) as number;
    if (r === 0) throw new Error("division by zero");
    return (this.left.interpret(context) as number) / r;
  }
}

// --- Recursive-descent formula parser --------------------------------------
//
// parseExpression handles + and - (lowest precedence),
// parseFactor handles * and / (bind tighter),
// parseTerm handles literals and variables.

export function parseFormula(tokens: string[]): Expression {
  let index = 0;

  function parseExpression(): Expression {
    let left = parseFactor();
    while (
      index < tokens.length &&
      (tokens[index] === "+" || tokens[index] === "-")
    ) {
      const op = tokens[index++];
      const right = parseFactor();
      left =
        op === "+"
          ? new AddExpression(left, right)
          : new SubtractExpression(left, right);
    }
    return left;
  }

  function parseFactor(): Expression {
    let left = parseTerm();
    while (
      index < tokens.length &&
      (tokens[index] === "*" || tokens[index] === "/")
    ) {
      const op = tokens[index++];
      const right = parseTerm();
      left =
        op === "*"
          ? new MultiplyExpression(left, right)
          : new DivideExpression(left, right);
    }
    return left;
  }

  function parseTerm(): Expression {
    const token = tokens[index++];
    if (token === undefined) throw new Error("unexpected end of formula");
    if (!isNaN(Number(token))) return new NumberExpression(Number(token));
    return new VariableExpression(token);
  }

  return parseExpression();
}

// --- Demo -------------------------------------------------------------------

if (process.argv[1]?.endsWith("rule-engine.ts") || process.argv[1]?.endsWith("rule-engine.js")) {
  // Rule: cart value > 100 AND isVIP
  const rule = new AndExpression(
    new GreaterThanExpression(
      new VariableExpression("cartValue"),
      new NumberExpression(100),
    ),
    new VariableExpression("isVIP"),
  );
  console.log("cart>100 AND isVIP:", rule.interpret({ cartValue: 150, isVIP: true })); // true

  // Access rule: NOT (status == 'banned') OR isAdmin
  const accessRule = new OrExpression(
    new NotExpression(
      new EqualsExpression(
        new VariableExpression("status"),
        new VariableExpression("banned"),
      ),
    ),
    new VariableExpression("isAdmin"),
  );
  console.log(
    "access:",
    accessRule.interpret({ status: "banned", isAdmin: false, banned: "banned" }),
  ); // false

  // Formula: price * 0.8 + shipping  ->  100 * 0.8 + 10 = 90
  const formula = parseFormula(["price", "*", "0.8", "+", "shipping"]);
  console.log("price * 0.8 + shipping:", formula.interpret({ price: 100, shipping: 10 })); // 90

  // Precedence check: 1 + 2 * 3 must be 7, not 9
  const prec = parseFormula(["1", "+", "2", "*", "3"]);
  console.log("1 + 2 * 3:", prec.interpret({})); // 7
}
