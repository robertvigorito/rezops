"""Tests for the Rez build command."""

import logging
from pathlib import Path

import pytest
from typer.testing import CliRunner

from rezops.build import app
from rezops.get_requires import app as get_requires_app
from rezops.get_version import app as get_version_app
from rezops.logger import ColorFormatter
from rezops.utils import get_requires, get_version

runner = CliRunner()


def test_get_version_reads_pyproject(tmp_path: Path) -> None:
    """Check the version getter reads [project].version.

    Args:
        tmp_path: Temporary project root.

    Returns:
        None: The assertion validates the returned version.
    """
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo-package"\nversion = "1.2.3"\n',
        encoding="utf-8",
    )

    assert get_version(tmp_path) == "1.2.3"


def test_get_requires_reads_pyproject_dependencies(tmp_path: Path) -> None:
    """Check the requires getter returns dependencies declared in pyproject.

    Args:
        tmp_path: Temporary project root.

    Returns:
        None: The assertion validates the dependency list.
    """
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo-package"\nversion = "1.2.3"\n'
        'dependencies = ["typer>=0.27", "tomli>=2; python_version < \'3.11\'"]\n',
        encoding="utf-8",
    )

    assert get_requires(tmp_path) == ["typer>=0.27", "tomli>=2; python_version < '3.11'"]


def test_get_requires_defaults_to_empty_list(tmp_path: Path) -> None:
    """Check a project without dependencies has no Rez requirements.

    Args:
        tmp_path: Temporary project root.

    Returns:
        None: The assertion validates the empty dependency list.
    """
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo-package"\nversion = "1.2.3"\n',
        encoding="utf-8",
    )

    assert get_requires(tmp_path) == []


