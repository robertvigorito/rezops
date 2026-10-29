"""Build and install Python packages into Rez package releases."""

import os
from pathlib import Path

import typer

from rezops.logger import LOGGER, configure_logging
import rezops.utils


app = typer.Typer(help="Install a Python package into a Rez package release.")


def build(
    package_name: str | None = None,
) -> bool:
    """Install a Python package from the Rez source root into the install root.

    Args:
        package_name: Python package directory under ``src``; defaults to
            ``REZ_BUILD_PROJECT_NAME``.

    Returns:
        True when the package is installed; False when required build inputs are missing.
    """
    rez_source_path = Path(os.getenv("REZ_BUILD_SOURCE_PATH", ""))
    rez_install_path = Path(os.getenv("REZ_BUILD_INSTALL_PATH", ""))
    rez_project_name = package_name or os.environ.get("REZ_BUILD_PROJECT_NAME", "")
    if not any([rez_source_path.exists(), rez_install_path.exists(), rez_project_name]):
        LOGGER.error("Missing required environment variables or package name, skipping build...")
        return False

    # Log all the rez information
    LOGGER.info("Rez package name: %s", rez_project_name)
    LOGGER.info("Rez source path: %s", rez_source_path)
    LOGGER.info("Rez install path: %s", rez_install_path)
    resolved_source_path = rez_source_path / "src" / rez_project_name
    rezops.utils.copy_directory(resolved_source_path, rez_install_path / "python" / rez_project_name)

    # This will handle any additional subfolders in the source path, copying them to the install path.
    # For example nuke or houdini or any dcc related subfolders.
    for subfolder in resolved_source_path.parent.iterdir():
        if not subfolder.is_dir() or subfolder.name == rez_project_name:
            continue
        subfolder_target = rez_install_path / subfolder.name
        LOGGER.info("Copying subfolder %s to %s", subfolder, subfolder_target)
        # rezops.utils.copy_directory(subfolder, subfolder_target)

    LOGGER.info("Build completed successfully")
    return True


@app.command()
def build_command(
    _: typer.Context,
    package_name: str | None = typer.Argument(
        None,
        help="Python package directory to install from src (defaults to REZ_BUILD_PROJECT_NAME or pyproject.toml).",
    ),
) -> None:
    """Install a Python package into the Rez install root.

    Args:
        package_name: Python package directory under ``src``; defaults to
            ``REZ_BUILD_PROJECT_NAME``.

    Returns:
        None: Runs the package installation command.
    """
    configure_logging()
    build(package_name=package_name)


def main() -> None:
    """Run the rezops command-line application.

    Returns:
        None: Typer manages the process exit status.
    """
    app()


if __name__ == "__main__":
    main()
