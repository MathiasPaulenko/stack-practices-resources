"""Weighted risk scoring for vendor assessments.

Companion to the vendor risk assessment template. Feed it the raw 1-5
scores per category and it returns the weighted total and decision band
defined by the template.
"""

from dataclasses import dataclass, field


@dataclass
class VendorRiskScorer:
    scores: dict  # category -> score (1-5)
    weights: dict = field(default_factory=lambda: {
        "security": 0.30,
        "compliance": 0.25,
        "operational": 0.20,
        "data_protection": 0.25,
    })

    @property
    def total_score(self) -> float:
        return round(sum(
            self.scores.get(cat, 0) * weight
            for cat, weight in self.weights.items()
        ), 2)

    @property
    def decision(self) -> str:
        score = self.total_score
        if score >= 4.0:
            return "LOW RISK — standard contract, annual review"
        if score >= 3.0:
            return "MEDIUM RISK — remediation plan, 6-month review"
        if score >= 2.0:
            return "HIGH RISK — improvements required before onboarding"
        return "CRITICAL RISK — do not onboard without CISO approval"

    @property
    def critical_gaps(self) -> list:
        return [
            f"{cat}: {score}/5 is critical"
            for cat, score in self.scores.items() if score <= 2
        ]

    def report(self) -> str:
        lines = ["Vendor Risk Assessment Report", "=" * 40]
        for cat, score in self.scores.items():
            weight = self.weights.get(cat, 0)
            lines.append(
                f"  {cat}: {score}/5 "
                f"(weight: {weight:.0%}, weighted: {score * weight:.2f})"
            )
        lines.append(f"\n  Total Score: {self.total_score}/5.0")
        lines.append(f"  Decision: {self.decision}")
        if self.critical_gaps:
            lines.append(f"  Critical Gaps: {', '.join(self.critical_gaps)}")
        return "\n".join(lines)


if __name__ == "__main__":
    scorer = VendorRiskScorer(scores={
        "security": 4,
        "compliance": 5,
        "operational": 3,
        "data_protection": 4,
    })
    print(scorer.report())
