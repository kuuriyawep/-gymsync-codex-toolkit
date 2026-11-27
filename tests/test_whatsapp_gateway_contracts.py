from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MESSAGE = json.loads((ROOT / "schemas" / "whatsapp-message-envelope.schema.json").read_text(encoding="utf-8"))
APPROVAL = json.loads((ROOT / "schemas" / "whatsapp-approval-request.schema.json").read_text(encoding="utf-8"))
DOC = (ROOT / "docs" / "whatsapp-intelligence-gateway-contract.md").read_text(encoding="utf-8")


class WhatsAppGatewayContractTests(unittest.TestCase):
    def test_message_schema_is_closed_and_has_identity_and_dedupe_fields(self):
        self.assertFalse(MESSAGE["additionalProperties"])
        self.assertTrue({"sender", "recipient", "provider_message_id", "idempotency_key", "correlation_id"}.issubset(MESSAGE["required"]))

    def test_message_classes_and_directions_are_bounded(self):
        props = MESSAGE["properties"]
        self.assertEqual(set(props["message_class"]["enum"]), {"user_command", "status_report", "incident_alert", "approval_request", "approval_response", "media_artifact"})
        self.assertEqual(set(props["direction"]["enum"]), {"inbound", "outbound"})

    def test_approval_response_is_bound_to_verified_user_and_digest(self):
        rule = next(x for x in MESSAGE["allOf"] if x["if"]["properties"]["message_class"].get("const") == "approval_response")
        then = rule["then"]
        self.assertEqual(then["properties"]["direction"]["const"], "inbound")
        self.assertEqual(then["properties"]["sender"]["properties"]["identity_type"]["const"], "verified_user")
        self.assertIn("payload_digest", then["required"])

    def test_approval_request_has_exact_action_target_digest_and_expiry(self):
        self.assertTrue({"operation_id", "action", "target", "payload_digest", "expires_at", "nonce", "issuer"}.issubset(APPROVAL["required"]))
        self.assertEqual(APPROVAL["properties"]["issuer"]["const"], "codex")
        self.assertEqual(APPROVAL["properties"]["risk"]["enum"], ["R3", "R4"])

    def test_docs_preserve_codex_and_human_authority(self):
        for phrase in ("Codex remains the single router", "user retains final authority", "never approval", "fail closed"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, DOC)

    def test_docs_require_identity_replay_and_redaction_controls(self):
        for phrase in ("pre-verified user identity", "Deduplicate retries", "redact", "rate limits", "replay"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), DOC.lower())

    def test_external_integration_requires_separate_explicit_approval(self):
        self.assertIn("separate explicit user approval", DOC)
        self.assertIn("NOT_RUN / BLOCKED", DOC)


if __name__ == "__main__":
    unittest.main()
