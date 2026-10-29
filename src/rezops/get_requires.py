"""Typer command for reading project dependencies from pyproject.toml."""

from pathlib import Path

import typer

from rezops.utils import get_requires

app = typer.Typer(help="Read project metadata from pyproject.toml.")


@app.command()
def get_requires_command(
    source_path: Path | None = typer.Option(
        None,
        "--source-path",
        help="Project root (defaults to REZ_BUILD_SOURCE_PATH or the current directory).",
    ),
) -> None:
    """Print project dependencies, one requirement per output line.

    Args:
        source_path: Project root containing pyproject.toml.

    Returns:
        None: Prints dependencies or exits with an error for invalid metadata.
    """
    try:
        requirements = get_requires(source_path)
    except (OSError, ValueError) as error:
        typer.echo(f"rezops-get-requires: {error}", err=True)
        raise typer.Exit(code=1) from error

    for requirement in requirements:
        typer.echo(requirement)


def main() -> None:
    """Run the get-requires Typer application.

    Returns:
        None: Typer manages command-line parsing and process exit status.
    """
    app()


if __name__ == "__main__":
    main()