def test_get_version_cli_uses_typer(tmp_path: Path) -> None:
    """Check the version console command prints the requested project's version.

    Args:
        tmp_path: Temporary project root.

    Returns:
        None: Assertions validate the Typer CLI output and status.
    """
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo-package"\nversion = "2.0.0"\n',
        encoding="utf-8",
    )

    result = runner.invoke(get_version_app, ["--source-path", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert result.output == "2.0.0\n"


def test_get_requires_cli_uses_typer(tmp_path: Path) -> None:
    """Check the requires console command prints dependencies using Typer.

    Args:
        tmp_path: Temporary project root.

    Returns:
        None: Assertions validate the Typer CLI output and status.
    """
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo-package"\nversion = "2.0.0"\ndependencies = ["typer>=0.27"]\n',
        encoding="utf-8",
    )

    result = runner.invoke(get_requires_app, ["--source-path", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert result.output == "typer>=0.27\n"


def test_color_formatter_uses_distinct_level_colors() -> None:
    """Check informational and error log levels receive different colors.

    Returns:
        None: Assertions validate colored output and record immutability.
    """
    formatter = ColorFormatter(use_color=True)
    info_record = logging.LogRecord("rezops.test", logging.INFO, __file__, 1, "message", (), None)
    error_record = logging.LogRecord("rezops.test", logging.ERROR, __file__, 1, "message", (), None)

    info_output = formatter.format(info_record)
    error_output = formatter.format(error_record)

    assert "\033[32mINFO\033[0m" in info_output
    assert "\033[31mERROR\033[0m" in error_output
    assert info_record.levelname == "INFO"
    assert error_record.levelname == "ERROR"


def _write_pyproject(source: Path, project_name: str = "socket-dcc") -> None:
    """Write minimal project metadata for a default-name build test.

    Args:
        source: Project source root.
        project_name: Distribution name written to [project].name.

    Returns:
        None: Creates the project's pyproject.toml.
    """
    source.mkdir(parents=True, exist_ok=True)
    (source / "pyproject.toml").write_text(f'[project]\nname = "{project_name}"\n', encoding="utf-8")


def test_build_installs_package_and_nuke_files(tmp_path: Path) -> None:
    """Check the CLI installs both the Python package and Nuke files.

    Args:
        tmp_path: Temporary directory used to construct source and install roots.

    Returns:
        None: Assertions validate the copied files and command status.
    """
    source = tmp_path / "project"
    install = tmp_path / "install"
    _write_pyproject(source)
    package_file = source / "src" / "socket_dcc" / "__init__.py"
    nuke_file = source / "src" / "nuke" / "menu.py"
    package_file.parent.mkdir(parents=True)
    nuke_file.parent.mkdir(parents=True)
    package_file.write_text("PACKAGE = True\n", encoding="utf-8")
    nuke_file.write_text("NUKE = True\n", encoding="utf-8")

    result = runner.invoke(app, ["--source-path", str(source), "--install-path", str(install)])

    assert result.exit_code == 0, result.output
    assert (install / "python" / "socket_dcc" / "__init__.py").read_text(encoding="utf-8") == "PACKAGE = True\n"
    assert (install / "nuke" / "menu.py").read_text(encoding="utf-8") == "NUKE = True\n"


def test_build_removes_nuke_target_when_source_is_absent(tmp_path: Path) -> None:
    """Check stale Nuke files are removed when the source folder is absent.

    Args:
        tmp_path: Temporary directory used to construct source and install roots.

    Returns:
        None: Assertions validate the target cleanup and command status.
    """
    source = tmp_path / "project"
    install = tmp_path / "install"
    _write_pyproject(source)
    package_dir = source / "src" / "socket_dcc"
    stale_nuke_file = install / "nuke" / "menu.py"
    package_dir.mkdir(parents=True)
    stale_nuke_file.parent.mkdir(parents=True)
    stale_nuke_file.write_text("stale", encoding="utf-8")

    result = runner.invoke(app, ["--source-path", str(source), "--install-path", str(install)])

    assert result.exit_code == 0, result.output
    assert not (install / "nuke").exists()


def test_build_reports_missing_package_source(tmp_path: Path) -> None:
    """Check a missing package source produces a nonzero CLI result.

    Args:
        tmp_path: Temporary directory used as the project root.

    Returns:
        None: Assertions validate the failure status and message.
    """
    _write_pyproject(tmp_path)
    result = runner.invoke(
        app,
        ["--source-path", str(tmp_path), "--install-path", str(tmp_path / "install")],
    )

    assert result.exit_code == 1
    assert "Package source directory does not exist" in result.output
    assert "Command options for troubleshooting:" in result.output
    assert "--source-path" in result.output
    assert "--install-path" in result.output
    assert "--package-name" in result.output


def test_build_uses_rez_environment_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Check Rez environment variables provide the default paths.

    Args:
        tmp_path: Temporary directory used to construct source and install roots.
        monkeypatch: Pytest fixture for controlling environment variables.

    Returns:
        None: Assertions validate the environment-based build result.
    """
    source = tmp_path / "project"
    install = tmp_path / "install"
    _write_pyproject(source)
    package_dir = source / "src" / "socket_dcc"
    package_dir.mkdir(parents=True)
    monkeypatch.setenv("REZ_BUILD_SOURCE_PATH", str(source))
    monkeypatch.setenv("REZ_BUILD_INSTALL_PATH", str(install))

    result = runner.invoke(app, [])

    assert result.exit_code == 0, result.output
    assert (install / "python" / "socket_dcc").is_dir()


def test_build_uses_rez_project_name_before_pyproject(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Check Rez's project name selects the source package over pyproject metadata.

    Args:
        tmp_path: Temporary directory used to construct source and install roots.
        monkeypatch: Pytest fixture for controlling environment variables.

    Returns:
        None: Assertions validate the Rez project-name behavior.
    """
    source = tmp_path / "project"
    install = tmp_path / "install"
    _write_pyproject(source, "different-distribution")
    (source / "src" / "rez_package").mkdir(parents=True)
    monkeypatch.setenv("REZ_BUILD_SOURCE_PATH", str(source))
    monkeypatch.setenv("REZ_BUILD_INSTALL_PATH", str(install))
    monkeypatch.setenv("REZ_BUILD_PROJECT_NAME", "rez-package")

    result = runner.invoke(app, [])

    assert result.exit_code == 0, result.output
    assert (install / "python" / "rez_package").is_dir()


def test_build_accepts_package_name_as_positional_argument(tmp_path: Path) -> None:
    """Check a positional package name overrides pyproject metadata.

    Args:
        tmp_path: Temporary directory used to construct source and install roots.

    Returns:
        None: Assertions validate the positional package-name behavior.
    """
    source = tmp_path / "project"
    install = tmp_path / "install"
    (source / "src" / "custom_package").mkdir(parents=True)

    result = runner.invoke(
        app,
        ["custom_package", "--source-path", str(source), "--install-path", str(install)],
    )

    assert result.exit_code == 0, result.output
    assert (install / "python" / "custom_package").is_dir()


def test_build_requires_rez_paths_when_options_are_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check missing Rez path variables produce an actionable failure.

    Args:
        monkeypatch: Pytest fixture for controlling environment variables.

    Returns:
        None: Assertions validate the failure status and message.
    """
    monkeypatch.delenv("REZ_BUILD_SOURCE_PATH", raising=False)
    monkeypatch.delenv("REZ_BUILD_INSTALL_PATH", raising=False)

    result = runner.invoke(app, [])

    assert result.exit_code == 1
    assert "REZ_BUILD_SOURCE_PATH" in result.output
    assert "Command options for troubleshooting:" in result.output
    assert "--help" in result.output
