# Deprecation policy

Goal: a learner reading an old tutorial elsewhere should come away knowing *what the old thing was, why it changed, and what to write today*, and a learner who reads only this course never learns a dead idiom as current.

## Status legend
| Marker | Status | Meaning | What the lesson does |
|---|---|---|---|
| 🔴 | removed | gone in the newest supported Python/tool; code fails | explain, show the error if safe, give the replacement |
| 🟠 | deprecated | works but warns / scheduled for removal | name the removal version if documented; teach the replacement first |
| 🟡 | legacy | still fine but a clearly better modern way exists | show both, recommend the modern one |
| 🔵 | incorrect | the earlier explanation or example was wrong or misleading | fix it, add a short note on the right mental model |

## Decision procedure
1. **Is it still valid on the support floor** (`course-state.json` → `supported_floor`)? If yes → keep, mark 🟡/🟠, show both idioms and the version boundary ("works on 3.12+, preferred from 3.14").
2. **Removed or broken on the newest Python?** → 🔴, rewrite the example so the *taught* code works, keep a short ⚠️ block describing the old form.
3. **Was it simply wrong?** → 🔵, rewrite; mention the correction in the changelog.
4. Prove each marker: run the old form on the newest Python (or read the official docs' deprecation notice) and capture the warning/error text. For warnings, a lesson cell can demonstrate it with `warnings.catch_warnings(record=True)`.

## Where to record a deprecation
1. In the lesson where learners meet the concept (callout with replacement and version).
2. In `17-Whats-New-in-Python/02-…Deprecated…` : add a row to the relevant table (Part 3 for language/stdlib, Part 4 for tools/libraries), and to Part 1/2 audit tables only for things that were in the bootcamp/handbook.
3. In `17-…/01-…Feature-Tour` under the release it happened in.
4. In `scripts/patterns.json`: a regex + status + since + replacement, so future scans catch the same pattern elsewhere.
5. `CHANGELOG.md` entry.

## Don'ts
- Don't delete a deprecated section just because it's old; others' code still uses it. Mark it.
- Don't mark something deprecated based on a blog post: cite the official deprecation notice or demonstrate the warning.
- Don't leave a 🔴 example in a *runnable* cell unless it's tagged `error` and explained.
