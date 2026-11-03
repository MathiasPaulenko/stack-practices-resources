from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List

@dataclass
class ReviewMetric:
    pr_number: int
    author: str
    reviewer: str
    created_at: datetime
    merged_at: datetime
    comments_count: int
    blockers_count: int
    post_merge_defects: int

def calculate_review_metrics(metrics: List[ReviewMetric]) -> Dict:
    """Calculate aggregate review metrics for the team."""
    if not metrics:
        return {}

    cycle_times = [(m.merged_at - m.created_at).total_seconds() / 3600 for m in metrics]
    comment_counts = [m.comments_count for m in metrics]
    defect_rate = sum(1 for m in metrics if m.post_merge_defects > 0) / len(metrics)

    by_reviewer = defaultdict(list)
    for m in metrics:
        by_reviewer[m.reviewer].append(m)

    reviewer_stats = {}
    for reviewer, reviews in by_reviewer.items():
        reviewer_stats[reviewer] = {
            "total_reviews": len(reviews),
            "avg_comments": sum(r.comments_count for r in reviews) / len(reviews),
            "avg_blockers": sum(r.blockers_count for r in reviews) / len(reviews),
            "defects_missed": sum(r.post_merge_defects for r in reviews),
        }

    return {
        "avg_cycle_time_hours": sum(cycle_times) / len(cycle_times),
        "avg_comments_per_pr": sum(comment_counts) / len(comment_counts),
        "defect_escape_rate": defect_rate,
        "by_reviewer": reviewer_stats,
    }

# Example usage
metrics = [
    ReviewMetric(101, "alice", "bob", datetime.now() - timedelta(hours=5), datetime.now(), 3, 1, 0),
    ReviewMetric(102, "charlie", "bob", datetime.now() - timedelta(hours=2), datetime.now(), 5, 2, 1),
    ReviewMetric(103, "alice", "dave", datetime.now() - timedelta(hours=8), datetime.now(), 1, 0, 0),
]

results = calculate_review_metrics(metrics)
print(f"Average cycle time: {results['avg_cycle_time_hours']:.1f}h")
print(f"Defect escape rate: {results['defect_escape_rate']:.0%}")
