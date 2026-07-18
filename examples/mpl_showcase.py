"""Matplotlib theme showcase — mirrors the structure of the Altair test chart.

Run with:
    python examples/mpl_showcase.py
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

from charite_plot.mpl_themes import enable
from charite_plot.palettes import PALETTES

rng = np.random.default_rng(42)

# ── shared data (mirrors the Altair test dataset) ──────────────────────────
COMMON = {
    "Index":    list(range(1, 19)),
    "Value":    [28, 55, 43, 91, 81, 53, 19, 87, 52, 48, 24, 49, 87, 66, 17, 27, 68, 16],
    "Position": [1, 2, 3, 4, 5, 6] * 3,
    "Category": ["A"] * 6 + ["B"] * 6 + ["C"] * 6,
}
MARKERS = {"A": "o", "B": "s", "C": "^"}

# ── apply theme globally ───────────────────────────────────────────────────
enable(palette="primary")
COLORS = PALETTES["primary"]

# ── figure layout ──────────────────────────────────────────────────────────
HEIGHT_SMALL = 2.2
STANDARD     = 2.8

fig = plt.figure(figsize=(13, 11), constrained_layout=True)
fig.suptitle(
    "Charité Matplotlib Theme Test",
    fontsize=16,
    y=1.01,
)
sub = fig.add_gridspec(3, 3, hspace=0.125, wspace=0.1)

cats = ["A", "B", "C"]


# ── 1. Bar ─────────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(sub[0, 0])
bar_idx = [v for i, v in enumerate(COMMON["Index"])  if COMMON["Index"][i] <= 9]
bar_val = [v for i, v in enumerate(COMMON["Value"])  if COMMON["Index"][i] <= 9]
ax1.bar(bar_idx, bar_val, color=COLORS[0], width=0.7)
ax1.set_title("Bar")
ax1.set_xlabel("Index")
ax1.set_ylabel("Value")


# ── 2. Line (multi-series) ─────────────────────────────────────────────────
ax2 = fig.add_subplot(sub[0, 1])
for cat, col in zip(cats, COLORS):
    idx = [i for i, c in enumerate(COMMON["Category"]) if c == cat]
    pos = [COMMON["Position"][i] for i in idx]
    val = [COMMON["Value"][i]    for i in idx]
    ax2.plot(pos, val, marker="o", markersize=4, label=cat, color=col)
ax2.set_title("Line")
ax2.set_xlabel("Position")
ax2.set_ylabel("Value")
ax2.legend(frameon=False, fontsize=8)


# ── 3. Point (shape per category) ─────────────────────────────────────────
ax3 = fig.add_subplot(sub[0, 2])
for cat, col in zip(cats, COLORS):
    idx = [i for i, c in enumerate(COMMON["Category"]) if c == cat]
    pos = [COMMON["Position"][i] for i in idx]
    val = [COMMON["Value"][i]    for i in idx]
    ax3.scatter(pos, val, marker=MARKERS[cat], label=cat, color=col, s=55)
ax3.set_title("Point (Shape)")
ax3.set_xlabel("Position")
ax3.set_ylabel("Value")
ax3.legend(frameon=False, fontsize=8)


# ── 4. Point (continuous color = rating delta) ────────────────────────────
ax4 = fig.add_subplot(sub[1, 0])
n_pts       = 200
release_yr  = rng.integers(1960, 2020, n_pts)
rating      = rng.uniform(1, 10, n_pts)
delta       = rating - rating.mean()
vmax        = np.abs(delta).max()
sc = ax4.scatter(
    release_yr, delta,
    c=delta, cmap="RdBu_r", vmin=-vmax, vmax=vmax,
    s=18, alpha=0.75, linewidths=0,
)
plt.colorbar(sc, ax=ax4, label="Rating Delta", shrink=0.85)
ax4.axhline(0, color="grey", lw=0.6, ls="--", alpha=0.6)
ax4.set_title("Point (Color)")
ax4.set_xlabel("Release Year")
ax4.set_ylabel("Rating Delta")


# ── 5. Stacked horizontal bar (like barley/variety/site) ──────────────────
ax5 = fig.add_subplot(sub[1, 1])
varieties  = ["Manchuria", "Glabron", "Svansota", "Velvet", "Trebi"]
sites      = ["Waseca", "Crookston", "Duluth"]
site_data  = rng.integers(20, 80, size=(len(varieties), len(sites))).astype(float)
left       = np.zeros(len(varieties))
for j, (site, col) in enumerate(zip(sites, COLORS)):
    ax5.barh(varieties, site_data[:, j], left=left, label=site, color=col, height=0.65)
    left += site_data[:, j]
ax5.set_title("Bar (Stacked)")
ax5.set_xlabel("Sum of Yield")
ax5.legend(frameon=False, fontsize=7, loc="lower right")


# ── 6. Area (stacked, normalized = 100 %) ─────────────────────────────────
ax6 = fig.add_subplot(sub[1, 2])
years    = np.arange(2001, 2022)
sources  = ["Wind", "Solar", "Hydro"]
raw      = np.abs(rng.normal(loc=[50, 20, 30], scale=8, size=(len(years), 3)))
pct      = raw / raw.sum(axis=1, keepdims=True)
bottom   = np.zeros(len(years))
for j, (src, col) in enumerate(zip(sources, COLORS)):
    ax6.fill_between(years, bottom, bottom + pct[:, j], label=src, color=col, alpha=0.9)
    bottom += pct[:, j]
ax6.set_ylim(0, 1)
ax6.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0%}"))
ax6.set_title("Area (Normalized)")
ax6.set_xlabel("Year")
ax6.set_ylabel("Share of generation")
ax6.legend(frameon=False, fontsize=7, loc="upper left")


# ── 7. Histogram ──────────────────────────────────────────────────────────
ax7 = fig.add_subplot(sub[2, 0])
grp_a = rng.normal(50, 12, 250)
grp_b = rng.normal(70,  9, 250)
ax7.hist(grp_a, bins=22, alpha=0.75, label="Group A", color=COLORS[0])
ax7.hist(grp_b, bins=22, alpha=0.75, label="Group B",
         color=COLORS[1] if len(COLORS) > 1 else COLORS[0])
ax7.set_title("Histogram")
ax7.set_xlabel("Value")
ax7.set_ylabel("Count")
ax7.legend(frameon=False, fontsize=8)


# ── 8. Violin ─────────────────────────────────────────────────────────────
ax8 = fig.add_subplot(sub[2, 1])
violin_data = [rng.normal(45 + i * 12, 8 + i * 1.5, 120) for i in range(3)]
parts = ax8.violinplot(violin_data, positions=[1, 2, 3], showmedians=True, showextrema=True)
for body, col in zip(parts["bodies"], COLORS):
    body.set_facecolor(col)
    body.set_alpha(0.75)
for key in ("cmedians", "cbars", "cmins", "cmaxes"):
    parts[key].set_color("black")
    parts[key].set_linewidth(0.8)
ax8.set_xticks([1, 2, 3])
ax8.set_xticklabels(cats)
ax8.set_title("Violin")
ax8.set_xlabel("Category")
ax8.set_ylabel("Value")


# ── 9. Palette swatches ────────────────────────────────────────────────────
ax9 = fig.add_subplot(sub[2, 2])
palette_names = list(PALETTES.keys())
n_rows = len(palette_names)
n_cols = max(len(p) for p in PALETTES.values())
for row, name in enumerate(palette_names):
    pal = PALETTES[name]
    for col, hex_c in enumerate(pal):
        ax9.add_patch(mpatches.Rectangle((col, n_rows - row - 1), 1, 0.82, color=hex_c))
ax9.set_xlim(0, n_cols)
ax9.set_ylim(-0.1, n_rows)
ax9.set_yticks([n_rows - i - 0.6 for i in range(n_rows)])
ax9.set_yticklabels(palette_names, fontsize=7)
ax9.set_xticks([])
ax9.spines["left"].set_visible(False)
ax9.spines["bottom"].set_visible(False)
ax9.tick_params(left=False)
ax9.tick_params(bottom=False)
ax9.set_title("Color Palettes")


# ── export ─────────────────────────────────────────────────────────────────
out = pathlib.Path(__file__).parent / "charite_mpl_showcase.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved → {out}")
plt.show()
