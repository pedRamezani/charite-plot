"""Palette preview — generates swatch strips for every built-in palette of every brand.

Produces one asset per brand in docs/assets/:
    palette_preview.png       (Charité)
    palette_preview_bih.png   (BIH)

All previews share the same canvas and swatch size, so they line up when shown side by side.

Run with:
    python examples/palette_preview.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from charite_plot import BRANDS
from charite_plot.mpl_themes import using

OUT_NAMES = {"charite": "palette_preview.png", "bih": "palette_preview_bih.png"}
MAX_COLS = max(len(p) for brand in BRANDS.values() for p in brand.palettes.values())
MAX_ROWS = max(len(brand.palettes) for brand in BRANDS.values())
LABEL_W = 1.6  # inches reserved for the palette names
ROW_H = 0.58
FIG_W = 7.5
FIG_H = MAX_ROWS * ROW_H + 0.3

ASSETS = pathlib.Path(__file__).parent.parent / "docs" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
SAVE_KW = {"dpi": 300, "facecolor": "white", "transparent": False}


def _draw_row(ax: plt.Axes, name: str, colors: list[str]) -> None:
    for i, color in enumerate(colors):
        ax.add_patch(mpatches.Rectangle((i, 0), 1.0, 0.82, facecolor=color, edgecolor="none"))
    ax.set_xlim(0, MAX_COLS)
    ax.set_ylim(-0.1, 1.0)
    ax.text(-0.15, 0.41, name, ha="right", va="center", fontsize=12)
    ax.axis("off")


for brand_name, brand in BRANDS.items():
    with using(brand=brand):
        fig, axes = plt.subplots(MAX_ROWS, 1, figsize=(FIG_W, FIG_H), gridspec_kw={"hspace": 0})
        fig.subplots_adjust(left=LABEL_W / FIG_W, right=0.98, top=1 - 0.15 / FIG_H, bottom=0.15 / FIG_H)
        palettes = list(brand.palettes.items())
        for i, ax in enumerate(axes):
            if i < len(palettes):
                _draw_row(ax, *palettes[i])
            else:
                ax.axis("off")  # pad brands with fewer palettes to the same height
        out = ASSETS / OUT_NAMES[brand_name]
        fig.savefig(out, bbox_inches=fig.bbox_inches, **SAVE_KW)  # full canvas, not the theme's tight bbox
        print(f"Saved → {out}")
plt.show()
