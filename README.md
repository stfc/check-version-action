# Check Version
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/stfc/check-version-action/self_test.yaml?label=Integration%20Test)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/stfc/check-version-action/lint.yaml?label=Linting)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/stfc/check-version-action/test.yaml?label=Tests)
[![codecov](https://codecov.io/gh/stfc/check-version-action/graph/badge.svg?token=OD2Z90ST8R)](https://codecov.io/gh/stfc/check-version-action)


This action compares the app version number from your working branch to the main branch.
The pull request must have one of the below labels matching the version change.<br>

`major | minor | bug | patch`

You can also check that the **first** image version that appears in your `docker-compose.yaml` file matches the app version

The comparison follows the PEP 440 Version Identification and Dependency Specification.

More detailed information about the versions can be found [here](https://packaging.python.org/en/latest/specifications/version-specifiers/)

# Usage

## Notes:

As of October 2024 GitHub actions using Docker Containers can only be run on GitHub runners using a Linux operating system.<br>
Read here for details: [Link to GitHub docs](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#types-of-actions)

The release tag is extracted and stored in `$GITHUB_ENV`,
you can access this in your workflow with `$ {{ env.release_tag }}` 

If you are making a change which should not affect the version such as README or CI changes. You can label the pull request with `documentation` or `workflow` and the version checks will be skipped.

<!-- start usage -->
```yaml
- name: Checkout main
  uses: actions/checkout@v4
  with:
    # Change to "master" if needed
    ref: 'main'
    # Do not change the path here
    path: 'main'

- name: Checkout current working branch
  uses: actions/checkout@v4
  with:
    # Do not change the path here
    path: 'branch'
    
- name: Compare versions
  # Don't run on main otherwise it compares main with main
  if: ${{ github.ref != 'refs/heads/main' }} 
  id: version_comparison
  uses: stfc/check-version-action@main
  with:
    # Path to version file from project root
    app_version_path: "version.txt"
    # Optional: to check if Docker compose image version matches app version
    docker_compose_path: "docker-compose.yaml"
    labels: ${{ toJSON(github.event.pull_request.labels.*.name) }}
```
<!-- end usage -->

