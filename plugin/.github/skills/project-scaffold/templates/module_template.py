"""One-line summary of what this module does.

Longer description: inputs, outputs and where it fits in the pipeline.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

# TODO(content): replace with the project's package name and the real impala-helper import.
from project_name.constants import QUERIES_DIR, TRANSACTIONS_TABLE

logger = logging.getLogger(__name__)


class TransactionsExtractor:
    """Extract transactions from Impala for a date range.

    Args:
        client: impala-helper client used to run queries.
        queries_dir: Folder with the project's .sql files.
    """

    QUERY_FILE = "01_extract_transactions.sql"

    def __init__(self, client: object, queries_dir: Path = QUERIES_DIR) -> None:
        self._client = client
        self._queries_dir = queries_dir

    def extract(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Run the extraction query and return the result.

        Args:
            start_date: Inclusive start date, ``YYYY-MM-DD``.
            end_date: Inclusive end date, ``YYYY-MM-DD``.

        Returns:
            Transactions in the date range.
        """
        query = (self._queries_dir / self.QUERY_FILE).read_text(encoding="utf-8")
        logger.info("Extracting %s from %s to %s", TRANSACTIONS_TABLE, start_date, end_date)
        # TODO(content): replace with the real impala-helper call and parameter syntax.
        return self._client.query(query, params={"start_date": start_date, "end_date": end_date})


def main() -> None:
    """Entrypoint: wire dependencies and run the pipeline step."""
    logging.basicConfig(level=logging.INFO)
    # TODO(content): build the impala-helper client here.


if __name__ == "__main__":
    main()
