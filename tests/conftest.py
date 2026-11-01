import matplotlib
import pytest

matplotlib.use("Agg")


@pytest.fixture(autouse=True)
def _restore_rcparams():
    """Keep matplotlib's global rcParams isolated between tests."""
    import matplotlib as mpl

    with mpl.rc_context():
        yield


@pytest.fixture
def alt():
    """Altair, with the active theme restored after the test."""
    alt = pytest.importorskip("altair")
    previous = alt.theme.active
    yield alt
    alt.theme.enable(previous)
