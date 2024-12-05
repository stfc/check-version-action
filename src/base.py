"""This is the base module including helper/abstract classes and errors."""

from abc import ABC, abstractmethod
from pathlib import Path
import semver


class VersionNotUpdated(Exception):
    """The version number has not been updated or updated incorrectly."""


class Base(ABC):
    """The base abstract class to build features on."""

    @abstractmethod
    def run(self, path1: Path, target_version: semver) -> bool:
        """
        This method is the entry point to the feature.
        It should take a file path to retrieve a version from and the new Semantic Version and return the comparison result.
        """

    @staticmethod
    @abstractmethod
    def read_files(path1: Path) -> str:
        """This method should read the contents of the compared files and return the strings"""
