#!/bin/bash
# Toxiproxy network chaos for a MySQL dependency.
# Usage: ./toxiproxy-setup.sh   (needs docker + toxiproxy-cli)

docker run -p 8474:8474 -p 3306:3306 ghcr.io/shopify/toxiproxy:latest

toxiproxy-cli create mysql-proxy -l 0.0.0.0:3306 -u 127.0.0.1:3307

# 2000ms latency on MySQL connections
toxiproxy-cli toxic add mysql-proxy -n latency -t latency=2000

# Hard timeout: connections drop after 500ms
# toxiproxy-cli toxic add mysql-proxy -n timeout -t timeout=500

# Cleanup:
# toxiproxy-cli toxic delete mysql-proxy -n latency
