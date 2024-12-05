"""This module is the entry point for the Action."""

import os
from typing import List

import semver
from pathlib import Path
from comparison import CompareAppVersion, CompareComposeVersion


def main() -> bool:
    """
    The entry point function for the action.
    Here we get environment variables then set environment variables when finished.
    """
    app_path, compose_path, root_path = get_env_vars()
    main_path = root_path / "main"
    branch_path = root_path / "branch"

    # get the old semver before changes
    # get new semver
    # compare the two versions
    labels = get_labels()
    if should_skip_step(labels):
        return False

    old_semver = get_semver(main_path / app_path)
    new_semver = bump_semver_by_label(old_semver, labels)
    # incremented_correctly = semver_incremented_correctly(old_semver, new_semver)

    CompareAppVersion().run(branch_path / app_path, new_semver)
    if compose_path:
        compose_path = Path(compose_path)
        CompareComposeVersion().run(branch_path / compose_path, new_semver)

    github_env = os.getenv("GITHUB_ENV")
    with open(github_env, "a", encoding="utf-8") as env:
        # We can assume either/both of these values returned true otherwise they would have errored
        env.write("app_updated=true\n")
        if compose_path:
            env.write("compose_updated=true")
        env.write(f"release_tag={release_version}")
    return True


def get_env_vars():
    app_path = Path(os.environ.get("INPUT_APP_VERSION_PATH"))
    compose_path = os.environ.get("INPUT_DOCKER_COMPOSE_PATH")
    root_path = Path(os.environ.get("GITHUB_WORKSPACE"))
    return app_path, compose_path, root_path


def should_skip_step(labels) -> bool:
    for label in labels:
        if label in ["documentation", "workflow"]:
            return False

def get_semver(file: Path) -> semver:
    with open(file, "r", encoding="utf-8") as release_file:
        return release_file.read().strip("\n")


def bump_semver_by_label(semver: semver.Version, labels: List[str]) -> semver.Version:
    for label in labels:

        if label == "major":
            bumped_semver = semver.bump_major()
        elif label == "minor":
            bumped_semver = semver.bump_minor()
        elif label == "patch":
            bumped_semver = semver.bump_patch()

    return bumped_semver

def semver_incremented_correctly(old_semver, new_semver) -> bool:
    # todo
    pass

def get_labels() -> List[str]:
    labels = os.environ.get("INPUT_LABELS")
    return labels


if __name__ == "__main__":
    main()
