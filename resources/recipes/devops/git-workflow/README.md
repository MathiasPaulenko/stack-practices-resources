# Team Git Workflow — Practice Demo

Companion files for the StackPractices recipe
[Team Git Workflow: Feature Branches, PRs and Clean History](https://stackpractices.com/recipes/git-workflow/).

## Files

- `demo.sh` — builds a throwaway repository (`git-workflow-demo/`) and executes
  the complete GitHub Flow loop shown in the recipe.

## What the demo covers

1. Initializes a repo on `main` (protected branch in the real world).
2. Creates a `feature/login` branch with two Conventional Commits.
3. Squash-merges it back into `main` — what a PR merge looks like.
4. Tags `v1.0.0` as the release.
5. Fixes a bug on `release/1.0.x` and cherry-picks the hotfix back to `main`.

## Usage

```bash
chmod +x demo.sh
./demo.sh
```

The script leaves a `git-workflow-demo/` directory you can inspect
(`git log`, `git branch`, `git tag`) and delete when done.

## Requirements

- Bash (Git Bash on Windows works)
- Git 2.x
