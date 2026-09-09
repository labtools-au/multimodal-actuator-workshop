#!/usr/bin/env python3
"""
Copy logger.h into every sketch folder.

The logger is duplicated rather than installed as a library, so students do
not have to install anything before the first upload. The cost is fifteen
copies, so this script keeps them identical.

Master copy: bench_tests/01_erm_motor/logger.h

    python3 scripts/sync_logger.py          # copy out
    python3 scripts/sync_logger.py --check  # verify, non-zero if any drifted
"""
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "bench_tests/01_erm_motor/logger.h"


def sketch_dirs():
    for ino in sorted(ROOT.glob("*/*/*.ino")):
        if ino.parent.parent.name in {"bench_tests", "tasks", "utils"}:
            yield ino.parent


def main() -> int:
    check = "--check" in sys.argv
    drifted = []

    for d in sketch_dirs():
        target = d / "logger.h"
        if target == MASTER:
            continue
        if not target.exists() or not filecmp.cmp(MASTER, target, shallow=False):
            drifted.append(target.relative_to(ROOT))
            if not check:
                shutil.copy(MASTER, target)

    if check:
        for p in drifted:
            print(f"drifted: {p}")
        print("all in sync" if not drifted else f"{len(drifted)} out of sync")
        return 1 if drifted else 0

    print(f"synced {len(drifted)} of {sum(1 for _ in sketch_dirs())} sketches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
