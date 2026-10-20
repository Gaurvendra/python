# 🐍 Python Mastery Course (updated for Python 3.15)

A complete, structured Python course in Jupyter notebooks. It's the **union** of:

- 📗 **Complete Python 3 Bootcamp** (Pierian Data notebooks), in `../Complete-Python-3-Bootcamp-master/`
- 📘 **Python Handbook** (PDF), `../python-handbook.pdf`

All content from both sources is included and reorganised into one syllabus. Outdated and deprecated material is flagged and fixed, and modern topics missing from both are added, up to advanced level: internals & metaprogramming, advanced typing, the full packaging toolchain (pyproject.toml, uv, Poetry, wheels, twine), deep concurrency & asyncio, advanced testing & CI, SQLAlchemy, Pydantic & FastAPI, and Python 3.10–3.15 features.

**Start here → [`00-Start-Here/00-Course-Guide-and-Syllabus.ipynb`](00-Start-Here/00-Course-Guide-and-Syllabus.ipynb)**

## Structure

| Module | Topic | Lessons |
|---|---|---|
| 00 | Start Here: syllabus, coverage map | 2 |
| 01 | Getting Started | 2 |
| 02 | Python Basics | 8 + exercises |
| 03 | Data Structures (incl. heaps, bisect, graphs) | 7 + exercises |
| 04 | Control Flow (incl. `match`/`case`) | 4 + exercises |
| 05 | Functions (incl. type hints) | 6 + exercises |
| 06 | Object-Oriented Programming | 7 + exercises |
| 07 | Errors, Debugging, Testing & Professional Workflow | 5 + exercises |
| 08 | Modules, Packaging & Dependency Management: pip, `pyproject.toml`, **uv**, **Poetry**, wheels, **twine** | 9 |
| 09 | Advanced Functions | 4 + exercises |
| 10 | 🆕 Advanced Python: Internals, Metaprogramming, Advanced Typing, Patterns, Performance | 9 |
| 11 | Files & OS (incl. binary data, subprocess) | 6 + exercises |
| 12 | Standard Library Essentials | 6 |
| 13 | Concurrency & asyncio (threading, multiprocessing, futures, asyncio, networking, free-threading) | 8 |
| 14 | Working with Data & the Web (incl. SQLAlchemy) | 6 + exercises |
| 15 | 🆕 Pydantic: Data Validation & Settings (incl. FastAPI) | 11 |
| 16 | Git & Version Control | 4 |
| 17 | What's New (3.10→3.15) & Deprecations Reference | 2 |
| 18 | Projects (3 milestones + 6 modern briefs) | 13 |
| 19 | Bonus: GUIs with ipywidgets | 9 |

Every lesson notebook has learning objectives, explanations, many runnable examples (pre-executed on **Python 3.15.0**), callouts (🆕 new · ⚠️ deprecated · ❌ common mistake · 💡 tip), a summary, and practice questions with hidden solutions.

## Setup

```bash
cd Python-Mastery-Course
uv venv && source .venv/bin/activate     # or: python3 -m venv .venv (Windows: .venv\Scripts\activate)
uv pip install -r requirements.txt       # or: python -m pip install -r requirements.txt
jupyter lab                          # or open the folder in VS Code
```

Python **3.15** is recommended. A handful of cells demonstrate 3.15-only features and are labelled as such; everything else runs on Python 3.12+.

## Credits
- Bootcamp exercises, projects and GUI notebooks © Pierian Data (Jose Portilla), *Complete Python 3 Bootcamp*. Copied notebooks keep their attribution and are marked 📗.
- Handbook material is adapted from `python-handbook.pdf` and marked 📘.
