#!/usr/bin/env python3
"""Scan the whole course and print a maintenance report (markdown).

    python scan_course.py [--course PATH] [--pypi] [--json out.json]

Sections of the report:
  1. Inventory           modules, lesson counts, cells, last-reviewed Python version (course-state.json)
  2. Deprecation hits    patterns from patterns.json; UNANNOTATED ones are the real work items,
                         annotated ones are already inside a ⚠️/legacy/removed explanation
  3. Version mentions    every "Python 3.x" / "3.x+" mention, to spot stale "latest/current" claims
  4. Stale tools         (with --pypi) tracked tool versions in course-state.json vs the newest on PyPI
Standard library only, so it runs anywhere.
"""
import argparse, json, re, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_COURSE = HERE.parents[3] / "Python-Mastery-Website" / "Python-Mastery-Course"
MARKERS = re.compile(r"⚠️|🔴|🟠|🟡|deprecat|legacy|removed|old[- ]style|old way|outdated|\bold\b|python 2|no longer|superseded|replaced by", re.I)
VERSION = re.compile(r"(?:Python\s*)?\b3\.(\d{1,2})(?:\.\d+)?\+?")
LATEST_CLAIM = re.compile(r"(latest|newest|current(?:ly)?|most recent)[^.\n]{0,60}\b3\.\d{1,2}|\b3\.\d{1,2}[^.\n]{0,40}(is|as of)[^.\n]{0,20}(latest|newest|current)", re.I)


def cells(nb):
    for i, c in enumerate(nb["cells"]):
        src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        yield i, c["cell_type"], src


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--course", default=str(DEFAULT_COURSE))
    ap.add_argument("--pypi", action="store_true", help="compare tracked tool versions with PyPI (needs internet)")
    ap.add_argument("--json", help="also write machine-readable results here")
    a = ap.parse_args()
    course = Path(a.course)
    if not course.is_dir():
        sys.exit(f"course folder not found: {course}")

    patterns = [dict(p, rx=re.compile(p["regex"])) for p in json.loads((HERE / "patterns.json").read_text())["patterns"]]
    state_path = course / "course-state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}

    modules, hits, versions, claims = {}, [], {}, []
    for nbp in sorted(course.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in nbp.parts:
            continue
        rel = str(nbp.relative_to(course))
        mod = rel.split("/")[0]
        nb = json.loads(nbp.read_text(encoding="utf-8"))
        cs = list(cells(nb))
        m = modules.setdefault(mod, {"lessons": 0, "cells": 0})
        m["lessons"] += 1; m["cells"] += len(cs)
        for i, kind, src in cs:
            for p in patterns:
                if kind == "code" and p["rx"].search(src):
                    window = "\n".join(s for j, _, s in cs if abs(j - i) <= 2)   # same cell + neighbours
                    hits.append({"file": rel, "cell": i, "id": p["id"], "status": p["status"], "use": p["use"],
                                 "annotated": bool(MARKERS.search(window))})
            for vm in VERSION.finditer(src):
                versions.setdefault(int(vm.group(1)), set()).add(rel)
            for cm in LATEST_CLAIM.finditer(src):
                claims.append({"file": rel, "cell": i, "text": cm.group(0)[:110]})

    out = []
    out.append(f"# Course scan: {course}\n")
    out.append(f"Last reviewed Python: **{state.get('python', {}).get('version', 'unknown')}** on {state.get('reviewed_on', 'unknown')}\n")
    out.append("## 1. Inventory\n\n| Module | Lessons | Cells |\n|---|---|---|")
    for k, v in modules.items():
        out.append(f"| {k} | {v['lessons']} | {v['cells']} |")
    total = sum(v["lessons"] for v in modules.values())
    out.append(f"\n**{total} notebooks in {len(modules)} modules.**\n")

    out.append("## 2. Deprecation / legacy pattern hits\n")
    todo = [h for h in hits if not h["annotated"]]
    out.append(f"{len(todo)} unannotated (need a ⚠️ explanation or a fix), {len(hits) - len(todo)} already annotated.\n")
    if todo:
        out.append("| File | Cell | Pattern | Status | Use instead |\n|---|---|---|---|---|")
        for h in todo:
            out.append(f"| {h['file']} | {h['cell']} | {h['id']} | {h['status']} | {h['use']} |")
    out.append("")

    out.append("## 3. Python version mentions\n")
    newest = max(versions) if versions else None
    out.append("Highest minor version mentioned: **3.%s**. Mentions per minor version: " % newest
               + ", ".join(f"3.{k} ({len(v)} files)" for k, v in sorted(versions.items())) + "\n")
    if claims:
        out.append("Possible 'latest/current version' claims to re-verify:\n")
        for c in claims[:40]:
            out.append(f"- {c['file']} cell {c['cell']}: “{c['text']}”")
        out.append("")

    stale = []
    if a.pypi:
        out.append("## 4. Tracked tool versions vs PyPI\n\n| Package | Course | PyPI latest | |\n|---|---|---|---|")
        for pkg, ver in state.get("packages", {}).items():
            try:
                with urllib.request.urlopen(f"https://pypi.org/pypi/{pkg}/json", timeout=15) as r:
                    latest = json.load(r)["info"]["version"]
            except Exception as e:  # offline / unknown package
                latest = f"? ({type(e).__name__})"
            flag = "" if latest == ver else "⬆️ newer"
            if flag:
                stale.append({"package": pkg, "course": ver, "latest": latest})
            out.append(f"| {pkg} | {ver} | {latest} | {flag} |")
        out.append("")

    print("\n".join(out))
    if a.json:
        Path(a.json).write_text(json.dumps({"modules": modules, "hits": hits, "claims": claims, "stale": stale}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
