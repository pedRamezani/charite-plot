# charite-plot

A Python package with a Charité-styled Matplotlib theme, [visual identity](https://marke.charite.de/d/Y3FxSwD6Tz3a) colour palettes, and an Altair theme — ported from the [`charite` R package](https://github.com/johannesjuliusm/charite).

## Installation

```bash
pip install charite-plot                   # Matplotlib only
pip install "charite-plot[altair]"         # with Altair support
```

## Examples

Visualize your data with `theme_charite()` to match the Charité corporate style.

<p align="center">
<img src="https://raw.githubusercontent.com/pedramezani/charite-plot/main/docs/assets/theme_example.png" width="80%"/>
</p>

Preview the available colour palettes.

<p align="center">
<img src="https://raw.githubusercontent.com/pedramezani/charite-plot/main/docs/assets/palette_preview.png" width="80%"/>
</p>

## Quick start

### Matplotlib

```python
import matplotlib.pyplot as plt
from charite_plot.mpl_themes import theme_charite, apply_theme

apply_theme(theme_charite())

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 7, 3])
ax.set_title("My chart")
plt.show()
```

Use as a context manager to scope the theme to a single figure:

```python
from charite_plot.mpl_themes import theme_charite, using

with using(theme_charite(palette="goldelse")):
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C"], [3, 7, 5])
```

### Altair

```python
from charite_plot.altair_themes import enable
import altair as alt

enable()

chart = alt.Chart(df).mark_bar().encode(...)
```

Customise with keyword arguments:

```python
enable(palette="berryseason", font_size=13)
```

## API overview

| Symbol | Description |
|--------|-------------|
| `mpl_themes.theme_charite()` | Returns a matplotlib rcParams dict for the Charité theme |
| `mpl_themes.apply_theme(params)` | Applies a theme dict permanently to `rcParams` |
| `mpl_themes.using(params)` | Context manager: applies theme temporarily |
| `altair_themes.theme_charite()` | Returns a Vega-Lite config dict for the Charité theme |
| `altair_themes.enable(**kwargs)` | Registers and enables the theme in Altair |
| `PALETTES` | Dict of 10 named colour palettes |
| `make_palette(name, n, reverse)` | Subsample or interpolate any palette |
| `CHARITE_COLORS` | Dict of all 27 hex colour constants |

## Fonts

The fallback chain follows the official Charité brand guidelines:

**Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif**

`DejaVu Sans` ships with Matplotlib and is always available as the penultimate fallback; `sans-serif` lets the browser or system choose if nothing else matches (important for Altair/Vega-Lite). To override the preferred font:

```python
apply_theme(theme_charite(font="Arial"))
```

## How to cite

If you use charite-plot in your work, please cite it as:

```bibtex
@software{ramezani2026chariteplot,
  author    = {Ramezani, Pedram},
  title     = {charite-plot: Matplotlib and Altair Themes for Charité – Universitätsmedizin Berlin},
  year      = {2026},
  version   = {0.1.1},
  url       = {https://github.com/pedramezani/charite-plot},
  license   = {MIT},
}
```

## License

MIT © 2026 Pedram Ramezani
