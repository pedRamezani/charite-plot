# Altair

## Enabling the theme

Call `enable()` once before rendering any charts. All Altair charts created afterwards will use the Charité theme automatically.

```python
from charite_plot.altair_themes import enable
import altair as alt

enable()

chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(x="category:N", y="value:Q")
)
chart
```

### With parameters

```python
enable(palette="goldelse")
enable(palette="nineties", font_size=13)
enable(font="Arial")
```

### Just register without enabling

```python
from charite_plot.altair_themes import register
import altair as alt

register()
alt.theme.enable("charite")   # enable later
```

---

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `font` | `str | None` | `None` | Preferred font. CSS fallback: Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif. |
| `font_size` | `int` | `12` | Base font size in pixels. |
| `thickness` | `float` | `0.5` | Axis line and tick width. |
| `grid` | `bool` | `False` | Show axis grid lines. |
| `palette` | `str | list[str]` | `"primary"` | Named palette or list of hex strings for the categorical color range. |
| `background` | `str` | `"white"` | Chart background color. |
| `tiny_margins` | `bool` | `False` | Minimise all paddings around the chart. Useful for dense layouts. |

---

## Color ranges

The theme sets all Vega-Lite color ranges from the selected palette:

| Range | Usage | Colors |
|-------|-------|--------|
| `category` | Categorical encodings | palette colors |
| `ordinal` | Ordinal encodings | palette colors |
| `diverging` | Diverging scales (e.g. `domainMid=0`) | `SECOND_DBLUE → white → KORALL` |
| `heatmap` | Sequential heatmaps | `white → PRIME_BLUE` |
| `ramp` | Sequential ramp | `white → PRIME_BLUE` |

---

## Examples

### Categorical color encoding

```python
enable(palette="berryseason")

alt.Chart(df).mark_line().encode(
    x="date:T",
    y="value:Q",
    color="group:N",
)
```

### Diverging color scale

The `diverging` range (`SECOND_DBLUE → white → KORALL`) is used automatically when `domainMid` is set:

```python
alt.Chart(df).mark_point().encode(
    x="x:Q",
    y="y:Q",
    color=alt.Color("delta:Q").scale(domainMid=0),
)
```

### Transparent background

```python
enable(background="transparent")
```

### Dense layout with minimal margins

```python
enable(tiny_margins=True)
```

### Thicker axis lines

```python
enable(thickness=1.0)
```
