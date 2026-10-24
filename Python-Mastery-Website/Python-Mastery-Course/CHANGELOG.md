# Course changelog

Maintained by the `python-course-updater` skill. Newest first. Each entry lists what changed and the source it was verified against. Versions tracked are in `course-state.json`.

## 2026-10-24: new lesson on the object model, verified on Python 3.15.0

### Added
- **06·08 Everything Is an Object: Objects, Classes, `type` & Metaclasses**: identity/type/value, names vs objects, `is` vs `==`, mutability, what is and isn't an object, `__new__`/`__init__`, `__dict__` lookup, classes as runtime objects, `type(name, bases, ns)`, the `type`/`object` relationship, custom metaclasses, `__call__`, full class-creation sequence, `__init_subclass__`, metaclasses in the stdlib. Every output executed on Python 3.15.0 (ran it, outputs in the notebook).

### Changed
- **08·01** gains a subsection *Top-level code runs the moment you import* (inside §5, after `__init__.py`): every top-level line of `__init__.py` and sub-modules executes on first import, a demo package whose loose calls fire on import, and the fix (functions + `__name__` guard, side-effect-free `__init__.py`). Executed on Python 3.15.0.
- Syllabus and coverage map list 06·08; 06·01 and 10·03 link to it; course README shows 8 lessons in Module 06.

## 2026-10-20: initial release, verified on Python 3.15.0

### Added
- Modules 01–19 covering fundamentals to advanced Python: internals & metaprogramming, advanced typing, packaging (pip, `pyproject.toml`, uv, Poetry, wheels, twine), concurrency & asyncio, Pydantic, SQLAlchemy, testing & CI, Git.
- Python 3.10–3.15 feature tour (17·01) and a deprecation/removal reference (17·02).
- Executed on Python 3.15.0 (released 2026-10-09; source: docs.python.org/3.15/whatsnew/3.15.html).

### Deprecated / removed (documented in 17·02)
- Removed stdlib modules (`distutils`, `imp`, `cgi`, `telnetlib`, …), `NamedTuple` keyword syntax (3.15), `datetime.utcnow()` (deprecated), Pydantic v1 APIs, Poetry 1.x conventions, PyPDF2, Pillow `ANTIALIAS`.

### Fixed (bootcamp/handbook issues found while merging)
- PDF page-extraction loop, email construction, Windows-only paths, small-int `is` explanation, decorator wrappers, walrus-scope note. Full table in 17·02.
