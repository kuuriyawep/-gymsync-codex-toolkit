#!/usr/bin/env python3
"""Synchronize portable skills/ copies from the native .agents/skills/ source.

Preview by default. Use --write to copy files. Use --check in CI to fail if
mirrors differ. No third-party packages are required.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
TARGET = ROOT / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="copy native skills to portable mirror")
    mode.add_argument("--check", action="store_true", help="fail if mirror is out of sync")
    args = parser.parse_args()

    if not SOURCE.is_dir():
        print("ERROR: .agents/skills source directory not found", file=sys.stderr)
        return 2

    differences: list[str] = []
    for source_file in sorted(SOURCE.glob("*/SKILL.md")):
        relative = source_file.relative_to(SOURCE)
        target_file = TARGET / relative
        source_bytes = source_file.read_bytes()
        if not target_file.exists() or target_file.read_bytes() != source_bytes:
            differences.append(str(relative))
            if args.write:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                target_file.write_bytes(source_bytes)
                print(f"SYNCED {relative}")
            else:
                print(f"DIFF {relative}")

    if args.write:
        print(f"Sync complete: {len(differences)} file(s) copied.")
        return 0
    if args.check and differences:
        print(f"Out of sync: {len(differences)} skill mirror(s). Run with --write.")
        return 1
    if differences:
        print(f"Preview only: {len(differences)} difference(s); no files changed.")
    else:
        print("Skill mirrors are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
