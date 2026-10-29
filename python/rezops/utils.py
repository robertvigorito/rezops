"""Shared helpers for Rez package builds."""

import os
import shutil
from pathlib import Path

import rezops.logger

try:
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:  # Python 3.10 compatibility.
    import tomli as tomllib  # type: ignore[import-not-found]

# Create a utils logger
LOGGER = rezops.logger.LOGGER.getChild("utils")


def _read_project_metadata(source_path: Path | None = None) -> dict[str, object]:
    """Read the [project] metadata from a pyproject.toml file.

    Args:
        source_path: Project root; defaults to REZ_BUILD_SOURCE_PATH or the current directory.

    Returns:
        The parsed project metadata table.

    Raises:
        ValueError: If pyproject.toml is missing, invalid, or lacks [project].
    """
    project_root = source_path
    if project_root is None:
        environment_path = os.environ.get("REZ_BUILD_SOURCE_PATH")
        project_root = Path(environment_path) if environment_path else Path.cwd()

    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.is_file():
        raise ValueError(f"Project configuration not found: {pyproject_path}")

    try:
        with pyproject_path.open("rb") as pyproject_file:
            pyproject_data = tomllib.load(pyproject_file)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ValueError(f"Unable to read project configuration from {pyproject_path}: {error}") from error

    project_metadata = pyproject_data.get("project")
    if not isinstance(project_metadata, dict):
        raise ValueError(f"Missing [project] table in {pyproject_path}")
    return project_metadata


def get_version(source_path: Path | None = None) -> str:
    """Get the static project version from pyproject.toml.

    Args:
        source_path: Project root; defaults to REZ_BUILD_SOURCE_PATH or the current directory.

    Returns:
        The version declared in [project].version.

    Raises:
        ValueError: If [project].version is missing or is not a non-empty string.
    """
    project_metadata = _read_project_metadata(source_path)
    version = project_metadata.get("version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("[project].version must be a non-empty static version string")
    return version


def get_requires(source_path: Path | None = None) -> list[str]:
    """Get project dependencies from pyproject.toml for Rez package requirements.

    Args:
        source_path: Project root; defaults to REZ_BUILD_SOURCE_PATH or the current directory.

    Returns:
        Dependency requirement strings declared in [project].dependencies.

    Raises:
        ValueError: If dependencies is not a list of non-empty strings.
    """
    project_metadata = _read_project_metadata(source_path)
    dependencies = project_metadata.get("dependencies", [])
    if not isinstance(dependencies, list):
        raise ValueError("[project].dependencies must be a list of requirement strings")

    requires: list[str] = []
    for dependency in dependencies:
        if not isinstance(dependency, str) or not dependency.strip():
            raise ValueError("Every [project].dependencies entry must be a non-empty string")
        requires.append(dependency)
    return requires


def copy_directory(source: Path, target: Path) -> bool:
    """Copy a source directory to a target location.

    Args:
        source: Source directory to install.
        target: Destination path in the Rez install root.

    Returns:
        True when the operation succeeds.
    """
    LOGGER.info("Copying %s to %s", source, target)
    if target.is_dir() and target.exists():
        LOGGER.info("Removing existing build target: %s", target)
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    return True
