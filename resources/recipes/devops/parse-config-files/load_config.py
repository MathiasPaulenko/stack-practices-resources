"""Parse and validate YAML/JSON config with Pydantic."""

import json
import re
import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError


class DatabaseConfig(BaseModel):
    host: str
    port: int = Field(default=5432, ge=1, le=65535)
    username: str
    password: str


class AppConfig(BaseModel):
    app_name: str
    debug: bool = False
    database: DatabaseConfig


def substitute_env_vars(content: str) -> str:
    pattern = re.compile(r"\$\{(\w+)(?::([^}]*))?\}")

    def replacer(match):
        var_name = match.group(1)
        default = match.group(2)
        return os.getenv(var_name, default if default is not None else "")

    return pattern.sub(replacer, content)


def load_config(path: str) -> AppConfig:
    file_path = Path(path)
    raw = substitute_env_vars(file_path.read_text(encoding="utf-8"))

    if file_path.suffix in (".yaml", ".yml"):
        data = yaml.safe_load(raw)
    elif file_path.suffix == ".json":
        data = json.loads(raw)
    else:
        raise ValueError(f"Unsupported config format: {file_path.suffix}")

    return AppConfig.model_validate(data)


if __name__ == "__main__":
    try:
        config = load_config("config.yaml")
        print(f"App: {config.app_name}")
        print(f"DB host: {config.database.host}")
    except ValidationError as e:
        print("Config validation failed:", e)
