---
description: Python coding standards for analytics scripts and modules
applyTo: "**/*.py"
---

# Python standards

Copy the shape of [module_template.py](../skills/project-scaffold/templates/module_template.py) instead of inventing a new one.

<!-- TODO(content): proposed defaults below. Confirm or replace them with the team's coding standard. -->

## Structure

- Constants (paths, table names, thresholds, column lists) go in the project's constants module as `UPPER_SNAKE_CASE`. No magic numbers or strings inline.
- Group related behavior in classes with a single responsibility (e.g. `Extractor`, `Transformer`, `Loader`). Prefer composition over inheritance.
- Keep functions short (aim for under 30 lines) and free of side effects when possible.
- Scripts expose a `main()` and a thin `if __name__ == "__main__":` entrypoint. No logic at module level.

## Style

- Naming: `snake_case` for functions and variables, `PascalCase` for classes, `_leading_underscore` for private members.
- Type hints on every public function and method, including return types.
- Google-style docstrings on every public module, class and function.
- Use `logging` (module-level `logger = logging.getLogger(__name__)`), never `print`.
- Use `pathlib.Path` for paths.
- Raise specific exceptions with a clear message; never use a bare `except:`.

## Data access

- Queries: load `.sql` files and run them with `impala-helper`. See the `impala-query` skill.
- Transfers: use `harbor`. See the `harbor-transfer` skill.

## Tooling

The project's `pyproject.toml` configures `ruff`. Code must pass `ruff check` and `ruff format`.
