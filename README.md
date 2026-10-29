# rezops

Build and install Python packages into Rez package releases with the `rezops-build` command.

## Getting started

Install the project and its development tools with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
```

Run the test suite:

```sh
uv run pytest
```

Run the Rez build command:

```sh
uv run rezops-build --help
```

## Rez build command

`rezops-build` installs a Python package from `src/<package_name>` in the project
source root to `python/<package_name>` in the Rez install root. It reads
`REZ_BUILD_SOURCE_PATH` and `REZ_BUILD_INSTALL_PATH` from the build environment and
uses `REZ_BUILD_PROJECT_NAME` as the package name unless one is passed as an argument.

```python
# package.py for the package being built
build_requires = ["rezops"]
build_command = "rezops-build my_package"
```

See the command options with:

```sh
uv run rezops-build --help
```

The package name can also be supplied positionally, for example
`uv run rezops-build custom_package`.

## Documentation

This project uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) with
generated API reference documentation. The site starts in dark mode and its built-in palette control
lets you switch to light mode; your choice is remembered in the browser.

Preview the documentation locally:

```sh
uv run mkdocs serve
```

Build the static site:

```sh
uv run mkdocs build
```


## Code formatting

Use Ruff to apply safe lint fixes and format Python files:

```sh
uv run ruff check --fix .
uv run ruff format .
```


## Template paths

Edit the generated `pbtemp.toml` file (rendered from `resources/pbtemp.toml`) to change where
package, Nuke, and Rez directories are placed. Paths are relative to the project root.
