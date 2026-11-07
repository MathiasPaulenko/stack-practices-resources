// Type predicates and assertion functions.

export function isString(x: unknown): x is string {
  return typeof x === "string";
}

export function assertDefined<T>(x: T | null | undefined): asserts x is T {
  if (x === null || x === undefined) throw new Error("Value is missing");
}

export function isPresent<T>(x: T | null | undefined): x is NonNullable<T> {
  return x !== null && x !== undefined;
}

const values: unknown[] = ["a", 1, "b"];
export const strings = values.filter(isString); // string[]
