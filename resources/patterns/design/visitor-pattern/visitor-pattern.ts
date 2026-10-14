/**
 * Visitor pattern: an expression AST with eval and print visitors.
 *
 * Classic real-world shape of the pattern — compilers, linters and
 * exporters all walk a stable node hierarchy while new operations get
 * added as visitors.
 *
 * No dependencies; run with ts-node or tsx: npx tsx visitor-pattern.ts
 */

interface ExprVisitor<R> {
  visitNumber(node: NumberNode): R;
  visitAdd(node: AddNode): R;
  visitMul(node: MulNode): R;
}

interface Expr {
  accept<R>(visitor: ExprVisitor<R>): R;
}

class NumberNode implements Expr {
  constructor(public readonly value: number) {}
  accept<R>(visitor: ExprVisitor<R>): R {
    return visitor.visitNumber(this);
  }
}

class AddNode implements Expr {
  constructor(public readonly left: Expr, public readonly right: Expr) {}
  accept<R>(visitor: ExprVisitor<R>): R {
    return visitor.visitAdd(this);
  }
}

class MulNode implements Expr {
  constructor(public readonly left: Expr, public readonly right: Expr) {}
  accept<R>(visitor: ExprVisitor<R>): R {
    return visitor.visitMul(this);
  }
}

class EvalVisitor implements ExprVisitor<number> {
  visitNumber(node: NumberNode): number {
    return node.value;
  }
  visitAdd(node: AddNode): number {
    return node.left.accept(this) + node.right.accept(this);
  }
  visitMul(node: MulNode): number {
    return node.left.accept(this) * node.right.accept(this);
  }
}

class PrintVisitor implements ExprVisitor<string> {
  visitNumber(node: NumberNode): string {
    return String(node.value);
  }
  visitAdd(node: AddNode): string {
    return `(${node.left.accept(this)} + ${node.right.accept(this)})`;
  }
  visitMul(node: MulNode): string {
    return `(${node.left.accept(this)} * ${node.right.accept(this)})`;
  }
}

// (2 + 3) * 4
const expr = new MulNode(new AddNode(new NumberNode(2), new NumberNode(3)), new NumberNode(4));

console.log(expr.accept(new PrintVisitor())); // -> ((2 + 3) * 4)
console.log(expr.accept(new EvalVisitor()));  // -> 20
