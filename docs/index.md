# rezops

Utilities to support Rez workflows, including `rezops-build` for installing Python
packages into Rez package releases.

## Install

Install the package and its development tools:

```sh
uv sync
```

## Rez build command

During a Rez build, `rezops-build` reads `REZ_BUILD_SOURCE_PATH` and
`REZ_BUILD_INSTALL_PATH` and installs `src/<package_name>` as
`python/<package_name>` in the Rez install root. The package name defaults to
`REZ_BUILD_PROJECT_NAME`, or can be supplied as a positional argument.

```sh
uv run rezops-build --help
```

Add `rezops` as a build requirement and configure `rezops-build <package_name>` as
the package's `build_command` in `package.py`.
## Documentation development

Preview the documentation locally with live reload:

```sh
uv run mkdocs serve
```

Build the static site into `dist/docs/`:

```sh
uv run mkdocs build
```

This site uses Material for MkDocs and starts in dark mode. Use its built-in palette control to
switch to light mode; your choice is remembered in the browser.
