/**
 * Mixin Pattern — runnable TypeScript companion.
 *
 * Typed mixins as functions that take a base class and return an extended
 * one. The Constructor constraint lets ...args flow through each layer,
 * so `EnhancedUser` keeps `log`, `serialize` and `validate` fully typed.
 *
 * Run: npx tsx mixins.ts
 */

type Constructor<T = object> = new (...args: any[]) => T;

function Loggable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    private logPrefix = "[LOG]";
    log(msg: string) {
      console.log(`${this.logPrefix} ${msg}`);
    }
    setPrefix(prefix: string) {
      this.logPrefix = prefix;
    }
  };
}

function Serializable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    serialize(): string {
      return JSON.stringify(this);
    }
  };
}

function Validatable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    private validators: Record<string, (v: unknown) => boolean> = {};
    addValidator(field: string, fn: (v: unknown) => boolean) {
      this.validators[field] = fn;
    }
    validate(): string[] {
      const errors: string[] = [];
      for (const [field, fn] of Object.entries(this.validators)) {
        if (!fn((this as any)[field])) errors.push(`Invalid: ${field}`);
      }
      return errors;
    }
  };
}

class User {
  constructor(public name: string, public email: string) {}
}

// Order matters: each mixin wraps the previous layer.
const EnhancedUser = Loggable(Serializable(Validatable(User)));

const user = new EnhancedUser("Alice", "alice@test.com");
user.setPrefix("[USER]");
user.log("Created");
console.log(user.serialize());
user.addValidator("email", (v) => typeof v === "string" && v.includes("@"));
console.log(user.validate()); // []
