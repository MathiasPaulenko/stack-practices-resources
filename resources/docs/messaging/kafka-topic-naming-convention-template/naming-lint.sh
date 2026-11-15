#!/usr/bin/env bash
# Lint Kafka topic names against the <env>.<domain>.<event-name>[.<version>] convention
# where <event-name> ends in a known type suffix (snapshot, dlq, ...) or a past-tense
# verb (order-created, stock-updated, ...).
# Usage: ./naming-lint.sh < topics.txt   (one topic name per line; # comments allowed)
set -euo pipefail

ENVIRONMENTS="dev|staging|prod|sandbox"
TYPES="event|command|snapshot|dlq|audit|metric"
VERBS="created|updated|deleted|cancelled|processed|completed|failed|viewed|signed-up|signed-in|signed-out|received|sent|delivered|started|stopped"
# component = lowercase words joined by hyphens; components joined by dots
COMPONENT='[a-z0-9]+(-[a-z0-9]+)*'
PATTERN="^($ENVIRONMENTS)\.$COMPONENT(\.$COMPONENT)*\.(($TYPES)|v[0-9]+|$COMPONENT-($VERBS))$"

fail=0
while IFS= read -r line; do
  name="${line%%#*}"; name="$(echo "$name" | xargs)"
  [ -z "$name" ] && continue
  if [ ${#name} -gt 249 ]; then
    echo "FAIL  $name — exceeds 249 characters"; fail=1; continue
  fi
  if ! [[ "$name" =~ $PATTERN ]]; then
    echo "FAIL  $name — does not match <env>.<domain>.<event-name>[.<version>]"
    fail=1; continue
  fi
  echo "OK    $name"
done

exit "$fail"
