"""Check an analytics project against the team standards.

Standard library only, so it runs anywhere. Exit code 1 when violations exist.

Usage:
    python check_project.py [project_root] [--json]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "project-scaffold" / "scripts"))
from scaffold import PACKAGE_PLACEHOLDER, PROJECT_TREE  # noqa: E402

logger = logging.getLogger(__name__)

# TODO(content): align patterns and rules with the official standards.
NOTEBOOK_NAME = re.compile(r"^\d{2}_[a-z0-9_]+\.ipynb$")
SQL_NAME = re.compile(r"^\d{2}_[a-z0-9_]+\.sql$")
MODULE_NAME = re.compile(r"^[a-z_][a-z0-9_]*\.py$")
SELECT_STAR = re.compile(r"\bselect\s+\*", re.IGNORECASE)
INLINE_SQL = re.compile(r"[\"']{1,3}\s*(select|insert|create\s+table|with)\s", re.IGNORECASE)
HEX_COLOR = re.compile(r"[\"']#[0-9a-fA-F]{6}[\"']")
CREDENTIAL = re.compile(r"(password|passwd|token|secret)\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE)
PRINT_CALL = re.compile(r"^\s*print\(", re.MULTILINE)

STYLE_MODULE = "org_style.py"
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", ".ipynb_checkpoints", ".github", "outputs"}


@dataclass(frozen=True)
class Finding:
    """A single standards violation."""

    rule: str
    path: str
    message: str


class ProjectChecker:
    """Run every standards rule over a project tree.

    Args:
        root: Project root folder.
    """

    def __init__(self, root: Path) -> None:
        self._root = root
        self._findings: list[Finding] = []
        self._files_checked = 0
        self._files_failed: set[str] = set()

    def run(self) -> list[Finding]:
        """Run all checks and return the findings."""
        self._check_structure()
        for path in self._iter_files():
            self._files_checked += 1
            suffix = path.suffix.lower()
            if suffix == ".sql":
                self._check_sql(path)
            elif suffix == ".py":
                self._check_python(path)
            elif suffix == ".ipynb":
                self._check_notebook(path)
        self._run_ruff()
        return self._findings

    def summary(self) -> dict[str, float | int]:
        """Return totals and the share of files without violations."""
        passed = self._files_checked - len(self._files_failed)
        compliance = passed / self._files_checked if self._files_checked else 1.0
        return {
            "files_checked": self._files_checked,
            "files_with_findings": len(self._files_failed),
            "findings": len(self._findings),
            "compliance": round(compliance, 3),
        }

    def _add(self, rule: str, path: Path, message: str) -> None:
        relative = path.relative_to(self._root).as_posix() if path != self._root else "."
        self._findings.append(Finding(rule, relative, message))
        if path.is_file():
            self._files_failed.add(relative)

    def _iter_files(self) -> list[Path]:
        return sorted(
            path
            for path in self._root.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".sql", ".py", ".ipynb"}
            and not IGNORED_DIRS.intersection(path.relative_to(self._root).parts)
        )

    def _check_structure(self) -> None:
        package = self._root.name
        for folder in PROJECT_TREE:
            expected = self._root / folder.replace(PACKAGE_PLACEHOLDER, package)
            if not expected.is_dir():
                self._add("structure", self._root, f"missing folder '{expected.name}' ({folder})")

    def _check_sql(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8", errors="replace")
        if not SQL_NAME.match(path.name):
            self._add("naming", path, "SQL files must be named NN_verb_subject.sql")
        if path.parent.name != "queries":
            self._add("structure", path, "SQL files belong in queries/")
        if SELECT_STAR.search(text):
            self._add("sql", path, "SELECT * is not allowed; list the columns")
        first_line = next((line for line in text.splitlines() if line.strip()), "")
        if not first_line.lstrip().startswith(("--", "/*")):
            self._add("sql", path, "missing header comment (purpose, sources, parameters)")

    def _check_python(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8", errors="replace")
        if not MODULE_NAME.match(path.name):
            self._add("naming", path, "modules must be snake_case.py")
        self._check_code(path, text)
        if PRINT_CALL.search(text):
            self._add("python", path, "use logging instead of print")

    def _check_notebook(self, path: Path) -> None:
        if not NOTEBOOK_NAME.match(path.name):
            self._add("naming", path, "notebooks must be named NN_short_description.ipynb")
        try:
            cells = json.loads(path.read_text(encoding="utf-8")).get("cells", [])
        except json.JSONDecodeError:
            self._add("notebook", path, "invalid notebook JSON")
            return
        if not cells or cells[0].get("cell_type") != "markdown":
            self._add("notebook", path, "first cell must be a markdown header")
        code = "\n".join(
            "".join(cell.get("source", [])) for cell in cells if cell.get("cell_type") == "code"
        )
        self._check_code(path, code)

    def _check_code(self, path: Path, code: str) -> None:
        if INLINE_SQL.search(code):
            self._add("sql", path, "inline SQL found; move it to queries/*.sql")
        if path.name != STYLE_MODULE and HEX_COLOR.search(code):
            self._add("viz", path, "hardcoded color; use org_style")
        if CREDENTIAL.search(code):
            self._add("security", path, "possible hardcoded credential")

    def _run_ruff(self) -> None:
        ruff = shutil.which("ruff")
        if ruff is None:
            logger.info("ruff not installed; skipping lint")
            return
        result = subprocess.run(
            [ruff, "check", "--quiet", "--output-format", "concise", str(self._root)],
            capture_output=True,
            text=True,
            check=False,
        )
        for line in result.stdout.splitlines():
            file_part, _, message = line.partition(": ")
            path = Path(file_part.split(":")[0])
            if path.is_file():
                self._add("ruff", path.resolve(), message)


def main() -> int:
    """Parse arguments, run the checker and print the report."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    checker = ProjectChecker(args.root.resolve())
    findings = checker.run()
    summary = checker.summary()

    if args.json:
        sys.stdout.write(
            json.dumps({"summary": summary, "findings": [asdict(f) for f in findings]}, indent=2)
        )
    else:
        for finding in findings:
            logger.info("[%s] %s: %s", finding.rule, finding.path, finding.message)
        logger.info(
            "%s findings in %s/%s files - compliance %.0f%%",
            summary["findings"],
            summary["files_with_findings"],
            summary["files_checked"],
            summary["compliance"] * 100,
        )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
