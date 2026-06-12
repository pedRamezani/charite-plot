"""Charité color definitions — the single source of truth shared by all themes."""

# Primary
WHITE        = "#ffffff"
BLACK        = "#000000"
TEXT_GREY    = "#5e676c"
PRIME_BLUE   = "#004d9b"
PRIME_LGREY  = "#cbcfd2"
PRIME_DGREY  = "#7e898f"

# Secondary
SECOND_DBLUE = "#002552"
SECOND_LBLUE = "#007bc3"
KORALL       = "#ea5451"

# Accents
BRAUN        = "#89725b"
MOCCA        = "#c8b8ad"
GRASGRUEN    = "#a1ba0c"
LIMETTE      = "#d1d811"
GRUEN        = "#008939"
MINT         = "#88c69a"
MINERAL      = "#009aa9"
AQUA         = "#61c3d7"
LILA         = "#564091"
LAVENDEL     = "#7876b6"
BROMBEERE    = "#6f186d"
PFLAUME      = "#944292"
WEINROT      = "#89014c"
HIMBEER      = "#d74b7f"
ROT          = "#e31f2c"
MANGO        = "#fab600"
RAPSGELB     = "#ffdf43"

# Special
EMPLOYER_BRANDING_GREEN = "#ccefcb"

# Lookup dict (lowercase keys)
CHARITE_COLORS: dict[str, str] = {
    "white":        WHITE,
    "black":        BLACK,
    "text_grey":    TEXT_GREY,
    "prime_blue":   PRIME_BLUE,
    "prime_lgrey":  PRIME_LGREY,
    "prime_dgrey":  PRIME_DGREY,
    "second_dblue": SECOND_DBLUE,
    "second_lblue": SECOND_LBLUE,
    "korall":       KORALL,
    "braun":        BRAUN,
    "mocca":        MOCCA,
    "grasgruen":    GRASGRUEN,
    "limette":      LIMETTE,
    "gruen":        GRUEN,
    "mint":         MINT,
    "mineral":      MINERAL,
    "aqua":         AQUA,
    "lila":         LILA,
    "lavendel":     LAVENDEL,
    "brombeere":    BROMBEERE,
    "pflaume":      PFLAUME,
    "weinrot":      WEINROT,
    "himbeer":      HIMBEER,
    "rot":          ROT,
    "mango":        MANGO,
    "rapsgelb":     RAPSGELB,
    "employer_branding_green": EMPLOYER_BRANDING_GREEN,
}

__all__ = [
    "WHITE", "BLACK", "TEXT_GREY", "PRIME_BLUE", "PRIME_LGREY", "PRIME_DGREY",
    "SECOND_DBLUE", "SECOND_LBLUE", "KORALL",
    "BRAUN", "MOCCA", "GRASGRUEN", "LIMETTE", "GRUEN", "MINT",
    "MINERAL", "AQUA", "LILA", "LAVENDEL", "BROMBEERE", "PFLAUME",
    "WEINROT", "HIMBEER", "ROT", "MANGO", "RAPSGELB",
    "EMPLOYER_BRANDING_GREEN",
    "CHARITE_COLORS",
]
