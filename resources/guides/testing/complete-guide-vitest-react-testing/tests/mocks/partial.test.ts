// tests/mocks/partial.test.ts — Partial module mocking
import { describe, it, expect, vi } from "vitest";

vi.mock("@/utils/format", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/utils/format")>();
  return {
    ...actual,
    formatDate: vi.fn(() => "2026-01-01"),
  };
});

import { formatDate, formatCurrency } from "@/utils/format";

describe("partial mock", () => {
  it("uses mocked formatDate", () => {
    expect(formatDate(new Date())).toBe("2026-01-01");
  });

  it("uses real formatCurrency", () => {
    expect(formatCurrency(10.5)).toBe("$10.50");
  });
});
