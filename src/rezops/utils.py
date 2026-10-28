"""Shared helpers for Rez package builds."""

import shutil
from pathlib import Path

import rezops.logger

# Create a utils logger
LOGGER = rezops.logger.LOGGER.getChild("utils")


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
