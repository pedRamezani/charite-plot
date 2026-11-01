"""Berlin Institute of Health at Charité (BIH) brand: colors, palettes, fonts and roles.

Source: BIH Markenhandbuch (draft, 2026-01) and Markenportal "Farbwelt" / "Farbabstufungen".

Deliberate deviation from the handbook: text, tick labels and axes are black
instead of BIH-Blau, because scientific journals expect black figure text.
Titles stay BIH-Blau. Dunkelrot and Hellrosa are text-only colors in the
handbook, so they are not used in any palette. The discrete palettes only use
tints in 10 % steps of the five diagram colors (Blau, Korall, Gold, Mineral,
Lavendel), as the handbook requires; ``mono`` uses black tints, following the
black-text deviation. Continuous colormaps (:func:`charite_plot.make_cmap`)
are smooth gradients and deliberately not restricted to 10 % steps.
"""

from ..brand import Brand, Roles, tint

# fmt: off
WHITE     = "#ffffff"
BLACK     = "#000000"  # not a BIH color; used for text and axes (see module docstring)
BLAU      = "#003754"
DUNKELROT = "#af1821"  # text only
HELLROSA  = "#ffb0ac"  # text only
KORALL    = "#ea5451"
GOLD      = "#9d7220"
MINERAL   = "#009aa9"
LAVENDEL  = "#7876b6"

BIH_COLORS: dict[str, str] = {
    "white":     WHITE,
    "black":     BLACK,
    "blau":      BLAU,
    "dunkelrot": DUNKELROT,
    "hellrosa":  HELLROSA,
    "korall":    KORALL,
    "gold":      GOLD,
    "mineral":   MINERAL,
    "lavendel":  LAVENDEL,
}

# One palette per use case. Blau and Weiß are the primary brand colors; Korall, Gold,
# Mineral and Lavendel are accent colors. Continuous scales are the roles below
# (``make_cmap("sequential" | "diverging", brand="bih")``).
BIH_PALETTES: dict[str, list[str]] = {
    # Categorical. Ordered so the first three stay distinct for color-vision deficiencies;
    # Mineral and Lavendel are hard to tell apart for deuteranopes, so Lavendel comes last.
    "accents": [BLAU, MINERAL, GOLD, KORALL, LAVENDEL],
    "versus":  [BLAU, KORALL],                              # two groups
    "primary": [BLAU, tint(BLAU, 60), tint(BLAU, 30)],      # ordered levels (L* 21 / 54 / 79)
    "mono":    [BLACK, tint(BLACK, 60), tint(BLACK, 30)],   # greyscale, like Charité's mono
}
# fmt: on

BIH_FONT_STACK = ["Trebuchet MS", "DejaVu Sans", "sans-serif"]

BIH = Brand(
    name="bih",
    display_name="Berlin Institute of Health at Charité",
    colors=BIH_COLORS,
    palettes=BIH_PALETTES,
    roles=Roles(
        primary=BLAU,
        text=BLACK,
        axis=BLACK,
        grid=tint(BLAU, 20),
        # Lavendel and Gold have the same lightness (L* 52 / 51), so both halves look equally strong.
        diverging=(LAVENDEL, WHITE, GOLD),
        sequential=(WHITE, BLAU),
    ),
    font_stack=BIH_FONT_STACK,
    default_palette="accents",
)

# fmt: off
__all__ = [
    "WHITE", "BLACK", "BLAU", "DUNKELROT", "HELLROSA",
    "KORALL", "GOLD", "MINERAL", "LAVENDEL",
    "BIH_COLORS", "BIH_PALETTES", "BIH_FONT_STACK", "BIH",
]
# fmt: on
