#!/usr/bin/env bash
# demo.sh — Builds a toy git repository with messy history so you can
# practice every interactive-rebase action from the StackPractices recipe:
# https://stackpractices.com/recipes/git-rebase-interactive-tutorial/
#
# Usage:
#   ./demo.sh            # create ./rebase-demo and print the practice guide
#   ./demo.sh --cleanup  # remove ./rebase-demo

set -euo pipefail

DEMO_DIR="rebase-demo"

if [[ "${1:-}" == "--cleanup" ]]; then
  rm -rf "$DEMO_DIR"
  echo "Removed $DEMO_DIR"
  exit 0
fi

if [[ -d "$DEMO_DIR" ]]; then
  echo "$DEMO_DIR already exists — run ./demo.sh --cleanup first" >&2
  exit 1
fi

mkdir -p "$DEMO_DIR/src/models" "$DEMO_DIR/src/api" "$DEMO_DIR/tests"
cd "$DEMO_DIR"

git init -q -b main
git config user.name "Rebase Demo"
git config user.email "rebase-demo@example.com"

# Base commit: gives HEAD~5 a valid rebase target below the messy history.
cat > README.md <<'EOF'
# rebase-demo

Toy project for practicing `git rebase -i`.
EOF
git add .
git commit -qm "Initial project skeleton"

# Commit 1: two changes packed into one commit — perfect for the split exercise.
cat > src/models/user.py <<'EOF'
class User:
    def __init__(self, name):
        self.name = name
EOF
cat > src/api/users.py <<'EOF'
def get_user(id):
    return {"id": id, "name": "Ada"}
EOF
git add .
git commit -qm "Add user model and API endpoints"

# Commits 2-3: WIP noise that belongs inside commit 1 — squash/fixup targets.
cat > src/validation.py <<'EOF'
def validate(user):
    # TODO: tighten this later
    return bool(user.name)
EOF
git add .
git commit -qm "WIP: fix validation"

cat > tests/test_user.py <<'EOF'
from src.models.user import User


def test_user_name():
    assert User("Ada").name == "Ada"
EOF
git add .
git commit -qm "WIP: tests"

# Commit 4: something that should never ship — drop target.
cat > src/debug.py <<'EOF'
print("debug checkpoint")
EOF
git add .
git commit -qm "Add debug logging"

# Commit 5: a message that needs rewording.
cat > src/api/users.py <<'EOF'
def get_user(user_id):
    return {"id": user_id, "name": "Ada"}
EOF
git add .
git commit -qm "Fix typo in endpoint"

cat <<'GUIDE'

=== rebase-demo created ===

History (git log --oneline, newest first):

  Fix typo in endpoint        <- reword: the message hides what changed
  Add debug logging           <- drop: should never ship
  WIP: tests                  <- squash into the model commit
  WIP: fix validation         <- squash into the model commit
  Add user model and API endpoints  <- edit: split into two commits
  Initial project skeleton    <- base commit, stays untouched

Practice with:  git rebase -i HEAD~5

  1. Split   — mark 'edit' on "Add user model and API endpoints",
               then: git reset HEAD^ && git add -p && two commits.
  2. Squash  — mark 'squash' on both WIP commits to merge them
               into "Add user model and API endpoints" with one
               clean message.
  3. Drop    — mark 'drop' on "Add debug logging" (or delete the line).
  4. Reword  — mark 'reword' on "Fix typo in endpoint".

Bonus: create a fixup commit and let autosquash place it:

  git commit --fixup <sha>
  git rebase -i --autosquash HEAD~5

Cleanup: ./demo.sh --cleanup

GUIDE

git log --oneline
