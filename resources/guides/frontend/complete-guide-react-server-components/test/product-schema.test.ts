import { describe, expect, it } from "vitest";
import {
  parseProductInput,
  productFormSchema,
} from "../lib/product-schema";

const validInput = {
  name: "Standing Desk",
  price: 499.99,
  description: "Electric sit-stand desk with memory presets.",
  image: "https://example.com/desk.jpg",
};

describe("productFormSchema", () => {
  it("accepts a valid product", () => {
    const result = productFormSchema.safeParse(validInput);
    expect(result.success).toBe(true);
  });

  it("rejects an empty name", () => {
    const result = productFormSchema.safeParse({ ...validInput, name: "" });
    expect(result.success).toBe(false);
  });

  it("rejects a name over 100 characters", () => {
    const result = productFormSchema.safeParse({
      ...validInput,
      name: "x".repeat(101),
    });
    expect(result.success).toBe(false);
  });

  it("rejects a zero or negative price", () => {
    expect(
      productFormSchema.safeParse({ ...validInput, price: 0 }).success
    ).toBe(false);
    expect(
      productFormSchema.safeParse({ ...validInput, price: -10 }).success
    ).toBe(false);
  });

  it("rejects a description shorter than 10 characters", () => {
    const result = productFormSchema.safeParse({
      ...validInput,
      description: "Too short",
    });
    expect(result.success).toBe(false);
  });

  it("rejects an image that is not a URL", () => {
    const result = productFormSchema.safeParse({
      ...validInput,
      image: "not-a-url",
    });
    expect(result.success).toBe(false);
  });
});

describe("parseProductInput", () => {
  it("returns typed data on success", () => {
    const result = parseProductInput(validInput);
    expect(result).toEqual({ success: true, data: validInput });
  });

  it("returns the first issue message on failure", () => {
    const result = parseProductInput({ ...validInput, price: -1 });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error).toContain("greater than 0");
    }
  });

  it("fails on missing fields", () => {
    const result = parseProductInput({ name: "Desk" });
    expect(result.success).toBe(false);
  });
});
