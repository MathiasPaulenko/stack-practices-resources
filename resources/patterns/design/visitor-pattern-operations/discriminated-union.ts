// Discriminated-union alternative to the Visitor pattern.
// Same expression AST, same operations — no accept() boilerplate.
// Run: npx tsx discriminated-union.ts

type Expr =
  | { kind: 'number'; value: number }
  | { kind: 'variable'; name: string }
  | { kind: 'binaryOp'; op: string; left: Expr; right: Expr };

function evaluate(node: Expr, vars: Record<string, number>): number {
  switch (node.kind) {
    case 'number': return node.value;
    case 'variable': return vars[node.name] ?? 0;
    case 'binaryOp': {
      const l = evaluate(node.left, vars);
      const r = evaluate(node.right, vars);
      switch (node.op) {
        case '+': return l + r;
        case '-': return l - r;
        case '*': return l * r;
        case '/': return l / r;
        default: throw new Error(`unknown operator ${node.op}`);
      }
    }
  }
}

function print(node: Expr): string {
  switch (node.kind) {
    case 'number': return String(node.value);
    case 'variable': return node.name;
    case 'binaryOp': return `(${print(node.left)} ${node.op} ${print(node.right)})`;
  }
}

const ast: Expr = {
  kind: 'binaryOp',
  op: '+',
  left: { kind: 'number', value: 2 },
  right: {
    kind: 'binaryOp',
    op: '*',
    left: { kind: 'variable', name: 'x' },
    right: { kind: 'number', value: 3 },
  },
};

console.log('eval:', evaluate(ast, { x: 4 })); // 14
console.log('print:', print(ast)); // (2 + (x * 3))
