# cutover.py — track migration progress and cutover readiness
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RouteMigration:
    method: str
    path: str
    status: str  # "legacy", "shadow", "canary", "migrated", "verified"
    legacy_latency_ms: float
    new_latency_ms: float
    error_rate_legacy: float
    error_rate_new: float

class CutoverTracker:
    def __init__(self):
        self.routes: List[RouteMigration] = []

    def add_route(self, route: RouteMigration):
        self.routes.append(route)

    def migration_progress(self) -> dict:
        total = len(self.routes)
        migrated = sum(1 for r in self.routes if r.status == "migrated")
        verified = sum(1 for r in self.routes if r.status == "verified")
        in_progress = sum(1 for r in self.routes if r.status in ("shadow", "canary"))

        return {
            "total_routes": total,
            "migrated": migrated,
            "verified": verified,
            "in_progress": in_progress,
            "still_legacy": total - migrated - verified - in_progress,
            "progress_pct": (migrated + verified) / total * 100 if total else 0
        }

    def ready_for_cutover(self) -> bool:
        """All routes must be verified before legacy can be decommissioned."""
        return all(r.status == "verified" for r in self.routes)

    def cutover_report(self) -> str:
        progress = self.migration_progress()
        report = f"""
        === Strangler Fig Cutover Report ===
        Total routes: {progress['total_routes']}
        Migrated:     {progress['migrated']}
        Verified:     {progress['verified']}
        In progress:  {progress['in_progress']}
        Still legacy: {progress['still_legacy']}
        Progress:     {progress['progress_pct']:.1f}%
        Ready for cutover: {'YES' if self.ready_for_cutover() else 'NO'}
        """
        return report
