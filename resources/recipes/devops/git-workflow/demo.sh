#!/usr/bin/env bash
# Companion demo for https://stackpractices.com/recipes/git-workflow/
# Builds a throwaway repo and walks the full GitHub Flow loop:
# feature branch -> PR-style squash merge -> release tag -> hotfix cherry-pick.
set -euo pipefail

DEMO_DIR="git-workflow-demo"
rm -rf "$DEMO_DIR"
mkdir "$DEMO_DIR" && cd "$DEMO_DIR"

git init -q -b main
git config user.name "Demo User"
git config user.email "demo@example.com"

echo "# Shop API" > README.md
git add README.md
git commit -qm "chore: initial commit"
echo "== 1. Repo initialized on main =="

# --- 2. Feature branch workflow -------------------------------------------
git checkout -qb feature/login
echo "login endpoint" > login.js
git add login.js
git commit -qm "feat(auth): add login endpoint"
echo "logout endpoint" > logout.js
git add logout.js
git commit -qm "feat(auth): add logout endpoint"
echo "== 2. Two commits on feature/login =="

# --- 3. Squash merge into main (the PR lands) ------------------------------
git checkout -q main
git merge --squash feature/login
git commit -qm "feat(auth): add login and logout endpoints"
# -d refuses here: squash-merged branches don't look "merged" to Git
git branch -D feature/login
echo "== 3. Squash-merged: main now has ONE clean commit =="

# --- 4. Tag the release -----------------------------------------------------
git tag -a v1.0.0 -m "Release 1.0.0"
echo "== 4. Tagged v1.0.0 =="

# --- 5. Hotfix on a release branch + cherry-pick back ----------------------
git checkout -qb release/1.0.x v1.0.0
echo "fix: rate-limit login attempts" > ratelimit.js
git add ratelimit.js
git commit -qm "fix(auth): rate-limit login attempts"
HOTFIX=$(git rev-parse --short HEAD)
git checkout -q main
git cherry-pick "$HOTFIX"
echo "== 5. Hotfix $HOTFIX cherry-picked back to main =="

# --- Result -----------------------------------------------------------------
echo
echo "Final history on main (linear, conventional):"
git log --oneline main
echo
echo "Branches: $(git branch | tr '\n' ' ')"
echo "Tags:     $(git tag | tr '\n' ' ')"
echo
echo "Demo repo left in ./$DEMO_DIR — explore it, then delete it."
