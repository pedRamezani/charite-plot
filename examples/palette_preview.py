"""Palette preview — generates swatch strips and continuous gradients for every brand.

Produces two assets per brand in docs/assets/:
    palette_preview.png, palette_preview_bih.png   discrete palettes
    cmap_preview.png, cmap_preview_bih.png         continuous colormaps (make_cmap): the brand's sequential
                                                   and diverging scales, every palette, then white → color
                                                   for the main brand colors

All previews of one kind share the same canvas and swatch size, so they line up when shown side by side.

Run with:
    python examples/palette_preview.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from charite_plot import BRANDS, make_cmap
from charite_plot.mpl_themes import using

SUFFIX = {"charite": "", "bih": "_bih"}
# Single colors shown as white → color ramps in the continuous preview.
RAMP_COLORS = {
    "charite": ["prime_blue", "second_dblue", "korall", "mineral", "gruen"],
    "bih": ["blau", "korall", "gold", "mineral", "lavendel"],
}
MAX_COLS = max(len(p) for brand in BRANDS.values() for p in brand.palettes.values())
LABEL_W = 1.6  # inches reserved for the names
ROW_H = 0.58
FIG_W = 7.5

ASSETS = pathlib.Path(__file__).parent.parent / "docs" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
SAVE_KW = {"dpi": 300, "facecolor": "white", "transparent": False}
GRADIENT = np.linspace(0, 1, 256)[None, :]


def _draw_swatches(ax: plt.Axes, colors: list[str]) -> None:
    for i, color in enumerate(colors):
        ax.add_patch(mpatches.Rectangle((i, 0), 1.0, 0.82, facecolor=color, edgecolor="none"))
    ax.set_xlim(0, MAX_COLS)
    ax.set_ylim(-0.1, 1.0)


def _draw_gradient(ax: plt.Axes, cmap) -> None:
    ax.imshow(GRADIENT, aspect="auto", cmap=cmap, extent=(0, MAX_COLS, 0, 0.82))
    ax.set_xlim(0, MAX_COLS)
    ax.set_ylim(-0.1, 1.0)


def _save(rows: list[tuple[str, callable]], n_rows: int, out: pathlib.Path) -> None:
    fig_h = n_rows * ROW_H + 0.3
    fig, axes = plt.subplots(n_rows, 1, figsize=(FIG_W, fig_h), gridspec_kw={"hspace": 0})
    fig.subplots_adjust(left=LABEL_W / FIG_W, right=0.98, top=1 - 0.15 / fig_h, bottom=0.15 / fig_h)
    for i, ax in enumerate(axes):
        if i < len(rows):  # brands with fewer rows are padded to the same height
            name, draw = rows[i]
            draw(ax)
            ax.text(-0.15, 0.41, name, ha="right", va="center", fontsize=12, transform=ax.transData)
        ax.axis("off")
    fig.savefig(out, bbox_inches=fig.bbox_inches, **SAVE_KW)  # full canvas, not the theme's tight bbox
    print(f"Saved → {out}")


discrete = {
    b: [(name, lambda ax, c=colors: _draw_swatches(ax, c)) for name, colors in brand.palettes.items()]
    for b, brand in BRANDS.items()
}
continuous = {
    b: [
        (name, lambda ax, n=name, b=b: _draw_gradient(ax, make_cmap(n, brand=b)))
        for name in ["sequential", "diverging", *brand.palettes, *RAMP_COLORS[b]]
    ]
    for b, brand in BRANDS.items()
}
for kind, rows_by_brand in {"palette_preview": discrete, "cmap_preview": continuous}.items():
    n_rows = max(len(rows) for rows in rows_by_brand.values())
    for b, rows in rows_by_brand.items():
        with using(brand=b):
            _save(rows, n_rows, ASSETS / f"{kind}{SUFFIX[b]}.png")
plt.show()
