"""Compare app version.txt on main to the branch."""

from pathlib import Path
from typing import Union, Type

from packaging.version import Version


class CompareAppVersion:
    """This class compares the app versions"""

    def run(self, path1: Path, path2: Path) -> bool:
        """
        Entry point to compare app versions.
        :param path1: Path to main version
        :param path2: Path to branch version
        :return: true if success, error if fail
        """
        main_content, branch_content = self.read_files(path1, path2)
        main_ver = self.get_version(main_content)
        branch_ver = self.get_version(branch_content)
        comparison = self.compare(main_ver, branch_ver)
        if comparison == RuntimeError:
            raise RuntimeError(
                f"The version in {('/'.join(str(path2).split('/')[4:]))[0:]} has not been updated correctly."
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
    def compare(main: Version, branch: Version) -> Union[bool, Type[RuntimeError]]:
        """
        Returns if the branch version is larger than the main version
        :param main: Version on main
        :param branch: Version on branch
        :return: If the version update is correct return true, else return error
        """
        if branch > main:
            return True
        return RuntimeError
