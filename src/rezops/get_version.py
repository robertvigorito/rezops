"""Typer command for reading a project's pyproject version."""

from pathlib import Path

import typer

from rezops.utils import get_version

app = typer.Typer(help="Read project metadata from pyproject.toml.")


@app.command()
def get_version_command(
    source_path: Path | None = typer.Option(
        None,
        "--source-path",
        help="Project root (defaults to REZ_BUILD_SOURCE_PATH or the current directory).",
    ),
) -> None:
    """Print the project version from pyproject.toml.

    Args:
        source_path: Project root containing pyproject.toml.

    Returns:
        None: Prints the version or exits with an error for invalid metadata.
    """
    try:
        version = get_version(source_path)
    except (OSError, ValueError) as error:
        typer.echo(f"rezops-get-version: {error}", err=True)
        raise typer.Exit(code=1) from error

    typer.echo(version)


def main() -> None:
    """Run the get-version Typer application.

    Returns:
        None: Typer manages command-line parsing and process exit status.
    """
    app()


if __name__ == "__main__":
    main()
