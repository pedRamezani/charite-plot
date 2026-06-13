# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
