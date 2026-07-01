"""Palette preview — generates swatch strips for every built-in palette.

Produces one asset in docs/assets/:
    palette_preview.png

Run with:
    python examples/palette_preview.py
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from charite_plot.mpl_themes import theme_charite, apply_theme
from charite_plot.palettes import PALETTES

apply_theme(theme_charite())

MAX_COLS = max(len(p) for p in PALETTES.values())
names = list(PALETTES.keys())
LABEL_PAD = 0.4
ROW_H = 0.58
FIG_W = 7.5

ASSETS = pathlib.Path(__file__).parent.parent / "docs" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
OUT = ASSETS / "palette_preview.png"
SAVE_KW = dict(dpi=300, bbox_inches="tight", facecolor="white", transparent=False)


def _draw_row(ax: plt.Axes, name: str) -> None:
    for i, color in enumerate(PALETTES[name]):
        ax.add_patch(
            mpatches.Rectangle(
                (i, 0),
                1.0,
                0.82,
                facecolor=color,
                edgecolor="none",
            )
        )
    ax.set_xlim(-LABEL_PAD, MAX_COLS)
    ax.set_ylim(-0.1, 1.0)
    ax.text(-LABEL_PAD, 0.41, name, ha="right", va="center", fontsize=12)
    ax.axis("off")


fig, axes = plt.subplots(
    len(names),
    1,
    figsize=(FIG_W, len(names) * ROW_H + 0.3),
    gridspec_kw={"hspace": 0},
)
for ax, name in zip(axes, names):
    _draw_row(ax, name)
fig.savefig(OUT, **SAVE_KW)
print(f"Saved → {OUT}")
plt.show()
