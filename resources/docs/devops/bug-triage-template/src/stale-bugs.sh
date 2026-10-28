#!/bin/bash
# Find S3/S4 bugs older than 90 days with no activity
gh issue list \
  --label "s3-medium,s4-low" \
  --state open \
  --search "created:<$(date -d '90 days ago' +%Y-%m-%d) updated:<$(date -d '30 days ago' +%Y-%m-%d)" \
  --json number,title,createdAt,updatedAt \
  --jq '.[] | "#\(.number) \(.title) (created: \(.createdAt[:10]))"'
