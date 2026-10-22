#!/usr/bin/env bash
# Generates an RSA key pair for RS256 signing.
# The private key stays on the auth service; distribute public.pem to
# every service that only verifies.
set -euo pipefail

openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

chmod 600 private.pem
echo "Generated private.pem (keep secret) and public.pem (distribute)"
