#!/bin/bash
# dependency-checks.sh - Verify third-party dependencies after a DR cutover.
# Run each block and compare against the expected result in the comment.

# Test DNS failover
dig @8.8.8.8 app.example.com +short
# Should return DR region IP after cutover

# Test CDN failover
curl -sI https://app.example.com | grep "x-served-by"
# Should show DR cache node after cutover

# Test external API dependency circuit breaker
curl -X POST http://app.internal/admin/test-circuit-breaker \
  -d '{"dependency":"payment-gateway","action":"open"}'
