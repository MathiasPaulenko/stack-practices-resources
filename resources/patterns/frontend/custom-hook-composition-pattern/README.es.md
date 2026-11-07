# Composición de custom hooks — Ejemplos en React

Implementaciones ejecutables de los hooks del patrón [Composición de custom hooks](https://stackpractices.com/es/patterns/custom-hook-composition-pattern/) en StackPractices.

## Archivos

- `useDebounce.js` — retrasa la actualización de un valor según un retardo configurable.
- `useFetch.js` — obtención de datos con estados de carga/error; una URL `null` es un no-op (el patrón `enabled`); `options` se lee por ref para evitar refetches en bucle.
- `useSort.js` — ordenación de arrays con alternancia asc/desc.
- `usePagination.js` — paginación del lado del cliente.
- `useUserTable.js` — el hook compuesto: debounce → url → fetch → ordenación → paginación.
- `useAuth.js` — hook de autenticación con guarda correcta del provider (comprueba el *valor* del contexto).
- `useProtectedFetch.js` — compone `useAuth` con fetch: token bearer + logout automático ante 401.
- `useDebounce.test.js` — tests con `renderHook` y temporizadores falsos.

## Uso

Copia los hooks a un proyecto React 18+ e impórtalos donde los necesites:

```jsx
import useUserTable from './useUserTable';

function UserTable() {
  const { users, loading, sortKey, toggleSort } = useUserTable(searchQuery, {
    itemsPerPage: 5,
    initialSortKey: 'name',
  });
  // ...
}
```

Para ejecutar los tests instala las devDependencies (`jest`, `@testing-library/react`) en tu propio proyecto: `package.json` las declara, pero los ejemplos están pensados para copiarse, no para instalarse como paquete.
