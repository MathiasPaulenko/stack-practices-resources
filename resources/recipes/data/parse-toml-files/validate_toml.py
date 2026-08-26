"""Validate TOML config with Pydantic.

Requires: pip install pydantic
"""
import tomllib
from pydantic import BaseModel, ConfigDict, ValidationError


class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432
    password: str = ""


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    app_name: str
    debug: bool = False
    database: DatabaseConfig


def validate_config(path: str) -> AppConfig:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    try:
        return AppConfig(**raw)
    except ValidationError as e:
        print(f"Config validation failed: {e}")
        raise


if __name__ == "__main__":
    config = validate_config("config.toml")
    print(f"App: {config.app_name}")
    print(f"Debug: {config.debug}")
    print(f"DB Host: {config.database.host}")
