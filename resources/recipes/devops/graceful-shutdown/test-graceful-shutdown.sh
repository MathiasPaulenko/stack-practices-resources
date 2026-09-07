#!/bin/bash
# test-graceful-shutdown.sh — CI test for graceful shutdown
# Requires: vegeta (https://github.com/tsenart/vegeta)

start_server &
SERVER_PID=$!
sleep 2  # Wait for startup

# Start load test in background
vegeta attack -duration=30s -rate=100 | vegeta report &
LOAD_PID=$!

# Send SIGTERM after 10s
sleep 10
kill -TERM $SERVER_PID

# Wait for load test to finish
wait $LOAD_PID

# Check results: success rate should be 100%
vegeta attack -duration=30s -rate=100 | vegeta report | grep -q "100.00%"
