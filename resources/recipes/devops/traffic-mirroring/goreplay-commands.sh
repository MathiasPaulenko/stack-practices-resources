#!/bin/bash
# GoReplay commands for traffic mirroring

# Capture and replay live traffic
gor --input-raw :8080 --output-http http://staging-api:8080

# Mirror 10% of traffic
gor --input-raw :8080 --output-http "http://staging-api:8080|10%"

# Save to file for later replay
gor --input-raw :8080 --output-file requests.gor

# Replay at 2x speed
gor --input-file "requests.gor|200%" --output-http http://staging-api:8080

# Filter POST requests to /api
gor --input-raw :8080 --http-allow-method POST --http-allow-url ^/api --output-http http://staging-api:8080

# Strip Authorization header before sending to staging
gor --input-raw :8080 --output-http http://staging-api:8080 --http-set-header "Authorization: Bearer staging-token"

# Rate limit to 100 requests per second
gor --input-raw :8080 --output-http "http://staging-api:8080|100"
