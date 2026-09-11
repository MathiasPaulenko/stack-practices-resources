// test_validation.js — Unit tests for the GraphQL mutation validation pattern.
// Run: node test_validation.js

const { validateInput, collectErrors } = require("./validation.js");
const { rules, userRules, postRules } = require("./rules.js");
const { isValidEmail, normalizeEmail } = require("./scalars.js");

function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL: ${message}`);
    process.exit(1);
  }
  console.log(`PASS: ${message}`);
}

function assertThrows(fn, message) {
  try {
    fn();
    console.error(`FAIL: ${message} (expected throw)`);
    process.exit(1);
  } catch (e) {
    console.log(`PASS: ${message}`);
  }
}

// === Tests for validation.ts ===

function testValidateInputPassesValidInput() {
  const input = { name: "Alice", email: "alice@example.com" };
  validateInput(input, [rules.required("name"), rules.email("email")]);
  assert(true, "validateInput passes valid input");
}

function testValidateInputThrowsOnInvalidInput() {
  const input = { name: "", email: "not-an-email" };
  assertThrows(() => {
    validateInput(input, [rules.required("name"), rules.email("email")]);
  }, "validateInput throws on invalid input");
}

function testValidateInputCollectsAllErrors() {
  const input = { name: "", email: "bad" };
  try {
    validateInput(input, [
      rules.required("name"),
      rules.minLength("name", 2),
      rules.email("email"),
    ]);
    assert(false, "should have thrown");
  } catch (e) {
    const errors = e.extensions.errors;
    assert(errors.length === 3, "collects all 3 errors");
    assert(e.extensions.code === "VALIDATION_ERROR", "error code is VALIDATION_ERROR");
    assert(e.extensions.fields.length === 3, "fields array has 3 entries");
  }
}

function testCollectErrorsReturnsArray() {
  const input = { name: "", email: "" };
  const errors = collectErrors(input, [
    rules.required("name"),
    rules.email("email"),
  ]);
  assert(errors.length === 2, "collectErrors returns 2 errors");
  assert(errors[0].field === "name", "first error is on name field");
  assert(errors[1].field === "email", "second error is on email field");
}

function testCollectErrorsEmptyForValidInput() {
  const input = { name: "Bob", email: "bob@test.com" };
  const errors = collectErrors(input, [
    rules.required("name"),
    rules.email("email"),
  ]);
  assert(errors.length === 0, "collectErrors returns 0 for valid input");
}

// === Tests for rules.ts ===

function testRequiredRule() {
  const rule = rules.required("name");
  assert(rule.rule("Alice", {}), "required accepts non-empty string");
  assert(!rule.rule("", {}), "required rejects empty string");
  assert(!rule.rule(null, {}), "required rejects null");
  assert(!rule.rule(undefined, {}), "required rejects undefined");
  assert(rule.code === "REQUIRED", "required code is REQUIRED");
}

function testMinLengthRule() {
  const rule = rules.minLength("name", 3);
  assert(rule.rule("abc", {}), "minLength accepts 3 chars");
  assert(!rule.rule("ab", {}), "minLength rejects 2 chars");
  assert(!rule.rule(123, {}), "minLength rejects non-string");
}

function testMaxLengthRule() {
  const rule = rules.maxLength("name", 5);
  assert(rule.rule("abc", {}), "maxLength accepts 3 chars");
  assert(!rule.rule("abcdef", {}), "maxLength rejects 6 chars");
}

function testEmailRule() {
  const rule = rules.email("email");
  assert(rule.rule("alice@example.com", {}), "email accepts valid email");
  assert(!rule.rule("not-an-email", {}), "email rejects invalid email");
  assert(!rule.rule(null, {}), "email rejects null");
}

function testRangeRule() {
  const rule = rules.range("status", 0, 3);
  assert(rule.rule(2, {}), "range accepts 2");
  assert(rule.rule(0, {}), "range accepts 0 (boundary)");
  assert(rule.rule(3, {}), "range accepts 3 (boundary)");
  assert(!rule.rule(4, {}), "range rejects 4");
  assert(!rule.rule(-1, {}), "range rejects -1");
}

function testUrlRule() {
  const rule = rules.url("website");
  assert(rule.rule("https://example.com", {}), "url accepts valid URL");
  assert(rule.rule("", {}), "url accepts empty (optional)");
  assert(rule.rule(null, {}), "url accepts null (optional)");
  assert(!rule.rule("not-a-url", {}), "url rejects invalid URL");
}

function testUserRulesSet() {
  const validInput = {
    name: "Alice",
    email: "alice@example.com",
    bio: "Developer",
    website: "https://alice.dev",
  };
  const errors = collectErrors(validInput, userRules);
  assert(errors.length === 0, "userRules passes valid input");

  const invalidInput = { name: "A", email: "bad" };
  const invalidErrors = collectErrors(invalidInput, userRules);
  assert(invalidErrors.length >= 3, "userRules catches multiple errors on invalid input");
}

function testPostRulesSet() {
  const validInput = {
    id: "123",
    title: "My Post Title",
    body: "This is a long enough body for the post to pass validation.",
    status: 1,
  };
  const errors = collectErrors(validInput, postRules);
  assert(errors.length === 0, "postRules passes valid input");
}

// === Tests for scalars.ts ===

function testIsValidEmail() {
  assert(isValidEmail("alice@example.com"), "isValidEmail accepts valid email");
  assert(!isValidEmail("not-an-email"), "isValidEmail rejects invalid email");
  assert(!isValidEmail("a@b"), "isValidEmail rejects short email");
  assert(!isValidEmail(""), "isValidEmail rejects empty string");
}

function testNormalizeEmail() {
  assert(
    normalizeEmail("  Alice@Example.COM  ") === "alice@example.com",
    "normalizeEmail trims and lowercases",
  );
}

// === Run all tests ===

console.log("=== Running tests ===\n");

testValidateInputPassesValidInput();
testValidateInputThrowsOnInvalidInput();
testValidateInputCollectsAllErrors();
testCollectErrorsReturnsArray();
testCollectErrorsEmptyForValidInput();
testRequiredRule();
testMinLengthRule();
testMaxLengthRule();
testEmailRule();
testRangeRule();
testUrlRule();
testUserRulesSet();
testPostRulesSet();
testIsValidEmail();
testNormalizeEmail();

console.log("\n=== All 15 tests passed ===");
