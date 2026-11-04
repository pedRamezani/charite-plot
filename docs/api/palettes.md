# palettes

```python
from charite_plot.palettes import PALETTES, make_cmap, make_palette, make_ramp
```

See the [Palettes guide](../palettes.md) for visual palette strips and usage examples.

---

## `PALETTES`

**Type:** `dict[str, list[str]]`

The Charité palettes and their hex colors:

| Name | Colors |
|------|--------|
| `primary` | `#004d9b` · `#7e898f` · `#cbcfd2` |
| `secondary` | `#002552` · `#007bc3` · `#ea5451` |
| `mono` | `#000000` · `#7e898f` · `#cbcfd2` |
| `light` | `#007bc3` · `#cbcfd2` |
| `versus` | `#004d9b` · `#e31f2c` |
| `nineties` | `#564091` · `#88c69a` · `#009aa9` |
| `brickhouse` | `#89014c` · `#d74b7f` · `#88c69a` · `#008939` |
| `sunrise` | `#002552` · `#007bc3` · `#ffdf43` · `#fab600` |
| `berryseason` | `#d74b7f` · `#944292` · `#6f186d` · `#002552` · `#c8b8ad` · `#89725b` |
| `goldelse` | `#fab600` · `#ffdf43` · `#d1d811` · `#a1ba0c` · `#61c3d7` · `#009aa9` · `#7876b6` · `#564091` |

---

## `BIH_PALETTES`

**Type:** `dict[str, list[str]]`

The BIH palettes, in `charite_plot.brands.bih` (and `BIH.palettes`). Pass `brand="bih"` to use them by name,
e.g. `make_palette("accents", brand="bih")`.

| Name | Colors |
|------|--------|
| `primary` | `#003754` · `#668798` · `#b2c3cc` |
| `accents` | `#003754` · `#009aa9` · `#9d7220` · `#ea5451` · `#7876b6` |
| `mono` | `#000000` · `#666666` · `#b2b2b2` |
| `light` | `#009aa9` · `#cccccc` |
| `versus` | `#003754` · `#ea5451` |

---

## `make_palette`

::: charite_plot.palettes.make_palette

---

## `make_ramp`

::: charite_plot.palettes.make_ramp

---

## `make_cmap`

::: charite_plot.palettes.make_cmap
