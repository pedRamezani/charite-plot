"""Colormap showcase — a sequential and a diverging heatmap for every brand.

The sequential panel uses the theme's default colormap (no ``cmap`` argument);
the diverging panel uses ``make_cmap("diverging")``.

Produces one asset per brand in docs/assets/:
    cmap_example.png       (Charité)
    cmap_example_bih.png   (BIH)

Run with:
    python examples/cmap_showcase.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import matplotlib.pyplot as plt
import numpy as np

from charite_plot import get_brand, make_cmap
from charite_plot.mpl_themes import using

# brand → (figure title, output file name)
SHOWCASES = {
    "charite": ("Charité", "cmap_example.png"),
    "bih": ("BIH", "cmap_example_bih.png"),
}
ASSETS = pathlib.Path(__file__).parent.parent / "docs" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
SAVE_KW = {"dpi": 300, "bbox_inches": "tight", "facecolor": "white"}

# ── data ────────────────────────────────────────────────────────────────────
y, x = np.mgrid[-2:2:200j, -3:3:300j]
# Sequential: two overlapping blobs of different height (0 … 1).
density = np.exp(-((x + 1) ** 2 + y**2) / 0.8) + 0.6 * np.exp(-((x - 1.2) ** 2 + (y - 0.6) ** 2) / 0.5)
density /= density.max()
# Diverging: a negative and a positive blob (-1 … 1); zero (white) towards the edges.
signed = np.exp(-((x + 1.1) ** 2 + y**2) / 0.7) - np.exp(-((x - 1.1) ** 2 + y**2) / 0.7)
signed /= np.abs(signed).max()

# ── one figure per brand ────────────────────────────────────────────────────
for brand, (title, filename) in SHOWCASES.items():
    roles = get_brand(brand).roles
    with using(brand=brand, font_size=14):
        fig, (ax_seq, ax_div) = plt.subplots(1, 2, figsize=(9, 3.6))
        fig.subplots_adjust(top=0.8, wspace=0.08)
        fig.suptitle(title, fontsize=16, y=0.99, color=roles.primary)
        fig.text(0.5, 0.905, "Colormaps", ha="center", va="top", fontsize=9.5, color=roles.text)

        ax_seq.imshow(density)  # default colormap from the theme
        ax_seq.set_title("Sequential", fontsize=12)
        ax_div.imshow(signed, cmap=make_cmap("diverging", brand=brand), vmin=-1, vmax=1)
        ax_div.set_title("Diverging", fontsize=12)
        for ax in (ax_seq, ax_div):
            ax.set_axis_off()

        out = ASSETS / filename
        fig.savefig(out, **SAVE_KW)
        print(f"Saved → {out}")
plt.show()
