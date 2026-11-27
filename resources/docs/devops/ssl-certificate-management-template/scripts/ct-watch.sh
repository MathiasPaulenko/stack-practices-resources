# Check CT logs for your domain using crt.sh
curl -s "https://crt.sh/?q=%25.example.com&output=json" | \
  jq '.[] | select(.not_before > "2026-01-01") | {issuer_name, common_name, not_before}'
