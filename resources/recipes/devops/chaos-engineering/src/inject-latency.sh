#!/bin/bash
# Add 500ms latency to egress traffic on eth0 for 60 seconds, then clean up.
# Usage: sudo ./inject-latency.sh   (needs root for tc)

echo "Injecting 500ms latency for 60 seconds..."
tc qdisc add dev eth0 root netem delay 500ms 50ms distribution normal

sleep 60

echo "Removing latency..."
tc qdisc del dev eth0 root

ping -c 5 api.example.com
