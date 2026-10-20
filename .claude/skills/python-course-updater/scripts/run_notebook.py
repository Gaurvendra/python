#!/usr/bin/env python3
"""Execute lesson notebooks and save the real outputs (in place by default).

    python run_notebook.py path/to/lesson.ipynb [more.ipynb ...] [--out FILE] [--timeout 300]

Needs: nbclient, nbformat, ipykernel (+ the libraries the lessons import; see
Python-Mastery-Course/requirements.txt). Use scripts/ensure_env.sh to create such an environment.

How it behaves (so lessons stay reproducible and your files stay clean):
  * runs in a TEMPORARY COPY of the lesson's folder, so files a lesson creates/deletes never
    touch the course; data files next to the notebook (images, csv, pdf) are available;
  * cells tagged `skip-execution` are not run and keep no outputs;
  * cells tagged `raises-exception` are allowed to fail (the error is kept as the output);
  * ANSI colour codes are stripped from saved text output;
  * exits non-zero if an UNtagged cell raised, so you notice broken examples.
"""
import argparse, os, re, shutil, sys, tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\]8;[^\x1b\x07]*(?:\x1b\\|\x07)")


def run(path: Path, out: Path | None, timeout: int) -> bool:
    nb = nbformat.read(path, as_version=4)
    runnable = [c for c in nb.cells if "skip-execution" not in c.metadata.get("tags", [])]
    for c in nb.cells:
        if c.cell_type == "code" and "skip-execution" in c.metadata.get("tags", []):
            c.outputs, c.execution_count = [], None
    work_nb = nbformat.v4.new_notebook(cells=runnable, metadata=nb.metadata)

    for var in ("FORCE_COLOR", "CLICOLOR_FORCE"):
        os.environ.pop(var, None)
    os.environ["NO_COLOR"] = "1"

    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        for item in path.parent.iterdir():          # copy data files (not other notebooks)
            if item.suffix == ".ipynb" or item.name.startswith("."):
                continue
            (shutil.copytree if item.is_dir() else shutil.copy2)(item, Path(tmp) / item.name)
        client = NotebookClient(work_nb, timeout=timeout, kernel_name="python3",
                                resources={"metadata": {"path": tmp}}, allow_errors=False)
        try:
            client.execute()
        except CellExecutionError as e:
            ok = False
            print(f"  ✗ {path.name}: unexpected error → {str(e).strip().splitlines()[-1][:200]}")

    for orig, done in zip(runnable, work_nb.cells):
        if orig.cell_type == "code":
            for o in done.get("outputs", []):
                if o.get("output_type") == "stream":
                    o["text"] = ANSI.sub("", o["text"])
                elif o.get("output_type") == "error":
                    o["traceback"] = [ANSI.sub("", t) for t in o.get("traceback", [])]
            orig.outputs, orig.execution_count = done.get("outputs", []), done.get("execution_count")
    nbformat.validate(nb)
    nbformat.write(nb, out or path)
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("notebooks", nargs="+")
    ap.add_argument("--out", help="write the executed notebook here (single input only)")
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()
    if a.out and len(a.notebooks) > 1:
        ap.error("--out needs exactly one notebook")
    failures = 0
    for nbp in a.notebooks:
        p = Path(nbp)
        good = run(p, Path(a.out) if a.out else None, a.timeout)
        print(("✓ " if good else "✗ ") + str(p))
        failures += not good
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
