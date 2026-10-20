# Python Mastery

A complete Python course delivered as **158 executed Jupyter notebooks** and a **static, responsive website** that displays them. It runs from first `print()` to advanced internals, packaging (uv, Poetry, wheels, twine), concurrency & asyncio, Pydantic, SQLAlchemy and testing/CI, verified on **Python 3.15**.

A Claude Code **skill** keeps the course current: when Python (or a tool it teaches) changes, the skill scans every notebook, researches the change from official sources, rewrites and re-executes the affected lessons, marks deprecated features, and rebuilds the site.

```
python/                                   ← repository root
├── .claude/skills/python-course-updater/ ← the update skill (SKILL.md, scripts, references)
├── Python-Mastery-Website/               ← Vite static site + Docker setup
│   ├── Python-Mastery-Course/            ← the notebooks (single source of truth)
│   │   ├── 00-Start-Here … 19-Bonus-…    ← modules, each with numbered lessons
│   │   ├── course-state.json             ← what the course was last verified against
│   │   └── CHANGELOG.md
│   ├── scripts/build-content.mjs         ← renders notebooks to static pages (read-only)
│   ├── Dockerfile · docker-compose.yml
│   └── README.md                         ← website details
└── README.md                             ← you are here
```

The original `Complete-Python-3-Bootcamp-master/` folder and `python-handbook.pdf` were the sources this course was built from. They are not part of the project and are never modified.

## 1. View the course website

**Docker** (no Node needed):
```bash
cd Python-Mastery-Website
docker compose up --build        # then open http://localhost:8082  (host port is set in docker-compose.yml)
docker compose down              # stop
```

**Node** (Node 20+):
```bash
cd Python-Mastery-Website
npm install
npm run dev                      # development server
npm run build                    # static site in dist/ (open dist/index.html or host it anywhere)
```

The site shows every notebook with its saved outputs, a course tree, search, four themes (Light, Dark, Sepia, Midnight) and a layout that works on phones. It only **reads** the notebooks.

## 2. Work with the notebooks

Open `Python-Mastery-Website/Python-Mastery-Course/` in JupyterLab or VS Code and start at `00-Start-Here/00-Course-Guide-and-Syllabus.ipynb`. Install what the lessons need in a virtual environment:

```bash
python3 -m venv .venv && source .venv/bin/activate        # Python 3.15 recommended
python -m pip install -r Python-Mastery-Website/Python-Mastery-Course/requirements.txt
```

## 3. Keep the course up to date with the skill

The skill is `python-course-updater` (`.claude/skills/python-course-updater/`). Claude Code picks up project skills automatically when you start it from this repository.

### What it does

| Step | What happens |
|---|---|
| 1. Orient | Reads `course-state.json` (last verified Python + tool versions), builds a tooling environment with the **newest Python**, scans all notebooks for deprecated patterns, version claims and out-of-date tools |
| 2. Research | Reads the official *What's New*, *Deprecations*, PEPs and tool changelogs; anything it cannot source is left out and reported |
| 3. Plan | Maps each change to the lessons where it belongs (existing lesson, new lesson, tour, deprecation table) |
| 4. Write | Edits lessons to the course's quality standard (clear explanation, runnable examples, practice with solutions) |
| 5. Deprecate | Marks removed/deprecated/legacy/incorrect content with 🔴🟠🟡🔵 and the modern replacement; nothing valid is silently deleted |
| 6. Execute | Re-runs every changed notebook on the newest Python so outputs are real |
| 7. Verify | Updates syllabus, coverage map, tour, deprecation reference, requirements, changelog and `course-state.json`, then runs the quality gate |
| 8. Rebuild | Rebuilds the website and reports what changed and what could not be verified |

### How to run an update

1. Install `git` and (for the newest Python) one of `uv`, Homebrew or python.org, so the skill can get an interpreter for the new release.
2. Start Claude Code **in the repository root** (`python/`):
   ```bash
   cd path/to/python
   claude
   ```
3. Use one of the prompts below (copy, paste, edit the bracketed part). You can also invoke the skill explicitly with `/python-course-updater <what changed>`.
4. Review the result (see "After an update"), then commit.

### Prompts you can paste

