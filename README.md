# rezops

Contain code to help with rez operations.

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

## Rez build helper

The `rezops-build` command copies `src/socket_dcc` into the Rez install root at
`python/socket_dcc`. If `src/nuke` exists, it is copied to `nuke`; otherwise, any
existing `nuke` target is removed. During a Rez build, the command reads
`REZ_BUILD_SOURCE_PATH` and `REZ_BUILD_INSTALL_PATH` automatically. It uses
`REZ_BUILD_PROJECT_NAME` as the package directory name, falling back to the
normalized `[project].name` from `pyproject.toml` when that Rez variable is unset.
Build progress logs use distinct colors for each severity when written to a terminal;
color is disabled for redirected output and when `NO_COLOR` is set.

```python
# package.py for the package being built
build_requires = ["rezops"]
build_command = "rezops-build"
```

For local use, pass the roots explicitly:

```sh
uv run rezops-build --source-path /path/to/project --install-path /path/to/install
```

Use `--package-name` to select a different package directory under `src`.
The package name can also be supplied positionally, for example
`uv run rezops-build custom_package --source-path /path/to/project --install-path /path/to/install`.

The project also provides `rezops-get-version` and `rezops-get-requires` console commands.
They read the project's `pyproject.toml` from `REZ_BUILD_SOURCE_PATH` (or the current
directory), and can be pointed at another project explicitly:

```sh
rezops-get-version --source-path /path/to/project
rezops-get-requires --source-path /path/to/project
```

The version script prints one version. The requires script prints one dependency per line.

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
