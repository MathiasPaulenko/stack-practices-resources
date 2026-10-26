# Sample size calculation for an A/B test (two-proportion z-test)
# Requires: scipy
import scipy.stats as stats


def calculate_sample_size(
    baseline_rate: float,     # Current conversion rate
    mde: float,               # Minimum detectable effect (absolute)
    alpha: float = 0.05,      # Significance level
    power: float = 0.80,      # Statistical power
    ratio: float = 1.0        # Ratio of treatment to control
) -> int:
    """Calculate required sample size per group for a two-proportion test."""
    p1 = baseline_rate
    p2 = baseline_rate + mde

    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    pooled_p = (p1 + ratio * p2) / (1 + ratio)

    numerator = (
        z_alpha * (pooled_p * (1 - pooled_p) * (1 + 1 / ratio)) ** 0.5 +
        z_beta * (p1 * (1 - p1) + p2 * (1 - p2) / ratio) ** 0.5
    ) ** 2

    denominator = (p1 - p2) ** 2

    return int(numerator / denominator) + 1


if __name__ == "__main__":
    # Example: 20% baseline conversion, want to detect 2% absolute improvement
    sample_size = calculate_sample_size(
        baseline_rate=0.20,
        mde=0.02,
        alpha=0.05,
        power=0.80
    )
    print(f"Required sample size per group: {sample_size}")
    # Output: ~6,500 users per group
