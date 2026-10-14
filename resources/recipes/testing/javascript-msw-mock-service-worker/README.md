# MSW Mock Service Worker — Companion Project

Runnable MSW 2.x setup accompanying the StackPractices recipe:
<https://stackpractices.com/recipes/javascript-msw-mock-service-worker/>

## Contents

| Path | What it shows |
|------|---------------|
| `src/mocks/handlers.ts` | Shared request handlers: REST (params, JSON body, pagination) + a GraphQL query |
| `src/mocks/server.ts` | `setupServer` for Node.js test environments |
| `src/mocks/browser.ts` | `setupWorker` for browser development |
| `src/users.test.ts` | Complete Vitest suite: lifecycle hooks, per-test overrides, pagination |

## Run

```bash
npm install -D msw vitest
npx vitest src/users.test.ts       # Node.js interception
npx msw init public/ --save        # generate mockServiceWorker.js for browser use
```

The handlers are shared between tests, the dev server, and Storybook — one source of truth for mock data.
