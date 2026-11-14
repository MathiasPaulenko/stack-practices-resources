// Interpreter pattern: arithmetic expression language.
// Run: node interpreter-pattern.js

class Expression {
  interpret(context) {
    throw new Error("Subclasses must implement interpret()");
  }
}

class NumberLiteral extends Expression {
  constructor(value) {
    super();
    this.value = value;
  }
  interpret(context) {
    return this.value;
  }
}

class Variable extends Expression {
  constructor(name) {
    super();
    this.name = name;
  }
  interpret(context) {
    return context[this.name] ?? 0;
  }
}

class Add extends Expression {
  constructor(left, right) {
    super();
    this.left = left;
    this.right = right;
  }
  interpret(context) {
    return this.left.interpret(context) + this.right.interpret(context);
  }
}

class Subtract extends Expression {
  constructor(left, right) {
    super();
    this.left = left;
    this.right = right;
  }
  interpret(context) {
    return this.left.interpret(context) - this.right.interpret(context);
  }
}

// Evaluate "(10 + x) - 5" where x = 3
const expression = new Subtract(
  new Add(new NumberLiteral(10), new Variable("x")),
  new NumberLiteral(5)
);
console.log(expression.interpret({ x: 3 })); // 8
