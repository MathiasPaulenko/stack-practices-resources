"""Detect typosquatting and combosquatting of popular package names.

Usage:
    python typosquat_detector.py reqeusts
    python typosquat_detector.py --scan requirements.txt
"""
import difflib
import sys


class TyposquatDetector:
    POPULAR_PACKAGES = [
        "requests", "flask", "django", "fastapi", "numpy",
        "pandas", "scipy", "matplotlib", "tensorflow", "torch",
        "transformers", "pytest", "celery", "redis", "sqlalchemy",
        "pydantic", "uvicorn", "gunicorn", "httpx", "aiohttp",
    ]

    def detect_typosquats(self, package_name: str, threshold: float = 0.8) -> list:
        """Detect if a package name is a typosquat of a popular package."""
        typosquats = []

        for popular in self.POPULAR_PACKAGES:
            similarity = difflib.SequenceMatcher(None, package_name, popular).ratio()
            if similarity >= threshold and package_name != popular:
                typosquats.append({
                    "package": package_name,
                    "mimics": popular,
                    "similarity": similarity,
                    "reason": self._get_reason(package_name, popular),
                })

        return typosquats

    def _get_reason(self, name: str, target: str) -> str:
        if name == target + "s" or name == target + "2":
            return f"Appended suffix to {target}"
        if name == target.replace("s", ""):
            return f"Removed trailing 's' from {target}"
        if name == target.replace("-", "_") or name == target.replace("_", "-"):
            return f"Changed separator in {target}"
        if len(name) == len(target) and sum(a != b for a, b in zip(name, target)) <= 2:
            return f"Character substitution in {target}"
        return f"Similar to {target}"

    def scan_dependencies(self, dependencies: list) -> dict:
        """Scan all dependencies for typosquats."""
        results = {}
        for dep in dependencies:
            name = dep.split("==")[0].split(">=")[0].split("<=")[0].strip()
            typosquats = self.detect_typosquats(name)
            if typosquats:
                results[name] = typosquats
        return results


if __name__ == "__main__":
    detector = TyposquatDetector()

    if len(sys.argv) > 2 and sys.argv[1] == "--scan":
        with open(sys.argv[2]) as f:
            deps = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        results = detector.scan_dependencies(deps)
        for pkg, typosquats in results.items():
            for ts in typosquats:
                print(f"WARNING: {ts['package']} mimics {ts['mimics']} ({ts['reason']})")
    elif len(sys.argv) > 1:
        print(detector.detect_typosquats(sys.argv[1]))
    else:
        deps = ["requests==2.31.0", "flask==3.0.0", "reqeusts==1.0.0", "numpyy==1.0.0"]
        results = detector.scan_dependencies(deps)
        for pkg, typosquats in results.items():
            for ts in typosquats:
                print(f"WARNING: {ts['package']} mimics {ts['mimics']} ({ts['reason']})")
