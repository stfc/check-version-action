"""Tests for main.py"""

from unittest.mock import patch, mock_open
from pathlib import Path
import pytest
from main import main


@patch("main.CompareComposeVersion")
@patch("main.CompareAppVersion")
@patch("main.os")
def test_main(mock_os, mock_compare_app, mock_compare_compose):
    """Test the main method runs correctly."""
    mock_os.environ.get.side_effect = [
        '["patch"]',
        Path("app"),
        Path("compose"),
        Path("workspace"),
    ]

    with patch("builtins.open", mock_open(read_data="1.0.0")):
        main()
    mock_os.environ.get.assert_any_call("INPUT_LABELS")
    mock_os.environ.get.assert_any_call("INPUT_APP_VERSION_PATH")
    mock_os.environ.get.assert_any_call("INPUT_DOCKER_COMPOSE_PATH")
    mock_os.environ.get.assert_any_call("GITHUB_WORKSPACE")
    mock_branch_path = Path("workspace") / "branch"
    mock_main_path = Path("workspace") / "main"
    mock_compare_app.return_value.run.assert_called_once_with(
        mock_main_path / "app", mock_branch_path / "app", ["patch"]
    )
    mock_compare_compose.return_value.run.assert_called_once_with(
        mock_branch_path / "app", mock_branch_path / "compose"
    )


@patch("main.os")
def test_main_skip(mock_os):
    """Test the main method skips the comparison methods."""
    mock_os.environ.get.side_effect = [
        '["workflow", "documentation"]',
        Path("app"),
        Path("compose"),
        Path("workspace"),
    ]
    with patch("builtins.open", mock_open(read_data="1.0.0")):
        main()


@patch("main.os")
def test_main_too_many_labels(mock_os):
    """Test the main method skips the comparison methods."""
    mock_os.environ.get.side_effect = [
        '["patch", "minor"]',
        Path("app"),
        Path("compose"),
        Path("workspace"),
    ]
    with patch("builtins.open", mock_open(read_data="1.0.0")):
        with pytest.raises(RuntimeError):
            main()


@patch("main.os")
def test_main_too_little_labels(mock_os):
    """Test the main method skips the comparison methods."""
    mock_os.environ.get.side_effect = [
        '["useless_label"]',
        Path("app"),
        Path("compose"),
        Path("workspace"),
    ]
    with patch("builtins.open", mock_open(read_data="1.0.0")):
        with pytest.raises(RuntimeError):
            main()
