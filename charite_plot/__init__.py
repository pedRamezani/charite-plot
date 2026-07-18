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

from .colors import *  # noqa: F401, F403  (all color constants + CHARITE_COLORS)
from .palettes import PALETTES, make_palette  # noqa: F401
from . import mpl_themes  # noqa: F401
from . import altair_themes  # noqa: F401

__version__ = "0.3.0"
__author__ = "Pedram Ramezani"
