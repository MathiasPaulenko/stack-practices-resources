# MSW Mock Service Worker — Proyecto complementario

Setup ejecutable de MSW 2.x que acompaña a la receta de StackPractices:
<https://stackpractices.com/es/recipes/javascript-msw-mock-service-worker/>

## Contenido

| Ruta | Qué muestra |
|------|-------------|
| `src/mocks/handlers.ts` | Request handlers compartidos: REST (params, body JSON, paginación) + una query GraphQL |
| `src/mocks/server.ts` | `setupServer` para entornos de test en Node.js |
| `src/mocks/browser.ts` | `setupWorker` para desarrollo en navegador |
| `src/users.test.ts` | Suite completa de Vitest: hooks de ciclo de vida, overrides por test, paginación |

## Ejecutar

```bash
npm install -D msw vitest
npx vitest src/users.test.ts       # intercepción en Node.js
npx msw init public/ --save        # genera mockServiceWorker.js para el navegador
```

Los handlers se comparten entre tests, el servidor de desarrollo y Storybook — una única fuente de verdad para los datos mock.
