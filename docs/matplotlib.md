# Matplotlib

## Applying the theme

### Permanently — `apply_theme`

Sets rcParams globally for the rest of the session:

```python
import matplotlib.pyplot as plt
from charite_plot.mpl_themes import theme_charite, apply_theme

apply_theme(theme_charite())

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 7, 3])
ax.set_title("Survival over time")
ax.set_xlabel("Days")
ax.set_ylabel("Proportion")
plt.show()
```

### Temporarily — `using`

Applies the theme only inside the `with` block, then restores the previous rcParams:

```python
from charite_plot.mpl_themes import theme_charite, using

with using(theme_charite(palette="goldelse")):
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C", "D"], [3, 7, 5, 9])
```

### As a plain dict

`theme_charite()` returns a plain `dict` of rcParams, so you can inspect, merge, or pass it anywhere rcParams are accepted:

```python
from charite_plot.mpl_themes import theme_charite
import matplotlib as mpl

params = theme_charite(palette="nineties", font_size=8)
params["lines.linewidth"] = 2.0   # any extra overrides

mpl.rcParams.update(params)
```

---

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `font` | `str | None` | `None` | Preferred font. Falls back through Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif. |
| `font_size` | `float` | `10` | Base font size in points. Use `8` for print/journal figures. |
| `thickness` | `float` | `0.5` | Axis line and tick width. |
| `grid` | `bool` | `False` | Show major grid lines. |
| `palette` | `str | list[str]` | `"primary"` | Named palette or list of hex strings for `axes.prop_cycle`. |
| `interactive` | `bool` | `False` | Enable interactive mode (equivalent to `plt.ion()`). Useful in notebooks or scripts where plots should display without blocking. |
| `tiny_margins` | `bool` | `False` | Minimise all margins and paddings around the plot panel. Useful for dense layouts. |

---

## Examples

### Palette switcher

```python
from charite_plot.mpl_themes import theme_charite, apply_theme

apply_theme(theme_charite(palette="berryseason"))
```

### Custom font size for a journal figure

```python
apply_theme(theme_charite(font_size=8, thickness=0.4))
```

### Custom color list

```python
apply_theme(theme_charite(palette=["#004d9b", "#ea5451", "#fab600"]))
```

### Grid on

```python
apply_theme(theme_charite(grid=True))
```

### Dense layout with minimal margins

```python
apply_theme(theme_charite(tiny_margins=True))
```

### Interactive mode (notebooks / REPL)

```python
apply_theme(theme_charite(interactive=True))   # equivalent to plt.ion()
```
