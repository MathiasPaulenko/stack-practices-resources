#!/bin/bash
# Audit SSH private keys for missing passphrases and lock down credential files.
# From the StackPractices endpoint security checklist.
set -u

echo "== SSH keys without passphrase =="
for key in ~/.ssh/id_*; do
  case "$key" in *.pub) continue ;; esac
  [ -f "$key" ] || continue
  if ssh-keygen -y -P "" -f "$key" &>/dev/null; then
    echo "WARNING: $key has no passphrase"
  fi
done

echo "== Locking down credential files =="
find ~/.aws ~/.config/gcloud -name "credentials" -exec chmod 600 {} \; 2>/dev/null
echo "Done."
