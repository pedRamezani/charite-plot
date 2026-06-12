"""Palette preview — generates a swatch strip for every built-in palette.

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
names    = list(PALETTES.keys())

LABEL_PAD = 0.4   # data-units reserved to the left for labels at font size 12

fig, axes = plt.subplots(
    len(names), 1,
    figsize=(7.5, len(names) * 0.58 + 0.3),
    gridspec_kw={"hspace": 0},
)

for ax, name in zip(axes, names):
    palette = PALETTES[name]
    for i, color in enumerate(palette):
        ax.add_patch(mpatches.Rectangle(
            (i, 0), 1.0, 0.82,
            facecolor=color, edgecolor="none",
        ))
    ax.set_xlim(-LABEL_PAD, MAX_COLS)
    ax.set_ylim(-0.1, 1.0)
    ax.text(-LABEL_PAD, 0.41, name, ha="right", va="center", fontsize=12)
    ax.axis("off")


out = pathlib.Path(__file__).parent.parent / "docs" / "assets" / "palette_preview.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Saved → {out}")
plt.show()
