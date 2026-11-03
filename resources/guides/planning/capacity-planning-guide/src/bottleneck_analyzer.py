"""Bottleneck analyzer for capacity planning.

Evaluates per-resource headroom against saturation thresholds and reports
which resource is the effective capacity ceiling.

Usage: python bottleneck_analyzer.py
"""
from dataclasses import dataclass


@dataclass
class ResourceLimit:
    name: str
    current_usage: float
    max_capacity: float
    saturation_threshold: float

    def headroom(self) -> float:
        return (self.saturation_threshold - self.current_usage) / self.saturation_threshold * 100

    def utilization(self) -> float:
        return self.current_usage / self.max_capacity * 100


resources = [
    ResourceLimit("CPU", 45, 100, 70),
    ResourceLimit("Memory", 60, 100, 80),
    ResourceLimit("Disk IOPS", 75, 100, 85),
    ResourceLimit("Network", 30, 100, 70),
]

for r in sorted(resources, key=lambda r: r.headroom()):
    print(f"{r.name:12s} usage {r.utilization():5.1f}% | headroom to threshold: {r.headroom():5.1f}%")

bottleneck = min(resources, key=lambda r: r.headroom())
print(f"\nBottleneck: {bottleneck.name} with {bottleneck.headroom():.1f}% headroom")
print("Provision against this resource first — it's your effective capacity ceiling.")
