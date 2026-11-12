from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import evaluate_toolkit as evaluator  # noqa: E402


class TypeMatchingTests(unittest.TestCase):
    def test_boolean_is_not_integer(self) -> None:
        self.assertFalse(evaluator.type_matches(True, "integer"))

    def test_boolean_is_not_number(self) -> None:
        self.assertFalse(evaluator.type_matches(False, "number"))

    def test_integer_matches_number(self) -> None:
        self.assertTrue(evaluator.type_matches(7, "number"))


class SchemaValidationTests(unittest.TestCase):
    def test_required_and_additional_properties_are_checked(self) -> None:
        schema = {
            "type": "object",
            "required": ["name"],
            "properties": {"name": {"type": "string"}},
            "additionalProperties": False,
        }
        errors = evaluator.validate_instance({"unexpected": 1}, schema)
        self.assertTrue(any("missing required property 'name'" in item for item in errors))
        self.assertTrue(any("unexpected property 'unexpected'" in item for item in errors))

    def test_pattern_and_minimum_length_are_checked(self) -> None:
        schema = {"type": "string", "minLength": 3, "pattern": "^[a-z]+$"}
        self.assertEqual(evaluator.validate_instance("A", schema), [
            "$: shorter than minLength",
            "$: does not match required pattern",
        ])

    def test_timezone_is_required_for_date_time(self) -> None:
        schema = {"type": "string", "format": "date-time"}
        self.assertTrue(evaluator.validate_instance("2026-11-12T10:00:00", schema))
        self.assertEqual(evaluator.validate_instance("2026-11-12T10:00:00Z", schema), [])

    def test_unique_items_are_checked(self) -> None:
        schema = {"type": "array", "uniqueItems": True}
        self.assertTrue(evaluator.validate_instance(["same", "same"], schema))


class OverallStatusTests(unittest.TestCase):
    def status(self, status: str, critical: bool = False) -> str:
        return evaluator.overall_status([
            {"status": status, "critical": critical}
        ])

    def test_critical_failure_fails(self) -> None:
        self.assertEqual(self.status("FAIL", critical=True), "FAIL")

    def test_noncritical_failure_also_fails(self) -> None:
        self.assertEqual(self.status("FAIL"), "FAIL")

    def test_blocked_precedes_not_run(self) -> None:
        self.assertEqual(evaluator.overall_status([
            {"status": "BLOCKED", "critical": False},
            {"status": "NOT_RUN", "critical": False},
        ]), "BLOCKED")

    def test_not_run_is_not_a_pass(self) -> None:
        self.assertEqual(self.status("NOT_RUN"), "NOT_RUN")

    def test_all_pass_is_pass(self) -> None:
        self.assertEqual(evaluator.overall_status([
            {"status": "PASS", "critical": True},
            {"status": "PASS", "critical": False},
        ]), "PASS")

    def test_not_applicable_only_is_not_run(self) -> None:
        self.assertEqual(self.status("NOT_APPLICABLE"), "NOT_RUN")


class ArtifactSafetyTests(unittest.TestCase):
    def test_repository_path_is_accepted(self) -> None:
        path = evaluator.resolve_repo_path(ROOT / "evals" / "results" / "sample.json")
        self.assertEqual(path, (ROOT / "evals" / "results" / "sample.json").resolve())

    def test_path_outside_repository_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            evaluator.resolve_repo_path(ROOT.parent / "outside.json")

    def test_artifacts_are_created_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".phase4-test-", dir=ROOT) as temp:
            base = Path(temp)
            output = base / "results" / "run.json"
            report = base / "reports" / "run.md"
            evaluator.write_new_artifacts(output, report, '{"run": 1}\n', "# Run\n")
            self.assertEqual(output.read_text(encoding="utf-8"), '{"run": 1}\n')
            self.assertEqual(report.read_text(encoding="utf-8"), "# Run\n")
            with self.assertRaises(FileExistsError):
                evaluator.write_new_artifacts(output, report, '{"run": 2}\n', "# Changed\n")
            self.assertEqual(output.read_text(encoding="utf-8"), '{"run": 1}\n')
            self.assertEqual(report.read_text(encoding="utf-8"), "# Run\n")

    def test_partial_artifact_creation_is_rolled_back(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".phase4-test-", dir=ROOT) as temp:
            base = Path(temp)
            output = base / "results" / "run.json"
            report = base / "reports" / "run.md"
            report.parent.mkdir(parents=True)
            report.write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                evaluator.write_new_artifacts(output, report, '{"run": 1}\n', "# Run\n")
            self.assertFalse(output.exists())
            self.assertEqual(report.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
