"""Palette lookup, resampling and continuous colormaps, for any registered brand."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .brand import Brand
from .brands import DEFAULT_BRAND, get_brand
from .brands.charite import CHARITE_PALETTES

if TYPE_CHECKING:
    from matplotlib.colors import LinearSegmentedColormap

__all__ = ["PALETTES", "make_palette", "make_ramp", "make_cmap"]

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


def make_ramp(
    name_or_colors: str | list[str],
    reverse: bool = False,
    brand: str | Brand = DEFAULT_BRAND,
) -> list[str]:
    """Return the color stops of a continuous scale.

    Parameters
    ----------
    name_or_colors:
        - a palette name of *brand*: a gradient through all its colors
          (like ``scale_color_charite(palette, discrete = FALSE)`` in the R package);
        - ``"sequential"`` or ``"diverging"``: the brand's continuous scales
          (``Brand.roles``; also used by the themes for heatmaps and diverging scales);
        - a color name of *brand* (see ``Brand.colors``) or a hex color: a gradient
          from white to that color, like matplotlib's ``"Blues"``;
        - a list of hex colors: a gradient through them.

        Palette names take precedence over ``"sequential"``/``"diverging"``, and those over color names.
    reverse:
        Reverse the gradient.
    brand:
        Brand name or :class:`~charite_plot.brand.Brand` whose palettes and colors are searched.

    Examples
    --------
    Altair interpolates between the stops itself; ``interpolate="rgb"`` matches matplotlib:

    ```python
    alt.Color("value:Q", scale=alt.Scale(range=make_ramp("blau", brand="bih"), interpolate="rgb"))
    ```
    """
    brand = get_brand(brand)
    roles = {"sequential": brand.roles.sequential, "diverging": brand.roles.diverging}
    if isinstance(name_or_colors, str) and name_or_colors not in brand.palettes and name_or_colors in roles:
        colors = list(roles[name_or_colors])
    elif isinstance(name_or_colors, str) and name_or_colors not in brand.palettes:
        color = brand.colors.get(name_or_colors, name_or_colors)
        if not color.startswith("#"):
            raise ValueError(
                f"{name_or_colors!r} is neither a palette nor a color of brand {brand.name!r}. "
                f"Palettes: {list(brand.palettes)}; colors: {list(brand.colors)}"
            )
        colors = ["#ffffff", color]
    else:
        colors = brand.palette(name_or_colors)
    return colors[::-1] if reverse else colors


def make_cmap(
    name_or_colors: str | list[str],
    reverse: bool = False,
    brand: str | Brand = DEFAULT_BRAND,
    n: int = 256,
) -> LinearSegmentedColormap:
    """Return a continuous matplotlib colormap; see :func:`make_ramp` for the accepted names.

    Parameters
    ----------
    name_or_colors:
        Palette name, color name, hex color or list of hex colors (see :func:`make_ramp`).
    reverse:
        Reverse the colormap.
    brand:
        Brand name or :class:`~charite_plot.brand.Brand` whose palettes and colors are searched.
    n:
        Number of entries in the colormap's lookup table.

    Examples
    --------
    ```python
    ax.imshow(data, cmap=make_cmap("prime_blue"))  # white → Charité blue
    ax.scatter(x, y, c=z, cmap=make_cmap("berryseason"))  # through the whole palette
    ```
    """
    from matplotlib.colors import LinearSegmentedColormap

    brand = get_brand(brand)
    colors = make_ramp(name_or_colors, reverse=reverse, brand=brand)
    label = name_or_colors if isinstance(name_or_colors, str) else "custom"
    name = f"{brand.name}_{label}" + ("_r" if reverse else "")
    return LinearSegmentedColormap.from_list(name, colors, N=n)
