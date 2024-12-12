"""The comparison module which is where the main check classes are."""

from pathlib import Path
import semver
from base import VersionNotUpdated


class CompareVersion:
    """This class compares the application version to the updated semantic version."""

    @staticmethod
    def run(path1: Path, file_semver, target_version) -> bool:
        """
        Entry point to compare application versions.
        :param path1: Path to main version
        :param file_semver - the version extracted from the updated file
        :param target_version: The updated Semantic Version that the file version should match
        :return: true if success, error if fail
        """

        if semver.compare(str(target_version), file_semver) == 1:
            raise VersionNotUpdated(
                f"The version in {('/'.join(str(path1).split('/')[4:]))[0:]} has not been updated correctly."
            )
        return True
