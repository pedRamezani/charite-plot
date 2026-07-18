"""charite_plot — Matplotlib and Altair themes for Charité – Universitätsmedizin Berlin.

Quick start
-----------
Matplotlib::

    import matplotlib.pyplot as plt
    from charite_plot.mpl_themes import enable

    enable()            # permanent
    # or temporarily:
    from charite_plot.mpl_themes import using
    with using(palette="goldelse"):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])

Altair::

    from charite_plot.altair_themes import enable
    enable()
    # charts rendered after this call use the theme automatically
"""

from .colors import *  # noqa: F403  (all color constants + CHARITE_COLORS)
from .colors import __all__ as _COLOR_ALL
from .palettes import PALETTES, make_palette
from . import mpl_themes
from . import altair_themes

__version__ = "0.3.0"
__author__ = "Pedram Ramezani"

__all__ = [
    *_COLOR_ALL,
    "PALETTES",
    "make_palette",
    "mpl_themes",
    "altair_themes",
]
