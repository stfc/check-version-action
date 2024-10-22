"""The comparison module which is where the main check classes are."""

from pathlib import Path
from typing import Union, List, Type

from packaging.version import Version
from base import Base, VersionNotUpdated


class CompareAppVersion(Base):
    """This class compares the application versions"""

    def run(self, path1: Path, path2: Path) -> bool:
        """
        Entry point to compare application versions.
        :param path1: Path to main version
        :param path2: Path to branch version
        :return: true if success, error if fail
        """
        main_content, branch_content = self.read_files(path1, path2)
        main_ver = self.get_version(main_content)
        branch_ver = self.get_version(branch_content)
        comparison = self.compare(main_ver, branch_ver)
        if comparison == VersionNotUpdated:
            raise VersionNotUpdated(
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
        For application versions we expect nothing else in the file than the version.
        :param content: Application version string
        :return: Application version object
        """
        return Version(content)

    @staticmethod
    def compare(main: Version, branch: Version) -> Union[bool, Type[VersionNotUpdated]]:
        """
        Returns if the branch version is larger than the main version
        :param main: Version on main
        :param branch: Version on branch
        :return: If the version update is correct return true, else return error
        """
        if branch > main:
            return True
        return VersionNotUpdated


class CompareComposeVersion(Base):
    """This class compares the docker compose image version to the application version."""

    def run(self, app: Path, compose: Path) -> bool:
        """
        Entry point to compare docker compose and application versions.
        :param app: Path to application version
        :param compose: Path to compose image version
        :return: true if success, error if fail
        """
        app_content, compose_content = self.read_files(app, compose)
        app_ver = Version(app_content)
        compose_ver = self.get_version(compose_content)
        comparison = self.compare(app_ver, compose_ver)
        if comparison == VersionNotUpdated:
            raise VersionNotUpdated(
                f"The version in {('/'.join(str(compose).split('/')[4:]))[0:]}"
                f"does not match {('/'.join(str(app).split('/')[4:]))[0:]}."
            )
        return True

    @staticmethod
    def read_files(app: Path, compose: Path) -> (str, List):
        """
        Read both version files and return the contents
        :param app: Path to app version
        :param compose: Path to compose version
        :return: main_ver, branch_ver
        """
        with open(app, "r", encoding="utf-8") as file1:
            content1 = file1.read()
        with open(compose, "r", encoding="utf-8") as file2:
            content2 = file2.readlines()
        return content1, content2

    @staticmethod
    def get_version(content: List[str]) -> Version:
        """
        This method returns the version from the file as an object
        For compose versions we have to do some data handling.
        :param content: Compose version string
        :return: Compose version object
        """
        version_str = ""
        for line in content:
            if "image" in line:
                version_str = line.strip("\n").split(":")[-1]
                break
        return Version(version_str)

    @staticmethod
    def compare(app: Version, compose: Version) -> Union[bool, Type[VersionNotUpdated]]:
        """
        Returns if the application version and docker compose version are equal.
        :param app: App version
        :param compose: Compose version
        :return: If the version update is correct return true, else return error
        """
        if app == compose:
            return True
        return VersionNotUpdated
