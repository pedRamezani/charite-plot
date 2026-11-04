"""Continuous scales: ``make_ramp`` (color stops, also for Altair) and ``make_cmap`` (matplotlib colormaps)."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest
from matplotlib.colors import to_hex

from charite_plot import BIH, PALETTES, get_brand, make_cmap, make_ramp, mpl_themes
from charite_plot.brands import bih, charite

# --- make_ramp -----------------------------------------------------------------------------


def test_ramp_palette_goes_through_all_colors() -> None:
    assert make_ramp("berryseason") == PALETTES["berryseason"]
    assert make_ramp("versus", reverse=True) == PALETTES["versus"][::-1]


@pytest.mark.parametrize(
    ("name", "brand", "end"),
    [("prime_blue", "charite", charite.PRIME_BLUE), ("blau", "bih", bih.BLAU), ("#123456", "charite", "#123456")],
)
def test_ramp_single_color_starts_at_white(name: str, brand: str, end: str) -> None:
    """A brand color name or any hex color gives a white → color ramp, like matplotlib's ``"Blues"``."""
    assert make_ramp(name, brand=brand) == ["#ffffff", end]


def test_ramp_palette_name_wins_over_color_name() -> None:
    """BIH has both a ``primary`` palette and colors; the palette takes precedence."""
    assert make_ramp("primary", brand="bih") == BIH.palettes["primary"]


@pytest.mark.parametrize("brand", ["charite", "bih"])
def test_ramp_roles(brand: str) -> None:
    """``"sequential"`` and ``"diverging"`` resolve to the brand's continuous scales."""
    roles = get_brand(brand).roles
    assert make_ramp("sequential", brand=brand) == list(roles.sequential)
    assert make_ramp("diverging", brand=brand, reverse=True) == list(roles.diverging)[::-1]


def test_ramp_unknown() -> None:
    with pytest.raises(ValueError, match="neither a palette nor a color of brand 'bih'"):
        make_ramp("nope", brand="bih")


# --- make_cmap -----------------------------------------------------------------------------


def test_make_cmap_endpoints_and_name() -> None:
    cmap = make_cmap("blau", brand="bih")
    assert cmap.name == "bih_blau"
    assert cmap.N == 256
    assert to_hex(cmap(0.0)) == "#ffffff"
    assert to_hex(cmap(1.0)) == bih.BLAU


def test_make_cmap_is_continuous() -> None:
    """Not restricted to the palette colors: the midpoint of a two-color ramp is interpolated."""
    assert to_hex(make_cmap(["#000000", "#ffffff"])(0.5)) in {"#7f7f7f", "#808080"}


def test_make_cmap_palette_and_reverse() -> None:
    """Sampled at the stops, the reversed colormap gives back the reversed palette."""
    cmap = make_cmap("goldelse", reverse=True, n=8)
    assert cmap.name == "charite_goldelse_r"
    assert [to_hex(cmap(i / 7)) for i in range(8)] == PALETTES["goldelse"][::-1]


@pytest.mark.parametrize("brand", ["charite", "bih"])
def test_make_cmap_matches_ramp_for_every_name(brand: str) -> None:
    """Every palette and color name works, and the colormap starts and ends at the ramp's ends."""
    for name in [*get_brand(brand).palettes, *get_brand(brand).colors]:
        cmap, ramp = make_cmap(name, brand=brand), make_ramp(name, brand=brand)
        assert [to_hex(cmap(0.0)), to_hex(cmap(1.0))] == [ramp[0], ramp[-1]], name


# --- default colormap of the theme ---------------------------------------------------------


@pytest.mark.parametrize("brand", ["charite", "bih"])
def test_theme_default_cmap_is_sequential(brand: str) -> None:
    """rcParams can only name a colormap, so the theme registers the brand's sequential one."""
    name = mpl_themes.theme(brand=brand)["image.cmap"]
    assert name == f"{brand}_sequential"
    cmap = mpl.colormaps[name]
    assert [to_hex(cmap(x)) for x in (0.0, 1.0)] == list(get_brand(brand).roles.sequential)


def test_using_sets_default_cmap() -> None:
    """``imshow`` without ``cmap`` picks up the brand colormap (a colormap object in rcParams would crash here)."""
    with mpl_themes.using(brand="bih"):
        fig, ax = plt.subplots()
        assert ax.imshow([[0, 1]]).get_cmap().name == "bih_sequential"
        plt.close(fig)
