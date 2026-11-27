// counter.test.js — stores are plain JS objects; test them with get()
import { describe, test, expect } from "vitest";
import { get } from "svelte/store";
import { counter } from "./stores/counter.js";

describe("counter store", () => {
  test("increments by step (5)", () => {
    counter.reset();
    counter.increment();
    expect(get(counter)).toBe(5);
  });

  test("decrements by step (5)", () => {
    counter.reset();
    counter.decrement();
    expect(get(counter)).toBe(-5);
  });

  test("reset returns to 0", () => {
    counter.increment();
    counter.reset();
    expect(get(counter)).toBe(0);
  });
});
