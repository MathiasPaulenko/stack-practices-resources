"""Parse YAML with PyYAML: safe_load, anchors/merge keys, and safe_dump."""
import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

print("app:", config["app"]["name"], config["app"]["version"])
print("database host:", config["database"]["host"])
# The merge key copies `defaults` into `production`; retries is overridden
print("production:", config["production"])
print("staging:", config["staging"])
print("features:", config["features"])

# Write back with safe_dump (comments are not preserved by PyYAML)
print(yaml.safe_dump({"app": config["app"]}, default_flow_style=False, sort_keys=False))
