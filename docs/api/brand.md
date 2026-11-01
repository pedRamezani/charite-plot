# brand

Every organisation-specific value — colors, palettes, font stack and which
color is used for what — lives in a `Brand`. The theme builders only read from
a `Brand`, so supporting another organisation means defining a new one; no
theme code changes. The built-in Charité brand is defined in
`charite_plot/brands/charite.py` and is the default everywhere.

```python
from charite_plot import Brand, Roles, register_brand
from charite_plot import mpl_themes, altair_themes, make_palette

register_brand(Brand(
    name="demo",
    display_name="Demo Organisation",
    colors={"red": "#aa0000", "blue": "#0000aa"},
    palettes={"main": ["#aa0000", "#0000aa"]},
    roles=Roles(
        primary="#aa0000", text="#333333", axis="#000000", grid="#dddddd",
        diverging=("#0000aa", "#ffffff", "#aa0000"),
        sequential=("#ffffff", "#aa0000"),
    ),
    font_stack=["Source Sans 3", "DejaVu Sans", "sans-serif"],
    default_palette="main",
))

mpl_themes.enable(brand="demo")
altair_themes.enable(brand="demo")      # registered as Altair theme "demo"
make_palette("main", 5, brand="demo")
```

A `Brand` instance can also be passed directly (`enable(brand=my_brand)`)
without registering it.

::: charite_plot.brand.Brand

::: charite_plot.brand.Roles

::: charite_plot.brands.register_brand

::: charite_plot.brands.get_brand
