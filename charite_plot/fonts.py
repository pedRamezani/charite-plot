"""Font detection and fallback utilities."""

import warnings

FONT_STACK = ["Charité Text Office", "Charit? Text Office", "Calibri", "DejaVu Sans", "sans-serif"]


def _available_fonts() -> set[str]:
    try:
        import matplotlib.font_manager as fm
        return {f.name for f in fm.fontManager.ttflist}
    except Exception:
        return set()


def check_font(font: str) -> bool:
    """Return True if *font* is available on this system, else warn and return False."""
    if font in _available_fonts():
        return True
    warnings.warn(
        f"Font '{font}' is not installed on this system. "
        "Using the fallback chain: Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif.",
        UserWarning,
        stacklevel=3,
    )
    return False


def build_font_stack(preferred: str | None) -> list[str]:
    """Return the font list for matplotlib's ``font.sans-serif`` rcParam."""
    if preferred is None:
        return FONT_STACK
    check_font(preferred)
    return [preferred, *[f for f in FONT_STACK if f != preferred]]

if __name__ == "__main__":
    print(sorted(_available_fonts()))