**A new Python version was released**
```text
Python 3.16 has been released. Use the python-course-updater skill: scan the whole course,
research what is new, changed, deprecated and removed in 3.16 from the official docs, update every
affected lesson and the "What's new" tour, mark deprecated features, execute all changed
notebooks on Python 3.16, update course-state.json and CHANGELOG.md, run the checker, and rebuild
the website. Add new lessons where a topic deserves one. Report anything you could not verify.
```

**Full refresh (no specific trigger)**
```text
Use the python-course-updater skill to run a complete freshness audit of the course: check
for new Python releases, new versions of uv, Poetry, Pydantic, FastAPI, SQLAlchemy, pytest and
the other tracked packages, find outdated or deprecated content in all notebooks, fix it with
high-quality executed lessons, mark deprecations, and rebuild the website.
```

**Deprecation audit only**
```text
Use the python-course-updater skill in audit mode: scan all notebooks for deprecated, removed
or legacy features on the newest Python and tool versions. Mark each one properly with the
status legend and the modern replacement, update the deprecation reference and patterns.json,
re-execute only the notebooks you change, and rebuild the site. Do not add new feature lessons.
```

**Add a new topic**
```text
Use the python-course-updater skill to add "[topic, e.g. the new profiling.sampling tool]" to the
course. Find where it belongs, write it to the course standard (explanation, runnable examples,
practice with solutions), execute it, add cross-links, update the syllabus, coverage map,
changelog and website.
```

**Only one library or module changed**
```text
A new major version of [Pydantic / uv / Poetry / pytest ...] came out. Use the
python-course-updater skill to update every lesson that teaches it: verify behaviour against the
official changelog and by running it, fix examples, mark what the new version deprecated, update
course-state.json, and rebuild the website.
```

### After an update

```bash
git status                                                  # review which notebooks changed
cat Python-Mastery-Website/Python-Mastery-Course/CHANGELOG.md   # what and why, with sources
python .claude/skills/python-course-updater/scripts/check_course.py   # should print ✓
```

Skim the changed lessons on the website (`npm run dev`) and spot-check a few executed outputs. If you are happy: `git add -A && git commit`.

### Using the helper scripts yourself

The scripts need `nbclient`, `nbformat` and `ipykernel`. The skill's `ensure_env.sh` creates `.course-tools/venv` with those plus the course requirements:

```bash
bash .claude/skills/python-course-updater/scripts/ensure_env.sh python3.15   # use your newest Python
PY=.course-tools/venv/bin/python
S=.claude/skills/python-course-updater/scripts

$PY $S/scan_course.py --pypi        # maintenance report: deprecated patterns, version claims, stale tools
$PY $S/check_course.py              # quality gate: links, executed cells, expected errors, numbering
$PY $S/run_notebook.py path/to/lesson.ipynb        # re-execute a lesson (runs in a temp copy of its folder)
python $S/nbtext.py to-text   lesson.ipynb -o lesson.nb      # edit a notebook as plain text…
python $S/nbtext.py from-text lesson.nb    -o lesson.ipynb   # …and turn it back (then run it)
```

To teach the scanner about a new deprecation, add an entry to `scripts/patterns.json` (regex, status, since, replacement).

### Ground rules the skill follows

- Facts (versions, flags, API names, dates) come from official sources or from code it ran. Unverifiable facts are listed in its report instead of being guessed.
- Notebooks are edited as text and **re-executed**, so every output on the website is real.
- Existing modules and lesson numbers never change; new lessons are appended and all cross-references are updated.
- Deprecated content is marked and replaced, not silently removed.
- The original bootcamp and handbook files are read-only.

## Troubleshooting

| Problem | Fix |
|---|---|
| The skill isn't picked up | Start `claude` from the repository root (`python/`) so `.claude/skills/` is found; run `/python-course-updater` explicitly |
| `ensure_env.sh` fails to install packages | Make sure the Python you pass is the newest installed one and that it supports the packages in `requirements.txt`; install a new Python with `uv python install 3.X` |
| `check_course.py` says "never executed" | Run `run_notebook.py` on the named notebook |
| A lesson errors when executing | The error is a bug in the lesson: fix the cell (or tag it `error` if it is meant to fail) and re-run |
| Website shows old content | `npm run build` again (it re-renders all notebooks), or `docker compose up --build` |
