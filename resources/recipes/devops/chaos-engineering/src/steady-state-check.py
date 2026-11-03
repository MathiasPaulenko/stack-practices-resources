# Steady-state SLO checker: run before, during and after chaos experiments.
# Usage: python steady-state-check.py
import requests
import time
import sys

def check_steady_state():
    """Verify SLOs before, during, and after chaos experiments."""
    checks = [
        ("https://api.example.com/health", 200, 500),  # URL, expected_status, max_latency_ms
        ("https://api.example.com/metrics", 200, 1000),
    ]
    all_pass = True
    for url, expected_status, max_latency in checks:
        try:
            start = time.time()
            resp = requests.get(url, timeout=5)
            latency_ms = (time.time() - start) * 1000
            if resp.status_code != expected_status:
                print(f"FAIL: {url} returned {resp.status_code}, expected {expected_status}")
                all_pass = False
            elif latency_ms > max_latency:
                print(f"FAIL: {url} latency {latency_ms:.0f}ms exceeds {max_latency}ms")
                all_pass = False
            else:
                print(f"OK: {url} - {resp.status_code} in {latency_ms:.0f}ms")
        except requests.RequestException as e:
            print(f"FAIL: {url} unreachable: {e}")
            all_pass = False
    return all_pass

if __name__ == "__main__":
    if not check_steady_state():
        print("Steady state violated. Aborting experiment.")
        sys.exit(1)
    print("Steady state confirmed. Safe to proceed.")
