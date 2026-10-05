"""Project-wide constants. Every path, table name and threshold lives here."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUERIES_DIR = PROJECT_ROOT / "queries"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"

# TODO(content): real database and table names.
TRANSACTIONS_TABLE = "db_name.table_name"
