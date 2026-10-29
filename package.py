"""Rez package definition for rezops."""

name = "rezops"
version = "0.1.0"
description = "Build Python packages for Rez package releases."
requires = []
private_build_requires = []
build_command = f"rezops-build {name}"


def commands() -> bool:
    """Add the installed Python package directory to Rez's Python path.

    Returns:
        True after adding the Python package directory to ``PYTHONPATH``.
    """
    env.PYTHONPATH.append("{root}/python")  # noqa: F821 -- Rez injects ``env`` at runtime.

    return True
