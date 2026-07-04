"""Shared theme primitives for the matplotlib and Altair backends.

These small ``NamedTuple`` structures keep the per-backend theme builders
readable by giving names to the derived size/margin values. The font-size
ratios are shared so both backends scale identically from their base size
(matplotlib works in points, Altair in pixels, but the ratios are the same).
"""

from typing import NamedTuple


class FontSizes(NamedTuple):
    """Derived font sizes, all scaled from the base ``font_size``."""
    title: float
    subtitle: float
    label: float
    legend: float


class Margins(NamedTuple):
    """Derived margins/paddings around the plot panel.

    ``wspace`` / ``hspace`` are subplot-spacing fractions used only by the
    matplotlib backend; they default to ``0`` so the Altair backend can build
    a ``Margins`` without supplying them.
    """
    title: float
    label: float
    legend: float
    wspace: float = 0.0
    hspace: float = 0.0


class Thickness(NamedTuple):
    """Derived line widths, scaled from the base ``thickness``.

    ``lines`` / ``patches`` are matplotlib-specific defaults; they carry
    defaults so the Altair backend can build a ``Thickness`` from just the
    axis-related widths.
    """
    axes: float
    grid: float
    ticks: float
    lines: float = 1.5
    patches: float = 0.0


def resolve_font_sizes(font_size: float) -> FontSizes:
    """Return the standard Charité font-size ramp derived from *font_size*."""
    return FontSizes(
        title=round(font_size * 1.2),
        subtitle=font_size,
        label=font_size,
        legend=round(font_size * 0.8),
    )
