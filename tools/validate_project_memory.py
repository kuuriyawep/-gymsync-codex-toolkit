#!/usr/bin/env python3
"""Validate project-memory template structure and selected safety/freshness rules."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "templates" / "project-memory"
REQUIRED = {
    "project-profile.md": ["## Purpose and users", "## Technology stack", "## Sources"],
    "repository-map.md": ["## Entry points", "## Major modules", "## Sources"],
    "architecture.md": ["## System context", "## Components and boundaries", "## Sources"],
    "system-inventory.md": ["## Runtime and dependencies", "## Services and integrations", "## Sources"],
    "constraints.md": ["## Non-negotiable invariants", "## Security and privacy", "## Sources"],
    "current-state.md": ["## Objective", "## Completed", "## Verification performed", "## Next action"],
    "decisions/README.md": ["# Decision records"],
}
ALLOWED_STATUS = {"Proposed", "Verified", "Assumption", "Unknown", "Stale", "Approved"}
SECRET_PATTERNS = [
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{16,}"),
]


def parse_date(content: str) -> date | None:
    match = re.search(r"(?m)^- Last verified:\s*(\d{4}-\d{2}-\d{2})\s*$", content)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def validate(max_age_days: int = 90, strict_freshness: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not MEMORY.is_dir():
        return [f"Missing memory template directory: {MEMORY.relative_to(ROOT)}"], warnings

    for relative, headings in REQUIRED.items():
        path = MEMORY / relative
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
            continue
        content = path.read_text(encoding="utf-8")
        for heading in headings:
            if heading not in content:
                errors.append(f"{path.relative_to(ROOT)}: missing heading {heading!r}")

        status = re.search(r"(?m)^- Status:\s*(.+?)\s*$", content)
        if status and status.group(1) not in ALLOWED_STATUS:
            errors.append(f"{path.relative_to(ROOT)}: unsupported status {status.group(1)!r}")

        if "## Sources" in headings:
            source_section = content.split("## Sources", 1)[1]
            if not re.search(r"(?m)^- .+\S", source_section):
                warnings.append(f"{path.relative_to(ROOT)}: add a concrete source reference")

        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            errors.append(f"{path.relative_to(ROOT)}: possible secret-like value detected")

        verified = parse_date(content)
        if verified:
            age = (date.today() - verified).days
            if age > max_age_days:
                message = f"{path.relative_to(ROOT)}: last verified {age} days ago (limit {max_age_days})"
                (errors if strict_freshness else warnings).append(message)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-age-days", type=int, default=90, help="freshness window (default: 90 days)")
    parser.add_argument("--strict-freshness", action="store_true", help="treat stale dated pages as errors")
    args = parser.parse_args()
    if args.max_age_days < 1:
        parser.error("--max-age-days must be at least 1")

    errors, warnings = validate(args.max_age_days, args.strict_freshness)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Project memory validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"Project memory structure valid: {len(REQUIRED)} required files, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
