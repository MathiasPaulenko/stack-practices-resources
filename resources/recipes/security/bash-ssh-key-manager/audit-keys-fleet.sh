#!/usr/bin/env bash
# Audit authorized_keys across a fleet and write a CSV report.
# Usage: ./audit-keys-fleet.sh server1 server2 server3
set -euo pipefail

REPORT_FILE="ssh-key-audit-$(date +%Y%m%d).csv"
echo "server,user,key_type,bits,fingerprint,comment" > "$REPORT_FILE"

for server in "$@"; do
    ssh -o BatchMode=yes -o ConnectTimeout=10 "$server" \
        'for user_dir in /home/* /root; do
             auth_keys="$user_dir/.ssh/authorized_keys"
             [ -f "$auth_keys" ] || continue
             while IFS= read -r line; do
                 [ -z "$line" ] || [[ "$line" == \#* ]] && continue
                 info=$(echo "$line" | ssh-keygen -lf - 2>/dev/null) || continue
                 bits=$(echo "$info" | awk "{print \$1}")
                 fp=$(echo "$info" | awk "{print \$2}")
                 ktype=$(echo "$line" | awk "{print \$1}")
                 comment=$(echo "$line" | awk "{print \$3}")
                 echo "'"$server"',$(basename "$user_dir"),$ktype,$bits,$fp,$comment"
             done < "$auth_keys"
         done' >> "$REPORT_FILE" 2>/dev/null \
        || echo "WARN: could not audit $server" >&2
done

# ssh-keygen -lf prints "<bits> <SHA256:fp> <comment> (<TYPE>)" — the CSV
# carries bits in column 4, so flagging weak keys is a plain numeric check.
echo "=== Weak key alerts ==="
awk -F',' 'NR>1 && ($3=="ssh-dss" || $3=="ecdsa" || ($3=="ssh-rsa" && $4+0 < 4096)) \
    {print "WEAK: " $0}' "$REPORT_FILE"

echo "Report written to $REPORT_FILE"
