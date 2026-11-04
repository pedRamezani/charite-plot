"""The Brand abstraction: registry, palettes, and themes built from a non-Charité brand."""

import re
from collections.abc import Iterator
from types import ModuleType

import matplotlib as mpl
import pytest
from matplotlib.colors import to_rgb

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


def lightness(color: str) -> float:
    """CIELAB L* (0 = black, 100 = white) of a hex color."""
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in to_rgb(color)]
    y = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    return 116 * y ** (1 / 3) - 16 if y > (6 / 29) ** 3 else y * (29 / 3) ** 3


@pytest.fixture
def demo() -> Iterator[Brand]:
    """A registered non-Charité brand with distinct role colors, removed again after the test."""
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


# --- built-in brands -----------------------------------------------------------------------


def test_charite_is_default() -> None:
    assert get_brand() is CHARITE
    assert mpl_themes.theme() == mpl_themes.theme_charite()
    assert altair_themes.theme() == altair_themes.theme_charite()


def test_font_stack_alias_is_charites() -> None:
    """``fonts.FONT_STACK`` predates brands and must keep pointing to the Charité stack."""
    assert list(CHARITE.font_stack) == FONT_STACK


@pytest.mark.parametrize("brand", BRANDS.values(), ids=BRANDS.keys())
def test_colors_are_lowercase_hex(brand: Brand) -> None:
    """Palettes and roles are compared by value, so every color must use the same notation."""
    colors = [*brand.colors.values(), *(c for p in brand.palettes.values() for c in p)]
    assert all(re.fullmatch(r"#[0-9a-f]{6}", c) for c in colors)


@pytest.mark.parametrize("brand", BRANDS.values(), ids=BRANDS.keys())
def test_diverging_ends_have_equal_lightness(brand: Brand) -> None:
    """Both halves of a diverging scale look equally strong, so neither side is visually favoured."""
    low, _, high = brand.roles.diverging
    assert abs(lightness(low) - lightness(high)) < 3


# --- registry ------------------------------------------------------------------------------


def test_get_brand_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown brand 'nope'"):
        get_brand("nope")


def test_brand_validates_default_palette(demo: Brand) -> None:
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


# --- themes from a custom brand ------------------------------------------------------------


@pytest.mark.parametrize("by", ["name", "instance"])
def test_mpl_theme_uses_brand(demo: Brand, by: str) -> None:
    """Every role ends up in the right rcParam, whether the brand is passed by name or as an object."""
    params = mpl_themes.theme(brand="demo" if by == "name" else demo)
    assert params["axes.titlecolor"] == "#aa0000"
    assert params["axes.labelcolor"] == "#333333"
    assert params["xtick.color"] == "#111111"
    assert params["grid.color"] == "#dddddd"
    assert params["font.sans-serif"] == ["Comic Sans MS", "sans-serif"]
    assert [d["color"] for d in params["axes.prop_cycle"]] == ["#aa0000", "#0000aa"]


def test_mpl_using_with_brand(demo: Brand) -> None:
    with mpl_themes.using(brand="demo"):
        assert mpl.rcParams["axes.titlecolor"] == "#aa0000"
    assert mpl.rcParams["axes.titlecolor"] != "#aa0000"


def test_altair_theme_uses_brand(demo: Brand) -> None:
    config = altair_themes.theme(brand="demo")["config"]
    assert config["title"]["color"] == "#aa0000"
    assert config["range"]["category"] == ["#aa0000", "#0000aa"]
    assert config["range"]["diverging"] == ["#0000aa", "#ffffff", "#aa0000"]
    assert config["range"]["heatmap"] == ["#ffffff", "#aa0000"]


def test_altair_enable_registers_under_brand_name(alt: ModuleType, demo: Brand) -> None:
    altair_themes.enable(brand=demo, palette="main")
    assert alt.theme.active == "demo"
    assert alt.Chart().mark_point().to_dict()["config"]["title"]["color"] == "#aa0000"


def test_make_palette_with_brand(demo: Brand) -> None:
    """Palette names are looked up in the given brand only."""
    assert make_palette("main", 3, brand="demo")[0] == "#aa0000"
    with pytest.raises(ValueError, match="for brand 'demo'"):
        make_palette("primary", brand="demo")


def test_font_warning_lists_brand_stack(demo: Brand) -> None:
    with pytest.warns(UserWarning, match="Comic Sans MS → sans-serif"):
        mpl_themes.theme(brand="demo", font="Definitely Not A Font")
