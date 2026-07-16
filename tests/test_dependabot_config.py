"""Tests for Dependabot configuration."""

import pathlib
import yaml
import pytest

DEPENDABOT_PATH = pathlib.Path(__file__).parent.parent / ".github" / "dependabot.yml"


@pytest.fixture(scope="module")
def dependabot_config():
    return yaml.safe_load(DEPENDABOT_PATH.read_text())


def test_dependabot_config_file_exists():
    assert DEPENDABOT_PATH.exists(), f"Expected {DEPENDABOT_PATH} to exist"


def test_updates_key_present(dependabot_config):
    assert "updates" in dependabot_config
    assert len(dependabot_config["updates"]) > 0


def test_pip_ecosystem_present(dependabot_config):
    ecosystems = [u["package-ecosystem"] for u in dependabot_config["updates"]]
    assert "pip" in ecosystems


def test_github_actions_ecosystem_present(dependabot_config):
    ecosystems = [u["package-ecosystem"] for u in dependabot_config["updates"]]
    assert "github-actions" in ecosystems


def test_all_updates_have_schedule(dependabot_config):
    for update in dependabot_config["updates"]:
        assert "schedule" in update, f"{update['package-ecosystem']} saknar schedule"
        assert "interval" in update["schedule"]
