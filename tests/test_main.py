"""Tests for main"""

import semver
from unittest.mock import patch, mock_open
from pathlib import Path

from src.main import bump_semver_by_label, main


@patch("main.CompareComposeVersion")
@patch("main.CompareAppVersion")
@patch("main.os")
def test_main(mock_os, mock_compare_app, mock_compare_compose):
    """Test the main method runs correctly."""
    mock_os.environ.get.side_effect = [
        Path("app"),
        Path("compose"),
        Path("workspace"),
        [],
    ]

    with patch("builtins.open", mock_open(read_data="1.0.0")):
        res = main()
    mock_os.environ.get.assert_any_call("INPUT_LABELS")
    mock_os.environ.get.assert_any_call("INPUT_APP_VERSION_PATH")
    mock_os.environ.get.assert_any_call("INPUT_DOCKER_COMPOSE_PATH")
    mock_os.environ.get.assert_any_call("GITHUB_WORKSPACE")
    mock_branch_path = Path("workspace") / "branch"
    mock_compare_app.return_value.run.assert_called_once_with(
        mock_branch_path / "app", "1.0.0"
    )
    mock_compare_compose.return_value.run.assert_called_once_with(
        mock_branch_path / "compose", "1.0.0"
    )
    assert res

def test_bump_semver_by_label():
    old_semver = semver.Version.parse("1.2.3")
    labels = ["major"]
    new_version = bump_semver_by_label(old_semver, labels)
    assert semver.compare(str(new_version), "2.0.0") == 0

@patch("main.os")
def test_main_skip(mock_os):
    """Test the main method skips the comparison methods."""
    mock_os.environ.get.side_effect = [
        Path("app"),
        Path("compose"),
        Path("workspace"),
        ["workflow", "documentation"],
    ]
    with patch("builtins.open", mock_open(read_data="1.0.0")):
        res = main()
    assert not res
