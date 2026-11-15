# Jest Snapshot Testing — Companion Project

Runnable companion for the [Snapshot Testing React Components with Jest](https://stackpractices.com/recipes/jest-snapshot-testing/) recipe on StackPractices.

A minimal Jest + React Testing Library setup with five components exercising every pattern from the recipe, plus committed `.snap` files so you can see what a real snapshot looks like.

## Files

| Path | What it shows |
|---|---|
| `src/Button.test.jsx` | Basic `toMatchSnapshot()` on `container.firstChild`, one test per variant |
| `src/Card.test.jsx` | Snapshot per meaningful state (full props, no image, loading) |
| `src/Badge.test.jsx` | `toMatchInlineSnapshot()` — the expected output lives inside the test file |
| `src/UserProfile.test.jsx` | `asFragment()` snapshots via Testing Library |
| `src/LastLogin.test.jsx` | `jest.useFakeTimers().setSystemTime()` for deterministic timestamps |
| `src/Dashboard.test.jsx` + `src/lib/__mocks__/Chart.jsx` | Manual mock that replaces a third-party component with a stable stub |
| `src/__snapshots__/` | The `.snap` files Jest generated on the first run — committed on purpose |

## Run it

```bash
npm install
npm test          # all 11 tests pass against the committed snapshots
```

Then try the workflow:

```bash
npm run test:ci       # CI mode: missing snapshots fail instead of writing
npm run test:update   # bless intentional changes (same as jest -u)
npm run test:watch    # press i for interactive snapshot review
```

## Things to try

1. **Break a snapshot**: change `className` in `src/Button.jsx` and run `npm test`. The diff output shows exactly which variant moved.
2. **See an obsolete snapshot**: rename a test in `Card.test.jsx` — Jest reports `1 obsolete snapshot`; `npm run test:update` cleans it.
3. **Feel the flake**: comment out `jest.mock('./lib/Chart')` in `Dashboard.test.jsx` and run `npm test` twice — the random `style.width` in `src/lib/Chart.jsx` fails the snapshot every time. That's why third-party output gets stubbed.
4. **Inline snapshot regeneration**: clear the template string in `Badge.test.jsx` and run `npm test -- -u`; Jest writes it back (requires Prettier 2 — see below).

## Notes

- `jest-environment-jsdom` is a separate package since Jest 28.
- `prettier` stays on v2 on purpose: Jest 29 can't write inline snapshots against Prettier 3+ yet.
- `babel.config.js` uses `@babel/preset-react` with `runtime: 'automatic'`, so no `import React` needed in the components.
