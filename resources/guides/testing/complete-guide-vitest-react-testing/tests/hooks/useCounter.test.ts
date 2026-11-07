// tests/hooks/useCounter.test.ts — Hook testing
import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "@/hooks/useCounter";

describe("useCounter", () => {
  it("initializes with default value", () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it("initializes with custom value", () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it("increments count", () => {
    const { result } = renderHook(() => useCounter());

    act(() => result.current.increment());
    expect(result.current.count).toBe(1);

    act(() => result.current.increment());
    expect(result.current.count).toBe(2);
  });

  it("decrements count", () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => result.current.decrement());
    expect(result.current.count).toBe(4);
  });

  it("resets count", () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => result.current.increment());
    expect(result.current.count).toBe(11);

    act(() => result.current.reset());
    expect(result.current.count).toBe(10);
  });
});
