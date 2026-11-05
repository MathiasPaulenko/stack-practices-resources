// fast-check property tests (TypeScript + vitest).
// Run: npm install && npx vitest run properties.test.ts
import { describe, it, expect } from "vitest";
import fc from "fast-check";

const validEmail = fc.tuple(
  fc.string({ minLength: 1 }).map((s) => s.replace(/[^a-zA-Z0-9]/g, "a")),
  fc.string({ minLength: 1 }).map((s) => s.replace(/[^a-zA-Z0-9]/g, "a")),
  fc.constantFrom("com", "org", "net", "io", "dev")
).map(([local, domain, tld]) => `${local}@${domain}.${tld}`);

const userArbitrary = fc.record({
  id: fc.integer({ min: 1, max: 1000000 }),
  name: fc.string({ minLength: 1, maxLength: 50 }),
  email: validEmail,
  age: fc.integer({ min: 0, max: 150 }),
  isActive: fc.boolean(),
});

describe("String properties", () => {
  it("reversing twice returns the original", () => {
    fc.assert(fc.property(fc.string(), (s) => {
      expect(s.split("").reverse().reverse().join("")).toBe(s);
    }));
  });
});

describe("User properties", () => {
  it("serialization roundtrip preserves data", () => {
    fc.assert(fc.property(userArbitrary, (user) => {
      expect(JSON.parse(JSON.stringify(user))).toEqual(user);
    }));
  });
});

type StackCommand = { type: "push"; value: number } | { type: "pop" };

const stackCommands = fc.array(
  fc.oneof(
    fc.record({ type: fc.constant("push"), value: fc.integer() }),
    fc.record({ type: fc.constant("pop") })
  )
);

describe("Stack stateful properties", () => {
  it("pop returns last pushed value (LIFO)", () => {
    fc.assert(fc.property(stackCommands, (commands) => {
      const stack: number[] = [];
      for (const cmd of commands) {
        if (cmd.type === "push") stack.push(cmd.value);
        else if (stack.length > 0) {
          const top = stack[stack.length - 1];
          expect(stack.pop()).toBe(top);
        }
      }
    }));
  });
});
