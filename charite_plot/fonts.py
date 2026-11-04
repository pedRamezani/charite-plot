"""Font detection and fallback utilities."""

from __future__ import annotations

import warnings
from collections.abc import Sequence

from .brands.charite import CHARITE_FONT_STACK

__all__ = ["FONT_STACK", "check_font", "build_font_stack"]

# Default stack (Charité), kept for backwards compatibility. Themes use ``Brand.font_stack``.
FONT_STACK = CHARITE_FONT_STACK


def _available_fonts() -> set[str]:
    try:
        import matplotlib.font_manager as fm

        return {f.name for f in fm.fontManager.ttflist}
    except Exception:
        return set()


def check_font(font: str, fallback: Sequence[str] = FONT_STACK) -> bool:
    """Return True if *font* is available on this system, else warn and return False."""
    if font in _available_fonts():
        return True
    warnings.warn(
        f"Font '{font}' is not installed on this system. Using the fallback chain: {' → '.join(fallback)}.",
        UserWarning,
        stacklevel=3,
    )
    return False


def build_font_stack(preferred: str | None, stack: Sequence[str] = FONT_STACK) -> list[str]:
    """Return *stack* with *preferred* moved to the front (for matplotlib's ``font.sans-serif``)."""
    if preferred is None:
        return list(stack)
    check_font(preferred, fallback=stack)
    return [preferred, *[f for f in stack if f != preferred]]


if __name__ == "__main__":
    print(sorted(_available_fonts()))
