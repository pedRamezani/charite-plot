# colors

All color constants are importable directly from the module or via the lookup dict:

```python
from charite_plot.colors import PRIME_BLUE, TEXT_GREY

from charite_plot.colors import CHARITE_COLORS
CHARITE_COLORS["prime_blue"]   # "#004d9b"
```

See the [Colors guide](../colors.md) for a visual swatch reference of all values.

---

## `CHARITE_COLORS`

**Type:** `dict[str, str]`

Mapping of lowercase color names to hex strings. Available keys:

`white` · `black` · `text_grey` · `prime_blue` · `prime_lgrey` · `prime_dgrey` · `second_dblue` · `second_lblue` · `korall` · `braun` · `mocca` · `grasgruen` · `limette` · `gruen` · `mint` · `mineral` · `aqua` · `lila` · `lavendel` · `brombeere` · `pflaume` · `weinrot` · `himbeer` · `rot` · `mango` · `rapsgelb` · `employer_branding_green`

---

## Constants

Individual constants are also exported at the module level:

| Constant | Hex |
|----------|-----|
| `WHITE` | `#ffffff` |
| `BLACK` | `#000000` |
| `TEXT_GREY` | `#5e676c` |
| `PRIME_BLUE` | `#004d9b` |
| `PRIME_LGREY` | `#cbcfd2` |
| `PRIME_DGREY` | `#7e898f` |
| `SECOND_DBLUE` | `#002552` |
| `SECOND_LBLUE` | `#007bc3` |
| `KORALL` | `#ea5451` |
| `BRAUN` | `#89725b` |
| `MOCCA` | `#c8b8ad` |
| `GRASGRUEN` | `#a1ba0c` |
| `LIMETTE` | `#d1d811` |
| `GRUEN` | `#008939` |
| `MINT` | `#88c69a` |
| `MINERAL` | `#009aa9` |
| `AQUA` | `#61c3d7` |
| `LILA` | `#564091` |
| `LAVENDEL` | `#7876b6` |
| `BROMBEERE` | `#6f186d` |
| `PFLAUME` | `#944292` |
| `WEINROT` | `#89014c` |
| `HIMBEER` | `#d74b7f` |
| `ROT` | `#e31f2c` |
| `MANGO` | `#fab600` |
| `RAPSGELB` | `#ffdf43` |
| `EMPLOYER_BRANDING_GREEN` | `#ccefcb` |
