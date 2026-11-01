"""The BIH brand: handbook colors and tints, and the black-text deviation for papers."""

import re

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
def test_tint(color, percent, expected):
    assert tint(color, percent) == expected


@pytest.mark.parametrize("percent", [-1, 101])
def test_tint_out_of_range(percent):
    with pytest.raises(ValueError, match="between 0 and 100"):
        tint("#003754", percent)


@pytest.mark.parametrize("name", BIH.palettes)
def test_palettes_use_only_allowed_tints(name):
    """The handbook allows the five diagram colors in 10 % steps (plus black for ``mono``)."""
    assert set(BIH.palettes[name]) <= ALLOWED


def test_primary_palette_uses_only_primary_colors():
    """Blau and Weiß are BIH's primary colors; the accents have their own palette and are the default."""
    assert set(BIH.palettes["primary"]) <= {tint(bih.BLAU, p) for p in range(10, 101, 10)}
    assert BIH.default_palette == "accents"


def test_diverging_ends_have_equal_lightness():
    """Lavendel and Gold: both halves of a diverging scale look equally strong (unlike Blau vs Korall)."""
    assert BIH.roles.diverging == (bih.LAVENDEL, bih.WHITE, bih.GOLD)


def test_colors_are_hex():
    assert all(re.fullmatch(r"#[0-9a-f]{6}", c) for c in BIH.colors.values())


def test_mpl_text_and_axes_are_black():
    params = mpl_themes.theme_bih()
    for key in ("text.color", "axes.labelcolor", "axes.edgecolor", "xtick.color", "xtick.labelcolor"):
        assert params[key] == bih.BLACK
    assert params["axes.titlecolor"] == bih.BLAU
    assert params["font.sans-serif"][0] == "Trebuchet MS"


def test_altair_text_and_axes_are_black():
    config = altair_themes.theme_bih()["config"]
    assert config["axis"]["labelColor"] == config["axis"]["domainColor"] == bih.BLACK
    assert config["title"]["color"] == bih.BLAU
    assert config["range"]["category"] == BIH.palettes["accents"]


def test_aliases_match_brand_keyword():
    assert mpl_themes.theme_bih(font_size=8) == mpl_themes.theme(font_size=8, brand="bih")
    assert altair_themes.theme_bih(grid=True) == altair_themes.theme(grid=True, brand=BIH)
