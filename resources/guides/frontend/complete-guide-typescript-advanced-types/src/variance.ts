// Variance annotations (TS 4.7+): declare how a generic parameter is used.
// `out` = covariant (output positions), `in` = contravariant (input positions).

export interface Producer<out T> {
  next(): T;
}

export interface Consumer<in T> {
  accept(value: T): void;
}

// Producer<"a"|"b"> is assignable to Producer<string>
// Consumer<string> is assignable to Consumer<"a"|"b">

// A wrong position fails at declaration time:
// interface Bad<out T> { set(v: T): void }  // Error: contravariant position
