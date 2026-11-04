"""Snapshot tests: the generated theme configs must not change unintentionally.

Regenerate after an intentional change with ``uv run pytest --snapshot-update``
and review the diff of ``tests/__snapshots__/``.
"""

from typing import Any

import matplotlib as mpl
import pytest
from syrupy.assertion import SnapshotAssertion

from charite_plot import BRANDS, PALETTES, altair_themes, make_palette, mpl_themes

CASES: dict[str, dict[str, Any]] = {
    "default": {},
    "custom": {"palette": "goldelse", "grid": True, "tiny_margins": True, "font_size": 8, "thickness": 1},
    "font": {"font": "Arial"},
    "color_list": {"palette": ["#123456", "#abcdef"]},
}

# Requesting a font that isn't installed only warns; the output is the same everywhere.
pytestmark = pytest.mark.filterwarnings("ignore:Font .* is not installed")


@pytest.mark.parametrize("kwargs", CASES.values(), ids=CASES.keys())
def test_mpl_theme(kwargs: dict[str, Any], snapshot: SnapshotAssertion) -> None:
    """The Charité rcParams (the prop cycle as a plain color list, since a cycler has no stable repr)."""
    params = mpl_themes.theme_charite(**kwargs)
    params["axes.prop_cycle"] = [d["color"] for d in params["axes.prop_cycle"]]
    assert params == snapshot


@pytest.mark.parametrize("kwargs", CASES.values(), ids=CASES.keys())
def test_altair_theme(kwargs: dict[str, Any], snapshot: SnapshotAssertion) -> None:
    assert altair_themes.theme_charite(**kwargs) == snapshot


@pytest.mark.parametrize("brand", BRANDS)
@pytest.mark.parametrize("kwargs", CASES.values(), ids=CASES.keys())
def test_themes_are_valid(kwargs: dict[str, Any], brand: str) -> None:
    """Every key/value is accepted by matplotlib and by the Vega-Lite schema (unknown keys are errors)."""
    if isinstance(kwargs.get("palette"), str) and kwargs["palette"] not in BRANDS[brand].palettes:
        kwargs = kwargs | {"palette": list(BRANDS[brand].palettes)[-1]}  # palette names are per brand
    mpl.RcParams(mpl_themes.theme(**kwargs, brand=brand))

    schema = pytest.importorskip("altair.vegalite.v6.schema.core")
    schema.Config.from_dict(altair_themes.theme(**kwargs, brand=brand)["config"], validate=True)


def test_palettes(snapshot: SnapshotAssertion) -> None:
    assert snapshot == PALETTES


@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        (("goldelse", 3), {}),
        (("primary", 5), {}),
        (("versus",), {"reverse": True}),
        (("versus", 1), {}),
        ((["#000000", "#ffffff"], 3), {}),
    ],
    ids=["subsample", "interpolate", "reverse", "single", "color_list"],
)
def test_make_palette(args: tuple[Any, ...], kwargs: dict[str, Any], snapshot: SnapshotAssertion) -> None:
    assert make_palette(*args, **kwargs) == snapshot
