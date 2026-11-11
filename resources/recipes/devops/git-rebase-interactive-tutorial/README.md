# Interactive Git Rebase — Practice Demo

Companion code for the StackPractices recipe:
https://stackpractices.com/recipes/git-rebase-interactive-tutorial/

## What's inside

| File | Purpose |
|---|---|
| `demo.sh` | Builds a toy git repo (`rebase-demo/`) with 5 messy commits matching the recipe's examples, then prints a practice guide. |

## How to use

1. Run `./demo.sh` — it creates `rebase-demo/` with this history:

```text
Fix typo in endpoint
Add debug logging
WIP: tests
WIP: fix validation
Add user model and API endpoints
```

2. `cd rebase-demo` and run `git rebase -i HEAD~5`.
3. Practice each action against real commits:
   - **split** — `edit` on "Add user model and API endpoints", then `git reset HEAD^` and commit the model and endpoints separately.
   - **squash** — `squash` both WIP commits into the first one.
   - **drop** — `drop` "Add debug logging".
   - **reword** — `reword` "Fix typo in endpoint".
4. Try the autosquash flow too: `git commit --fixup <sha>` then `git rebase -i --autosquash HEAD~5`.
5. `./demo.sh --cleanup` removes the practice repo.

Requires: git 2.32+ (for `--fixup=amend:` / `--fixup=reword:`), bash.
