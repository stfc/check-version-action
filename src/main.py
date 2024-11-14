"""This module is the entry point for the Action."""

import os
from pathlib import Path
from comparison import CompareAppVersion, CompareComposeVersion


def main():
    """
    The entry point function for the action.
    Here we get environment variables then set environment variables when finished.
    """
    app_path = Path(os.environ.get("INPUT_APP_VERSION_PATH"))
    compose_path = os.environ.get("INPUT_DOCKER_COMPOSE_PATH")
    root_path = Path(os.environ.get("GITHUB_WORKSPACE"))
    main_path = root_path / "main"
    branch_path = root_path / "branch"
    with open(branch_path / app_path, "r", encoding="utf-8") as release_file:
        release_version = release_file.read().strip("\n")

    labels = os.environ.get("INPUT_LABELS")
    if not any(label in labels for label in ["documentation", "workflow"]):
        CompareAppVersion().run(main_path / app_path, branch_path / app_path)
        if compose_path:
            compose_path = Path(compose_path)
            CompareComposeVersion().run(branch_path / app_path, branch_path / compose_path)

        github_env = os.getenv("GITHUB_ENV")
        with open(github_env, "a", encoding="utf-8") as env:
            # We can assume either/both of these values returned true otherwise they would have errored
            env.write("app_updated=true\n")
            if compose_path:
                env.write("compose_updated=true")
            env.write(f"release_tag={release_version}")


if __name__ == "__main__":
    main()
