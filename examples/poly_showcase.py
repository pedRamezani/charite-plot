"""Synthetic time-series showcase — generates the charite-plot theme example image.

Replicates the curves from ``tools/data/simulate_timeseries_data.R`` in the
charite R package: three conditions (wiggly normal, cubic polynomial, square
root) z-scored and plotted with uniform ±SE bands.

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

apply_theme(theme_charite(font_size=10))

# ── reproduce R's simulate_timeseries_data.R (set.seed(42)) ────────────────
# R and numpy use different RNGs so the tiny noise terms differ slightly,
# but they are visually negligible after z-scoring (sd ≤ 0.01).
rng = np.random.default_rng(42)

n_time = 100
time   = np.linspace(0, 1, n_time)   # seq(0, 1, length.out = 100)
t_axis = np.arange(1, n_time + 1)    # seq(1, 100) — x-axis


def _dnorm(x: np.ndarray, mean: float, sd: float) -> np.ndarray:
    """Normal PDF — equivalent to R's dnorm()."""
    return np.exp(-0.5 * ((x - mean) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


def _scale(x: np.ndarray) -> np.ndarray:
    """Center and unit-scale — equivalent to R's scale()."""
    return (x - x.mean()) / x.std(ddof=1)


# C1: wiggly normal
c1_core = _dnorm(time, mean=0.5, sd=0.15)
c1 = (c1_core
      + 0.1  * np.sin(25 * time)
      + 0.05 * np.cos(40 * time)
      + rng.normal(0, 0.005, n_time))

# C2: 3rd-order polynomial
c2 = 3.9 * time**3 - 6 * time**2 + 3 * time + rng.normal(0, 0.01, n_time)

# C3: square root
c3 = time**0.5 + rng.normal(0, 0.005, n_time)

# z-score and shift (matching the R data frame construction)
means = {
    "C1": _scale(c1) + 2.2,
    "C2": _scale(c2) + 2.8,
    "C3": _scale(c3) + 2.8,
}

# SE: runif(n_time * 3, min = 0.4, max = 0.6), sliced per condition
se_all = rng.uniform(0.4, 0.6, n_time * 3)
ses = {
    "C1": se_all[0          : n_time],
    "C2": se_all[n_time     : 2 * n_time],
    "C3": se_all[2 * n_time :],
}

# ── plot ───────────────────────────────────────────────────────────────────
colors = [KORALL, PRIME_BLUE, PRIME_DGREY]   # C1, C2, C3

fig, ax = plt.subplots(figsize=(6, 4.5))     # 4:3
fig.subplots_adjust(top=0.88)
fig.suptitle("Charité", fontsize=16, y=0.95, color=PRIME_BLUE)
fig.text(0.5, 0.90, "mpl Theme", ha="center", va="top", fontsize=9.5, color=TEXT_GREY)

for (label, mean), se, color in zip(means.items(), ses.values(), colors):
    ax.fill_between(t_axis, mean - se, mean + se, alpha=0.25, color=color, linewidth=0)
    ax.plot(t_axis, mean, lw=2, label=label, color=color)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.set_xlabel("Time")
ax.set_ylabel("Signal")
ax.legend(frameon=False)

# despine: offset spines outward and trim to tick extent (seaborn-style)
for side in ("left", "bottom"):
    ax.spines[side].set_position(("outward", 0))
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
xt = np.asarray(ax.get_xticks())
xt = xt[(xt >= ax.get_xlim()[0]) & (xt <= ax.get_xlim()[1])]
if xt.size:
    ax.spines["bottom"].set_bounds(xt[0], xt[-1])
yt = np.asarray(ax.get_yticks())
yt = yt[(yt >= ax.get_ylim()[0]) & (yt <= ax.get_ylim()[1])]
if yt.size:
    ax.spines["left"].set_bounds(yt[0], yt[-1])

# ── save ───────────────────────────────────────────────────────────────────
out = pathlib.Path(__file__).parent.parent / "docs" / "assets" / "theme_example.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Saved → {out}")
plt.show()
