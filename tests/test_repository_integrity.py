from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_toolkit  # noqa: E402


VALID_WORKFLOW = """## Workflow

1. Inspect the task.
2. Execute the approved steps.

## Stop conditions

- Stop when required evidence is unavailable.

## Required output

- Report the outcome and evidence.
"""


class RepositoryIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.root.mkdir(exist_ok=True)
        self.root_patch = patch.object(validate_toolkit, "ROOT", self.root)
        self.root_patch.start()
        validate_toolkit.ERRORS.clear()
        validate_toolkit.WARNINGS.clear()

    def tearDown(self) -> None:
        self.root_patch.stop()
        self.temp_dir.cleanup()
        validate_toolkit.ERRORS.clear()
        validate_toolkit.WARNINGS.clear()

    def collect_errors(self, validator) -> list[str]:
        validate_toolkit.ERRORS.clear()
        validator()
        return list(validate_toolkit.ERRORS)

    def test_missing_canonical_skill_is_rejected(self) -> None:
        (self.root / ".agents" / "skills").mkdir(parents=True)
        (self.root / "skills").mkdir()
        errors = self.collect_errors(validate_toolkit.validate_skills)
        self.assertTrue(any(
            ".agents/skills/change-impact-analysis/SKILL.md: required canonical skill is missing" in error
            for error in errors
        ))

    def test_whitespace_only_skill_body_is_rejected(self) -> None:
        skill_name = validate_toolkit.REQUIRED_SKILLS[0]
        native = self.root / ".agents" / "skills" / skill_name
        mirror = self.root / "skills" / skill_name
        native.mkdir(parents=True)
        mirror.mkdir(parents=True)
        empty_body = f"---\nname: {skill_name}\ndescription: Test skill\n---\n   \n"
        (native / "SKILL.md").write_text(empty_body, encoding="utf-8")
        (mirror / "SKILL.md").write_text(empty_body, encoding="utf-8")

        errors = self.collect_errors(validate_toolkit.validate_skills)
        self.assertTrue(any("skill body must be non-empty" in error for error in errors))

    def test_missing_required_workflow_is_rejected(self) -> None:
        directory = self.root / "workflows"
        directory.mkdir()
        for filename in validate_toolkit.REQUIRED_WORKFLOW_FILES:
            if filename != "bug-fix.md":
                (directory / filename).write_text(VALID_WORKFLOW, encoding="utf-8")

        errors = self.collect_errors(validate_toolkit.validate_workflows)
        self.assertTrue(any(
            "workflows/bug-fix.md: required workflow asset is missing" in error
            for error in errors
        ))

    def test_workflow_with_empty_procedure_section_is_rejected(self) -> None:
        directory = self.root / "workflows"
        directory.mkdir()
        for filename in validate_toolkit.REQUIRED_WORKFLOW_FILES:
            content = VALID_WORKFLOW
            if filename == "bug-fix.md":
                content = """## Workflow

## Stop conditions

- Stop when unsafe.

## Required output

- Report the result.
"""
            (directory / filename).write_text(content, encoding="utf-8")

        errors = self.collect_errors(validate_toolkit.validate_workflows)
        self.assertTrue(any(
            "bug-fix.md: workflow section must contain executable steps" in error
            for error in errors
        ))


if __name__ == "__main__":
    unittest.main()
