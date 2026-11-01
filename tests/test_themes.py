"""Behaviour of the public theme API (enable / using / register) and helpers."""

import io

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

from charite_plot import PALETTES, PRIME_BLUE, altair_themes, make_palette, mpl_themes
from charite_plot.fonts import FONT_STACK, build_font_stack

# --- matplotlib ---------------------------------------------------------------------------


def test_mpl_enable_updates_rcparams():
    mpl_themes.enable(palette="versus")
    assert mpl.rcParams["axes.titlecolor"] == PRIME_BLUE
    assert [d["color"] for d in mpl.rcParams["axes.prop_cycle"]] == PALETTES["versus"]


def test_mpl_using_restores_rcparams():
    before = mpl.rcParams["axes.titlecolor"]
    with mpl_themes.using(palette="goldelse"):
        assert mpl.rcParams["axes.titlecolor"] == PRIME_BLUE
    assert mpl.rcParams["axes.titlecolor"] == before


def test_mpl_theme_renders_a_figure():
    """All rcParams are valid: matplotlib accepts them and can draw a figure."""
    with mpl_themes.using(grid=True):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label="a")
        ax.bar([1, 2], [3, 4])
        ax.set_title("Title")
        ax.legend()
        fig.savefig(io.BytesIO(), format="png")
        plt.close(fig)


# --- Altair --------------------------------------------------------------------------------


def test_altair_register_does_not_enable(alt):
    alt.theme.enable("default")
    altair_themes.register()
    assert "charite" in alt.theme.names()
    assert alt.theme.active == "default"


def test_altair_enable_with_kwargs(alt):
    altair_themes.enable(palette="goldelse")
    assert alt.theme.active == "charite"
    config = alt.Chart().mark_point().to_dict()["config"]
    assert config["range"]["category"] == PALETTES["goldelse"]


def test_altair_using_restores_theme_and_cleans_registry(alt):
    alt.theme.enable("default")
    with altair_themes.using(palette="versus"):
        assert alt.theme.active != "default"
        config = alt.Chart().mark_point().to_dict()["config"]
        assert config["range"]["category"] == PALETTES["versus"]
    assert alt.theme.active == "default"
    assert not [name for name in alt.theme.names() if name.startswith("_charite_")]


# --- palettes & fonts ----------------------------------------------------------------------


def test_make_palette_unknown_name():
    with pytest.raises(ValueError, match="Unknown palette"):
        make_palette("nope")


def test_theme_unknown_palette():
    with pytest.raises(KeyError):
        mpl_themes.theme_charite(palette="nope")


def test_font_stack_default():
    assert build_font_stack(None) == FONT_STACK


def test_font_stack_preferred_first():
    with pytest.warns(UserWarning, match="is not installed"):
        stack = build_font_stack("Definitely Not A Font")
    assert stack == ["Definitely Not A Font", *FONT_STACK]
