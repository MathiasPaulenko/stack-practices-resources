// Composite Pattern: arithmetic expression tree.
// Leaves are numbers, composites are operators, eval() folds the tree.
// Run: npx tsx expression-tree.ts  (or tsc + node)

interface Expr {
  eval(): number;
}

class Num implements Expr {
  constructor(private value: number) {}
  eval(): number { return this.value; }
}

class Add implements Expr {
  constructor(private left: Expr, private right: Expr) {}
  eval(): number { return this.left.eval() + this.right.eval(); }
}

class Mul implements Expr {
  constructor(private left: Expr, private right: Expr) {}
  eval(): number { return this.left.eval() * this.right.eval(); }
}

// (1 + 2) * (3 + 4) = 21
const expr = new Mul(
  new Add(new Num(1), new Num(2)),
  new Add(new Num(3), new Num(4))
);
console.log(expr.eval()); // 21
