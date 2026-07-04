"""Matplotlib theme for Charité – Universitätsmedizin Berlin."""

from contextlib import contextmanager

from cycler import cycler

from .colors import TEXT_GREY, PRIME_BLUE, PRIME_LGREY, BLACK, WHITE
from .palettes import PALETTES
from .fonts import build_font_stack
from ._theme_common import Margins, Thickness, resolve_font_sizes


def theme_charite(
    font: str | None = None,
    font_size: int = 10,
    thickness: float = 0.5,
    grid: bool = False,
    palette: str | list[str] = "primary",
    interactive: bool = False,
    tiny_margins: bool = False,
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
    interactive:
        Enable matplotlib interactive mode (equivalent to ``plt.ion()``).
        Useful in notebooks or scripts where you want plots to display
        without blocking.
    tiny_margins:
        Minimise all margins around the plot panel. Useful for dense layouts or 
        when saving figures with little surrounding whitespace.
    """
    sans_font_stack = build_font_stack(preferred=font)
    monospace_font_stack = ["Andale Mono", "Nimbus Mono L", "Courier New", "Courier", "Fixed", "Terminal", "monospace"]
    colors = PALETTES[palette] if isinstance(palette, str) else list(palette)

    FONT_SIZES = resolve_font_sizes(font_size)
    MARGINS = Margins(
        title=4 if tiny_margins else 8,
        label=2 if tiny_margins else 4,
        legend=2 if tiny_margins else 4,
        wspace=0.1 if tiny_margins else 0.2,
        hspace=0.125 if tiny_margins else 0.25
    )
    THICKNESS = Thickness(
        axes=thickness,
        grid=thickness * 0.6,
        ticks=thickness,
        lines=1.5,
        patches=0
    )

    return {
        # Font — monospace is a fallback for latex mathtt, code blocks, etc.
        "font.family":     "sans-serif",
        "font.sans-serif": sans_font_stack,
        "font.monospace":  monospace_font_stack,
        "font.size":       FONT_SIZES.label,

        # Axes
        "axes.linewidth":  THICKNESS.axes,
        "axes.titlelocation": "center",
        "xaxis.labellocation": "center",
        "yaxis.labellocation": "center",
        "axes.titlesize":  FONT_SIZES.title,
        "axes.titlecolor": PRIME_BLUE,
        "axes.titlepad":   MARGINS.title,
        "axes.labelsize":  FONT_SIZES.label,
        "axes.labelcolor": TEXT_GREY,
        "axes.labelpad":   MARGINS.label,
        "axes.edgecolor":  BLACK,
        "axes.facecolor":  WHITE,
        "axes.grid":       grid,
        "axes.axisbelow":  True,
        "axes.spines.top":   False,
        "axes.spines.right": False,

        # Axes 3D (only visible when projection='3d')
        "axes3d.grid":            grid,
        "axes3d.xaxis.panecolor": WHITE,
        "axes3d.yaxis.panecolor": WHITE,
        "axes3d.zaxis.panecolor": WHITE,

        # Polar axes (only visible when projection='polar')
        "polaraxes.grid":         grid,

        # Grid (only visible when grid=True)
        "grid.color":       PRIME_LGREY,
        "grid.linewidth":   THICKNESS.grid,
        # "grid.minor.alpha": 0.48,

        # Ticks
        "xtick.color":         BLACK,
        "ytick.color":         BLACK,
        "xtick.labelsize":     FONT_SIZES.label,
        "ytick.labelsize":     FONT_SIZES.label,
        "xtick.labelcolor":    TEXT_GREY,
        "ytick.labelcolor":    TEXT_GREY,
        "xtick.major.size":    2,
        "ytick.major.size":    2,
        "xtick.major.pad":     2,
        "ytick.major.pad":     2,
        "xtick.major.width":   THICKNESS.ticks,
        "ytick.major.width":   THICKNESS.ticks,
        "xtick.minor.visible": False,
        "ytick.minor.visible": False,

        # Text
        "text.color": TEXT_GREY,
        "text.antialiased": True,

        # Figure
        "figure.facecolor":      WHITE,
        "figure.edgecolor":      WHITE,
        "figure.dpi":            100,
        "figure.figsize":        (11, 8),
        "figure.subplot.hspace": MARGINS.hspace,
        "figure.subplot.wspace": MARGINS.wspace,
        "figure.titlesize":      FONT_SIZES.title,
        "figure.labelsize":      FONT_SIZES.label,

        # Lines / markers
        "lines.linewidth":   THICKNESS.lines,
        "lines.markersize":  6,
        "lines.antialiased": True,

        # Patches (bars, etc.)
        "patch.linewidth":       THICKNESS.patches,
        "patch.force_edgecolor": False,
        "patch.antialiased":     True,

        # Histograms
        "hist.bins": "auto",

        # Legend
        "legend.fancybox":       True,
        "legend.frameon":        False,
        "legend.fontsize":       FONT_SIZES.legend,
        "legend.title_fontsize": FONT_SIZES.title,
        "legend.labelcolor":     TEXT_GREY,

        # Interactive mode
        "interactive": interactive,

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
