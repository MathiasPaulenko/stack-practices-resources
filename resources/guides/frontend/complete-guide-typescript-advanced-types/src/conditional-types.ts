// Conditional types: T extends U ? X : Y
// The building block every other advanced feature relies on.

export type IsString<T> = T extends string ? true : false;

export type MyExclude<T, U> = T extends U ? never : T;
export type MyExtract<T, U> = T extends U ? T : never;

export type TypeName<T> =
  T extends string ? "string" :
  T extends number ? "number" :
  T extends boolean ? "boolean" :
  T extends undefined ? "undefined" :
  T extends Function ? "function" :
  "object";

// Status selects the shape; the payload is a second parameter.
export type ApiResponse<S extends number, T> =
  S extends 200 ? { status: 200; data: T } :
  S extends 400 ? { status: 400; error: string } :
  S extends 500 ? { status: 500; error: string; retryAfter: number } :
  never;

// infer: pattern matching inside the extends clause
export type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
export type MyAwaited<T> = T extends Promise<infer U> ? MyAwaited<U> : T;
export type ElementOf<T> = T extends (infer E)[] ? E : never;
export type FirstParam<T> = T extends (arg: infer P, ...rest: any[]) => any ? P : never;
export type ValueOf<T> = T extends Record<any, infer V> ? V : never;
export type DeepFlatten<T> = T extends (infer U)[] ? DeepFlatten<U> : T;

// Distribution over unions
export type ToArray<T> = T extends any ? T[] : never;
export type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
export type OnlyStrings<T> = T extends string ? T : never;
