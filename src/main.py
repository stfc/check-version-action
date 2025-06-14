"""This module is the entry point for the Action."""

import os
import json
from pathlib import Path
from features.compose_version import CompareComposeVersion
from features.app_version import CompareAppVersion


def main():
    """
    The entry point function for the action.
    Here we get environment variables then set environment variables when finished.
    """
    # Check if the action should skip version checks
    json_labels = os.environ.get("INPUT_LABELS")
    labels = json.loads(json_labels)
    for label in labels:
        if label in ["documentation", "workflow"]:
            return
    accepted_labels = ["major", "minor", "bug", "patch"]
    matching_labels = [label for label in labels if label in accepted_labels]
    if len(matching_labels) > 1:
        raise RuntimeError(
            f"You can only have one of the following labels: major, minor, bug, patch.\n"
            f"You have provided the following labels: {matching_labels}\n"
        )
    if len(matching_labels) == 0:
        raise RuntimeError(
            f"You must provide at least one of the following labels: major, minor, bug, patch.\n"
            f"You have provided the following labels: {labels}\n"
        )

    # Collect various paths from the environment
    app_path = Path(os.environ.get("INPUT_APP_VERSION_PATH"))
    compose_path = Path(os.environ.get("INPUT_DOCKER_COMPOSE_PATH"))
    root_path = Path(os.environ.get("GITHUB_WORKSPACE"))
    main_path = root_path / "main"
    branch_path = root_path / "branch"

    # Action must compare the app version as the minimum feature.
    CompareAppVersion().run(main_path / app_path, branch_path / app_path, labels)

    # Compare the Docker compose file version if given
    if compose_path:
        CompareComposeVersion().run(branch_path / app_path, branch_path / compose_path)

    with open(os.getenv("GITHUB_ENV"), "a", encoding="utf-8") as env:
        # We can assume these values returned true otherwise they would have raised an error.
        env.write("app_updated=true\n")
        # If Docker compose path was provided we can assume it returned true otherwise there would be an error.
        if compose_path:
            env.write("compose_updated=true")


if __name__ == "__main__":
    main()
