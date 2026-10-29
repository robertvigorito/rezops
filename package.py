"""Rez package definition for rezops."""

import subprocess

name = "rezops"
version = subprocess.check_output(["rezops-get-version"]).decode().strip()
description = "Contain code to help with rez operations."
requires = []
private_build_requires = []
build_command = f"rezops-build {name}"


def commands() -> bool:
    """Expose the generated package and optional Nuke tools in Rez.

    Returns:
        bool: ``True`` after updating the Rez environment.
    """
    env.PYTHONPATH.append("{root}/python")  # noqa: F821 -- Rez injects ``env`` at runtime.

    return True
