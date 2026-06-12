# Palettes

Ten named palettes are available in `PALETTES`. Each can be used directly or passed as the `palette` argument to any theme function.

```python
from charite_plot.palettes import PALETTES, make_palette

colors = PALETTES["goldelse"]         # list of hex strings
three  = make_palette("goldelse", n=3)        # subsample to 3
six    = make_palette("goldelse", n=12)       # interpolate to 12
rev    = make_palette("primary", reverse=True)
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

## `make_palette`

`make_palette` handles subsampling and interpolation so you can request any number of colors from any palette:

```python
from charite_plot.palettes import make_palette

# Exact palette colors
make_palette("berryseason")           # all 6 colors

# Subsample (picks evenly spaced colors)
make_palette("goldelse", n=4)

# Interpolate beyond palette length
make_palette("versus", n=20)          # smooth gradient between blue and red

# Reverse
make_palette("sunrise", reverse=True)
```
