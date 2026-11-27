# Suspense Boundary Pattern — React Examples

Runnable examples for the [Suspense Boundary pattern](https://stackpractices.com/patterns/suspense-boundary-pattern/): declarative loading states with `<Suspense>` boundaries, a suspense-compatible resource with promise caching, skeleton fallbacks, and an error boundary.

## Files

| File | Purpose |
|------|---------|
| `App.jsx` | App with nested Suspense boundaries wrapped in an error boundary |
| `suspenseResource.js` | Minimal `wrapPromise` + cache so `read()` can suspend safely |
| `ErrorBoundary.jsx` | Class error boundary with fallback UI and retry |
| `Skeletons.jsx` | Skeleton fallbacks matching the content shape |
| `package.json` | React 19 dependencies |

## Usage

```jsx
import { Suspense } from 'react';
import ErrorBoundary from './ErrorBoundary';
import { UserCardSkeleton } from './Skeletons';

<ErrorBoundary>
  <Suspense fallback={<UserCardSkeleton />}>
    <UserCard userId={42} />
  </Suspense>
</ErrorBoundary>
```

Key rules: cache the promise (never call `fetch()` raw in render), match the fallback to the content shape, and always pair Suspense with an error boundary — Suspense only handles loading, not failures.
