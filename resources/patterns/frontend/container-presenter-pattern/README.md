# Container-Presenter Pattern

Runnable companion for the [Container-Presenter pattern](https://stackpractices.com/patterns/container-presenter-pattern/): custom hook as container, pure presenter, legacy class container, and isolation tests.

## Contents

- `useUsers.ts` — custom hook playing the container role (fetch, state, derived view with `useMemo`)
- `ProductGrid.tsx` — pure presenter (props in, UI out, no fetch/store)
- `FeaturedProducts.tsx` — container feeding the presenter with featured-product data
- `UserListContainer.jsx` + `UserListPresenter.jsx` — legacy class version with PropTypes
- `ProductGrid.test.tsx` — presenter tested in isolation, no network mocking
- `package.json` — React 18 + Testing Library + Jest

## Notes

- The split: containers own fetch/state/callbacks; presenters only render props. Swap the container and the same presenter draws different data.
- Derived data stays derived — filter at render or with `useMemo`, never `setState` a filtered list back over the source.
- For new code prefer hooks + TypeScript; the class + PropTypes pair exists for legacy maintenance.
