"""The comparison module which is where the main check classes are."""

from pathlib import Path
import semver
from base import Base, VersionNotUpdated


class CompareAppVersion(Base):
    """This class compares the application version to the updated semantic version."""

    def run(self, path1: Path, target_version) -> bool:
        """
        Entry point to compare application versions.
        :param path1: Path to main version
        :param target_version: The updated Semantic Version
        :return: true if success, error if fail
        """
        branch_content = self.read_files(path1)
        if semver.compare(str(target_version), branch_content) == 1:
            raise VersionNotUpdated(
                f"The version in {('/'.join(str(path1).split('/')[4:]))[0:]} has not been updated correctly."
            )
        return True

    @staticmethod
    def read_files(path1: Path) -> str:
        """
        Read both version files and return the contents
        :param path1: Path to branched version
        :return: branch_ver
        """
        with open(path1, "r", encoding="utf-8") as file1:
            content1 = file1.read()
        return content1


class CompareComposeVersion(Base):
    """This class compares the docker compose image version to the updated semantic version."""

    def run(self, compose: Path, target_version) -> bool:
        """
        Entry point to compare docker compose and updated semantic versions.
        :param compose: Path to compose image version
        :param target_version: Updated Semantic Version
        :return: true if success, error if fail
        """
        compose_content = self.read_files(compose)
        if semver.compare(str(target_version), compose_content) == 1:
            raise VersionNotUpdated(
                f"The version in {('/'.join(str(compose).split('/')[4:]))[0:]} has not been updated correctly."
            )
        return True

    @staticmethod
    def read_files(compose: Path) -> str:
        """
        Read both version files and return the contents
        :param compose: Path to compose version
        :return: branch_ver
        """
        with open(compose, "r", encoding="utf-8") as file1:
            content1 = file1.read()
        return content1
