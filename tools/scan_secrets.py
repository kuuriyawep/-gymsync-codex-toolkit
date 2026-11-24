#!/usr/bin/env python3
"""Scan repository text files for likely credentials without printing secret values."""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache"}
MAX_FILE_BYTES = 1_000_000

# Provider-specific patterns are deliberately narrow to limit false positives.
RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("aws-access-key-id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-personal-access-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("stripe-live-secret", re.compile(r"\bsk_live_[A-Za-z0-9]{20,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("private-key-header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
    r"password|passwd|secret|token)\b\s*[:=]\s*['\" ]?([A-Za-z0-9_./+\-=]{24,})"
)


def shannon_entropy(value: str) -> float:
    counts = Counter(value)
    length = len(value)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def candidate_files(root: Path = ROOT):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        for filename in sorted(files):
            path = Path(current) / filename
            try:
                if path.stat().st_size <= MAX_FILE_BYTES:
                    yield path
            except OSError:
                continue


def scan_file(path: Path, root: Path = ROOT) -> list[tuple[str, int]]:
    try:
        raw = path.read_bytes()
        if b"\x00" in raw:
            return []
        content = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    findings: set[tuple[str, int]] = set()
    for line_number, line in enumerate(content.splitlines(), start=1):
        for rule, pattern in RULES:
            if pattern.search(line):
                findings.add((rule, line_number))
        for match in ASSIGNMENT.finditer(line):
            value = match.group(1).rstrip(".,;")
            if len(value) >= 24 and shannon_entropy(value) >= 3.5:
                findings.add(("high-entropy-credential-assignment", line_number))
    return sorted(findings)


def scan_repository(root: Path = ROOT) -> list[tuple[str, str, int]]:
    findings: list[tuple[str, str, int]] = []
    for path in candidate_files(root):
        for rule, line_number in scan_file(path, root):
            findings.append((path.relative_to(root).as_posix(), rule, line_number))
    return sorted(findings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    findings = scan_repository(args.root.resolve())
    for relative_path, rule, line_number in findings:
        # Never print the matched text or a surrounding source excerpt.
        print(f"ERROR: {relative_path}:{line_number}: possible secret detected ({rule})")
    if findings:
        print(f"Secret scan failed: {len(findings)} finding(s); values were redacted")
        return 1
    print("Secret scan passed: no known credential patterns detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
