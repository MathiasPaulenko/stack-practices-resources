// rules.ts — Reusable validation rule factories.
// Run: npx ts-node rules.ts

import { ValidationRule } from "./validation";

export const rules = {
  required: (field: string): ValidationRule => ({
    field,
    rule: (value) => value !== undefined && value !== null && value !== "",
    message: `${field} is required`,
    code: "REQUIRED",
  }),

  minLength: (field: string, min: number): ValidationRule => ({
    field,
    rule: (value) => typeof value === "string" && value.length >= min,
    message: `${field} must be at least ${min} characters`,
    code: "MIN_LENGTH",
  }),

  maxLength: (field: string, max: number): ValidationRule => ({
    field,
    rule: (value) => typeof value === "string" && value.length <= max,
    message: `${field} must be at most ${max} characters`,
    code: "MAX_LENGTH",
  }),

  email: (field: string): ValidationRule => ({
    field,
    rule: (value) =>
      typeof value === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    message: `${field} must be a valid email address`,
    code: "INVALID_EMAIL",
  }),

  range: (field: string, min: number, max: number): ValidationRule => ({
    field,
    rule: (value) => typeof value === "number" && value >= min && value <= max,
    message: `${field} must be between ${min} and ${max}`,
    code: "OUT_OF_RANGE",
  }),

  url: (field: string): ValidationRule => ({
    field,
    rule: (value) => {
      if (!value) return true;
      try {
        new URL(value);
        return true;
      } catch {
        return false;
      }
    },
    message: `${field} must be a valid URL`,
    code: "INVALID_URL",
  }),
};

// Common rule sets for reuse across mutations
export const userRules: ValidationRule[] = [
  rules.required("name"),
  rules.minLength("name", 2),
  rules.maxLength("name", 100),
  rules.required("email"),
  rules.email("email"),
  rules.maxLength("bio", 500),
  rules.url("website"),
];

export const postRules: ValidationRule[] = [
  rules.required("id"),
  rules.required("title"),
  rules.minLength("title", 5),
  rules.maxLength("title", 200),
  rules.required("body"),
  rules.minLength("body", 50),
  rules.range("status", 0, 3),
];
