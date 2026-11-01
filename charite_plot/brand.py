"""Brand definition — everything organisation-specific that a theme needs.

A :class:`Brand` bundles the colors, palettes, font stack and color *roles*
of one corporate identity. The theme builders in :mod:`charite_plot.mpl_themes`
and :mod:`charite_plot.altair_themes` are brand-agnostic and only read from a
``Brand``, so adding a new organisation means defining a new ``Brand`` (see
``charite_plot/brands/charite.py``) — no theme code has to change.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

__all__ = ["Roles", "Brand"]


@dataclass(frozen=True)
class Roles:
    """Which brand color is used for which part of a chart."""

    primary: str  # titles, facet header background
    text: str  # axis/legend labels, tick labels, body text
    axis: str  # spines/domain lines and tick marks
    grid: str  # grid lines
    diverging: tuple[str, str, str]  # low → mid → high for diverging scales
    sequential: tuple[str, str]  # low → high for heatmaps / ramps
    on_primary: str = "#ffffff"  # text drawn on a ``primary`` background


@dataclass(frozen=True)
class Brand:
    """A corporate identity: colors, palettes, fonts and color roles.

    Parameters
    ----------
    name:
        Short registry key, e.g. ``"charite"``. Also used as the Altair theme name.
    display_name:
        Human-readable name, e.g. ``"Charité – Universitätsmedizin Berlin"``.
    colors:
        All named brand colors (lowercase name → hex).
    palettes:
        Named categorical palettes (name → list of hex colors).
    roles:
        Color roles used by the theme builders.
    font_stack:
        Preferred fonts in fallback order, ending in a generic family.
    default_palette:
        Palette used when a theme is built without an explicit ``palette``.
    """

    name: str
    display_name: str
    colors: Mapping[str, str]
    palettes: Mapping[str, Sequence[str]]
    roles: Roles
    font_stack: Sequence[str]
    default_palette: str = "primary"

    def __post_init__(self) -> None:
        if self.default_palette not in self.palettes:
            raise ValueError(
                f"Brand {self.name!r}: default_palette {self.default_palette!r} "
                f"is not one of its palettes {list(self.palettes)}"
            )

    def palette(self, name_or_colors: str | Sequence[str] | None = None) -> list[str]:
        """Resolve a palette name (or pass through a color list) to a list of hex colors.

        ``None`` returns the brand's ``default_palette``.
        """
        if name_or_colors is None:
            name_or_colors = self.default_palette
        if isinstance(name_or_colors, str):
            if name_or_colors not in self.palettes:
                raise ValueError(
                    f"Unknown palette {name_or_colors!r} for brand {self.name!r}. "
                    f"Available palettes: {list(self.palettes)}"
                )
            return list(self.palettes[name_or_colors])
        return list(name_or_colors)
