import hashlib
import re
from collections import defaultdict
from typing import List, Dict

def normalize_stack_trace(trace: str) -> str:
    """Normalize a stack trace by removing line numbers and memory addresses."""
    # Remove file paths, keeping only filenames
    trace = re.sub(r'/[\w/.-]+/', '', trace)
    # Remove line numbers
    trace = re.sub(r':\d+', '', trace)
    # Remove memory addresses
    trace = re.sub(r'0x[0-9a-fA-F]+', '0xADDR', trace)
    # Remove thread IDs
    trace = re.sub(r'Thread-\d+', 'Thread-N', trace)
    return trace.strip()

def fingerprint_stack_trace(trace: str) -> str:
    """Generate a hash fingerprint from a normalized stack trace."""
    normalized = normalize_stack_trace(trace)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]

def group_bug_reports(reports: List[Dict]) -> Dict[str, List[Dict]]:
    """Group bug reports by stack trace fingerprint."""
    groups = defaultdict(list)
    for report in reports:
        trace = report.get("stack_trace", "")
        if trace:
            fp = fingerprint_stack_trace(trace)
            groups[fp].append(report)
        else:
            groups["no-trace"].append(report)
    return groups

# Example usage
bug_reports = [
    {"id": "BUG-001", "stack_trace": "TypeError at /app/src/handlers.py:42\n  File /app/src/utils.py:128"},
    {"id": "BUG-002", "stack_trace": "TypeError at /app/src/handlers.py:45\n  File /app/src/utils.py:131"},
    {"id": "BUG-003", "stack_trace": "ValueError at /app/src/models.py:67"},
]

groups = group_bug_reports(bug_reports)
for fp, reports in groups.items():
    print(f"Fingerprint {fp}: {len(reports)} reports - {[r['id'] for r in reports]}")
