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

Pass `brand="bih"` to use these with any theme function or `make_palette`. They only use the five BIH diagram colors
and their tints in 10 % steps, as the BIH handbook requires.

```python
from charite_plot import BIH, make_palette

BIH.palettes["primary"]  # list of hex strings
make_palette("blau", n=5, brand="bih")
```

## primary
<div class="palette-strip">
  <div style="background:#003754"></div>
  <div style="background:#ea5451"></div>
  <div style="background:#009aa9"></div>
  <div style="background:#9d7220"></div>
  <div style="background:#7876b6"></div>
</div>

## secondary
<div class="palette-strip">
  <div style="background:#009aa9"></div>
  <div style="background:#7876b6"></div>
  <div style="background:#9d7220"></div>
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

## blau
<div class="palette-strip">
  <div style="background:#003754"></div>
  <div style="background:#4c7387"></div>
  <div style="background:#99afbb"></div>
</div>

## korall
<div class="palette-strip">
  <div style="background:#ea5451"></div>
  <div style="background:#f08785"></div>
  <div style="background:#f7bbb9"></div>
</div>

## gold
<div class="palette-strip">
  <div style="background:#9d7220"></div>
  <div style="background:#ba9c63"></div>
  <div style="background:#d8c7a6"></div>
</div>

## mineral
<div class="palette-strip">
  <div style="background:#009aa9"></div>
  <div style="background:#4cb8c3"></div>
  <div style="background:#99d7dd"></div>
</div>

## lavendel
<div class="palette-strip">
  <div style="background:#7876b6"></div>
  <div style="background:#a09fcc"></div>
  <div style="background:#c9c8e2"></div>
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
