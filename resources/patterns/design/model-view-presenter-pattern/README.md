# Model-View-Presenter Pattern — Companion Code

Runnable, dependency-free implementation of the [Model-View-Presenter pattern](https://stackpractices.com/patterns/model-view-presenter-pattern/): a `UserDetailPresenter` holds all the screen logic and talks only to an abstract `UserDetailView`, so tests can replace the GUI with a `FakeView` that records every call.

## Files

| File | Stack | Tests |
|------|-------|-------|
| `mvp.py` | Python stdlib (`abc`, `dataclasses`, `unittest`) | 5 unittest cases |
| `mvp.mjs` | Node.js (`node:test`, `node:assert`) | 5 cases under `node --test` |

## Run

```bash
# Python — test suite
python -m unittest mvp -v

# Node — test suite
node --test mvp.mjs
```

## What the tests cover

- The happy path: `onLoadClicked` reaches `showUser` with the right data.
- The not-found branch surfaces `showError`, not an exception.
- Invalid input is rejected before the repository is touched.
- `showLoading`/`hideLoading` wrap the lookup in the right order.
- `hideLoading` still runs on error — the `finally` seam that real UIs leak.

## Why a fake view instead of a UI test

The fake implements the same interface the screen does, so the assertion log reads like what the user would have seen. The only thing left untested is the wiring — which Activity or component instantiates the Presenter — and that belongs in a small integration test.
