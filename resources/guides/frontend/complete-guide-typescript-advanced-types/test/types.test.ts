// Compile-time type tests. `npm test` runs `tsc --noEmit`:
// any wrong expectation fails the build, which is the point.

import type {
  IsString, MyExclude, MyExtract, TypeName, ApiResponse,
  MyReturnType, MyAwaited, ElementOf, FirstParam, ValueOf,
  DeepFlatten, ToArray, ToArrayNonDist, OnlyStrings,
} from "../src/conditional-types";
import type { SnakeCase, ToSnakeCase, PickByValue } from "../src/mapped-types";
import type { EventName, Getter, ExtractParams } from "../src/template-literals";
import { routes, table } from "../src/satisfies-const";
import type { Route, Column } from "../src/satisfies-const";
import { strings, assertDefined } from "../src/narrowing";
import type { Producer, Consumer } from "../src/variance";
import { TypedEmitter } from "../src/typed-emitter";
import type { Events } from "../src/typed-emitter";
import { api } from "../src/api-client";
import type { HasOptions, Options, ResponseOf, User } from "../src/api-client";
import { Machine } from "../src/state-machine";
import type { TrafficLight, TrafficState, EventsOf } from "../src/state-machine";
import { getUser, createUserId, createOrderId } from "../src/branded-types";

type Expect<T extends true> = T;
type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2)
  ? true
  : false;

// --- Conditional types
type _1 = Expect<Equal<IsString<"hello">, true>>;
type _2 = Expect<Equal<IsString<string | number>, boolean>>;
type _3 = Expect<Equal<MyExclude<"a" | "b" | "c", "a">, "b" | "c">>;
type _4 = Expect<Equal<MyExtract<string | number, number>, number>>;
type _5 = Expect<Equal<TypeName<() => void>, "function">>;
type _6 = Expect<Equal<ApiResponse<200, { name: string }>, { status: 200; data: { name: string } }>>;
type _7 = Expect<Equal<ApiResponse<404, string>, never>>;

// --- infer
type _8 = Expect<Equal<MyReturnType<() => string>, string>>;
type _9 = Expect<Equal<MyAwaited<Promise<Promise<number>>>, number>>;
type _10 = Expect<Equal<ElementOf<string[]>, string>>;
type _11 = Expect<Equal<FirstParam<(id: string, o?: object) => void>, string>>;
type _12 = Expect<Equal<ValueOf<{ a: string; b: number }>, string | number>>;
type _13 = Expect<Equal<DeepFlatten<number[][][]>, number>>;

// --- Distribution
type _14 = Expect<Equal<ToArray<string | number>, string[] | number[]>>;
type _15 = Expect<Equal<ToArrayNonDist<string | number>, (string | number)[]>>;
type _16 = Expect<Equal<OnlyStrings<"a" | 1 | "b" | 2>, "a" | "b">>;

// --- Mapped types: the fixed SnakeCase actually produces snake_case
type _17 = Expect<Equal<SnakeCase<"userId">, "user_id">>;
type _18 = Expect<Equal<SnakeCase<"firstName">, "first_name">>;
type _19 = Expect<Equal<
  ToSnakeCase<{ userId: number; firstName: string }>,
  { user_id: number; first_name: string }
>>;
type _20 = Expect<Equal<
  PickByValue<{ id: number; onClick: () => void }, Function>,
  { onClick: () => void }
>>;

// --- Template literals
type _21 = Expect<Equal<EventName, "onClick" | "onChange" | "onSubmit">>;
type _22 = Expect<Equal<Getter<"name">, "getName">>;
type _23 = Expect<Equal<
  ExtractParams<"/users/:userId/posts/:postId">,
  { userId: string } & { postId: string }
>>;

// --- satisfies / const
type _24 = Expect<Equal<Route, "/" | "/users/:id">>;
type _25 = Expect<Equal<Column, "id" | "name">>;
const _routesCheck: Record<string, `/${string}`> = routes;
const _cols: readonly string[] = table.columns;

// --- Narrowing
type _26 = Expect<Equal<typeof strings, string[]>>;
declare const maybeU: { name: string } | undefined;
assertDefined(maybeU);
type _27 = Expect<Equal<typeof maybeU, { name: string }>>;

// --- Variance
declare const prodAB: Producer<"a" | "b">;
const _prodOk: Producer<string> = prodAB;
declare const consS: Consumer<string>;
const _consOk: Consumer<"a" | "b"> = consS;

// --- Emitter
const emitter = new TypedEmitter<Events>();
emitter.on("user:created", (d) => d.id);
emitter.emit("order:paid", { orderId: "o-1", amount: 1 });
// @ts-expect-error missing amount
emitter.emit("order:paid", { orderId: "o-1" });
// @ts-expect-error unknown event
emitter.on("user:archived", (d) => d);

// --- API client: options required or forbidden per route
type _28 = Expect<Equal<HasOptions<"GET /users">, true>>;
type _29 = Expect<Equal<ResponseOf<"GET /users">, User[]>>;
type _30 = Expect<Equal<Options<"DELETE /users/:id">["params"], { id: string }>>;

async function apiCalls() {
  const users = await api("GET /users", { query: { page: 1 } });
  const _u: User[] = users;
  const user = await api("GET /users/:id", { params: { id: "1" } });
  const _x: User = user;
  // @ts-expect-error params required
  await api("GET /users/:id");
  // @ts-expect-error body required
  await api("POST /users", {});
}

// --- State machine
type _31 = Expect<Equal<
  TrafficState,
  { state: "red"; transitions: "go" } |
  { state: "green"; transitions: "warn" } |
  { state: "yellow"; transitions: "stop" }
>>;
type _32 = Expect<Equal<EventsOf<TrafficLight>, "go" | "warn" | "stop">>;

const traffic = new Machine<TrafficLight>("red", {
  red: { transitions: { go: "green" } },
  green: { transitions: { warn: "yellow" } },
  yellow: { transitions: { stop: "red" } },
});
traffic.transition("go");
// @ts-expect-error unknown event name
traffic.transition("fly");

// --- Branded types
const uid = createUserId("3f2b9c1a-7e8d-4a5b-9c6d-1e2f3a4b5c6d");
const oid = createOrderId("1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d");
getUser(uid);
// @ts-expect-error OrderId is not a UserId
getUser(oid);
// @ts-expect-error raw string is not a UserId
getUser("3f2b9c1a-7e8d-4a5b-9c6d-1e2f3a4b5c6d");

export type { _1, _6, _14, _17, _23, _26, _28, _31 };
export { _routesCheck, _cols, _prodOk, _consOk, apiCalls };
