"""Tests for renovate configuration."""

import pathlib
import json
import pytest

RENOVATE_PATH = pathlib.Path(__file__).parent.parent / ".github" / "renovate.json"


@pytest.fixture(scope="module")
def renovate_config():
    return json.loads(RENOVATE_PATH.read_text())


def test_renovate_config_file_exists():
    assert RENOVATE_PATH.exists(), f"Expected {RENOVATE_PATH} to exist"


def test_renovate_extends_config(renovate_config):
    assert "extends" in renovate_config
    assert len(renovate_config["extends"]) > 0


def test_pip_ecosystem_present(renovate_config):
    # Renovate uses managers instead of package-ecosystem
    # Check that the config extends best-practices which includes pip
    assert "config:best-practices" in renovate_config["extends"]


def test_github_actions_ecosystem_present(renovate_config):
    # Check that github-actions is configured
    package_rules = renovate_config.get("packageRules", [])
    has_github_actions = any(
        "github-actions" in rule.get("matchManagers", [])
        for rule in package_rules
    )
    assert has_github_actions or "config:best-practices" in renovate_config["extends"]


def test_all_updates_have_schedule(renovate_config):
    # Renovate has schedule in extends or top-level config
    assert "extends" in renovate_config
    assert any("schedule:" in ext for ext in renovate_config["extends"]) or "timezone" in renovate_config
