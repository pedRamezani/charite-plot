"""Matplotlib theme for Charité – Universitätsmedizin Berlin."""

from contextlib import contextmanager

from cycler import cycler

from .colors import TEXT_GREY, PRIME_BLUE, PRIME_LGREY, BLACK
from .palettes import PALETTES
from .fonts import build_font_stack


def theme_charite(
    font: str | None = None,
    font_size: float = 10,
    thickness: float = 0.5,
    grid: bool = False,
    palette: str | list[str] = "primary",
) -> dict:
    """Return matplotlib rcParams dict for the Charité corporate identity theme.

    Parameters
    ----------
    font:
        Preferred font family. Falls back through Charité Text Office →
        Charit? Text Office → Calibri → DejaVu Sans → sans-serif if the requested font is not installed.
    font_size:
        Base font size in points. Defaults to 10 for screen; use 8 for print.
    thickness:
        Axis line and tick width. Mirrors the R ``thickness`` parameter.
    grid:
        Show major grid lines. Disabled by default.
    palette:
        Name of a built-in palette or a list of hex color strings used for the
        ``axes.prop_cycle``.
    """
    colors = PALETTES[palette] if isinstance(palette, str) else list(palette)

    return {
        # Font — monospace is a fallback for latex mathtt, code blocks, etc.
        "font.family":     "sans-serif",
        "font.sans-serif": build_font_stack(preferred=font),
        "font.monospace": ["Andale Mono", "Nimbus Mono L", "Courier New", "Courier", "Fixed", "Terminal", "monospace"],
        "font.size":       font_size,

        # Spines — only bottom and left visible (mirrors theme_classic in R)
        "axes.spines.top":   False,
        "axes.spines.right": False,

        # Axes
        "axes.linewidth":  thickness,
        "axes.titlesize":  round(font_size * 1.2),
        "axes.titlecolor": PRIME_BLUE,
        "axes.titlepad":   8,
        "axes.labelsize":  font_size,
        "axes.labelcolor": TEXT_GREY,
        "axes.edgecolor":  BLACK,
        "axes.facecolor":  "white",
        "axes.grid":       grid,
        "axes.axisbelow":  True,
        "axes3d.xaxis.panecolor": "white",
        "axes3d.yaxis.panecolor": "white",
        "axes3d.zaxis.panecolor": "white",

        # Grid (only visible when grid=True)
        "grid.color":     PRIME_LGREY,
        "grid.linewidth": thickness * 0.6,
        "grid.alpha":     0.8,

        # Ticks
        "xtick.color":         BLACK,
        "ytick.color":         BLACK,
        "xtick.labelsize":     font_size - 1,
        "ytick.labelsize":     font_size - 1,
        "xtick.labelcolor":    TEXT_GREY,
        "ytick.labelcolor":    TEXT_GREY,
        "xtick.major.size":    3,
        "ytick.major.size":    3,
        "xtick.major.pad":     6,
        "ytick.major.pad":     6,
        "xtick.major.width":   thickness,
        "ytick.major.width":   thickness,
        "xtick.minor.visible": False,
        "ytick.minor.visible": False,

        # Text
        "text.color": TEXT_GREY,
        "text.antialiased": True,

        # Figure
        "figure.facecolor":      "white",
        "figure.edgecolor":      "white",
        "figure.dpi":            100,
        "figure.figsize":        (11, 8),
        "figure.subplot.hspace": 0.5,
        "figure.titlesize":      round(font_size * 1.2),
        "figure.labelsize":      font_size,

        # Lines / markers
        "lines.linewidth":   1.5,
        "lines.markersize":  6,
        "lines.antialiased": True,

        # Patches (bars, etc.)
        "patch.linewidth":   0,
        "patch.force_edgecolor": False,
        "patch.antialiased": True,

        # Histograms
        "hist.bins": "auto",

        # Legend
        "legend.fancybox":       True,
        "legend.frameon":        False,
        "legend.fontsize":       round(font_size * 0.9),
        "legend.title_fontsize": font_size,
        "legend.labelcolor":     TEXT_GREY,

        # Save
        "savefig.dpi":         300,
        "savefig.bbox":        "tight",
        "savefig.transparent": True,

        # Color cycle
        "axes.prop_cycle": cycler("color", colors),
    }


def apply_theme(params: dict) -> None:
    """Apply a theme dict as the active matplotlib rcParams (permanent until reset)."""
    import matplotlib as mpl
    mpl.rcParams.update(params)


@contextmanager
def using(params: dict):
    """Context manager: temporarily apply *params* then restore previous rcParams.

    Examples
    --------
    ```python
    with using(theme_charite(palette="goldelse")):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
    ```
    """
    import matplotlib as mpl
    with mpl.rc_context(params):
        yield
