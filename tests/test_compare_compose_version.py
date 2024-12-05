"""Tests for comparison.CompareComposeVersion"""

from unittest.mock import patch, mock_open
from pathlib import Path
import pytest
from src.comparison import CompareComposeVersion, VersionNotUpdated


@pytest.fixture(name="instance", scope="function")
def instance_fixture():
    """Provide a fixture instance for the tests"""
    return CompareComposeVersion()


@patch("comparison.CompareComposeVersion.read_files")
def test_run(mock_read, instance):
    """Test the run method makes correct calls."""
    mock_path1 = Path("mock1")
    mock_read.return_value = "1.0.0"
    res = instance.run(mock_path1, "1.0.0")
    mock_read.assert_called_once_with(mock_path1)
    assert res


@patch("comparison.CompareComposeVersion.read_files")
def test_run_fails(mock_read, instance):
    """Test the run method fails."""
    mock_read.return_value = "1.0.0"
    with pytest.raises(VersionNotUpdated):
        instance.run(Path("mock1"), "1.0.1")


def test_read_files(instance):
    """Test the read files method returns a tuple"""
    with patch("builtins.open", mock_open(read_data="1.0.0")):
        res = instance.read_files(Path("mock1"))
    assert res == "1.0.0"
