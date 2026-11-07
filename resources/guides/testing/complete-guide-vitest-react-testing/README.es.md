# Vitest en React: tests de componentes, hooks e integración — Ejemplos

Companion ejecutable de la guía de StackPractices
[Vitest en React: tests de componentes, hooks e integración](https://stackpractices.com/es/guides/complete-guide-vitest-react-testing/).

Proyecto autocontenido de Vitest + React Testing Library con versiones funcionales de cada bloque de código mostrado en la guía:

- `tests/components/Button.test.tsx` — queries por rol, `userEvent`, variantes
- `tests/components/LoginForm.test.tsx` — validación de formularios y envío asíncrono
- `tests/components/UserProfile.test.tsx` — componente asíncrono con `vi.mock` sobre el módulo de API
- `tests/components/UserProfileMsw.test.tsx` — el mismo componente contra MSW 2.x (`setupServer`)
- `tests/components/ThemeAwareComponent.test.tsx` — provider de contexto real con valores controlados
- `tests/components/Card.snapshot.test.tsx` — snapshots en archivo e inline
- `tests/hooks/useCounter.test.ts` + `useDebounce.test.ts` — `renderHook`, `act`, fake timers
- `tests/mocks/api.test.ts` + `partial.test.ts` — mocks de módulos y mocks parciales con `importOriginal`
- `tests/integration/checkout.test.tsx` — flujo de usuario de varios pasos cruzando UI y API mockeada

## Ejecutar

```bash
npm install
npx vitest run          # ejecución única
npm test                # modo watch
npm run test:coverage   # cobertura con los thresholds de vitest.config.ts
```

Requiere Node 20+. El `vitest.config.ts` configura jsdom, el alias `@/`, `tests/setup.ts`
(stubs de matchMedia + IntersectionObserver, `cleanup`) y los thresholds de cobertura v8.
`.github/workflows/test.yml` es la versión en CI del mismo pipeline.
