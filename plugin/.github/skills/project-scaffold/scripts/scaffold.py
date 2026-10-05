"""Create a new analytics project with the team's standard structure.

Usage:
    python scaffold.py <project_name> [--path <parent_dir>]
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

SKILLS_DIR = Path(__file__).resolve().parents[2]
PACKAGE_PLACEHOLDER = "{package}"
PROJECT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

# TODO(content): mirror the official structure documented in references/structure.md.
PROJECT_TREE = (
    "queries",
    "notebooks",
    f"src/{PACKAGE_PLACEHOLDER}",
    "outputs/figures",
    "outputs/data",
    "tests",
)

# (source relative to .github/skills, destination relative to the project root)
TEMPLATE_FILES = (
    ("project-scaffold/templates/pyproject.toml", "pyproject.toml"),
    ("project-scaffold/templates/constants.py", f"src/{PACKAGE_PLACEHOLDER}/constants.py"),
    ("project-scaffold/templates/notebook_template.ipynb", "notebooks/01_extraction.ipynb"),
    ("org-visualization/assets/org_style.py", f"src/{PACKAGE_PLACEHOLDER}/org_style.py"),
)

README_TEMPLATE = "# {name}\n\n**Objective:**\n\n**Owner:**\n\n## How to run\n"


class ProjectScaffolder:
    """Create the folder tree and starter files for a project.

    Args:
        name: Project name in snake_case; also used as the package name.
        parent_dir: Directory where the project folder is created.
    """

    def __init__(self, name: str, parent_dir: Path) -> None:
        if not PROJECT_NAME_PATTERN.match(name):
            raise ValueError(f"Project name must be snake_case, got '{name}'")
        self._name = name
        self._root = parent_dir / name

    def create(self) -> Path:
        """Create the project and return its root path."""
        if self._root.exists():
            raise FileExistsError(f"{self._root} already exists")
        self._create_tree()
        self._copy_templates()
        (self._root / "README.md").write_text(README_TEMPLATE.format(name=self._name), "utf-8")
        logger.info("Project created at %s", self._root)
        return self._root

    def _resolve(self, relative: str) -> Path:
        return self._root / relative.replace(PACKAGE_PLACEHOLDER, self._name)

    def _create_tree(self) -> None:
        for folder in PROJECT_TREE:
            self._resolve(folder).mkdir(parents=True, exist_ok=True)
        (self._resolve(f"src/{PACKAGE_PLACEHOLDER}") / "__init__.py").touch()

    def _copy_templates(self) -> None:
        for template, destination in TEMPLATE_FILES:
            target = self._resolve(destination)
            shutil.copyfile(SKILLS_DIR / template, target)
            text = target.read_text(encoding="utf-8").replace("project_name", self._name)
            target.write_text(text, encoding="utf-8")


def main() -> int:
    """Parse arguments and scaffold the project."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name", help="Project name in snake_case")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Parent directory")
    args = parser.parse_args()
    try:
        ProjectScaffolder(args.name, args.path).create()
    except (ValueError, FileExistsError) as error:
        logger.error(error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
