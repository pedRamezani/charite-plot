"""Charité color palettes built from the shared color definitions."""

from .colors import (
    BLACK,
    PRIME_BLUE, PRIME_LGREY, PRIME_DGREY,
    SECOND_DBLUE, SECOND_LBLUE, KORALL,
    BRAUN, MOCCA, GRASGRUEN, LIMETTE, GRUEN, MINT,
    MINERAL, AQUA, LILA, LAVENDEL, BROMBEERE, PFLAUME,
    WEINROT, HIMBEER, ROT, MANGO, RAPSGELB,
)

PALETTES: dict[str, list[str]] = {
    "primary":     [PRIME_BLUE, PRIME_DGREY, PRIME_LGREY],
    "secondary":   [SECOND_DBLUE, SECOND_LBLUE, KORALL],
    "mono":        [BLACK, PRIME_DGREY, PRIME_LGREY],
    "light":       [SECOND_LBLUE, PRIME_LGREY],
    "versus":      [PRIME_BLUE, ROT],
    "nineties":    [LILA, MINT, MINERAL],
    "brickhouse":  [WEINROT, HIMBEER, MINT, GRUEN],
    "sunrise":     [SECOND_DBLUE, SECOND_LBLUE, RAPSGELB, MANGO],
    "berryseason": [HIMBEER, PFLAUME, BROMBEERE, SECOND_DBLUE, MOCCA, BRAUN],
    "goldelse":    [MANGO, RAPSGELB, LIMETTE, GRASGRUEN, AQUA, MINERAL, LAVENDEL, LILA],
}


def make_palette(
    name_or_colors: "str | list[str]",
    n: "int | None" = None,
    reverse: bool = False,
) -> list[str]:
    """Return a list of hex colors from a named palette or custom color list.

    Parameters
    ----------
    name_or_colors:
        A palette name (see ``PALETTES``) or a list of hex color strings.
    n:
        Number of colors to return. ``None`` returns all colors in the palette.
        If ``n`` is larger than the palette, colors are linearly interpolated.
        If ``n`` is smaller, colors are subsampled evenly.
    reverse:
        Reverse the palette before sampling.
    """
    if isinstance(name_or_colors, str):
        if name_or_colors not in PALETTES:
            raise ValueError(
                f"Unknown palette {name_or_colors!r}. "
                f"Available palettes: {list(PALETTES)}"
            )
        colors = list(PALETTES[name_or_colors])
    else:
        colors = list(name_or_colors)

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
    cmap = LinearSegmentedColormap.from_list("_charite_tmp", colors, N=n)
    return [to_hex(cmap(i / (n - 1))) for i in range(n)]
