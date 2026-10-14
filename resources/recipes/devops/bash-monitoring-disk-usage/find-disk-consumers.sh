#!/usr/bin/env bash

echo "=== Top 10 largest directories ==="
du -sh /* 2>/dev/null | sort -rh | head -10

echo "=== Top 10 largest files ==="
find / -type f -size +100M -exec du -h {} + 2>/dev/null | sort -rh | head -10
