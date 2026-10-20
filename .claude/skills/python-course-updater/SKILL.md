---
name: python-course-updater
description: Keep the Python Mastery course notebooks current. Scans every notebook in Python-Mastery-Website/Python-Mastery-Course, finds what a new Python release, library release (uv, Poetry, Pydantic, FastAPI, SQLAlchemy, pytest...) or deprecation has made new, wrong or outdated, then researches it from official sources, writes high-quality executed lessons, marks deprecated/removed features, and rebuilds the website. Use this whenever the user says update/refresh/audit/scan the course or notebooks, mentions a new Python version (3.16 and later), a new PEP, a deprecation or removal, "what changed in Python", "add X to the course", or wants the course to stay current, even if they never name this skill.
argument-hint: "[what changed, e.g. 'Python 3.16 released' | 'deprecation audit only' | 'add topic: <name>']"
---

# Python Course Updater

You maintain a ~160-notebook Python course so it stays **correct, current and beginner-friendly**. Learners trust executed outputs and "latest" claims, so a single wrong or stale lesson does real damage. Your job is to find what changed, verify it for real, and rewrite lessons to the same quality bar as the existing ones. Work from evidence (official docs + code you ran), never from memory: Python and its tooling move faster than your training data.

Request from the user (may be empty): $ARGUMENTS

## Where things live

| What | Path (from repo root) |
|---|---|
| Notebooks (the single source of truth) | `Python-Mastery-Website/Python-Mastery-Course/NN-Module/NN-Lesson.ipynb` |
| What the course was last verified against | `Python-Mastery-Website/Python-Mastery-Course/course-state.json` |
| Syllabus / coverage map | module `00-Start-Here` (two notebooks) |
| "What's new" tour and the deprecation reference | `17-Whats-New-in-Python/01-…` and `02-…` |
| Website that displays the notebooks | `Python-Mastery-Website/` (`npm run build`) |
| This skill's scripts | `.claude/skills/python-course-updater/scripts/` |

Never modify `Complete-Python-3-Bootcamp-master/` or `python-handbook.pdf` (read-only originals). Module numbers and lesson numbers are referenced in many places; never renumber existing modules. Add new lessons at the end of a module or as a new module at the end, and update every cross-reference you touch.

## Workflow

Follow these steps in order. Each one exists because skipping it caused a real class of bug (wrong outputs, dead links, stale claims, silent breakage).

### 1. Orient

1. Read the root `README.md` and `course-state.json` (last reviewed Python and tool versions).
2. Build the tooling environment with the **newest Python available** (the lessons must run on it): `bash .claude/skills/python-course-updater/scripts/ensure_env.sh python3.X`. If a newer Python exists than any installed, install it in isolation first (`uv python install 3.X`, python.org, or Homebrew) and say so. All commands below use `.course-tools/venv/bin/python`.
3. Run the scan: `.course-tools/venv/bin/python .claude/skills/python-course-updater/scripts/scan_course.py --pypi`. It lists unannotated deprecated patterns, every Python-version mention, "latest/current" claims to re-verify, and tracked packages that have newer releases than the course was verified against.

### 2. Establish what changed (research from primary sources)

Read `references/research-sources.md` for the exact places to look and how to treat each. In short: the official *What's New* page of every release since `course-state.json`'s version, the *Deprecations* page, the PEP index for accepted PEPs, and each tracked tool's changelog. Use WebFetch/WebSearch; if the web is unavailable, say so and limit the update to what you can verify locally (run code on the installed versions, read `--help`, `python -W error`).

Write down a **change list** with four buckets, each item sourced (URL or "ran it, output shows"): 🆕 new features/versions, 🟠 deprecations, 🔴 removals, 🔵 things that were wrong or misleading. A fact you cannot source goes in a "could not verify" list and stays out of the lessons.

### 3. Plan the edit set

Map each change to lessons: the module where the concept belongs (extend an existing lesson), whether it deserves a **new lesson**, and where it appears in the tour (17·01) and the deprecation reference (17·02). Prefer improving the lesson where learners already meet the concept over bolting facts onto the tour. Show the user a short plan (changed lessons, new lessons, deprecations) before editing when the change set is large (more than ~10 lessons); otherwise proceed and report afterwards.

### 4. Write the lessons

Edit through plain text, not raw notebook JSON: 

```
python .claude/skills/python-course-updater/scripts/nbtext.py to-text   <lesson>.ipynb -o /tmp/lesson.nb
# edit /tmp/lesson.nb  (blocks: "%% md", "%% code", "%% code error", "%% code skip")
python .claude/skills/python-course-updater/scripts/nbtext.py from-text /tmp/lesson.nb  -o <lesson>.ipynb
```

Read `references/lesson-standard.md` before writing: it defines the structure, tone, callout legend, example quality, and the rules for version-specific code. Core principles: explain *why* and *when*, not only syntax; examples are runnable and small; every claim about behaviour is backed by an executed output; beginner-friendly explanation first, depth after.

### 5. Deprecate properly (never silently delete)

Read `references/deprecation-policy.md`. Summary: old content that is still valid for supported Python versions stays, marked with the status legend (🔴 removed, 🟠 deprecated, 🟡 legacy, 🔵 incorrect) plus the modern replacement and the version where it changed. Content that is now **wrong** is rewritten. Every new deprecation also gets a row in the deprecation reference (17·02) and, if the scanner could not already catch it, a new entry in `scripts/patterns.json` so future scans find it.

### 6. Execute everything you changed

Run each changed or new notebook so outputs are real (it runs in a temp copy of the lesson folder, so lessons that create or delete files never dirty the course):

```
.course-tools/venv/bin/python .claude/skills/python-course-updater/scripts/run_notebook.py <lesson>.ipynb [...]
```

Any untagged cell that raises is a bug in your lesson. Read the outputs, don't just check the exit code: wrong-but-error-free output (a claim the output contradicts) is the most damaging failure. Tools that touch the machine (uv, Poetry, pip, Git, Docker) must run inside throw-away temp folders with their cache/config redirected, as the existing packaging lessons do.

### 7. Keep the whole course consistent

Work through `references/update-checklist.md`: syllabus and coverage map, the version tour and deprecation reference, `requirements.txt`, cross-links, the course README tables, `CHANGELOG.md`, and `course-state.json` (new Python version, date, updated tool versions). Then run the gate and fix everything it reports:

```
.course-tools/venv/bin/python .claude/skills/python-course-updater/scripts/check_course.py
```

### 8. Rebuild the website and report

`cd Python-Mastery-Website && npm run build` (renders all notebooks; the Docker image is built from the same folder with `docker compose up --build`). Confirm the page count matches the notebook count.

Finish with an honest report: lessons changed/added, deprecations marked, anything you could not verify and why, anything you deliberately left alone. Do not commit unless asked.

## Judgement calls

- **Support floor**: the course targets the newest stable Python while keeping older-version notes (`course-state.json` → `supported_floor`). When a feature needs a recent version, say which and show the older idiom beside it.
- **Pre-releases**: don't teach alpha/beta features as stable. A short "preview" callout citing the PEP is fine.
- **Tool versions in outputs**: lessons show real outputs from the version you ran. If outputs depend on a version, name it in the surrounding text.
- **Scope discipline**: a scan hit is a lead, not an order. Deprecated code shown *inside* an explanation of why it is deprecated is correct; fix only genuine problems.
- **Quality over coverage**: ten excellent updated lessons beat thirty thin ones. If time runs short, finish fewer lessons fully (executed, checked) and list the rest as follow-ups.
