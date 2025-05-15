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
        label_discrepancy = self.check_label(labels, main_ver, branch_ver)
        if not comparison:
            raise RuntimeError(
                f"The branch version file contains a version that is older than the main version file.\n"
                f"You cannot go back in versions.\n"
                f"Please make sure you have updated the version correctly.\n"
                f"File where error was detected {('/'.join(str(path2).split('/')[4:]))[0:]}\n"
            )
        if label_discrepancy:
            raise RuntimeError(
                f"Your labels do not match the version change you are making.\n"
                f"See the below message for more information.\n"
                f"{label_discrepancy}\n"
                f"Please update your version file or the labels on this pull request.\n"
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
    ) -> str:
        """
        Check that the semver change used in the labels is the same as the actual change.
        :param labels: Labels on the pull request
        :param main_version: Version on the main branch
        :param branch_version: Version on the pull request branch
        :return: If change is the same or not.
        """
        accepted_labels = ["major", "minor", "bug", "patch"]
        given_label = [label for label in labels if label in accepted_labels][0]
        if given_label in ["bug", "patch"]:
            given_label = "micro"
        error = ""
        if given_label == "major":
            if branch_version.minor != 0:
                error += (
                    "When making a major version change, minor version should be 0.\n"
                )
            if branch_version.micro != 0:
                error += (
                    "When making a major version change, micro version should be 0.\n"
                )
        if given_label == "minor":
            if branch_version.micro != 0:
                error += (
                    "When making a minor version change, micro version should be 0.\n"
                )
            if not branch_version.major == main_version.major:
                error += "When making a minor version change, major version should be the same.\n"
        if given_label == "micro":
            if not branch_version.major == main_version.major:
                error += "When making a micro version change, major version should be the same.\n"
            if not branch_version.minor == main_version.minor:
                error += "When making a micro version change, minor version should be the same.\n"
        return error
