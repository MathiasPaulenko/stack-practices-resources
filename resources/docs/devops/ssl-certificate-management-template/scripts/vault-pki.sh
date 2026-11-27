# Enable PKI engine
vault secrets enable -path=pki pki

# Configure max lease duration
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write pki/root/generate/internal \
    common_name="Internal CA" \
    ttl=87600h

# Configure URLs for CRL and issuing
vault write pki/config/urls \
    issuing_certificates="https://vault.internal:8200/v1/pki/ca" \
    crl_distribution_points="https://vault.internal:8200/v1/pki/crl"

# Create a role for issuing certificates
vault write pki/roles/internal-service \
    allowed_domains="internal.company.com" \
    allow_subdomains=true \
    max_ttl="720h" \
    key_type="rsa" \
    key_bits=2048

# Issue a certificate
vault write pki/issue/internal-service \
    common_name="api.internal.company.com" \
    ttl="24h"
