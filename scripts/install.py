"""Install the Copilot analytics bundle into a project's .github folder.

Usage:
    python scripts/install.py <target_project> [--force]

Skills, instructions and prompts are copied (overwriting previous plugin
versions). An existing copilot-instructions.md is kept unless --force.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

BUNDLE_DIR = Path(__file__).resolve().parents[1] / "plugin" / ".github"
BUNDLE_FOLDERS = ("skills", "instructions", "prompts")
ALWAYS_ON_FILE = "copilot-instructions.md"


class BundleInstaller:
    """Copy the plugin bundle into a target project.

    Args:
        target: Project root that receives the .github folder.
        force: Overwrite an existing copilot-instructions.md.
    """

    def __init__(self, target: Path, force: bool = False) -> None:
        if not target.is_dir():
            raise NotADirectoryError(f"{target} is not a directory")
        self._destination = target / ".github"
        self._force = force

    def install(self) -> None:
        """Copy every bundle folder and the always-on instructions."""
        for folder in BUNDLE_FOLDERS:
            shutil.copytree(
                BUNDLE_DIR / folder,
                self._destination / folder,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
            logger.info("Installed %s/", folder)
        self._install_always_on()

    def _install_always_on(self) -> None:
        target = self._destination / ALWAYS_ON_FILE
        if target.exists() and not self._force:
            logger.warning("%s exists; kept it. Merge the rules manually or use --force.", target)
            return
        shutil.copyfile(BUNDLE_DIR / ALWAYS_ON_FILE, target)
        logger.info("Installed %s", ALWAYS_ON_FILE)


def main() -> int:
    """Parse arguments and install the bundle."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", type=Path, help="Target project root")
    parser.add_argument("--force", action="store_true", help="Overwrite copilot-instructions.md")
    args = parser.parse_args()
    try:
        BundleInstaller(args.target, args.force).install()
    except NotADirectoryError as error:
        logger.error(error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
