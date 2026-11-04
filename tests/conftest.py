"""Shared fixtures: isolated matplotlib rcParams and Altair theme state for every test."""

from collections.abc import Iterator
from types import ModuleType

import matplotlib as mpl
import pytest

mpl.use("Agg")


@pytest.fixture(autouse=True)
def _restore_rcparams() -> Iterator[None]:
    """Keep matplotlib's global rcParams isolated between tests."""
    with mpl.rc_context():
        yield


@pytest.fixture
def alt() -> Iterator[ModuleType]:
    """Altair, with the active theme restored after the test (skipped if Altair isn't installed)."""
    alt = pytest.importorskip("altair")
    previous = alt.theme.active
    yield alt
    alt.theme.enable(previous)
