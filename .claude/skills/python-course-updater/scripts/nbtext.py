#!/usr/bin/env python3
"""Round-trip a notebook through an easy-to-edit text format.

    nbtext.py to-text   lesson.ipynb  [-o lesson.nb]     # notebook -> text
    nbtext.py from-text lesson.nb     [-o lesson.ipynb]  # text -> notebook (no outputs yet)

Text format (one block per cell):
    %% md                 markdown cell
    %% code               code cell, executed normally
    %% code error         code cell that is EXPECTED to raise (tag: raises-exception)
    %% code skip          code cell shown but never executed (needs input(), sudo, credentials...)

Outputs are not stored in the text form: after `from-text`, run run_notebook.py to execute
the lesson and save real outputs. Markdown cells may contain any markdown/HTML. Lines in code
cells that start with `%%bash` or `%%writefile` (IPython cell magics, no space) are fine.
"""
import argparse, json, re, sys
from pathlib import Path

MARK = re.compile(r"^%% (md|code)\s*(.*)$")


def to_text(nb: dict) -> str:
    out = []
    for cell in nb["cells"]:
        src = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
        if cell["cell_type"] == "markdown":
            out.append("%% md\n" + src.rstrip("\n"))
        elif cell["cell_type"] == "code":
            tags = cell.get("metadata", {}).get("tags", [])
            flag = " error" if "raises-exception" in tags else " skip" if "skip-execution" in tags else ""
            out.append(f"%% code{flag}\n" + src.rstrip("\n"))
    return "\n\n".join(out) + "\n"


def from_text(text: str) -> dict:
    cells, kind, opts, buf = [], None, set(), []

    def flush():
        if kind is None:
            return
        body = "\n".join(buf).strip("\n")
        cell = {"cell_type": "markdown" if kind == "md" else "code", "metadata": {}, "source": body}
        if kind == "code":
            cell["outputs"], cell["execution_count"] = [], None
            if "error" in opts:
                cell["metadata"]["tags"] = ["raises-exception"]
            if "skip" in opts:
                cell["metadata"]["tags"] = ["skip-execution"]
        cells.append(cell)

    for line in text.splitlines():
        m = MARK.match(line)
        if m:
            flush()
            kind, opts, buf = m.group(1), set(m.group(2).split()), []
        else:
            buf.append(line)
    flush()
    return {
        "cells": cells,
        "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                     "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 5,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["to-text", "from-text"])
    ap.add_argument("path")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    src = Path(a.path)
    if a.mode == "to-text":
        res = to_text(json.loads(src.read_text(encoding="utf-8")))
        dest = Path(a.out) if a.out else src.with_suffix(".nb")
        dest.write_text(res, encoding="utf-8")
    else:
        nb = from_text(src.read_text(encoding="utf-8"))
        # ids keep nbformat 4.5 valid
        for i, c in enumerate(nb["cells"]):
            c["id"] = f"cell-{i:04d}"
        dest = Path(a.out) if a.out else src.with_suffix(".ipynb")
        dest.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
