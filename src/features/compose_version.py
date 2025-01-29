"""Compare Docker compose image version to the version.txt."""

from pathlib import Path
from typing import List, Union, Type

from packaging.version import Version


class CompareComposeVersion:
    """This class compares the docker compose image version to the app version."""

    def run(self, app: Path, compose: Path) -> bool:
        """
        Entry point to compare docker compose and app versions.
        :param app: Path to app version
        :param compose: Path to compose image version
        :return: true if success, error if fail
        """
        app_content, compose_content = self.read_files(app, compose)
        app_ver = Version(app_content)
        compose_ver = self.get_version(compose_content)
        comparison = self.compare(app_ver, compose_ver)
        if comparison == RuntimeError:
            raise RuntimeError(
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
    def compare(app: Version, compose: Version) -> Union[bool, Type[RuntimeError]]:
        """
        Returns if the app version and docker compose version are equal.
        :param app: App version
        :param compose: Compose version
        :return: If the version update is correct return true, else return error
        """
        if app == compose:
            return True
        return RuntimeError
