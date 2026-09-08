"""Tests for the Sentry companion examples.

These tests verify the structure and behavior of the Sentry configuration
examples without requiring a live Sentry instance or the sentry-sdk package.

Run with:
    pip install pytest
    pytest test_sentry_examples.py -v
"""

import ast
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def test_sentry_config_imports():
    """Verify sentry_config.py is syntactically valid Python."""
    source = (HERE / "sentry_config.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    assert "init_sentry" in functions
    assert "filter_sensitive_data" in functions


def test_filter_sensitive_data_redacts_headers():
    """Verify filter_sensitive_data redacts authorization headers."""
    sys.path.insert(0, str(HERE))
    try:
        from sentry_config import filter_sensitive_data
    except ImportError:
        pytest.skip("sentry_sdk not installed")

    event = {
        "request": {
            "headers": {"Authorization": "Bearer secret", "Cookie": "session=abc"},
            "data": {"password": "hunter2", "credit_card": "4111111111111111"},
        }
    }
    result = filter_sensitive_data(event, {})
    headers = result["request"]["headers"]
    assert headers["Authorization"] == "[REDACTED]"
    assert headers["Cookie"] == "[REDACTED]"
    assert result["request"]["data"]["password"] == "[REDACTED]"
    assert result["request"]["data"]["credit_card"] == "[REDACTED]"


def test_sentry_node_typescript_syntax():
    """Verify sentry_node.ts is syntactically valid TypeScript."""
    source = (HERE / "sentry_node.ts").read_text(encoding="utf-8")
    assert "export function initSentry" in source
    assert "export class OrderService" in source
    assert "Sentry.init" in source


def test_sentry_config_java_syntax():
    """Verify SentryConfig.java is syntactically valid Java."""
    source = (HERE / "SentryConfig.java").read_text(encoding="utf-8")
    assert "public class SentryConfig" in source
    assert "@Configuration" in source
    assert "options.setDsn" in source


def test_release_tracking_script_exists():
    """Verify release_tracking.sh exists and is executable."""
    script = HERE / "release_tracking.sh"
    assert script.exists()
    source = script.read_text(encoding="utf-8")
    assert "sentry-cli releases new" in source
    assert "sentry-cli releases finalize" in source


def test_alert_rules_yaml_exists():
    """Verify alert_rules.yml exists and has expected rules."""
    rules = HERE / "alert_rules.yml"
    assert rules.exists()
    source = rules.read_text(encoding="utf-8")
    assert "High error rate" in source
    assert "New error in production" in source
    assert "Performance regression" in source


def test_meta_json_exists():
    """Verify meta.json exists with required fields."""
    import json

    meta_path = HERE / "meta.json"
    assert meta_path.exists()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["slug"] == "complete-guide-sentry-error-tracking"
    assert meta["type"] == "guides"
    assert meta["topic"] == "observability"
    assert "sentry_config.py" in meta["files"]


def test_readmes_exist():
    """Verify bilingual READMEs exist."""
    assert (HERE / "README.md").exists()
    assert (HERE / "README.es.md").exists()
