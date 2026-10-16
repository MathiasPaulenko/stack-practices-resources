#!/usr/bin/env bash
# Verified fleet-wide key rotation: install the new key on every server,
# verify login with it, and only then remove the old key. If any server
# fails verification the script aborts and keeps the old key in place.
# Usage: ./rotate-key-verified.sh servers.txt
set -euo pipefail

OLD_KEY="$HOME/.ssh/id_ed25519"
NEW_KEY="$HOME/.ssh/id_ed25519_new"
SERVERS_FILE="${1:-servers.txt}"

ssh-keygen -t ed25519 -a 100 -f "$NEW_KEY" -N "" -C "rotated-$(date +%Y-%m-%d)"

# 1. Push the new public key everywhere, authenticating with the old key
while IFS= read -r server; do
    [[ -z "$server" || "$server" == \#* ]] && continue
    ssh -i "$OLD_KEY" -o BatchMode=yes -o ConnectTimeout=10 "$server" \
        "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys" \
        < "${NEW_KEY}.pub" \
        && echo "OK: $server" || echo "FAIL: $server"
done < "$SERVERS_FILE"

# 2. Verify the new key on every server
ALL_OK=true
while IFS= read -r server; do
    [[ -z "$server" || "$server" == \#* ]] && continue
    ssh -i "$NEW_KEY" -o BatchMode=yes -o ConnectTimeout=10 "$server" true 2>/dev/null \
        || { echo "FAIL: $server rejects new key"; ALL_OK=false; }
done < "$SERVERS_FILE"

# 3. Only when all servers accept the new key, remove the old one.
# authorized_keys stores the public key blob, not its fingerprint,
# so match the whole line from the .pub file.
OLD_PUB=$(cat "${OLD_KEY}.pub")
if $ALL_OK; then
    while IFS= read -r server; do
        [[ -z "$server" || "$server" == \#* ]] && continue
        ssh -i "$NEW_KEY" -o BatchMode=yes "$server" \
            "grep -vxF '$OLD_PUB' ~/.ssh/authorized_keys > ~/.ssh/authorized_keys.tmp \
             && mv ~/.ssh/authorized_keys.tmp ~/.ssh/authorized_keys"
    done < "$SERVERS_FILE"
    mv "$NEW_KEY" "$OLD_KEY"
    mv "${NEW_KEY}.pub" "${OLD_KEY}.pub"
    echo "Rotation complete."
else
    echo "ABORT: keeping old key; rerun after fixing the failed servers."
    rm -f "$NEW_KEY" "${NEW_KEY}.pub"
    exit 1
fi
