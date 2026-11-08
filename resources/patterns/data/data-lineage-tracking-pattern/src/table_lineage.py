"""Simple in-memory table-level lineage — no column detail.

Good enough when you only need "which tables feed which"; upgrade to
OpenLineage + a real backend when you need column-level impact analysis.
"""
from datetime import datetime


class TableLineage:
    def __init__(self):
        self.edges = []  # list of {source, target, job, recorded_at}

    def record(self, source, target, job):
        self.edges.append({
            "source": source,
            "target": target,
            "job": job,
            "recorded_at": datetime.now().isoformat()
        })

    def get_downstream(self, table):
        """Find all tables that depend on this table (BFS)."""
        visited = set()
        queue = [table]
        result = []

        while queue:
            current = queue.pop(0)
            for edge in self.edges:
                if edge["source"] == current and edge["target"] not in visited:
                    visited.add(edge["target"])
                    result.append(edge["target"])
                    queue.append(edge["target"])

        return result


if __name__ == "__main__":
    lineage = TableLineage()
    lineage.record("source.customers", "warehouse.customers", "etl.customers_daily")
    lineage.record("warehouse.customers", "revenue_dashboard", "bi.sync")
    lineage.record("warehouse.customers", "churn_model", "ml.train")

    print(lineage.get_downstream("source.customers"))
    # ['warehouse.customers', 'revenue_dashboard', 'churn_model']
