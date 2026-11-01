"""Brand registry.

Themes look brands up by name (``enable(brand="charite")``) or accept a
:class:`~charite_plot.brand.Brand` instance directly. Custom brands can be
added at runtime with :func:`register_brand`.
"""

from __future__ import annotations

from ..brand import Brand
from .charite import CHARITE

__all__ = ["BRANDS", "DEFAULT_BRAND", "register_brand", "get_brand", "CHARITE"]

BRANDS: dict[str, Brand] = {CHARITE.name: CHARITE}

DEFAULT_BRAND = CHARITE.name


def register_brand(brand: Brand) -> Brand:
    """Add *brand* to the registry (replacing any brand with the same name)."""
    BRANDS[brand.name] = brand
    return brand


def get_brand(brand: str | Brand = DEFAULT_BRAND) -> Brand:
    """Return the registered brand called *brand*, or *brand* itself if it is a ``Brand``."""
    if isinstance(brand, Brand):
        return brand
    try:
        return BRANDS[brand]
    except KeyError:
        raise ValueError(
            f"Unknown brand {brand!r}. Available brands: {list(BRANDS)}"
        ) from None
