# Custom Hook Composition — React Examples

Runnable implementations of the hooks from the [Custom Hook Composition pattern](https://stackpractices.com/patterns/custom-hook-composition-pattern/) on StackPractices.

## Files

- `useDebounce.js` — debounces a value after a configurable delay.
- `useFetch.js` — data fetching with loading/error states; `null` URL is a no-op (the `enabled` pattern); `options` read via ref to avoid refetch loops.
- `useSort.js` — array sorting with asc/desc toggle.
- `usePagination.js` — client-side pagination.
- `useUserTable.js` — the composed hook: debounce → url → fetch → sort → paginate.
- `useAuth.js` — context-backed auth hook with a correct provider guard (checks the context *value*).
- `useProtectedFetch.js` — composes `useAuth` with fetch: bearer token + auto-logout on 401.
- `useDebounce.test.js` — `renderHook` tests with fake timers.

## Usage

Drop the hooks into a React 18+ project and import them where needed:

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

To run the tests, install the dev dependencies (`jest`, `@testing-library/react`) in your own project — `package.json` declares them but the examples are meant to be copied, not installed as a package.
