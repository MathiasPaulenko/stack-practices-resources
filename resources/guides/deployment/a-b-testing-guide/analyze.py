# Experiment result analysis (two-proportion z-test)
# Requires: statsmodels — proportions_ztest lives there, not in scipy.
from statsmodels.stats.proportion import proportions_ztest


def analyze_experiment(control_converted: int, control_total: int,
                       treatment_converted: int, treatment_total: int) -> dict:
    """Run a two-proportion z-test and return rates, lift and p-value."""
    control_rate = control_converted / control_total
    treatment_rate = treatment_converted / treatment_total

    _, p_value = proportions_ztest(
        [control_converted, treatment_converted],
        [control_total, treatment_total]
    )

    relative_lift = (treatment_rate - control_rate) / control_rate

    return {
        "control_rate": control_rate,
        "treatment_rate": treatment_rate,
        "relative_lift": relative_lift,
        "p_value": p_value,
        "significant": p_value < 0.05
    }


if __name__ == "__main__":
    result = analyze_experiment(
        control_converted=1300, control_total=6500,
        treatment_converted=1430, treatment_total=6500
    )
    print(result)
