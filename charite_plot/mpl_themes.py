"""Matplotlib theme for Charité – Universitätsmedizin Berlin (and other registered brands)."""

from __future__ import annotations

from contextlib import contextmanager
from functools import partial

from cycler import cycler

from ._theme_common import Margins, Thickness, resolve_font_sizes
from .brand import Brand
from .brands import DEFAULT_BRAND, get_brand
from .fonts import build_font_stack

__all__ = ["theme", "theme_charite", "theme_bih", "enable", "using"]


def theme(
    font: str | None = None,
    font_size: int = 10,
    thickness: float = 0.5,
    grid: bool = False,
    palette: str | list[str] | None = None,
    background: str = "white",
    tiny_margins: bool = False,
    interactive: bool = False,
    *,
    brand: str | Brand = DEFAULT_BRAND,
) -> dict:
    """Return matplotlib rcParams dict for a corporate identity theme.

    Parameters
    ----------
    font:
        Preferred font family. Falls back through the brand's font stack
        (for Charité: Charité Text Office → Calibri → DejaVu Sans → sans-serif)
        if the requested font is not installed.
    font_size:
        Base font size in points. Defaults to 10 for screen; use 8 for print.
    thickness:
        Axis line and tick width. Mirrors the R ``thickness`` parameter.
    grid:
        Show major grid lines. Disabled by default.
    palette:
        Name of one of the brand's palettes or a list of hex color strings used
        for the ``axes.prop_cycle``. ``None`` uses the brand's default palette.
    background:
        Figure and axes background color.
    tiny_margins:
        Minimise all margins around the plot panel. Useful for dense layouts or
        when saving figures with little surrounding whitespace.
    interactive:
        Enable matplotlib interactive mode (equivalent to ``plt.ion()``).
        Useful in notebooks or scripts where you want plots to display
        without blocking. Matplotlib-specific (Altair charts use
        ``.interactive()``).
    brand:
        Registered brand name (default ``"charite"``) or a
        :class:`~charite_plot.brand.Brand` instance. Keyword-only.
    """
    brand = get_brand(brand)
    roles = brand.roles
    sans_font_stack = build_font_stack(preferred=font, stack=brand.font_stack)
    monospace_font_stack = ["Andale Mono", "Nimbus Mono L", "Courier New", "Courier", "Fixed", "Terminal", "monospace"]
    colors = brand.palette(palette)

    FONT_SIZES = resolve_font_sizes(font_size)
    MARGINS = Margins(
        title=4 if tiny_margins else 8,
        label=2 if tiny_margins else 4,
        legend=2 if tiny_margins else 4,
        wspace=0.1 if tiny_margins else 0.2,
        hspace=0.125 if tiny_margins else 0.25,
    )
    THICKNESS = Thickness(axes=thickness, grid=thickness * 0.6, ticks=thickness, lines=1.5, patches=0)

    return {
        # Font — monospace is a fallback for latex mathtt, code blocks, etc.
        "font.family": "sans-serif",
        "font.sans-serif": sans_font_stack,
        "font.monospace": monospace_font_stack,
        "font.size": FONT_SIZES.label,
        # Axes
        "axes.linewidth": THICKNESS.axes,
        "axes.titlelocation": "center",
        "xaxis.labellocation": "center",
        "yaxis.labellocation": "center",
        "axes.titlesize": FONT_SIZES.title,
        "axes.titlecolor": roles.primary,
        "axes.titlepad": MARGINS.title,
        "axes.labelsize": FONT_SIZES.label,
        "axes.labelcolor": roles.text,
        "axes.labelpad": MARGINS.label,
        "axes.edgecolor": roles.axis,
        "axes.facecolor": background,
        "axes.grid": grid,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        # Axes 3D (only visible when projection='3d')
        "axes3d.grid": grid,
        "axes3d.xaxis.panecolor": "#ffffff",
        "axes3d.yaxis.panecolor": "#ffffff",
        "axes3d.zaxis.panecolor": "#ffffff",
        # Polar axes (only visible when projection='polar')
        "polaraxes.grid": grid,
        # Grid (only visible when grid=True)
        "grid.color": roles.grid,
        "grid.linewidth": THICKNESS.grid,
        # "grid.minor.alpha": 0.48,
        # Ticks
        "xtick.color": roles.axis,
        "ytick.color": roles.axis,
        "xtick.labelsize": FONT_SIZES.label,
        "ytick.labelsize": FONT_SIZES.label,
        "xtick.labelcolor": roles.text,
        "ytick.labelcolor": roles.text,
        "xtick.major.size": 2,
        "ytick.major.size": 2,
        "xtick.major.pad": 2,
        "ytick.major.pad": 2,
        "xtick.major.width": THICKNESS.ticks,
        "ytick.major.width": THICKNESS.ticks,
        "xtick.minor.visible": False,
        "ytick.minor.visible": False,
        # Text
        "text.color": roles.text,
        "text.antialiased": True,
        # Figure
        "figure.facecolor": background,
        "figure.edgecolor": background,
        "figure.dpi": 100,
        "figure.figsize": (11, 8),
        "figure.subplot.hspace": MARGINS.hspace,
        "figure.subplot.wspace": MARGINS.wspace,
        "figure.titlesize": FONT_SIZES.title,
        "figure.labelsize": FONT_SIZES.label,
        # Lines / markers
        "lines.linewidth": THICKNESS.lines,
        "lines.markersize": 6,
        "lines.antialiased": True,
        # Patches (bars, etc.)
        "patch.linewidth": THICKNESS.patches,
        "patch.force_edgecolor": False,
        "patch.antialiased": True,
        # Histograms
        "hist.bins": "auto",
        # Legend
        "legend.fancybox": True,
        "legend.frameon": False,
        "legend.fontsize": FONT_SIZES.legend,
        "legend.title_fontsize": FONT_SIZES.title,
        "legend.labelcolor": roles.text,
        # Interactive mode
        "interactive": interactive,
        # Save
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.transparent": True,
        # Color cycle
        "axes.prop_cycle": cycler("color", colors),
    }


theme_charite = partial(theme, brand="charite")
theme_bih = partial(theme, brand="bih")


def enable(**kwargs) -> None:
    """Apply a brand theme (Charité by default) to matplotlib's global rcParams (permanent until reset).

    Parameters
    ----------
    **kwargs:
        Any parameter accepted by :func:`theme` (``brand``, ``font``,
        ``font_size``, ``thickness``, ``grid``, ``palette``, ``background``,
        ``tiny_margins``, ``interactive``).

    Examples
    --------
    ```python
    from charite_plot.mpl_themes import enable
    enable(palette="goldelse", font_size=8)
    ```
    """
    import matplotlib as mpl

    mpl.rcParams.update(theme(**kwargs))


@contextmanager
def using(**kwargs):
    """Temporarily apply a brand theme (Charité by default), restoring the previous rcParams on exit.

    Parameters
    ----------
    **kwargs:
        Any parameter accepted by :func:`theme`.

    Examples
    --------
    ```python
    from charite_plot.mpl_themes import using
    with using(palette="goldelse"):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
    ```
    """
    import matplotlib as mpl

    with mpl.rc_context(theme(**kwargs)):
        yield
