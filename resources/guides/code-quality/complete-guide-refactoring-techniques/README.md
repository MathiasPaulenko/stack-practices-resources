# Refactoring Techniques — Runnable Examples

Companion code for the guide [Refactoring Techniques: A Complete Guide](https://stackpractices.com/guides/complete-guide-refactoring-techniques/).

`refactoring_examples.js` contains the messy `processOrder` function and its fully refactored version side by side: guard clauses, extract method, named constants, and move function (pricing decision moved to `Customer`). A smoke test at the bottom verifies both versions produce the same total — that equivalence check is the whole point of safe refactoring.

## Run

```bash
node refactoring_examples.js
```

Expected output: `before: 99` and `after: 99`.
