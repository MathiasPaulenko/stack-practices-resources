import re
import subprocess
from typing import Dict, List

class PRChecklistValidator:
    def __init__(self, pr_diff: str, pr_description: str):
        self.diff = pr_diff
        self.description = pr_description

    def check_tests_added(self) -> bool:
        """Verify that new code includes tests."""
        has_source = bool(re.search(r'\+\+\+ b/src/.*\.py', self.diff))
        has_tests = bool(re.search(r'\+\+\+ b/tests/.*\.py', self.diff))
        if has_source and not has_tests:
            return False
        return True

    def check_no_secrets(self) -> bool:
        """Check for common secret patterns in the diff."""
        secret_patterns = [
            r'(?i)api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'(?i)password\s*=\s*["\'][^"\']+["\']',
            r'(?i)secret\s*=\s*["\'][^"\']+["\']',
            r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
            r'(?i)aws_secret_access_key\s*=\s*["\'][^"\']+["\']',
        ]
        added_lines = [line for line in self.diff.split('\n') if line.startswith('+')]
        for line in added_lines:
            for pattern in secret_patterns:
                if re.search(pattern, line):
                    return False
        return True

    def check_pr_description(self) -> bool:
        """Verify PR description has required sections."""
        required_sections = ["## Summary", "## Testing", "## Breaking Changes"]
        return all(section in self.description for section in required_sections)

    def run_all_checks(self) -> List[Dict]:
        """Run all checklist validations and return results."""
        checks = [
            ("Tests added for new code", self.check_tests_added),
            ("No secrets in diff", self.check_no_secrets),
            ("PR description complete", self.check_pr_description),
        ]
        results = []
        for name, check_fn in checks:
            passed = check_fn()
            results.append({
                "check": name,
                "passed": passed,
                "status": "PASS" if passed else "FAIL",
            })
        return results

# Example usage: diff and description of the current branch vs main
diff = subprocess.run(
    ["git", "diff", "origin/main...HEAD"],
    capture_output=True, text=True
).stdout
pr_description = subprocess.run(
    ["git", "log", "-1", "--pretty=%B"],
    capture_output=True, text=True
).stdout

validator = PRChecklistValidator(diff, pr_description)
results = validator.run_all_checks()
for r in results:
    print(f"{r['status']}: {r['check']}")
