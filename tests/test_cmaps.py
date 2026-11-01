"""Continuous scales: ``make_ramp`` (color stops, also for Altair) and ``make_cmap`` (matplotlib colormaps)."""

import pytest
from matplotlib.colors import to_hex

from charite_plot import BIH, PALETTES, get_brand, make_cmap, make_ramp, mpl_themes
from charite_plot.brands import bih, charite


def test_ramp_palette_goes_through_all_colors():
    assert make_ramp("berryseason") == PALETTES["berryseason"]
    assert make_ramp("versus", reverse=True) == PALETTES["versus"][::-1]


@pytest.mark.parametrize(
    ("name", "brand", "end"),
    [("prime_blue", "charite", charite.PRIME_BLUE), ("blau", "bih", bih.BLAU), ("#123456", "charite", "#123456")],
)
def test_ramp_single_color_starts_at_white(name, brand, end):
    assert make_ramp(name, brand=brand) == ["#ffffff", end]


def test_ramp_palette_name_wins_over_color_name():
    assert make_ramp("primary", brand="bih") == BIH.palettes["primary"]


def test_ramp_custom_list():
    assert make_ramp(["#000000", "#ff0000", "#ffffff"]) == ["#000000", "#ff0000", "#ffffff"]


def test_ramp_unknown():
    with pytest.raises(ValueError, match="neither a palette nor a color of brand 'bih'"):
        make_ramp("nope", brand="bih")


def test_make_cmap_endpoints_and_name():
    cmap = make_cmap("blau", brand="bih")
    assert cmap.name == "bih_blau"
    assert cmap.N == 256
    assert to_hex(cmap(0.0)) == "#ffffff"
    assert to_hex(cmap(1.0)) == bih.BLAU


def test_make_cmap_is_continuous():
    """Not restricted to the 3 palette colors: the midpoint of a two-color ramp is interpolated."""
    assert to_hex(make_cmap(["#000000", "#ffffff"])(0.5)) in {"#7f7f7f", "#808080"}


def test_make_cmap_palette_and_reverse():
    cmap = make_cmap("goldelse", reverse=True, n=8)
    assert cmap.name == "charite_goldelse_r"
    assert [to_hex(cmap(i / 7)) for i in range(8)] == PALETTES["goldelse"][::-1]


@pytest.mark.parametrize("brand", ["charite", "bih"])
def test_make_cmap_for_every_palette_and_color(brand):
    for name in [*get_brand(brand).palettes, *get_brand(brand).colors]:
        make_cmap(name, brand=brand)


@pytest.mark.parametrize("brand", ["charite", "bih"])
def test_make_ramp_roles(brand):
    roles = get_brand(brand).roles
    assert make_ramp("sequential", brand=brand) == list(roles.sequential)
    assert make_ramp("diverging", brand=brand, reverse=True) == list(roles.diverging)[::-1]


@pytest.mark.parametrize("brand", ["charite", "bih"])
def test_theme_default_cmap_is_sequential(brand):
    import matplotlib as mpl

    name = mpl_themes.theme(brand=brand)["image.cmap"]
    assert name == f"{brand}_sequential"
    cmap = mpl.colormaps[name]
    assert [to_hex(cmap(x)) for x in (0.0, 1.0)] == list(get_brand(brand).roles.sequential)


def test_using_sets_default_cmap():
    import matplotlib.pyplot as plt

    with mpl_themes.using(brand="bih"):
        fig, ax = plt.subplots()
        assert ax.imshow([[0, 1]]).get_cmap().name == "bih_sequential"
        plt.close(fig)
