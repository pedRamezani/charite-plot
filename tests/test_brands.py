"""The Brand abstraction: registry, palettes, and themes built from a non-Charité brand."""

import matplotlib as mpl
import pytest

from charite_plot import (
    BRANDS,
    CHARITE,
    Brand,
    Roles,
    altair_themes,
    get_brand,
    make_palette,
    mpl_themes,
    register_brand,
)
from charite_plot.fonts import FONT_STACK


@pytest.fixture
def demo():
    brand = Brand(
        name="demo",
        display_name="Demo Org",
        colors={"red": "#aa0000", "blue": "#0000aa"},
        palettes={"main": ["#aa0000", "#0000aa"]},
        roles=Roles(
            primary="#aa0000",
            text="#333333",
            axis="#111111",
            grid="#dddddd",
            diverging=("#0000aa", "#ffffff", "#aa0000"),
            sequential=("#ffffff", "#aa0000"),
        ),
        font_stack=["Comic Sans MS", "sans-serif"],
        default_palette="main",
    )
    register_brand(brand)
    yield brand
    BRANDS.pop("demo", None)


def test_charite_is_default():
    assert get_brand() is CHARITE
    assert mpl_themes.theme() == mpl_themes.theme_charite()
    assert altair_themes.theme() == altair_themes.theme_charite()


def test_backwards_compatible_aliases():
    assert list(CHARITE.font_stack) == FONT_STACK
    assert get_brand("charite").palettes["primary"][0] == CHARITE.roles.primary


def test_get_brand_unknown():
    with pytest.raises(ValueError, match="Unknown brand 'nope'"):
        get_brand("nope")


def test_brand_validates_default_palette(demo):
    with pytest.raises(ValueError, match="default_palette 'missing'"):
        Brand(
            name="x",
            display_name="x",
            colors={},
            palettes={"a": ["#000000"]},
            roles=demo.roles,
            font_stack=["sans-serif"],
            default_palette="missing",
        )


@pytest.mark.parametrize("brand", ["demo", "instance"])
def test_mpl_theme_uses_brand(demo, brand):
    params = mpl_themes.theme(brand=demo if brand == "instance" else "demo")
    assert params["axes.titlecolor"] == "#aa0000"
    assert params["axes.labelcolor"] == "#333333"
    assert params["xtick.color"] == "#111111"
    assert params["grid.color"] == "#dddddd"
    assert params["font.sans-serif"] == ["Comic Sans MS", "sans-serif"]
    assert [d["color"] for d in params["axes.prop_cycle"]] == ["#aa0000", "#0000aa"]


def test_mpl_using_with_brand(demo):
    with mpl_themes.using(brand="demo"):
        assert mpl.rcParams["axes.titlecolor"] == "#aa0000"
    assert mpl.rcParams["axes.titlecolor"] != "#aa0000"


def test_altair_theme_uses_brand(demo):
    config = altair_themes.theme(brand="demo")["config"]
    assert config["title"]["color"] == "#aa0000"
    assert config["range"]["category"] == ["#aa0000", "#0000aa"]
    assert config["range"]["diverging"] == ["#0000aa", "#ffffff", "#aa0000"]
    assert config["range"]["heatmap"] == ["#ffffff", "#aa0000"]


def test_altair_enable_registers_under_brand_name(alt, demo):
    altair_themes.enable(brand=demo, palette="main")
    assert alt.theme.active == "demo"
    assert alt.Chart().mark_point().to_dict()["config"]["title"]["color"] == "#aa0000"


def test_make_palette_with_brand(demo):
    assert make_palette("main", 3, brand="demo")[0] == "#aa0000"
    with pytest.raises(ValueError, match="for brand 'demo'"):
        make_palette("primary", brand="demo")


def test_font_warning_lists_brand_stack(demo):
    with pytest.warns(UserWarning, match="Comic Sans MS → sans-serif"):
        mpl_themes.theme(brand="demo", font="Definitely Not A Font")
