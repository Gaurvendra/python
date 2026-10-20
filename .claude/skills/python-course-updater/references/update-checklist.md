# Finalisation checklist (step 7)

Tick every line; the checker (`check_course.py`) covers the mechanical ones.

- [ ] Every changed/new notebook executed with `run_notebook.py` on the newest Python; outputs read and match the surrounding text
- [ ] New lessons: correct numbering, `# NN · Title` heading, learn/summary/practice sections, solutions run
- [ ] **Syllabus** (`00-Start-Here/00-Course-Guide-and-Syllabus`): rows for new lessons, accurate "key topics", counts in learning paths still true
- [ ] **Coverage map** (`00-Start-Here/01-Coverage-Map…`): new topics added to the "added" tables
- [ ] **Version tour** (`17-…/01`): new section for the new release (features with runnable cells, removals, status table row updated, "How to keep up")
- [ ] **Deprecation reference** (`17-…/02`): new rows; removed-module checker cell still correct on the newest Python
- [ ] Older lessons that mention "latest"/"current"/"newest" versions fixed (scan section 3)
- [ ] Cross-links to the new/changed lessons added where learners will look for them
- [ ] `requirements.txt` bounds still valid for the newest versions; new libraries added
- [ ] `scripts/patterns.json` extended for each new deprecation
- [ ] `course-state.json`: `reviewed_on`, `python.version/released`, `packages` versions updated to what the lessons were actually executed with
- [ ] `Python-Mastery-Course/CHANGELOG.md`: dated entry (Added / Changed / Deprecated / Removed / Fixed, each with the source)
- [ ] Course `README.md` module/lesson table counts updated; root `README.md` if structure changed
- [ ] `check_course.py` → ✓
- [ ] `cd Python-Mastery-Website && npm run build` → page count equals notebook count; Docker image rebuild works if Docker is used
- [ ] Final report lists: lessons changed/added, deprecations marked, could-not-verify items, follow-ups
