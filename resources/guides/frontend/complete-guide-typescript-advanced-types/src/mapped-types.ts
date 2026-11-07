// Mapped types and key remapping with `as`.
// The recursive SnakeCase is the corrected version — the common
// non-recursive one produces "u_serid" instead of "user_id".

export type MyPartial<T> = { [K in keyof T]?: T[K] };
export type MyReadonly<T> = { readonly [K in keyof T]: T[K] };
export type MyRequired<T> = { [K in keyof T]-?: T[K] };
export type Mutable<T> = { -readonly [K in keyof T]: T[K] };

export type SnakeCase<S extends string, First extends boolean = true> =
  S extends `${infer C}${infer Rest}`
    ? C extends Lowercase<C>
      ? `${Lowercase<C>}${SnakeCase<Rest, false>}`
      : `${First extends true ? "" : "_"}${Lowercase<C>}${SnakeCase<Rest, false>}`
    : "";

export type ToSnakeCase<T> = {
  [K in keyof T as SnakeCase<string & K>]: T[K];
};

export type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};
