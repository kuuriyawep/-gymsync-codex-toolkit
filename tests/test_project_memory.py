from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_project_memory", ROOT / "tools" / "validate_project_memory.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ProjectMemoryValidatorTests(unittest.TestCase):
    def test_repository_templates_pass_structure_validation(self) -> None:
        errors, _warnings = validator.validate(90, False)
        self.assertEqual(errors, [])

    def test_date_parser_accepts_iso_date(self) -> None:
        self.assertEqual(
            validator.parse_date("- Last verified: 2026-11-16"),
            validator.date(2026, 11, 16),
        )

    def test_date_parser_ignores_template_placeholder(self) -> None:
        self.assertIsNone(validator.parse_date("- Last verified: YYYY-MM-DD"))

    def test_secret_pattern_detects_github_token_shape(self) -> None:
        token = "ghp_" + "A" * 30
        self.assertTrue(any(pattern.search(token) for pattern in validator.SECRET_PATTERNS))

    def test_status_vocabulary_is_explicit(self) -> None:
        self.assertIn("Verified", validator.ALLOWED_STATUS)
        self.assertNotIn("Final-ish", validator.ALLOWED_STATUS)


if __name__ == "__main__":
    unittest.main()
