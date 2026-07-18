# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-07-18

### Added

- `theme_charite` (matplotlib) gained a `background` parameter (sets figure and axes facecolor).
- Altair now provides a `using()` context manager mirroring the matplotlib one, for scoping the theme to a `with` block.
- Explicit `__all__` declarations on every module (and the package) to define the public API surface for `from charite_plot import *` and tooling.

### Changed

- **Unified API across backends.** The matplotlib activate function was renamed `apply_theme(params)` → `enable(**kwargs)`, and `using()` now takes theme keyword arguments instead of a pre-built dict — matching the Altair backend. Migrate `apply_theme(theme_charite(palette="x"))` to `enable(palette="x")` and `using(theme_charite(palette="x"))` to `using(palette="x")`. `theme_charite()` still returns a plain dict if you prefer to apply it manually via `mpl.rcParams.update()`.

### Removed

- `mpl_themes.apply_theme()` — replaced by `mpl_themes.enable()` (see above).

## [0.2.0] - 2026-07-01

### Added

- `theme_charite` (matplotlib) gained `interactive` and `tiny_margins` parameters.
- `theme_charite` (Altair) gained `thickness` and `tiny_margins` parameters, bringing it to parity with the matplotlib backend.

### Changed

- Font-size ramp is now shared between both backends: labels scale at 1× and legend text at 0.8× the base size. Altair legend labels are slightly smaller and axis labels slightly larger as a result.

## [0.1.1] - 2026-06-13

### Fixed

- README images now use absolute raw GitHub URLs so they render correctly on PyPI.
- Corrected PyPI project URLs (homepage, docs, repository, bug tracker).

## [0.1.0] - 2026-06-12

### Added

- Initial release.
- Matplotlib theme (`mpl_themes.theme_charite`) with `apply_theme()` and `using()` context manager.
- Altair/Vega-Lite theme (`altair_themes.theme_charite`) with `register()` and `enable()`.
- 10 built-in colour palettes: `primary`, `secondary`, `mono`, `light`, `versus`, `nineties`, `brickhouse`, `sunrise`, `berryseason`, `goldelse`.
- 27 Charité corporate identity colour constants in `colors.py`.
- `make_palette()` for subsampling and interpolating palettes.
- Font fallback chain: Charité Text Office → Charit? Text Office → Calibri → DejaVu Sans → sans-serif.
- MkDocs Material documentation with API reference.
- MIT License.
