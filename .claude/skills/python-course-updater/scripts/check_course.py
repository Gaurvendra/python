#!/usr/bin/env python3
"""Quality gate for the course. Run after every update; fix everything it reports.

    python check_course.py [--course PATH]

Checks:
  * every relative markdown link between notebooks resolves
  * every `raises-exception` cell really produced an error output
  * no UNtagged code cell has an error output
  * every runnable code cell was executed (has execution_count)   [skip-execution cells and copied
    bootcamp exercises/projects (header 'From the original ...') excluded]
  * no ANSI escape codes left in saved outputs
  * module folders and lesson files are numbered without gaps/duplicates
  * course-state.json exists and parses
Exit code 0 = clean, 1 = problems found.
"""
import argparse, json, re, sys
from pathlib import Path

DEFAULT_COURSE = Path(__file__).resolve().parents[4] / "Python-Mastery-Website" / "Python-Mastery-Course"
LINK = re.compile(r"\]\((\.\.?/[^)\s]+)\)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--course", default=str(DEFAULT_COURSE))
    course = Path(ap.parse_args().course)
    problems = []

    notebooks = sorted(p for p in course.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts)
    for nbp in notebooks:
        rel = nbp.relative_to(course)
        nb = json.loads(nbp.read_text(encoding="utf-8"))
        head = "".join("".join(c["source"]) if isinstance(c["source"], list) else c["source"] for c in nb["cells"][:3])
        copied = "From the original" in head   # copied bootcamp exercises/projects/widgets: templates, not executed lessons
        for i, c in enumerate(nb["cells"]):
            src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
            tags = c.get("metadata", {}).get("tags", [])
            if c["cell_type"] == "markdown":
                for link in LINK.findall(src):
                    if not (nbp.parent / link).resolve().exists():
                        problems.append(f"{rel} cell {i}: broken link {link}")
            elif c["cell_type"] == "code":
                has_error = any(o.get("output_type") == "error" for o in c.get("outputs", []))
                if "raises-exception" in tags and not has_error:
                    problems.append(f"{rel} cell {i}: tagged raises-exception but produced no error")
                if has_error and "raises-exception" not in tags and not copied:
                    problems.append(f"{rel} cell {i}: unexpected error output")
                if not copied and "skip-execution" not in tags and src.strip() and c.get("execution_count") is None:
                    problems.append(f"{rel} cell {i}: never executed (run run_notebook.py)")
                for o in c.get("outputs", []):
                    blob = "".join(o.get("text", [])) if o.get("output_type") == "stream" else ""
                    if "\x1b[" in blob:
                        problems.append(f"{rel} cell {i}: ANSI codes in output")
                        break

    # numbering: top-level modules NN-*, lessons NN-* inside each
    mods = sorted(d.name for d in course.iterdir() if d.is_dir() and re.match(r"\d{2}-", d.name))
    nums = [int(m[:2]) for m in mods]
    if nums != list(range(nums[0], nums[0] + len(nums))):
        problems.append(f"module numbering has gaps/duplicates: {nums}")
    for m in mods:
        lessons = sorted(p.name for p in (course / m).glob("*.ipynb"))
        ln = [int(n[:2]) for n in lessons if re.match(r"\d{2}-", n)]
        if ln and ln != list(range(ln[0], ln[0] + len(ln))):
            problems.append(f"{m}: lesson numbering has gaps/duplicates: {ln}")

    state = course / "course-state.json"
    try:
        json.loads(state.read_text())
    except Exception as e:
        problems.append(f"course-state.json missing or invalid ({e})")

    if problems:
        print(f"✗ {len(problems)} problem(s) in {len(notebooks)} notebooks:\n")
        print("\n".join(f"  - {p}" for p in problems))
        return 1
    print(f"✓ {len(notebooks)} notebooks clean (links, executed cells, expected errors, numbering)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
