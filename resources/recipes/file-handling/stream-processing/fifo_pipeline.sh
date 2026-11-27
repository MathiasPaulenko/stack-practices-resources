#!/usr/bin/env bash
set -euo pipefail

# Create a named pipe (FIFO) for inter-process streaming
PIPE="/tmp/stream_pipe_$$"
mkfifo "$PIPE"

# Producer: stream data into the pipe
generate_data() {
    for i in $(seq 1 1000000); do
        echo "record_$i,data_value_$i"
    done
}

# Consumer: read from pipe, transform, write to output
transform_data() {
    local output="$1"
    while IFS=',' read -r key value; do
        echo "${key^^}|${value^^}"  # Uppercase both fields
    done > "$output"
}

# Run producer and consumer in parallel
generate_data > "$PIPE" &
PRODUCER_PID=$!
transform_data "$PIPE" > "output.txt" &
CONSUMER_PID=$!

# Wait for both to finish
wait "$PRODUCER_PID"
wait "$CONSUMER_PID"

# Cleanup
rm -f "$PIPE"
echo "Streaming complete: output.txt"

# Alternative: pipe gzip decompression directly into processing
# gzip -dc large_file.csv.gz | awk -F',' '{print $1","toupper($2)}' > processed.csv

# Stream from S3 without downloading entire file
# aws s3 cp s3://bucket/large-file.csv.gz - | gzip -dc | head -n 1000 > preview.csv
