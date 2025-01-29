"""This module is the entry point for the Action."""

import os
from pathlib import Path
from src.features.compose_version import CompareComposeVersion
from src.features.app_version import CompareAppVersion


def main() -> bool:
    """
    The entry point function for the action.
    Here we get environment variables then set environment variables when finished.
    """
    # Check if the action should skip version checks
    for label in os.environ.get("INPUT_LABELS"):
        if label in ["documentation", "workflow"]:
            return False

    # Collect various paths from the environment
    app_path = Path(os.environ.get("INPUT_APP_VERSION_PATH"))
    compose_path = Path(os.environ.get("INPUT_DOCKER_COMPOSE_PATH"))
    root_path = Path(os.environ.get("GITHUB_WORKSPACE"))
    main_path = root_path / "main"
    branch_path = root_path / "branch"

    # Action must compare the app version as the minimum feature.
    CompareAppVersion().run(main_path / app_path, branch_path / app_path)

    # Compare the Docker compose file version if given
    if compose_path:
        CompareComposeVersion().run(branch_path / app_path, branch_path / compose_path)

    with open(os.getenv("GITHUB_ENV"), "a", encoding="utf-8") as env:
        # We can assume these values returned true otherwise they would have raised an error.
        env.write("app_updated=true\n")
        # If Docker compose path was provided we can assume it returned true otherwise there would be an error.
        if compose_path:
            env.write("compose_updated=true")

    return True


if __name__ == "__main__":
    main()
