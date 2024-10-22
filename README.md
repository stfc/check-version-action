# Check Version
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/stfc/check-version-action/self_test.yaml?label=Intergration%20Test)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/stfc/check-version-action/lint.yaml?label=Linting)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/stfc/check-version-action/test.yaml?label=Tests)
[![codecov](https://codecov.io/gh/stfc/check-version-action/graph/badge.svg?token=OD2Z90ST8R)](https://codecov.io/gh/stfc/check-version-action)


This action compares the application version number from your working branch to the main branch.

You can also check that the **first** image version that appears in your `docker-compose.yaml` file will match the application version

The comparison follows the PEP 440 Version Identification and Dependency Specification.

More detailed information about the versions can be found [here](https://packaging.python.org/en/latest/specifications/version-specifiers/)

# Usage

## Notes:

As of October 2024 GitHub actions using Docker Containers can only be run on GitHub runners using a Linux operating system.<br>
Read here for details: [Link to GitHub docs](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#types-of-actions)

The release tag is extracted and stored in `$GITHUB_ENV`,
you can access this in your workflow with `$ {{ env.release_tag }}` 

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
  # Don't run on main otherwise it will compare main with main
  if: ${{ github.ref != 'refs/heads/main' }} 
  id: version_comparison
  uses: khalford/check-version-action@main
  with:
    # Path to version file from project root
    app_version_path: "version.txt"
    # Optional: To check if compose image version matches application version
    docker_compose_path: "docker-compose.yaml"
    
- name: Log App Success
  if: ${{ env.app_updated == 'true' }}
  run: |
    echo "App version has been updated correctly!"

# Optional: If using the docker compose check
- name: Log Compose Success
  if: ${{ env.compose_updated == 'true' }}
  run: |
    echo "Compose version has been updated correctly!"
```
<!-- end usage -->

