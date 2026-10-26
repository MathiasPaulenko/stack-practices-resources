# Deterministic user assignment for A/B tests
# Same user + same experiment name always lands in the same bucket.
# Including the experiment name in the hash keeps assignments independent
# across concurrent experiments.
import hashlib


def get_experiment_group(user_id: str, experiment_name: str, num_groups: int = 2) -> str:
    """Deterministically assign a user to an experiment group based on a hash."""
    hash_input = f"{experiment_name}:{user_id}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    bucket = hash_value % num_groups

    groups = ["control", "treatment"] if num_groups == 2 else [
        f"group_{i}" for i in range(num_groups)
    ]
    return groups[bucket]


if __name__ == "__main__":
    user_id = "user-12345"
    experiment = "checkout-redesign"
    group = get_experiment_group(user_id, experiment)
    print(f"User assigned to: {group}")
