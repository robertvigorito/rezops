"""Rez package definition for rezops."""

name = "rezops"
version = "0.1.0"
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
