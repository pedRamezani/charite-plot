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
    grid: bool = False,
    palette: str | list[str] = "primary",
    background: str = "white",
) -> ThemeConfig:
    """Return an Altair theme config dict for the Charité corporate theme.

    Parameters
    ----------
    font:
        Preferred font. Falls back through Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif.
    font_size:
        Base font size in pixels.
    grid:
        Show axis grid lines.
    palette:
        Built-in palette name or list of hex colors for the categorical range.
    background:
        Chart background color.
    """
    colors = PALETTES[palette] if isinstance(palette, str) else list(palette)
    font_str = _css_font_stack(preferred=font)
    label_size = font_size - 1
    title_size = round(font_size * 1.2)

    axis: AxisConfigKwds = {
        "labelFont":     font_str,
        "titleFont":     font_str,
        "labelFontSize": label_size,
        "titleFontSize": font_size,
        "labelColor":    TEXT_GREY,
        "titleColor":    TEXT_GREY,
        "titlePadding":  6,
        "domain":        True,
        "domainColor":   BLACK,
        "domainWidth":   0.5,
        "ticks":         True,
        "tickColor":     BLACK,
        "tickWidth":     0.5,
        "tickSize":      4,
        "grid":          grid,
        "gridColor":     PRIME_LGREY,
        "gridWidth":     0.4,
        "gridOpacity":   0.8,
    }

    return {
        "config": {
            "background": background,
            "font":       font_str,
            "padding":    {"top": 10, "bottom": 10, "left": 10, "right": 10},
            "view":  {"stroke": None},
            "axis":  axis,
            "axisX": axis,
            "axisY": axis,
            "legend": {
                "labelFont":     font_str,
                "titleFont":     font_str,
                "labelFontSize": label_size,
                "titleFontSize": font_size,
                "labelColor":    TEXT_GREY,
                "titleColor":    TEXT_GREY,
                "titlePadding":  6,
                "padding":       4,
                "rowPadding":    3,
                "symbolSize":    100,
            },
            "header": {
                "labelFont":       font_str,
                "titleFont":       font_str,
                "labelFontSize":   label_size,
                "titleFontSize":   font_size,
                "labelColor":      WHITE,
                "titleColor":      PRIME_BLUE,
                "labelBackground": PRIME_BLUE,
            },
            "title": {
                "font":             font_str,
                "subtitleFont":     font_str,
                "fontSize":         title_size,
                "subtitleFontSize": font_size,
                "color":            PRIME_BLUE,
                "subtitleColor":    TEXT_GREY,
                "anchor":           "middle",
                "offset":           12,
            },
            "range": {
                "category":  colors,
                "ordinal":   colors,
                "diverging": [SECOND_DBLUE, "#ffffff", KORALL],
                "heatmap":   ["#ffffff", PRIME_BLUE],
                "ramp":      ["#ffffff", PRIME_BLUE],
            },
            "bar":      {"color": colors[0], "binSpacing": 1},
            "line":     {"color": colors[0], "strokeWidth": 2},
            "point":    {"color": colors[0], "size": 60, "opacity": 0.85, "filled": True},
            "area":     {"color": colors[0], "opacity": 0.8},
            "arc":      {"color": colors[0]},
            "rect":     {"color": colors[0]},
            "geoshape": {"stroke": WHITE, "strokeWidth": 0.4},
            "text":     {"font": font_str, "fontSize": label_size, "color": TEXT_GREY},
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
        (``font``, ``font_size``, ``grid``, ``palette``, ``background``).

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
