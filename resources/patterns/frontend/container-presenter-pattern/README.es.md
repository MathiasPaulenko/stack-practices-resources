# Patrón Container-Presenter

Companion ejecutable del patrón [Container-Presenter](https://stackpractices.com/es/patterns/container-presenter-pattern/): custom hook como container, presenter puro, container de clase legacy y tests aislados.

## Contenido

- `useUsers.ts` — custom hook haciendo el papel de container (fetch, estado, vista derivada con `useMemo`)
- `ProductGrid.tsx` — presenter puro (entran props, sale UI, sin fetch/store)
- `FeaturedProducts.tsx` — container que alimenta al presenter con productos destacados
- `UserListContainer.jsx` + `UserListPresenter.jsx` — versión legacy de clase con PropTypes
- `ProductGrid.test.tsx` — presenter testeado de forma aislada, sin mockear la red
- `package.json` — React 18 + Testing Library + Jest

## Notas

- La división: los containers poseen fetch/estado/callbacks; los presenters solo renderizan props. Cambia el container y el mismo presenter dibuja otros datos.
- Los datos derivados siguen siendo derivados — filtra al renderizar o con `useMemo`, nunca guardes una lista filtrada sobre la fuente.
- Para código nuevo prefiere hooks + TypeScript; el par clase + PropTypes existe para mantenimiento legacy.
