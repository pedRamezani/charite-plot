"""Berlin Institute of Health at Charité (BIH) brand: colors, palettes, fonts and roles.

Source: BIH Markenhandbuch (draft, 2026-01) and Markenportal "Farbwelt" / "Farbabstufungen".

Deliberate deviation from the handbook: text, tick labels and axes are black
instead of BIH-Blau, because scientific journals expect black figure text.
Titles stay BIH-Blau. Dunkelrot and Hellrosa are text-only colors in the
handbook, so they are not used in any palette. Tints are only allowed in
10 % steps of the five diagram colors (Blau, Korall, Gold, Mineral, Lavendel).
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

BIH_PALETTES: dict[str, list[str]] = {
    "primary":   [BLAU, KORALL, MINERAL, GOLD, LAVENDEL],
    "secondary": [MINERAL, LAVENDEL, GOLD],
    "light":     [tint(c, 50) for c in (BLAU, KORALL, MINERAL, GOLD, LAVENDEL)],
    "versus":    [BLAU, KORALL],
    "blau":      [tint(BLAU, p) for p in (100, 70, 40)],
    "korall":    [tint(KORALL, p) for p in (100, 70, 40)],
    "gold":      [tint(GOLD, p) for p in (100, 70, 40)],
    "mineral":   [tint(MINERAL, p) for p in (100, 70, 40)],
    "lavendel":  [tint(LAVENDEL, p) for p in (100, 70, 40)],
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
        diverging=(BLAU, WHITE, KORALL),
        sequential=(WHITE, BLAU),
    ),
    font_stack=BIH_FONT_STACK,
    default_palette="primary",
)

# fmt: off
__all__ = [
    "WHITE", "BLACK", "BLAU", "DUNKELROT", "HELLROSA",
    "KORALL", "GOLD", "MINERAL", "LAVENDEL",
    "BIH_COLORS", "BIH_PALETTES", "BIH_FONT_STACK", "BIH",
]
# fmt: on
