#!/usr/bin/env bash
# Disable SSH password authentication. Run only after confirming key-based
# login works — test `ssh -o PasswordAuthentication=no user@server` in a
# second terminal first, or you will lock yourself out.
set -euo pipefail

SSHD_CONFIG="/etc/ssh/sshd_config"

cp "$SSHD_CONFIG" "${SSHD_CONFIG}.bak"

sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' "$SSHD_CONFIG"
sed -i 's/^#*ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' "$SSHD_CONFIG"
sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' "$SSHD_CONFIG"

sshd -t   # validate config before restarting
systemctl restart sshd

echo "Password authentication disabled. Key-based auth only."
