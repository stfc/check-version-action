"""This is the base module including helper/abstract classes and errors."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from packaging.version import Version


class VersionNotUpdated(Exception):
    """The version number has not been updated or updated incorrectly."""


class Base(ABC):
    """The base abstract class to build features on."""

    @abstractmethod
    def run(self, path1: Path, path2: Path) -> bool:
        """
        This method is the entry point to the feature.
        It should take two paths and return the comparison result.
        """

    @staticmethod
    @abstractmethod
    def read_files(path1: Path, path2: Path) -> (str, str):
        """This method should read the contents of the compared files and return the strings"""

    @staticmethod
    @abstractmethod
    def get_version(content: str) -> Version:
        """This method should extract the version from the file and return it as a packaging Version object"""

    @staticmethod
    @abstractmethod
    def compare(version1: Version, version2: Version) -> Union[bool, VersionNotUpdated]:
        """This method should compare the versions and return a bool status"""
