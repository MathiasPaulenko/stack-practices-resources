"""AWS Signature Version 4 — full signer.

Kept as reference/interop code: in real integrations use the AWS SDK
or botocore's signer. This exists to show (and test) what the SDK hides.
"""
import hashlib
import hmac
import urllib.parse
from datetime import datetime, timezone


def get_aws_signature_v4(
    access_key: str,
    secret_key: str,
    region: str,
    service: str,
    method: str,
    url: str,
    headers: dict,
    body: str = '',
) -> dict:
    """Generate AWS Signature v4 headers for an API request."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc
    path = parsed.path or '/'

    # Canonical query: URI-encode each name/value, then sort
    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    canonical_query = '&'.join(
        f'{urllib.parse.quote(k, safe="")}={urllib.parse.quote(v, safe="")}'
        for k, v in sorted(pairs)
    )

    # Step 1: canonical request
    amz_date = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    date_stamp = amz_date[:8]

    headers = dict(headers)
    headers['Host'] = host  # Host is always signed in SigV4
    signed_headers = sorted(headers.keys())
    canonical_headers = ''.join(
        f'{h.lower()}:{headers[h].strip()}\n' for h in signed_headers
    )
    signed_header_str = ';'.join(h.lower() for h in signed_headers)

    payload_hash = hashlib.sha256(body.encode()).hexdigest()

    canonical_request = '\n'.join([
        method.upper(),
        path,
        canonical_query,
        canonical_headers,
        signed_header_str,
        payload_hash,
    ])

    # Step 2: string to sign
    credential_scope = f'{date_stamp}/{region}/{service}/aws4_request'
    string_to_sign = '\n'.join([
        'AWS4-HMAC-SHA256',
        amz_date,
        credential_scope,
        hashlib.sha256(canonical_request.encode()).hexdigest(),
    ])

    # Step 3: derived signing key (HMAC chain date → region → service)
    def sign(key: bytes, msg: str) -> bytes:
        return hmac.new(key, msg.encode(), hashlib.sha256).digest()

    signing_key = sign(
        sign(sign(sign(
            ('AWS4' + secret_key).encode(), date_stamp),
            region),
            service),
        'aws4_request'
    )

    signature = hmac.new(
        signing_key, string_to_sign.encode(), hashlib.sha256
    ).hexdigest()

    # Step 4: authorization header
    result = dict(headers)
    result['Authorization'] = (
        f'AWS4-HMAC-SHA256 '
        f'Credential={access_key}/{credential_scope}, '
        f'SignedHeaders={signed_header_str}, '
        f'Signature={signature}'
    )
    result['X-Amz-Date'] = amz_date
    result['X-Amz-Content-Sha256'] = payload_hash
    return result


if __name__ == '__main__':
    # AWS docs example credentials (public test values)
    out = get_aws_signature_v4(
        access_key='AKIAIOSFODNN7EXAMPLE',
        secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        region='us-east-1',
        service='s3',
        method='GET',
        url='https://s3.amazonaws.com/my-bucket/object.txt',
        headers={},
    )
    print(out['Authorization'][:80] + '...')
