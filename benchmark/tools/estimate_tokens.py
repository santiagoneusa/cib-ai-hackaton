"""Estimate the tokens of an exported Copilot chat session.

Counts every string in the exported JSON and divides by CHARS_PER_TOKEN. It is an
approximation meant to compare benchmark arms consistently, not an exact count.

Usage:
    python estimate_tokens.py <exported_chat.json> [<more.json> ...]
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

CHARS_PER_TOKEN = 4


class ChatTokenEstimator:
    """Approximate the tokens contained in an exported chat JSON file.

    Args:
        path: Exported chat session file.
    """

    def __init__(self, path: Path) -> None:
        self._path = path

    def estimate(self) -> int:
        """Return the estimated number of tokens in the file."""
        data = json.loads(self._path.read_text(encoding="utf-8"))
        return self._count_chars(data) // CHARS_PER_TOKEN

    def _count_chars(self, node: Any) -> int:
        if isinstance(node, str):
            return len(node)
        if isinstance(node, dict):
            return sum(self._count_chars(value) for value in node.values())
        if isinstance(node, list):
            return sum(self._count_chars(item) for item in node)
        return 0


def main() -> int:
    """Print the estimate for every file passed as argument."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if len(sys.argv) < 2:
        logger.error(__doc__)
        return 1
    for argument in sys.argv[1:]:
        path = Path(argument)
        logger.info("%s: ~%s tokens", path.name, f"{ChatTokenEstimator(path).estimate():,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
