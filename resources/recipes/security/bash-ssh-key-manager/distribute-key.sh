#!/usr/bin/env bash
# Distribute a public key to a list of servers (one user@host per line).
# Usage: ./distribute-key.sh servers.txt [path/to/key.pub]
set -euo pipefail

SERVERS_FILE="${1:?Usage: $0 <servers.txt> [key.pub]}"
PUBLIC_KEY="${2:-$HOME/.ssh/id_ed25519.pub}"

if command -v ssh-copy-id > /dev/null 2>&1; then
    # Preferred: ssh-copy-id sets remote permissions correctly
    while IFS= read -r server; do
        [[ -z "$server" || "$server" == \#* ]] && continue
        ssh-copy-id -i "$PUBLIC_KEY" "$server" \
            && echo "OK: $server" || echo "FAIL: $server"
    done < "$SERVERS_FILE"
else
    # Fallback for minimal environments without ssh-copy-id
    PUB_CONTENT=$(cat "$PUBLIC_KEY")
    while IFS= read -r server; do
        [[ -z "$server" || "$server" == \#* ]] && continue
        ssh "$server" "mkdir -p ~/.ssh && chmod 700 ~/.ssh \
            && echo '$PUB_CONTENT' >> ~/.ssh/authorized_keys \
            && chmod 600 ~/.ssh/authorized_keys" \
            && echo "OK: $server" || echo "FAIL: $server"
    done < "$SERVERS_FILE"
fi
