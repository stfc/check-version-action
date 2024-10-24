"""Tests for comparison.CompareAppVersion"""

from unittest.mock import patch, mock_open
from pathlib import Path
from packaging.version import Version
import pytest
from comparison import CompareAppVersion, VersionNotUpdated


@pytest.fixture(name="instance", scope="function")
def instance_fixture():
    """Provide a fixture instance for the tests"""
    return CompareAppVersion()


@patch("comparison.CompareAppVersion.compare")
@patch("comparison.CompareAppVersion.get_version")
@patch("comparison.CompareAppVersion.read_files")
def test_run(mock_read, mock_get_version, mock_compare, instance):
    """Test the run method makes correct calls."""
    mock_path1 = Path("mock1")
    mock_path2 = Path("mock2")
    mock_read.return_value = ("1.0.0", "1.0.1")
    mock_get_version.side_effect = [Version("1.0.0"), Version("1.0.0")]
    mock_compare.return_value = True
    res = instance.run(mock_path1, mock_path2)
    mock_read.assert_called_once_with(mock_path1, mock_path2)
    mock_get_version.assert_any_call("1.0.0")
    mock_get_version.assert_any_call("1.0.1")
    mock_compare.assert_called_once_with(Version("1.0.0"), Version("1.0.0"))
    assert res


@patch("comparison.CompareAppVersion.compare")
@patch("comparison.CompareAppVersion.get_version")
@patch("comparison.CompareAppVersion.read_files")
def test_run_fails(mock_read, _, mock_compare, instance):
    """Test the run method fails."""
    mock_read.return_value = ("mock1", "mock2")
    mock_compare.side_effect = VersionNotUpdated()
    with pytest.raises(VersionNotUpdated):
        instance.run(Path("mock1"), Path("mock2"))


def test_read_files(instance):
    """Test the read files method returns a tuple"""
    with patch("builtins.open", mock_open(read_data="1.0.0")):
        res = instance.read_files(Path("mock1"), Path("mock2"))
    assert res == ("1.0.0", "1.0.0")


def test_get_version(instance):
    """Test a version object is returned"""
    res = instance.get_version("1.0.0")
    assert isinstance(res, Version)


def test_compare_pass(instance):
    """Test that the compare returns true for a valid comparison"""
    res = instance.compare(Version("1.0.0"), Version("1.0.1"))
    assert res != VersionNotUpdated


def test_compare_fails(instance):
    """Test that the compare returns an error for an invalid comparison"""
    res = instance.compare(Version("1.0.1"), Version("1.0.0"))
    assert res == VersionNotUpdated
