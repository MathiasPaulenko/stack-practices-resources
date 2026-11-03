import sys

def estimate_cache_size(avg_value_bytes: int, num_entries: int) -> int:
    overhead_per_entry = 64  # Approximate overhead per entry in Python dict
    total_bytes = (avg_value_bytes + overhead_per_entry) * num_entries
    return total_bytes

# Example: 10,000 users, average 500 bytes each
size = estimate_cache_size(500, 10_000)
print(f"Estimated cache size: {size / 1024 / 1024:.1f} MB")
