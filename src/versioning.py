from typing import List

import semver
from pathlib import Path


def get_semver(file: Path) -> semver:
    with open(file, "r", encoding="utf-8") as release_file:
        return release_file.read().strip("\n")


def read_file(path1: Path) -> str:
    """
    Read both version files and return the contents
    :param path1: Path to branched version
    :return: branch_ver
    """
    with open(path1, "r", encoding="utf-8") as file1:
        content1 = file1.read()
    return content1


def bump_semver_by_label(old_semver: semver.Version, labels: List[str]) -> semver.Version:
    for label in labels:

        if label == "major":
            bumped_semver = old_semver.bump_major()
        elif label == "minor":
            bumped_semver = old_semver.bump_minor()
        elif label == "patch":
            bumped_semver = old_semver.bump_patch()

    return bumped_semver
