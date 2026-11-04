"""Altair / Vega-Lite theme for Charité – Universitätsmedizin Berlin (and other registered brands).

Register and enable with::

    from charite_plot.altair_themes import enable
    enable()                              # default params
    enable(palette="goldelse")            # custom palette
    enable(font="Arial", font_size=13)    # font override
"""

from __future__ import annotations

from collections.abc import Sequence
from contextlib import contextmanager
from functools import partial
from typing import TYPE_CHECKING, LiteralString, cast
from uuid import uuid4

from ._theme_common import Margins, Thickness, resolve_font_sizes
from .brand import Brand
from .brands import DEFAULT_BRAND, get_brand
from .fonts import build_font_stack

if TYPE_CHECKING:
    from altair.theme import AxisConfigKwds, ThemeConfig

__all__ = ["theme", "theme_charite", "theme_bih", "enable", "using", "register"]


def _literal(value: str) -> LiteralString:
    """Altair annotates colors and theme names as ``LiteralString``; brand values are only known at runtime."""
    return cast("LiteralString", value)


def _css_font_stack(preferred: str | None, stack: Sequence[str]) -> str:
    """Return a CSS font-family string (comma-separated, quoted if needed)."""

    def _quote(name: str) -> str:
        return f'"{name}"' if " " in name else name

    return ", ".join(_quote(f) for f in build_font_stack(preferred=preferred, stack=stack))


def theme(
    font: str | None = None,
    font_size: int = 12,
    thickness: float = 0.5,
    grid: bool = False,
    palette: str | list[str] | None = None,
    background: str = "white",
    tiny_margins: bool = False,
    *,
    brand: str | Brand = DEFAULT_BRAND,
) -> ThemeConfig:
    """Return an Altair theme config dict for a corporate identity theme.

    Parameters
    ----------
    font:
        Preferred font. Falls back through the brand's font stack
        (for Charité: Charité Text Office → Calibri → DejaVu Sans → sans-serif).
    font_size:
        Base font size in pixels.
    thickness:
        Axis line and tick width.
    grid:
        Show axis grid lines.
    palette:
        Name of one of the brand's palettes or a list of hex colors for the
        categorical range. ``None`` uses the brand's default palette.
    background:
        Chart background color.
    tiny_margins:
        Minimise all paddings around the chart.
    brand:
        Registered brand name (default ``"charite"``) or a
        [`Brand`][charite_plot.brand.Brand] instance. Keyword-only.
    """
    brand = get_brand(brand)
    roles = brand.roles
    # Altair types colors as ``LiteralString``; brand colors are only known at runtime.
    primary, text, axis_color, grid_color = map(_literal, (roles.primary, roles.text, roles.axis, roles.grid))
    colors = [_literal(c) for c in brand.palette(palette)]
    diverging = [_literal(c) for c in roles.diverging]
    sequential = [_literal(c) for c in roles.sequential]
    font_stack = _css_font_stack(preferred=font, stack=brand.font_stack)

    FONT_SIZES = resolve_font_sizes(font_size)
    # fmt: off
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
        "labelColor":    text,
        "titleColor":    text,
        "titlePadding":  MARGINS.label,
        "domain":        True,
        "domainColor":   axis_color,
        "domainWidth":   THICKNESS.axes,
        "ticks":         True,
        "tickColor":     axis_color,
        "tickWidth":     THICKNESS.ticks,
        "tickSize":      4,
        "grid":          grid,
        "gridColor":     grid_color,
        "gridWidth":     THICKNESS.grid,
        "gridOpacity":   0.85,
    }

    return {
        "config": {
            "background": _literal(background),
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
                "labelColor":    text,
                "titleColor":    text,
                "titlePadding":  MARGINS.label,
                "padding":       MARGINS.legend,
                "rowPadding":    FONT_SIZES.legend / 4,
                "symbolSize":    100,
            },
            "header": {
                "labelFont":     font_stack,
                "titleFont":     font_stack,
                "labelFontSize": FONT_SIZES.label,
                "titleFontSize": FONT_SIZES.subtitle,
                "labelColor":    text,
                "titleColor":    primary,
            },
            "title": {
                "font":             font_stack,
                "subtitleFont":     font_stack,
                "fontSize":         FONT_SIZES.title,
                "subtitleFontSize": FONT_SIZES.subtitle,
                "color":            primary,
                "subtitleColor":    text,
                "anchor":           "middle",
                "offset":           MARGINS.title,
            },
            "range": {
                "category":  colors,
                "ordinal":   colors,
                "diverging": diverging,
                "heatmap":   sequential,
                "ramp":      sequential,
            },
            "bar":      {"color": colors[0], "binSpacing": 1},
            "line":     {"color": colors[0], "strokeWidth": THICKNESS.lines},
            "point":    {"color": colors[0], "size": 60, "opacity": 0.85, "filled": True},
            "area":     {"color": colors[0], "opacity": 0.8},
            "arc":      {"color": colors[0]},
            "rect":     {"color": colors[0]},
            "geoshape": {"stroke": "#ffffff", "strokeWidth": THICKNESS.patches},
            "text":     {"font": font_stack, "fontSize": FONT_SIZES.label, "color": text},
        }
    }
    # fmt: on


