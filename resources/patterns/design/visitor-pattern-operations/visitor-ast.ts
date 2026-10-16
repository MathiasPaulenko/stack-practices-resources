// Companion code for "Visitor Pattern: Extensible Operations in TypeScript"
// https://stackpractices.com/patterns/visitor-pattern-operations/
//
// Run: npx tsx visitor-ast.ts   (or ts-node)

interface ASTNode {
  accept(visitor: ASTVisitor): void;
}

interface ASTVisitor {
  visitNumber(node: NumberNode): void;
  visitBinaryOp(node: BinaryOpNode): void;
  visitVariable(node: VariableNode): void;
}

class NumberNode implements ASTNode {
  constructor(public value: number) {}
  accept(visitor: ASTVisitor): void { visitor.visitNumber(this); }
}

class BinaryOpNode implements ASTNode {
  constructor(
    public operator: string,
    public left: ASTNode,
    public right: ASTNode
  ) {}
  accept(visitor: ASTVisitor): void { visitor.visitBinaryOp(this); }
}

class VariableNode implements ASTNode {
  constructor(public name: string) {}
  accept(visitor: ASTVisitor): void { visitor.visitVariable(this); }
}

// Evaluator visitor: accumulates results on an internal stack
class Evaluator implements ASTVisitor {
  private stack: number[] = [];

  constructor(private variables: Record<string, number>) {}

  visitNumber(node: NumberNode): void {
    this.stack.push(node.value);
  }

  visitVariable(node: VariableNode): void {
    this.stack.push(this.variables[node.name] ?? 0);
  }

  visitBinaryOp(node: BinaryOpNode): void {
    node.left.accept(this);
    node.right.accept(this);

    const right = this.stack.pop()!;
    const left = this.stack.pop()!;

    switch (node.operator) {
      case '+': this.stack.push(left + right); break;
      case '-': this.stack.push(left - right); break;
      case '*': this.stack.push(left * right); break;
      case '/': this.stack.push(left / right); break;
    }
  }

  getResult(): number {
    return this.stack[this.stack.length - 1];
  }
}

// Printer visitor: a new operation with zero changes to the nodes
class Printer implements ASTVisitor {
  private output = '';

  visitNumber(node: NumberNode): void {
    this.output += node.value;
  }

  visitVariable(node: VariableNode): void {
    this.output += node.name;
  }

  visitBinaryOp(node: BinaryOpNode): void {
    this.output += '(';
    node.left.accept(this);
    this.output += ` ${node.operator} `;
    node.right.accept(this);
    this.output += ')';
  }

  getOutput(): string {
    return this.output;
  }
}

// Serializer visitor: captures this.result between child traversals
class JSONSerializer implements ASTVisitor {
  private result: unknown = null;

  visitNumber(node: NumberNode): void {
    this.result = { type: 'number', value: node.value };
  }

  visitVariable(node: VariableNode): void {
    this.result = { type: 'variable', name: node.name };
  }

  visitBinaryOp(node: BinaryOpNode): void {
    node.left.accept(this);
    const left = this.result;
    node.right.accept(this);
    const right = this.result;

    this.result = {
      type: 'binaryOp',
      operator: node.operator,
      left,
      right,
    };
  }

  serialize(): string {
    return JSON.stringify(this.result);
  }
}

// Usage: AST for 2 + (x * 3)
const ast = new BinaryOpNode(
  '+',
  new NumberNode(2),
  new BinaryOpNode('*', new VariableNode('x'), new NumberNode(3))
);

const evaluator = new Evaluator({ x: 4 });
ast.accept(evaluator);
console.log('eval:', evaluator.getResult()); // 14

const printer = new Printer();
ast.accept(printer);
console.log('print:', printer.getOutput()); // (2 + (x * 3))

const serializer = new JSONSerializer();
ast.accept(serializer);
console.log('json:', serializer.serialize());
