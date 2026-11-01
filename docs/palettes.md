# Palettes

Ten named palettes are available in `PALETTES`. Each can be used directly or passed as the `palette` argument to any theme function.

```python
from charite_plot.palettes import PALETTES, make_palette

colors = PALETTES["goldelse"]  # list of hex strings
three = make_palette("goldelse", n=3)  # subsample to 3
six = make_palette("goldelse", n=12)  # interpolate to 12
rev = make_palette("primary", reverse=True)
```

---

## primary
<div class="palette-strip">
  <div style="background:#004d9b"></div>
  <div style="background:#7e898f"></div>
  <div style="background:#cbcfd2"></div>
</div>

## secondary
<div class="palette-strip">
  <div style="background:#002552"></div>
  <div style="background:#007bc3"></div>
  <div style="background:#ea5451"></div>
</div>

## mono
<div class="palette-strip">
  <div style="background:#000000"></div>
  <div style="background:#7e898f"></div>
  <div style="background:#cbcfd2"></div>
</div>

## light
<div class="palette-strip">
  <div style="background:#007bc3"></div>
  <div style="background:#cbcfd2"></div>
</div>

## versus
<div class="palette-strip">
  <div style="background:#004d9b"></div>
  <div style="background:#e31f2c"></div>
</div>

## nineties
<div class="palette-strip">
  <div style="background:#564091"></div>
  <div style="background:#88c69a"></div>
  <div style="background:#009aa9"></div>
</div>

## brickhouse
<div class="palette-strip">
  <div style="background:#89014c"></div>
  <div style="background:#d74b7f"></div>
  <div style="background:#88c69a"></div>
  <div style="background:#008939"></div>
</div>

## sunrise
<div class="palette-strip">
  <div style="background:#002552"></div>
  <div style="background:#007bc3"></div>
  <div style="background:#ffdf43"></div>
  <div style="background:#fab600"></div>
</div>

## berryseason
<div class="palette-strip">
  <div style="background:#d74b7f"></div>
  <div style="background:#944292"></div>
  <div style="background:#6f186d"></div>
  <div style="background:#002552"></div>
  <div style="background:#c8b8ad"></div>
  <div style="background:#89725b"></div>
</div>

## goldelse
<div class="palette-strip">
  <div style="background:#fab600"></div>
  <div style="background:#ffdf43"></div>
  <div style="background:#d1d811"></div>
  <div style="background:#a1ba0c"></div>
  <div style="background:#61c3d7"></div>
  <div style="background:#009aa9"></div>
  <div style="background:#7876b6"></div>
  <div style="background:#564091"></div>
</div>

---

# BIH palettes

Pass `brand="bih"` to use these with any theme function or `make_palette`. BIH-Blau and BIH-Weiß are the primary brand
colors, so `primary` is Blau with two tints; the categorical default is `accents`. The palettes only use the five BIH
diagram colors and their tints in 10 % steps, as the BIH handbook requires; `mono` uses black tints, following the
theme's black text and axes.

```python
from charite_plot import BIH, make_palette

BIH.palettes["accents"]  # list of hex strings
make_palette("primary", n=5, brand="bih")
```

## accents
<div class="palette-strip">
  <div style="background:#003754"></div>
  <div style="background:#ea5451"></div>
  <div style="background:#009aa9"></div>
  <div style="background:#9d7220"></div>
  <div style="background:#7876b6"></div>
</div>

## primary
<div class="palette-strip">
  <div style="background:#003754"></div>
  <div style="background:#668798"></div>
  <div style="background:#b2c3cc"></div>
</div>

## mono
<div class="palette-strip">
  <div style="background:#000000"></div>
  <div style="background:#666666"></div>
  <div style="background:#b2b2b2"></div>
</div>

## light
<div class="palette-strip">
  <div style="background:#809baa"></div>
  <div style="background:#f4aaa8"></div>
  <div style="background:#80ccd4"></div>
  <div style="background:#ceb890"></div>
  <div style="background:#bcbada"></div>
</div>

## versus
<div class="palette-strip">
  <div style="background:#003754"></div>
  <div style="background:#ea5451"></div>
</div>

---

## `make_palette`

`make_palette` handles subsampling and interpolation so you can request any number of colors from any palette:

```python
from charite_plot.palettes import make_palette

# Exact palette colors
make_palette("berryseason")  # all 6 colors

# Subsample (picks evenly spaced colors)
make_palette("goldelse", n=4)

# Interpolate beyond palette length
make_palette("versus", n=20)  # smooth gradient between blue and red

# Reverse
make_palette("sunrise", reverse=True)
```

---

## Continuous colormaps

`ramp` returns the color stops of a continuous scale, and `make_cmap` turns them into a matplotlib colormap
(a port of `scale_color_charite(palette, discrete = FALSE)` from the R package):

- a **palette name** gives a gradient through all its colors;
- a **color name** of the brand (or a hex color) gives a gradient from white to that color, like matplotlib's `"Blues"`;
- a **list of colors** gives a gradient through them.

The gradients are smooth: they are not restricted to the 10 % (BIH) or 20 % (Charité) tint steps of the brand guides,
which apply to discrete colors.

<table>
<tr><th>Charité</th><th>BIH</th></tr>
<tr>
<td><img src="../assets/cmap_preview.png" width="100%"/></td>
<td><img src="../assets/cmap_preview_bih.png" width="100%"/></td>
</tr>
</table>

```python
from charite_plot import make_cmap

ax.imshow(data, cmap=make_cmap("prime_blue"))  # white → Charité blue
ax.scatter(x, y, c=z, cmap=make_cmap("berryseason"))  # through the whole palette
ax.imshow(data, cmap=make_cmap("blau", brand="bih", reverse=True))
```

Vega-Lite interpolates between any color stops itself, so Altair only needs the stops from `ramp`.
Pass `interpolate="rgb"` to get exactly the matplotlib gradient (Vega-Lite blends in HCL by default):

```python
import altair as alt
from charite_plot import ramp

alt.Chart(df).mark_rect().encode(
    color=alt.Color("value:Q", scale=alt.Scale(range=ramp("blau", brand="bih"), interpolate="rgb")),
)
```