theme_charite = partial(theme, brand="charite")
"""Altair theme config for Charité: [`theme`][charite_plot.altair_themes.theme] with ``brand="charite"`` (same parameters, positional order kept)."""

theme_bih = partial(theme, brand="bih")
"""Altair theme config for the BIH: [`theme`][charite_plot.altair_themes.theme] with ``brand="bih"`` (same parameters)."""


def register(brand: str | Brand = DEFAULT_BRAND) -> None:
    """Register a brand theme (Charité by default) with Altair's theme registry (default params).

    The theme is registered under the brand's name, e.g. ``"charite"``.
    """
    import altair as alt

    brand = get_brand(brand)
    alt.theme.register(_literal(brand.name), enable=False)(partial(theme, brand=brand))


def enable(brand: str | Brand = DEFAULT_BRAND, **kwargs) -> None:
    """Register and enable a brand theme (Charité by default) in Altair.

    Parameters
    ----------
    brand:
        Registered brand name or [`Brand`][charite_plot.brand.Brand] instance.
        The theme is registered under the brand's name, e.g. ``"charite"``.
    **kwargs:
        Any other parameter accepted by [`theme`][charite_plot.altair_themes.theme]
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

    brand = get_brand(brand)
    alt.theme.register(_literal(brand.name), enable=True)(partial(theme, brand=brand, **kwargs))


@contextmanager
def using(brand: str | Brand = DEFAULT_BRAND, **kwargs):
    """Temporarily enable a brand theme (Charité by default), restoring the previous theme on exit.

    Mirrors [`charite_plot.mpl_themes.using`][charite_plot.mpl_themes.using]. Charts created (or serialised
    with ``chart.to_json()`` / ``chart.to_dict()``) inside the ``with`` block use
    the brand theme; the previously active theme is restored afterwards.

    Parameters
    ----------
    brand:
        Registered brand name or [`Brand`][charite_plot.brand.Brand] instance.
    **kwargs:
        Any other parameter accepted by [`theme`][charite_plot.altair_themes.theme].

    Examples
    --------
    ```python
    from charite_plot.altair_themes import using
    with using(palette="goldelse"):
        spec = chart.to_json()
    ```
    """
    import altair as alt

    brand = get_brand(brand)
    # Register under a unique throwaway name so we don't clobber the primary
    # brand registration and so nested ``using`` blocks don't collide.
    # ``alt.theme.enable`` restores the previous theme on exit; the temporary
    # registration is removed afterwards to keep the registry clean.
    name = _literal(f"_{brand.name}_{uuid4().hex}")
    alt.theme.register(name, enable=False)(partial(theme, brand=brand, **kwargs))
    try:
        # Altair's PluginEnabler.__exit__ lacks Optional parameter types, so ty rejects it as a context manager.
        with alt.theme.enable(name):  # ty: ignore[invalid-context-manager]
            yield
    finally:
        alt.theme.unregister(name)
