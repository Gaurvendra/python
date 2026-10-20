# Course changelog

Maintained by the `python-course-updater` skill. Newest first. Each entry lists what changed and the source it was verified against. Versions tracked are in `course-state.json`.

## 2026-10-20: initial release, verified on Python 3.15.0

### Added
- Modules 01–19 covering fundamentals to advanced Python: internals & metaprogramming, advanced typing, packaging (pip, `pyproject.toml`, uv, Poetry, wheels, twine), concurrency & asyncio, Pydantic, SQLAlchemy, testing & CI, Git.
- Python 3.10–3.15 feature tour (17·01) and a deprecation/removal reference (17·02).
- Executed on Python 3.15.0 (released 2026-10-09; source: docs.python.org/3.15/whatsnew/3.15.html).

### Deprecated / removed (documented in 17·02)
- Removed stdlib modules (`distutils`, `imp`, `cgi`, `telnetlib`, …), `NamedTuple` keyword syntax (3.15), `datetime.utcnow()` (deprecated), Pydantic v1 APIs, Poetry 1.x conventions, PyPDF2, Pillow `ANTIALIAS`.

### Fixed (bootcamp/handbook issues found while merging)
- PDF page-extraction loop, email construction, Windows-only paths, small-int `is` explanation, decorator wrappers, walrus-scope note. Full table in 17·02.
