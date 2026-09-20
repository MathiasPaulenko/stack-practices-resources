# Progressive Enhancement — Runnable Demo

Companion code for the StackPractices pattern:
[Progressive Enhancement](https://stackpractices.com/patterns/progressive-enhancement-pattern/)

A dependency-free demo of the three-layer approach: a baseline HTML page that
works with JavaScript disabled, a CSS layer for presentation, and a JavaScript
layer that adds inline validation, async form submit, and click-to-sort tables
only after feature detection passes.

## Run the demo

```bash
# any static server works; no build step needed
python -m http.server 8080
# then open http://localhost:8080
```

To verify the baseline, disable JavaScript in DevTools and reload: the form
still posts and the table still renders.

## Run the tests

```bash
npm test
```

`validation.test.mjs` covers the shared validation rules in `validation.mjs`
with `node:test` — no dependencies required.

## Files

| File | Role |
|---|---|
| `index.html` | Baseline page: form, nav, and table that work without JS |
| `styles.css` | Presentation layer; `.js`-scoped rules only apply with JS |
| `feature-detect.js` | Capability checks (`fetch`, `IntersectionObserver`, etc.) |
| `enhance.js` | Enhancement layer: inline validation, async submit, table sort |
| `validation.mjs` | Shared validation rules, pure functions |
| `validation.test.mjs` | `node:test` coverage of the validation rules |
