// rules.js — Reusable validation rule factories (JS version).

const rules = {
  required: (field) => ({
    field,
    rule: (value) => value !== undefined && value !== null && value !== "",
    message: `${field} is required`,
    code: "REQUIRED",
  }),

  minLength: (field, min) => ({
    field,
    rule: (value) => typeof value === "string" && value.length >= min,
    message: `${field} must be at least ${min} characters`,
    code: "MIN_LENGTH",
  }),

  maxLength: (field, max) => ({
    field,
    rule: (value) => typeof value === "string" && value.length <= max,
    message: `${field} must be at most ${max} characters`,
    code: "MAX_LENGTH",
  }),

  email: (field) => ({
    field,
    rule: (value) =>
      typeof value === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    message: `${field} must be a valid email address`,
    code: "INVALID_EMAIL",
  }),

  range: (field, min, max) => ({
    field,
    rule: (value) => typeof value === "number" && value >= min && value <= max,
    message: `${field} must be between ${min} and ${max}`,
    code: "OUT_OF_RANGE",
  }),

  url: (field) => ({
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

const userRules = [
  rules.required("name"),
  rules.minLength("name", 2),
  rules.maxLength("name", 100),
  rules.required("email"),
  rules.email("email"),
  rules.maxLength("bio", 500),
  rules.url("website"),
];

const postRules = [
  rules.required("id"),
  rules.required("title"),
  rules.minLength("title", 5),
  rules.maxLength("title", 200),
  rules.required("body"),
  rules.minLength("body", 50),
  rules.range("status", 0, 3),
];

module.exports = { rules, userRules, postRules };
