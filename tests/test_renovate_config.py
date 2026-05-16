"""Tests for .github/renovate.json configuration.

Covers the changes introduced in the PR:
- Patch-only automerge (removed "minor" from matchUpdateTypes, set automerge=true)
- devDependencies group gets automerge=true
"""

import json
import pathlib

import pytest

RENOVATE_CONFIG_PATH = pathlib.Path(__file__).parent.parent / ".github" / "renovate.json"


@pytest.fixture(scope="module")
def renovate_config():
    """Load and parse the renovate.json configuration file."""
    return json.loads(RENOVATE_CONFIG_PATH.read_text())


# ---------------------------------------------------------------------------
# Basic validity
# ---------------------------------------------------------------------------


def test_renovate_config_file_exists():
    """The renovate.json file must exist in .github/."""
    assert RENOVATE_CONFIG_PATH.exists(), f"Expected {RENOVATE_CONFIG_PATH} to exist"


def test_renovate_config_is_valid_json():
    """renovate.json must be valid JSON."""
    content = RENOVATE_CONFIG_PATH.read_text()
    parsed = json.loads(content)
    assert isinstance(parsed, dict)


def test_renovate_config_has_package_rules(renovate_config):
    """packageRules key must be present and non-empty."""
    assert "packageRules" in renovate_config
    assert isinstance(renovate_config["packageRules"], list)
    assert len(renovate_config["packageRules"]) > 0


# ---------------------------------------------------------------------------
# PR change 1: patch-only automerge rule
# ---------------------------------------------------------------------------


def _get_patch_automerge_rule(renovate_config):
    """Return the packageRule that targets matchUpdateTypes with 'patch'."""
    for rule in renovate_config["packageRules"]:
        if "matchUpdateTypes" in rule and "patch" in rule["matchUpdateTypes"]:
            return rule
    return None


def test_patch_rule_exists(renovate_config):
    """There must be a packageRule that matches the 'patch' update type."""
    rule = _get_patch_automerge_rule(renovate_config)
    assert rule is not None, "No packageRule found that matches 'patch' updateType"


def test_patch_rule_automerge_is_true(renovate_config):
    """The patch update-type rule must have automerge set to true (PR change)."""
    rule = _get_patch_automerge_rule(renovate_config)
    assert rule is not None
    assert rule.get("automerge") is True, (
        f"Expected automerge=true for patch rule, got {rule.get('automerge')!r}"
    )


def test_patch_rule_does_not_include_minor(renovate_config):
    """'minor' must NOT be in the patch rule's matchUpdateTypes (PR removed it)."""
    rule = _get_patch_automerge_rule(renovate_config)
    assert rule is not None
    update_types = rule.get("matchUpdateTypes", [])
    assert "minor" not in update_types, (
        f"'minor' should have been removed from matchUpdateTypes but found: {update_types}"
    )


def test_patch_rule_contains_only_patch(renovate_config):
    """The automerge rule should match exactly ['patch'] update types."""
    rule = _get_patch_automerge_rule(renovate_config)
    assert rule is not None
    update_types = rule.get("matchUpdateTypes", [])
    assert update_types == ["patch"], (
        f"Expected matchUpdateTypes=['patch'], got {update_types!r}"
    )


def test_patch_rule_automerge_is_not_false(renovate_config):
    """Regression: automerge must not revert to false for the patch rule."""
    rule = _get_patch_automerge_rule(renovate_config)
    assert rule is not None
    assert rule.get("automerge") is not False, (
        "automerge was reverted to false for patch rule"
    )


# ---------------------------------------------------------------------------
# PR change 2: devDependencies rule gets automerge=true
# ---------------------------------------------------------------------------


def _get_dev_dep_rule(renovate_config):
    """Return the packageRule that targets devDependencies."""
    for rule in renovate_config["packageRules"]:
        dep_types = rule.get("matchDepTypes", [])
        if "devDependencies" in dep_types:
            return rule
    return None


