# Optimistic Update Pattern

Runnable companion for the [Optimistic Update pattern](https://stackpractices.com/patterns/optimistic-update-pattern/): snapshot → optimistic UI → request → reconcile or rollback, in plain React, React 19, and React Query.

## Contents

- `LikeButton.jsx` — minimal optimistic update: fill the heart instantly, roll back on error
- `TodoList.jsx` — optimistic add/delete/toggle with temp IDs and `pending` styling
- `OptimisticTodo.jsx` — React 19's built-in `useOptimistic` inside a transition (no manual rollback)
- `useOptimisticTodo.js` — the same list on TanStack Query: `onMutate` snapshot, `onError` rollback, `onSettled` refetch
- `useOptimisticState.js` — generic optimistic-state hook for pre-React 19 codebases
- `CommentEditor.jsx` — `useOptimisticState` usage: local draft, optimistic save
- `EditableTitle.jsx` — conflict handling with `version` and `409` responses
- `MixedOptimistic.jsx` — optimistic for low-risk actions, pessimistic for cart removal
- `BatchOptimistic.jsx` — bulk optimistic update rolling back as a unit
- `package.json` — React 19 + TanStack Query

## Notes

- Snapshot the state *before* mutating — the rollback is only as good as what you captured.
- New items get a temp ID (`crypto.randomUUID()`); swap it for the server ID when the response lands.
- On React 19 prefer the native `useOptimistic`; the custom `useOptimisticState` exists for older versions.
- The example files call `/api/...` endpoints — wire them to your backend or a mock (MSW) to run them.
