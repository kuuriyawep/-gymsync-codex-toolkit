from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import scan_secrets


class SecretScannerTests(unittest.TestCase):
    def test_detects_provider_token_without_returning_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            token = "ghp_" + ("Ab3Cd5Ef7Gh9Jk2Lm4Np6Qr8St0Uv1Wx" * 1)
            target = root / "nested" / "config.env"
            target.parent.mkdir()
            target.write_text("GITHUB_TOKEN=" + token + "\n", encoding="utf-8")

            findings = scan_secrets.scan_repository(root)

            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0][0], "nested/config.env")
            self.assertEqual(findings[0][1], "github-personal-access-token")
            self.assertNotIn(token, repr(findings))

    def test_detects_high_entropy_credential_assignment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            value = "A9f3K8p2M7q4R6s1T5v0X9z2"
            (root / "settings.txt").write_text("client_secret=" + value, encoding="utf-8")

            findings = scan_secrets.scan_repository(root)

            self.assertEqual([item[1] for item in findings], ["high-entropy-credential-assignment"])

    def test_scans_nested_repository_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "docs" / "sample.txt"
            nested.parent.mkdir()
            nested.write_text("key = AKIA" + "1234567890ABCDEF", encoding="utf-8")

            findings = scan_secrets.scan_repository(root)

            self.assertEqual(findings[0][0], "docs/sample.txt")
            self.assertEqual(findings[0][1], "aws-access-key-id")

    def test_ignores_binary_files_and_git_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "image.bin").write_bytes(b"\x00AKIA1234567890ABCDEF")
            git_dir = root / ".git"
            git_dir.mkdir()
            (git_dir / "config").write_text("AKIA1234567890ABCDEF", encoding="utf-8")

            self.assertEqual(scan_secrets.scan_repository(root), [])

    def test_reports_rule_and_location_not_secret_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            token = "xoxb-" + ("A" * 24)
            target = root / "secrets.txt"
            target.write_text(token, encoding="utf-8")

            findings = scan_secrets.scan_repository(root)

            self.assertEqual(findings, [("secrets.txt", "slack-token", 1)])
            self.assertNotIn(token, repr(findings))


if __name__ == "__main__":
    unittest.main()
