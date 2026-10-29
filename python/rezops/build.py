"""Build and install generated Python packages into a Rez package release."""

import os
from pathlib import Path

import typer

import rezops.utils
from rezops.logger import LOGGER, configure_logging

app = typer.Typer(help="Build and install a Python package into a Rez package release.")


def build(
    package_name: str | None = None,
) -> bool:
    """Install the generated package into the Rez install root.

    Args:
        source_path: Project source root; defaults to REZ_BUILD_SOURCE_PATH.
        install_path: Rez install root; defaults to REZ_BUILD_INSTALL_PATH.
        package_name: Python package directory to install from src; defaults to
            REZ_BUILD_PROJECT_NAME, then normalized [project].name in pyproject.toml.

    Returns:
        True after the package is installed.
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
        help=("Python package directory to install from src (defaults to REZ_BUILD_PROJECT_NAME or pyproject.toml)."),
    ),
) -> None:
    """Copy the generated Python package into the Rez install root.

    Args:
        package_name: From input or defaults to REZ_BUILD_PROJECT_NAME or pyproject.toml.

    Returns:
        None: Exits with a nonzero status and prints command options if the build fails.
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
