#!/usr/bin/env bash
# Verification commands — run against a container started with run-hardened.sh
# or the compose stack. Each should PASS / fail closed.
set -uo pipefail
C=${1:-myapp}

echo "== user =="
docker exec "$C" id   # expect uid=1001

echo "== read-only rootfs =="
docker exec "$C" touch /etc/breakme && echo "FAIL: writable" || echo "PASS: read-only"

echo "== capabilities =="
docker exec "$C" grep CapEff /proc/1/status
# decode: capsh --decode=<hex>

echo "== limits =="
docker inspect --format='memory={{.HostConfig.Memory}} pids={{.HostConfig.PidsLimit}} cpus={{.HostConfig.NanoCpus}}' "$C"

echo "== published ports (bind addr) =="
docker inspect --format='{{json .NetworkSettings.Ports}}' "$C"

echo "== seccomp/security opts =="
docker inspect --format='{{.HostConfig.SecurityOpt}}' "$C"

echo "== log rotation =="
docker inspect --format='{{json .HostConfig.LogConfig}}' "$C"

echo "== secrets not in env =="
docker inspect --format='{{json .Config.Env}}' "$C" | grep -icE "password|secret|token" || echo "PASS: none"

echo "== history check =="
docker history myapp:hardened --no-trunc | grep -icE "password|secret|token" || echo "PASS: clean"
