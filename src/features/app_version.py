"""Compare app version.txt on main to the branch."""

from pathlib import Path
from typing import List

from packaging.version import Version


class CompareAppVersion:
    """This class compares the app versions"""

    def run(self, path1: Path, path2: Path, labels: List[str]) -> bool:
        """
        Entry point to compare app versions.
        :param path1: Path to main version
        :param path2: Path to branch version
        :param labels: Labels provided in the pull request
        :return: true if success, error if fail
        """
        main_content, branch_content = self.read_files(path1, path2)
        main_ver = self.get_version(main_content)
        branch_ver = self.get_version(branch_content)
        comparison = self.compare(main_ver, branch_ver)
        same_as_label = self.check_label(labels, main_ver, branch_ver)
        if not comparison:
            raise RuntimeError(
                f"The version in {('/'.join(str(path2).split('/')[4:]))[0:]} has not been updated correctly."
            )
        if not same_as_label:
            raise RuntimeError(
                f"The version in {('/'.join(str(path2).split('/')[4:]))[0:]} "
                f"does not reflect the labels on the pull request."
            )
        return True

    @staticmethod
    def read_files(path1: Path, path2: Path) -> (str, str):
        """
        Read both version files and return the contents
        :param path1: Path to main version
        :param path2: Path to branched version
        :return: main_ver, branch_ver
        """
        with open(path1, "r", encoding="utf-8") as file1:
            content1 = file1.read()
        with open(path2, "r", encoding="utf-8") as file2:
            content2 = file2.read()
        return content1, content2

    @staticmethod
    def get_version(content: str) -> Version:
        """
        This method returns the version from the file as an object
        For app versions we expect nothing else in the file than the version.
        :param content: app version string
        :return: app version object
        """
        return Version(content)

    @staticmethod
    def compare(main: Version, branch: Version) -> bool:
        """
        Returns if the branch version is larger than the main version
        :param main: Version on main
        :param branch: Version on branch
        :return: If the version update is correct return true, else return error
        """
        return branch > main

    @staticmethod
    def check_label(
        labels: List[str], main_version: Version, branch_version: Version
    ) -> bool:
        """
        Check that the semver change used in the labels is the same as the actual change.
        :param labels: Labels on the pull request
        :param main_version: Version on the main branch
        :param branch_version: Version on the pull request branch
        :return: If change is the same or not.
        """
        if main_version.major != branch_version.major:
            if "major" not in labels:
                return False
        if main_version.minor != branch_version.minor:
            if "minor" not in labels:
                return False
        if main_version.micro != branch_version.micro:
            if "bug" not in labels and "patch" not in labels:
                return False
        return True
