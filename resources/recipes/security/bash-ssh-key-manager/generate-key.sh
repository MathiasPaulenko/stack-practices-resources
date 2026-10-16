#!/usr/bin/env bash
# Generate an ed25519 SSH key. Usage: ./generate-key.sh [key-name]
set -euo pipefail

KEY_NAME="${1:-id_ed25519}"
KEY_PATH="$HOME/.ssh/${KEY_NAME}"

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

if [ -f "$KEY_PATH" ]; then
    echo "Key already exists: $KEY_PATH" >&2
    exit 1
fi

ssh-keygen -t ed25519 -a 100 -C "$(whoami)@$(hostname)-${KEY_NAME}" -f "$KEY_PATH" -N ""

echo "Generated: $KEY_PATH"
echo "Public key: ${KEY_PATH}.pub"
