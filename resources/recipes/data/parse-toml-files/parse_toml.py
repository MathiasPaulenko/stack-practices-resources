"""Parse and write TOML files in Python.

Requires Python 3.11+ (tomllib in stdlib) or tomli for older versions.
For writing: pip install tomli-w
"""
import tomllib
from pathlib import Path


def read_toml(path: str) -> dict:
    """Read a TOML file and return a dictionary."""
    with open(path, "rb") as f:
        return tomllib.load(f)


def write_toml(data: dict, path: str) -> None:
    """Write a dictionary to a TOML file. Requires tomli-w."""
    import tomli_w
    with open(path, "wb") as f:
        tomli_w.dump(data, f)


def merge_configs(base_path: str, env: str = "dev") -> dict:
    """Load base config and merge environment-specific overrides."""
    base = tomllib.loads(Path(base_path).read_text())
    env_file = Path(f"config/{env}.toml")
    if env_file.exists():
        override = tomllib.loads(env_file.read_text())
        return _deep_merge(base, override)
    return base


def _deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


if __name__ == "__main__":
    config = read_toml("config.toml")
    print(config["app"]["name"])
    print(config["database"]["host"])
    print(len(config.get("servers", [])))
