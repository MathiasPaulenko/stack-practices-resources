// Config DSL: a small command language for a key-value store.
// Grammar: SET key value | GET key | DEL key
// Run: npx ts-node config-dsl.ts  (or compile with tsc)

interface Expression {
  interpret(context: Map<string, string>): string;
}

class SetExpression implements Expression {
  constructor(private key: string, private value: string) {}
  interpret(context: Map<string, string>): string {
    context.set(this.key, this.value);
    return `OK: ${this.key} = ${this.value}`;
  }
}

class GetExpression implements Expression {
  constructor(private key: string) {}
  interpret(context: Map<string, string>): string {
    const value = context.get(this.key);
    return value !== undefined ? value : `NIL: ${this.key}`;
  }
}

class DelExpression implements Expression {
  constructor(private key: string) {}
  interpret(context: Map<string, string>): string {
    const existed = context.delete(this.key);
    return existed ? `OK: ${this.key} deleted` : `NIL: ${this.key}`;
  }
}

class SequenceExpression implements Expression {
  constructor(private expressions: Expression[]) {}
  interpret(context: Map<string, string>): string {
    return this.expressions.map(e => e.interpret(context)).join("\n");
  }
}

class ConfigParser {
  parse(input: string): Expression {
    const lines = input.trim().split("\n");
    const expressions: Expression[] = [];
    for (const line of lines) {
      const parts = line.split(" ");
      const cmd = parts[0].toUpperCase();
      if (cmd === "SET") expressions.push(new SetExpression(parts[1], parts.slice(2).join(" ")));
      else if (cmd === "GET") expressions.push(new GetExpression(parts[1]));
      else if (cmd === "DEL") expressions.push(new DelExpression(parts[1]));
      else throw new Error(`Unknown command: ${cmd}`);
    }
    return new SequenceExpression(expressions);
  }
}

const parser = new ConfigParser();
const context = new Map<string, string>();
const program = parser.parse("SET name Alice\nSET role admin\nGET name\nDEL role");
console.log(program.interpret(context));
// OK: name = Alice
// OK: role = admin
// Alice
// OK: role deleted
