// Template literal types: string manipulation at the type level.

export type EventName = `on${"Click" | "Change" | "Submit"}`;

export type Getter<K extends string> = `get${Capitalize<K>}`;

// Extract :param segments from a route string into an object type.
export type ExtractParams<S extends string> =
  S extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param]: string } & ExtractParams<`/${Rest}`>
    : S extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

export type HandlerName = `on${Capitalize<string>}`;
export type CssLength = `${number}px` | `${number}rem` | `${number}%`;
