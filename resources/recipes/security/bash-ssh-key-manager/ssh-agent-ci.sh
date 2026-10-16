#!/usr/bin/env bash
# Non-interactive ssh-agent setup for CI/CD runners.
# Store the private key as a base64-encoded secret in SSH_KEY.
set -euo pipefail

# Start an agent if none is running
ssh-add -l > /dev/null 2>&1 || eval "$(ssh-agent -s)"

# CI: key arrives base64-encoded in a secret env var
if [[ -n "${SSH_KEY:-}" ]]; then
    echo "$SSH_KEY" | base64 -d | ssh-add -
else
    for key in "$HOME"/.ssh/id_ed25519*; do
        [[ -f "$key" && "$key" != *.pub ]] && ssh-add "$key" 2>/dev/null || true
    done
fi

ssh-add -l

# Pin host keys instead of disabling verification entirely.
# accept-new trusts the first scan but still catches key changes later.
mkdir -p "$HOME/.ssh"
for host in ${SSH_HOSTS:-github.com gitlab.com}; do
    ssh-keyscan -H "$host" >> "$HOME/.ssh/known_hosts" 2>/dev/null
done
export GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=accept-new"
