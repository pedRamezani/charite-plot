"""Altair / Vega-Lite theme for Charité – Universitätsmedizin Berlin.

Register and enable with::

    from charite_plot.altair_themes import enable
    enable()                              # default params
    enable(palette="goldelse")            # custom palette
    enable(font="Arial", font_size=13)    # font override
"""

from __future__ import annotations

from .colors import (
    BLACK, WHITE, TEXT_GREY, PRIME_BLUE, PRIME_LGREY,
    SECOND_DBLUE, KORALL,
)
from .palettes import PALETTES
from .fonts import build_font_stack
from ._theme_common import Margins, Thickness, resolve_font_sizes

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from altair.theme import AxisConfigKwds, ThemeConfig


def _css_font_stack(preferred: str | None) -> str:
    """Return a CSS font-family string (comma-separated, quoted if needed)."""
    def _quote(name: str) -> str:
        return f'"{name}"' if " " in name else name

    return ", ".join(_quote(f) for f in build_font_stack(preferred=preferred))


def theme_charite(
    font: str | None = None,
    font_size: int = 12,
    thickness: float = 0.5,
    grid: bool = False,
    palette: str | list[str] = "primary",
    background: str = "white",
    tiny_margins: bool = False,
) -> ThemeConfig:
    """Return an Altair theme config dict for the Charité corporate theme.

    Parameters
    ----------
    font:
        Preferred font. Falls back through Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif.
    font_size:
        Base font size in pixels.
    thickness:
        Axis line and tick width.
    grid:
        Show axis grid lines.
    palette:
        Built-in palette name or list of hex colors for the categorical range.
    background:
        Chart background color.
    tiny_margins:
        Minimise all paddings around the chart.
    """
    colors = PALETTES[palette] if isinstance(palette, str) else list(palette)
    font_stack = _css_font_stack(preferred=font)

    FONT_SIZES = resolve_font_sizes(font_size)
    MARGINS = Margins(
        title=8 if tiny_margins else 12,   # chart title offset
        label=3 if tiny_margins else 6,    # axis / legend title padding
        legend=2 if tiny_margins else 4,   # legend inner padding
    )
    THICKNESS = Thickness(
        axes=thickness,          # domain line width
        grid=thickness * 0.8,    # grid line width
        ticks=thickness,         # tick mark width
        lines=2,                 # line-mark stroke width (independent of thickness)
        patches=0.4,             # geoshape stroke width
    )
    CHART_PAD = 6 if tiny_margins else 10

    axis: AxisConfigKwds = {
        "labelFont":     font_stack,
        "titleFont":     font_stack,
        "labelFontSize": FONT_SIZES.label,
        "titleFontSize": FONT_SIZES.subtitle,
        "labelColor":    TEXT_GREY,
        "titleColor":    TEXT_GREY,
        "titlePadding":  MARGINS.label,
        "domain":        True,
        "domainColor":   BLACK,
        "domainWidth":   THICKNESS.axes,
        "ticks":         True,
        "tickColor":     BLACK,
        "tickWidth":     THICKNESS.ticks,
        "tickSize":      4,
        "grid":          grid,
        "gridColor":     PRIME_LGREY,
        "gridWidth":     THICKNESS.grid,
        "gridOpacity":   0.85,
    }

    return {
        "config": {
            "background": background,
            "font":       font_stack,
            "padding":    {"top": CHART_PAD, "bottom": CHART_PAD, "left": CHART_PAD, "right": CHART_PAD},
            "view":  {"stroke": None},
            "axis":  axis,
            "axisX": axis,
            "axisY": axis,
            "legend": {
                "labelFont":     font_stack,
                "titleFont":     font_stack,
                "labelFontSize": FONT_SIZES.legend,
                "titleFontSize": FONT_SIZES.subtitle,
                "labelColor":    TEXT_GREY,
                "titleColor":    TEXT_GREY,
                "titlePadding":  MARGINS.label,
                "padding":       MARGINS.legend,
                "rowPadding":    FONT_SIZES.legend / 4,
                "symbolSize":    100,
            },
            "header": {
                "labelFont":       font_stack,
                "titleFont":       font_stack,
                "labelFontSize":   FONT_SIZES.label,
                "titleFontSize":   FONT_SIZES.subtitle,
                "labelColor":      WHITE,
                "titleColor":      PRIME_BLUE,
                "labelBackground": PRIME_BLUE,
            },
            "title": {
                "font":             font_stack,
                "subtitleFont":     font_stack,
                "fontSize":         FONT_SIZES.title,
                "subtitleFontSize": FONT_SIZES.subtitle,
                "color":            PRIME_BLUE,
                "subtitleColor":    TEXT_GREY,
                "anchor":           "middle",
                "offset":           MARGINS.title,
            },
            "range": {
                "category":  colors,
                "ordinal":   colors,
                "diverging": [SECOND_DBLUE, "#ffffff", KORALL],
                "heatmap":   ["#ffffff", PRIME_BLUE],
                "ramp":      ["#ffffff", PRIME_BLUE],
            },
            "bar":      {"color": colors[0], "binSpacing": 1},
            "line":     {"color": colors[0], "strokeWidth": THICKNESS.lines},
            "point":    {"color": colors[0], "size": 60, "opacity": 0.85, "filled": True},
            "area":     {"color": colors[0], "opacity": 0.8},
            "arc":      {"color": colors[0]},
            "rect":     {"color": colors[0]},
            "geoshape": {"stroke": WHITE, "strokeWidth": THICKNESS.patches},
            "text":     {"font": font_stack, "fontSize": FONT_SIZES.label, "color": TEXT_GREY},
        }
    }


def register() -> None:
    """Register the Charité theme with Altair's theme registry (default params)."""
    import altair as alt
    alt.theme.register("charite", enable=False)(theme_charite)


def enable(**kwargs) -> None:
    """Register and enable the Charité theme in Altair.

    Parameters
    ----------
    **kwargs:
        Any parameter accepted by ``theme_charite``
        (``font``, ``font_size``, ``thickness``, ``grid``, ``palette``,
        ``background``, ``tiny_margins``).

    Examples
    --------
    ```python
    from charite_plot.altair_themes import enable
    enable(palette="goldelse", font_size=13)
    ```
    """
    import altair as alt
    func = (lambda: theme_charite(**kwargs)) if kwargs else theme_charite
    alt.theme.register("charite", enable=True)(func)
