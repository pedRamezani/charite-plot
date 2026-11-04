"""The BIH brand: handbook colors and tints, and the black-text deviation for papers."""

import pytest

from charite_plot import BIH, altair_themes, mpl_themes, tint
from charite_plot.brands import bih

# Diagram colors from the BIH Farbwelt; Dunkelrot and Hellrosa are text-only.
DIAGRAM_COLORS = {bih.BLAU, bih.KORALL, bih.GOLD, bih.MINERAL, bih.LAVENDEL}
# Black tints are allowed for ``mono``, following the black-text deviation.
ALLOWED = {tint(c, p) for c in DIAGRAM_COLORS | {bih.BLACK} for p in range(10, 101, 10)}


@pytest.mark.parametrize(
    ("color", "percent", "expected"),
    [("#003754", 100, "#003754"), ("#003754", 20, "#ccd7dd"), ("#ea5451", 0, "#ffffff"), ("#000000", 50, "#808080")],
)
def test_tint(color: str, percent: int, expected: str) -> None:
    """Tints mix with white: 100 % is the color itself, 0 % is white (values from the BIH Farbabstufungen)."""
    assert tint(color, percent) == expected


@pytest.mark.parametrize("percent", [-1, 101])
def test_tint_out_of_range(percent: int) -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        tint("#003754", percent)


@pytest.mark.parametrize("name", BIH.palettes)
def test_palettes_use_only_allowed_tints(name: str) -> None:
    """The handbook allows the five diagram colors in 10 % steps (plus black for ``mono``)."""
    assert set(BIH.palettes[name]) <= ALLOWED


def test_primary_palette_uses_only_primary_colors() -> None:
    """Blau and Weiß are BIH's primary colors; the accents have their own palette and are the default."""
    assert set(BIH.palettes["primary"]) <= {tint(bih.BLAU, p) for p in range(10, 101, 10)}
    assert BIH.default_palette == "accents"


def test_text_only_colors_are_not_in_palettes() -> None:
    used = {c for colors in BIH.palettes.values() for c in colors}
    assert not used & {bih.DUNKELROT, bih.HELLROSA}


def test_mpl_text_and_axes_are_black() -> None:
    """Deviation from the handbook: journals expect black figure text; titles stay BIH-Blau."""
    params = mpl_themes.theme_bih()
    for key in ("text.color", "axes.labelcolor", "axes.edgecolor", "xtick.color", "xtick.labelcolor"):
        assert params[key] == bih.BLACK
    assert params["axes.titlecolor"] == bih.BLAU
    assert params["font.sans-serif"][0] == "Trebuchet MS"


def test_altair_text_and_axes_are_black() -> None:
    """Same deviation as for matplotlib, and the ``accents`` palette as the default category range."""
    config = altair_themes.theme_bih()["config"]
    assert config["axis"]["labelColor"] == config["axis"]["domainColor"] == bih.BLACK
    assert config["title"]["color"] == bih.BLAU
    assert config["range"]["category"] == BIH.palettes["accents"]


def test_aliases_match_brand_keyword() -> None:
    assert mpl_themes.theme_bih(font_size=8) == mpl_themes.theme(font_size=8, brand="bih")
    assert altair_themes.theme_bih(grid=True) == altair_themes.theme(grid=True, brand=BIH)
