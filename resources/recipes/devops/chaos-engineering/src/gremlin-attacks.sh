#!/bin/bash
# Gremlin attack examples. Usage: ./gremlin-attacks.sh <container-id>
# Needs the Gremlin CLI: sudo apt-get install gremlin

CONTAINER=${1:-'<container-id>'}

# CPU stress for 60 seconds
gremlin attack cpu --percent 80 --length 60 --container "$CONTAINER"

# Network blackhole to a dependency (30s)
# gremlin attack blackhole --ip 10.0.4.20 --length 30

# Memory consumption (45s)
# gremlin attack memory --percent 75 --length 45
