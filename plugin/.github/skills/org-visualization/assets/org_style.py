"""Organizational chart style: palette, fonts and figure export.

Usage:
    import org_style

    org_style.apply()
    fig, ax = plt.subplots()
    ax.bar(x, y, color=org_style.PRIMARY)
    org_style.save(fig, "deposits_by_segment")
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

# TODO(content): replace every value with the official brand guide (hex codes).
PRIMARY = "#1F3A5F"
SECONDARY = "#4A90C2"
ACCENT = "#F2B705"
POSITIVE = "#2E8B57"
NEGATIVE = "#C0392B"
NEUTRAL = "#8C8C8C"
BACKGROUND = "#FFFFFF"
TEXT = "#222222"

# Categorical order: the first series always gets PRIMARY.
PALETTE = [PRIMARY, SECONDARY, ACCENT, POSITIVE, NEGATIVE, NEUTRAL]
SEQUENTIAL_CMAP = "Blues"  # TODO(content): official sequential scale.

FONT_FAMILY = "sans-serif"  # TODO(content): official font, with a fallback.
FIGSIZE = (10, 6)
DPI = 150
DEFAULT_OUTPUT_DIR = Path("outputs/figures")


def apply() -> None:
    """Apply the organizational style to matplotlib (and seaborn/plotly if installed)."""
    mpl.rcParams.update(
        {
            "axes.prop_cycle": mpl.cycler(color=PALETTE),
            "axes.edgecolor": NEUTRAL,
            "axes.labelcolor": TEXT,
            "axes.titleweight": "bold",
            "axes.titlesize": 14,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": BACKGROUND,
            "figure.figsize": FIGSIZE,
            "font.family": FONT_FAMILY,
            "text.color": TEXT,
            "xtick.color": TEXT,
            "ytick.color": TEXT,
            "image.cmap": SEQUENTIAL_CMAP,
        }
    )
    _apply_optional_libraries()


def save(fig: plt.Figure, name: str, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    """Save a figure as PNG with the standard DPI and return its path.

    Args:
        fig: Figure to save.
        name: File name without extension, snake_case.
        output_dir: Destination folder; created if missing.

    Returns:
        Path of the saved file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    logger.info("Figure saved to %s", path)
    return path


def _apply_optional_libraries() -> None:
    try:
        import seaborn as sns

        sns.set_palette(PALETTE)
    except ImportError:
        pass
    try:
        import plotly.graph_objects as go
        import plotly.io as pio

        pio.templates["org"] = go.layout.Template(
            layout={"colorway": PALETTE, "font": {"family": FONT_FAMILY, "color": TEXT}}
        )
        pio.templates.default = "plotly_white+org"
    except ImportError:
        pass
