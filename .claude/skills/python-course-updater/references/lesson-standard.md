# Lesson standard (match the existing lessons)

Open two existing lessons in the same module before writing, and match their voice, depth and structure.

## Structure of every lesson notebook
1. `# NN · Title` then a line with module name and estimated time.
2. **🎯 What you will learn**: 4–8 concrete bullets.
3. Body sections with `##` headings. Each concept = short plain-language explanation → minimal runnable example → what the output shows → the common mistake/edge case.
4. **📝 Summary**: bullets and/or a comparison table.
5. **🏋️ Practice**: 3–6 exercises and a `<details><summary>Show solutions</summary>` block with a fenced ```python solution for each. Solutions must run.

## Voice
- Explain like a good teacher to a motivated beginner: why it exists, when to use it, when not to. Define a term the first time it appears.
- Use tables for comparisons, diagrams in fenced text for flows, and analogies sparingly and accurately.
- Short paragraphs. No filler, no hype, no unexplained jargon.

## Callout legend (use exactly these)
| Marker | Meaning |
|---|---|
| 🆕 | New in Python/tool version X (always name the version) |
| ⚠️ | Old/deprecated/legacy: say what to use instead |
| ❌ | Common mistake (show it failing) |
| 💡 | Tip |
| 📗 / 📘 | Content that came from the bootcamp / handbook |
| 🧪 | Experimental / preview feature |
| 🔒 | Needs elevated permissions or credentials (cell is `skip`) |

Put callouts in blockquotes (`> 🆕 **New in Python 3.X:** …`).

## Code cells
- Each cell is small and does one thing; show output by letting the last expression display or by `print`.
- Use `%% code error` for a cell that is *meant* to raise (the lesson explains the error). Use `%% code skip` for cells that cannot run unattended (`input()`, sudo, real credentials, destructive actions, long-running servers) and say why in the text.
- Deterministic output: seed randomness, avoid wall-clock times in printed values you then describe, avoid machine-specific paths in text you assert on.
- Network examples use stable public test services (httpbin.org, quotes.toscrape.com, api.github.com) with `timeout=`.
- Anything that installs software, changes config, or touches Git/Docker/system state runs in a temporary directory with redirected cache/config (see lessons 08·04, 08·05, 16·01 for the pattern).
- Never print secrets, tokens, or personal information. Use obviously fake values.

## Version-specific code
- Code that only runs on the newest Python must be introduced with a 🆕 callout naming the version, and, where practical, the older equivalent beside it.
- The tooling env runs the newest Python, so version-gated syntax executes for real; do not wrap it in `try/except SyntaxError` unless the lesson is about portability.
- Don't claim a feature is "stable" or "removed" unless the official docs say so.

## Cross-references
- Reference other lessons as `Module NN · MM` (or relative notebook links `../NN-Module/MM-Name.ipynb`). If you add or rename a lesson, search the course for references to its number and fix them, and run `check_course.py`.
- New lessons: next free number in the module, filename `NN-Short-Title-With-Hyphens.ipynb`, and add it to the syllabus table in `00-Start-Here`.

## Exercises that came from the bootcamp
Notebooks with the header "From the original Complete Python 3 Bootcamp" are copied templates. Don't re-execute them; improve their review notes if something in them is outdated.
