"""Tests for features.app_version.CompareAppVersion"""

from unittest.mock import patch, mock_open
from pathlib import Path
from packaging.version import Version
import pytest
from features.app_version import CompareAppVersion


@pytest.fixture(name="instance", scope="function")
def instance_fixture():
    """Provide a fixture instance for the tests"""
    return CompareAppVersion()


@patch("features.app_version.CompareAppVersion.get_version")
@patch("features.app_version.CompareAppVersion.read_files")
def test_run(mock_read, mock_get_version, instance):
    """Test the run method makes correct calls."""
    mock_path1 = Path("mock1")
    mock_path2 = Path("mock2")
    mock_read.return_value = ("1.0.0", "1.0.1")
    mock_get_version.side_effect = [Version("1.0.0"), Version("1.0.1")]
    res = instance.run(mock_path1, mock_path2, ["patch"])
    mock_read.assert_called_once_with(mock_path1, mock_path2)
    mock_get_version.assert_any_call("1.0.0")
    mock_get_version.assert_any_call("1.0.1")
    assert res


@patch("features.app_version.CompareAppVersion.get_version")
@patch("features.app_version.CompareAppVersion.read_files")
def test_run_fails_comparison(mock_read, mock_get_version, instance):
    """Test the run method fails on the comparison check."""
    mock_read.return_value = ("1.0.0", "0.1.0")
    mock_get_version.side_effect = [Version("1.0.0"), Version("0.1.0")]
    with pytest.raises(RuntimeError):
        instance.run(Path("mock1"), Path("mock2"), ["patch"])


@patch("features.app_version.CompareAppVersion.get_version")
@patch("features.app_version.CompareAppVersion.read_files")
def test_run_fails_check_label(mock_read, mock_get_version, instance):
    """Test the run method fails on the comparison check."""
    mock_read.return_value = ("1.0.0", "1.1.1")
    mock_get_version.side_effect = [Version("1.0.0"), Version("1.1.1")]
    with pytest.raises(RuntimeError):
        instance.run(Path("mock1"), Path("mock2"), ["minor"])


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
    """Test that the compare returns true for a valid features.app_version"""
    res = instance.compare(Version("1.0.0"), Version("1.0.1"))
    assert res


def test_compare_fails(instance):
    """Test that the compare returns an error for an invalid features.app_version"""
    res = instance.compare(Version("1.0.1"), Version("1.0.0"))
    assert not res


def test_check_label(instance):
    """Test that the check passes for a correct version change"""
    res = instance.check_label(["major"], Version("1.0.0"), Version("2.0.0"))
    assert res == ""


def test_check_label_fails_major(instance):
    """Test the function returns the correct error messages for major changes."""
    res = instance.check_label(["major"], Version("1.0.0"), Version("2.0.1"))
    assert res == "When making a major version change, micro version should be 0.\n"
    res2 = instance.check_label(["major"], Version("1.0.0"), Version("2.1.0"))
    assert res2 == "When making a major version change, minor version should be 0.\n"


def test_check_label_fails_minor(instance):
    """Test the function returns the correct error messages for minor changes."""
    res = instance.check_label(["minor"], Version("1.0.0"), Version("1.1.1"))
    assert res == "When making a minor version change, micro version should be 0.\n"
    res2 = instance.check_label(["minor"], Version("1.0.0"), Version("2.1.0"))
    assert (
        res2
        == "When making a minor version change, major version should be the same.\n"
    )


def test_check_label_fails_micro(instance):
    """Test the function returns the correct error messages for micro changes."""
    res = instance.check_label(["patch"], Version("1.0.0"), Version("1.1.1"))
    assert (
        res == "When making a micro version change, minor version should be the same.\n"
    )
    res2 = instance.check_label(["bug"], Version("1.0.0"), Version("2.0.1"))
    assert (
        res2
        == "When making a micro version change, major version should be the same.\n"
    )
