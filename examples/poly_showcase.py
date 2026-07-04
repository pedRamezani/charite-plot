"""Synthetic time-series showcase — generates the charite-plot theme example image.

Replicates the curves from ``tools/data/simulate_timeseries_data.R`` in the
charite R package: three conditions (wiggly normal, cubic polynomial, square
root) z-scored and plotted with uniform ±SE bands.

Produces one asset in docs/assets/:
    theme_example.png

Run with:
    python examples/poly_showcase.py
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt

from charite_plot.mpl_themes import theme_charite, apply_theme
from charite_plot.colors import PRIME_BLUE, PRIME_DGREY, KORALL, TEXT_GREY

COLORS = [KORALL, PRIME_BLUE, PRIME_DGREY]   # C1, C2, C3
ASSETS = pathlib.Path(__file__).parent.parent / "docs" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
OUT = ASSETS / "theme_example.png"
SAVE_KW = dict(dpi=300, bbox_inches="tight", facecolor="white")


# ── data helpers ────────────────────────────────────────────────────────────

def _dnorm(x: np.ndarray, mean: float, sd: float) -> np.ndarray:
    return np.exp(-0.5 * ((x - mean) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


def _scale(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / x.std(ddof=1)


def _generate_data():
    # R and numpy use different RNGs so the tiny noise terms differ slightly,
    # but they are visually negligible after z-scoring (sd ≤ 0.01).
    rng = np.random.default_rng(42)
    n = 100
    time   = np.linspace(0, 1, n)
    t_axis = np.arange(1, n + 1)

    c1_core = _dnorm(time, mean=0.5, sd=0.15)
    c1 = (c1_core
          + 0.1  * np.sin(25 * time)
          + 0.05 * np.cos(40 * time)
          + rng.normal(0, 0.005, n))
    c2 = 3.9 * time**3 - 6 * time**2 + 3 * time + rng.normal(0, 0.01, n)
    c3 = time**0.5 + rng.normal(0, 0.005, n)

    means = {"C1": _scale(c1) + 2.2, "C2": _scale(c2) + 2.8, "C3": _scale(c3) + 2.8}
    se_all = rng.uniform(0.4, 0.6, n * 3)
    ses = {"C1": se_all[:n], "C2": se_all[n:2*n], "C3": se_all[2*n:]}
    return t_axis, means, ses


# ── plot helpers ────────────────────────────────────────────────────────────

def _plot_curves(ax: plt.Axes, t_axis, means, ses, frameon: bool = False) -> None:
    for (label, mean), se, color in zip(means.items(), ses.values(), COLORS):
        ax.fill_between(t_axis, mean - se, mean + se, alpha=0.25, color=color, linewidth=0)
        ax.plot(t_axis, mean, lw=2, label=label, color=color)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Time")
    ax.set_ylabel("Signal")
    ax.legend(frameon=frameon)


def _despine(ax: plt.Axes) -> None:
    """Seaborn-style despine: trim spines to tick extent."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_position(("outward", 0))
    xt = np.asarray(ax.get_xticks())
    xt = xt[(xt >= ax.get_xlim()[0]) & (xt <= ax.get_xlim()[1])]
    if xt.size:
        ax.spines["bottom"].set_bounds(xt[0], xt[-1])
    yt = np.asarray(ax.get_yticks())
    yt = yt[(yt >= ax.get_ylim()[0]) & (yt <= ax.get_ylim()[1])]
    if yt.size:
        ax.spines["left"].set_bounds(yt[0], yt[-1])


# ── generate data once ──────────────────────────────────────────────────────
t_axis, means, ses = _generate_data()


# ── single: Charité theme ───────────────────────────────────────────────────
apply_theme(theme_charite(font_size=14, thickness=1))

fig, ax = plt.subplots(figsize=(6, 4.5))
fig.subplots_adjust(top=0.88)
fig.suptitle("Charité", fontsize=16, y=0.95, color=PRIME_BLUE)
fig.text(0.5, 0.90, "mpl Theme", ha="center", va="top", fontsize=9.5, color=TEXT_GREY)
_plot_curves(ax, t_axis, means, ses)
_despine(ax)
fig.savefig(OUT, **SAVE_KW)
print(f"Saved → {OUT}")
plt.show()
