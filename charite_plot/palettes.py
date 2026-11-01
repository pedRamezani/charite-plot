"""Palette lookup and resampling, for any registered brand."""

from __future__ import annotations

from .brand import Brand
from .brands import DEFAULT_BRAND, get_brand
from .brands.charite import CHARITE_PALETTES

__all__ = ["PALETTES", "make_palette"]

# Charité palettes, kept under the historical name for backwards compatibility.
PALETTES: dict[str, list[str]] = CHARITE_PALETTES


def make_palette(
    name_or_colors: str | list[str],
    n: int | None = None,
    reverse: bool = False,
    brand: str | Brand = DEFAULT_BRAND,
) -> list[str]:
    """Return a list of hex colors from a named palette or custom color list.

    Parameters
    ----------
    name_or_colors:
        A palette name of *brand* (see ``Brand.palettes``) or a list of hex color strings.
    n:
        Number of colors to return. ``None`` returns all colors in the palette.
        If ``n`` is larger than the palette, colors are linearly interpolated.
        If ``n`` is smaller, colors are subsampled evenly.
    reverse:
        Reverse the palette before sampling.
    brand:
        Brand name or :class:`~charite_plot.brand.Brand` whose palettes are searched.
    """
    colors = get_brand(brand).palette(name_or_colors)

    if reverse:
        colors = colors[::-1]

    if n is None:
        return colors

    if n == 1:
        return [colors[0]]

    if n <= len(colors):
        step = (len(colors) - 1) / (n - 1)
        return [colors[round(i * step)] for i in range(n)]

    # n > palette length: interpolate via matplotlib (lazy import)
    from matplotlib.colors import LinearSegmentedColormap, to_hex

    cmap = LinearSegmentedColormap.from_list("_palette_tmp", colors, N=n)
    return [to_hex(cmap(i / (n - 1))) for i in range(n)]
