# Installation

## Core (Matplotlib only)

```bash
pip install charite-plot
```

This installs the package with Matplotlib support. The Altair integration is an optional extra.

## With Altair support

```bash
pip install "charite-plot[altair]"
```

This adds `altair>=5.5` and `vega-datasets` (required to run the showcase example).

## Development / docs

```bash
pip install "charite-plot[all]"         # package + altair
pip install "charite-plot[docs]"        # mkdocs-material + mkdocstrings
```

## Fonts

charite-plot works out of the box with any system. The font fallback chain is:

**Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif**

- `sans-serif` is the final fallback, letting the browser or system choose a suitable font — this is particularly important for Altair/Vega-Lite charts.
- `DejaVu Sans` ships with Matplotlib and is always available as the penultimate fallback.
- `Calibri` is pre-installed on Windows and macOS (via Microsoft Office) and serves as the official replacement font, as defined in the Charité brand guidelines.
- `Charité Text Office` must be installed manually — it is available to Charité employees via the Markenportal. On some systems the `é` is not decoded correctly and the font is registered as `Charit? Text Office`; both names are tried automatically.

To use a different preferred font, pass it explicitly:

```python
from charite_plot.mpl_themes import theme_charite, apply_theme

apply_theme(theme_charite(font="Arial"))
```

A warning is shown if the requested font cannot be found on the system.
