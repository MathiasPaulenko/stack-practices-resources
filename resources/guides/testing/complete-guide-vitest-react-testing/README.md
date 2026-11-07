# Vitest for React: Component, Hook, and Integration Testing — Examples

Runnable companion for the StackPractices guide
[Vitest for React: Component, Hook, and Integration Testing](https://stackpractices.com/guides/complete-guide-vitest-react-testing/).

Self-contained Vitest + React Testing Library project with working versions of every code block shown in the guide:

- `tests/components/Button.test.tsx` — role queries, `userEvent`, variants
- `tests/components/LoginForm.test.tsx` — form validation and async submit
- `tests/components/UserProfile.test.tsx` — async component with `vi.mock` on the API module
- `tests/components/UserProfileMsw.test.tsx` — the same component against MSW 2.x (`setupServer`)
- `tests/components/ThemeAwareComponent.test.tsx` — real context provider with controlled values
- `tests/components/Card.snapshot.test.tsx` — file and inline snapshots
- `tests/hooks/useCounter.test.ts` + `useDebounce.test.ts` — `renderHook`, `act`, fake timers
- `tests/mocks/api.test.ts` + `partial.test.ts` — module mocks and `importOriginal` partial mocks
- `tests/integration/checkout.test.tsx` — multi-step user flow crossing UI and mocked API

## Run

```bash
npm install
npx vitest run          # single run
npm test                # watch mode
npm run test:coverage   # coverage with the thresholds from vitest.config.ts
```

Requires Node 20+. The `vitest.config.ts` wires jsdom, the `@/` alias, `tests/setup.ts`
(matchMedia + IntersectionObserver stubs, `cleanup`), and v8 coverage thresholds.
`.github/workflows/test.yml` is the CI version of the same pipeline.