def test_dev_dep_rule_exists(renovate_config):
    """There must be a packageRule that targets devDependencies."""
    rule = _get_dev_dep_rule(renovate_config)
    assert rule is not None, "No packageRule found for devDependencies"


def test_dev_dep_rule_automerge_is_true(renovate_config):
    """The devDependencies rule must have automerge=true (PR change)."""
    rule = _get_dev_dep_rule(renovate_config)
    assert rule is not None
    assert rule.get("automerge") is True, (
        f"Expected automerge=true for devDependencies rule, got {rule.get('automerge')!r}"
    )


def test_dev_dep_rule_group_name_preserved(renovate_config):
    """The devDependencies rule must still have groupName='dev-dependencies'."""
    rule = _get_dev_dep_rule(renovate_config)
    assert rule is not None
    assert rule.get("groupName") == "dev-dependencies", (
        f"groupName was changed, expected 'dev-dependencies', got {rule.get('groupName')!r}"
    )


def test_dev_dep_rule_matches_dev_dependencies(renovate_config):
    """matchDepTypes for the dev-dependencies rule must include 'devDependencies'."""
    rule = _get_dev_dep_rule(renovate_config)
    assert rule is not None
    dep_types = rule.get("matchDepTypes", [])
    assert "devDependencies" in dep_types


def test_dev_dep_rule_automerge_is_not_missing(renovate_config):
    """Regression: automerge key must be present in the devDependencies rule."""
    rule = _get_dev_dep_rule(renovate_config)
    assert rule is not None
    assert "automerge" in rule, (
        "automerge key is missing from the devDependencies packageRule"
    )


# ---------------------------------------------------------------------------
# Unchanged rules: github-actions rule should remain intact
# ---------------------------------------------------------------------------


def _get_github_actions_rule(renovate_config):
    """Return the packageRule that targets github-actions manager."""
    for rule in renovate_config["packageRules"]:
        managers = rule.get("matchManagers", [])
        if "github-actions" in managers:
            return rule
    return None


def test_github_actions_rule_still_present(renovate_config):
    """The github-actions packageRule must still be present (not accidentally removed)."""
    rule = _get_github_actions_rule(renovate_config)
    assert rule is not None, "github-actions packageRule is missing"


def test_github_actions_rule_group_name(renovate_config):
    """The github-actions rule must retain its groupName."""
    rule = _get_github_actions_rule(renovate_config)
    assert rule is not None
    assert rule.get("groupName") == "github-actions"


def test_github_actions_rule_has_no_automerge(renovate_config):
    """The github-actions rule should NOT have automerge set (unchanged from before PR)."""
    rule = _get_github_actions_rule(renovate_config)
    assert rule is not None
    assert "automerge" not in rule, (
        "automerge was unexpectedly added to the github-actions packageRule"
    )


# ---------------------------------------------------------------------------
# Structural integrity checks
# ---------------------------------------------------------------------------


def test_exactly_three_package_rules(renovate_config):
    """There should be exactly 3 packageRules (patch, devDeps, github-actions)."""
    rules = renovate_config["packageRules"]
    assert len(rules) == 3, f"Expected 3 packageRules, found {len(rules)}"


def test_no_duplicate_automerge_false(renovate_config):
    """No packageRule should have automerge=false after the PR changes."""
    for rule in renovate_config["packageRules"]:
        assert rule.get("automerge") is not False, (
            f"Found automerge=false in rule: {rule!r}"
        )


def test_both_automerge_rules_present(renovate_config):
    """Both the patch rule and devDependencies rule must have automerge=true."""
    patch_rule = _get_patch_automerge_rule(renovate_config)
    dev_rule = _get_dev_dep_rule(renovate_config)
    assert patch_rule is not None
    assert dev_rule is not None
    assert patch_rule.get("automerge") is True
    assert dev_rule.get("automerge") is True
