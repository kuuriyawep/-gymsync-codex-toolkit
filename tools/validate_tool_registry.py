#!/usr/bin/env python3
"""Validate the declarative tool registry without executing or connecting tools."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "tools.json"
SCHEMA_PATH = ROOT / "schemas" / "tool-registry.schema.json"
ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
CREDENTIAL_RE = re.compile(r"^(env:[A-Z][A-Z0-9_]*|secret://[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*)$")
TRANSPORTS = {"codex-native", "mcp", "cli", "http-api", "browser", "database", "filesystem", "git"}
RISKS = {"read", "write", "destructive", "external"}
ACTIONS = {"read", "list", "search", "create", "update", "delete", "execute", "publish"}
EFFECTS = {"none", "local-write", "remote-read", "remote-state-change", "external-communication", "production-data-mutation"}
APPROVALS = {"none", "required", "conditional"}
AVAILABILITY = {"planned", "configured", "verified", "disabled"}
EVIDENCE = {"not-run", "static-reviewed", "runtime-verified", "blocked"}


def _validate_io_schema(value: Any, path: str, errors: list[str]) -> None:
    """Validate the structural subset used by operation input/output JSON Schemas."""
    if not isinstance(value, dict):
        errors.append(f"{path} must be a JSON Schema object")
        return
    if value.get("type") != "object":
        errors.append(f"{path}.type must be 'object'")
    properties = value.get("properties", {})
    if not isinstance(properties, dict):
        errors.append(f"{path}.properties must be an object")
        return
    required = value.get("required", [])
    if not isinstance(required, list) or any(not isinstance(x, str) for x in required):
        errors.append(f"{path}.required must be an array of property names")
    elif set(required) - set(properties):
        errors.append(f"{path}.required references undefined properties")
    for name, spec in properties.items():
        if not isinstance(name, str) or not isinstance(spec, dict):
            errors.append(f"{path}.properties entries must map names to schema objects")
            continue
        if not isinstance(spec.get("type"), str) and "const" not in spec and "enum" not in spec:
            errors.append(f"{path}.properties.{name} must declare a type, const, or enum")
        if "items" in spec and not isinstance(spec["items"], dict):
            errors.append(f"{path}.properties.{name}.items must be a schema object")
        if "properties" in spec and not isinstance(spec["properties"], dict):
            errors.append(f"{path}.properties.{name}.properties must be an object")


def validate_registry(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry root must be an object"]
    root_keys = {"schema_version", "registry_id", "default_policy", "tools"}
    if set(data) - root_keys:
        errors.append(f"unexpected registry properties: {sorted(set(data) - root_keys)}")
    if root_keys - set(data):
        errors.append(f"missing registry properties: {sorted(root_keys - set(data))}")
    if data.get("schema_version") != "1.0.0":
        errors.append("schema_version must be '1.0.0'")
    if not isinstance(data.get("registry_id"), str) or not re.fullmatch(r"^[a-z][a-z0-9-]*$", data["registry_id"]):
        errors.append("registry_id must be a lowercase stable identifier")
    if data.get("default_policy") != "deny":
        errors.append("default_policy must be 'deny'")
    tools = data.get("tools")
    if not isinstance(tools, list):
        errors.append("tools must be an array")
        return errors

    seen_tools: set[str] = set()
    for i, tool in enumerate(tools):
        p = f"tools[{i}]"
        if not isinstance(tool, dict):
            errors.append(f"{p} must be an object")
            continue
        required = {"id", "name", "description", "provider", "transport", "capabilities",
                    "operations", "availability", "permission_profile", "evidence"}
        optional = {"provider_version", "credential_ref", "timeout_seconds", "retry"}
        if set(tool) - required - optional:
            errors.append(f"{p} has unexpected properties: {sorted(set(tool) - required - optional)}")
        if required - set(tool):
            errors.append(f"{p} is missing properties: {sorted(required - set(tool))}")
        tid = tool.get("id")
        if not isinstance(tid, str) or not ID_RE.fullmatch(tid):
            errors.append(f"{p}.id must be a stable lowercase identifier")
        elif tid in seen_tools:
            errors.append(f"duplicate tool id: {tid}")
        else:
            seen_tools.add(tid)
        for field in ("name", "description", "provider", "permission_profile"):
            if not isinstance(tool.get(field), str) or not tool[field].strip():
                errors.append(f"{p}.{field} must be a non-empty string")
        if not isinstance(tool.get("transport"), str) or tool["transport"] not in TRANSPORTS:
            errors.append(f"{p}.transport is unsupported")
        if not isinstance(tool.get("availability"), str) or tool["availability"] not in AVAILABILITY:
            errors.append(f"{p}.availability is unsupported")
        caps = tool.get("capabilities")
        if not isinstance(caps, list) or not caps or any(not isinstance(x, str) or not x.strip() for x in caps):
            errors.append(f"{p}.capabilities must be a non-empty array of strings")
        elif len(caps) != len(set(caps)):
            errors.append(f"{p}.capabilities must be unique")
        ops = tool.get("operations")
        if not isinstance(ops, list) or not ops:
            errors.append(f"{p}.operations must be a non-empty array")
        else:
            seen_ops: set[str] = set()
            for j, op in enumerate(ops):
                q = f"{p}.operations[{j}]"
                if not isinstance(op, dict):
                    errors.append(f"{q} must be an object")
                    continue
                req = {"id", "description", "resource_scope", "action", "effect", "risk", "idempotent", "approval", "input_schema", "output_schema"}
                opt = set()
                if set(op) - req - opt:
                    errors.append(f"{q} has unexpected properties: {sorted(set(op) - req - opt)}")
                if req - set(op):
                    errors.append(f"{q} is missing properties: {sorted(req - set(op))}")
                oid = op.get("id")
                if not isinstance(oid, str) or not ID_RE.fullmatch(oid):
                    errors.append(f"{q}.id must be a stable lowercase identifier")
                elif oid in seen_ops:
                    errors.append(f"{p} has duplicate operation id: {oid}")
                else:
                    seen_ops.add(oid)
                if not isinstance(op.get("description"), str) or len(op["description"].strip()) < 5:
                    errors.append(f"{q}.description must contain at least 5 characters")
                scopes = op.get("resource_scope")
                if not isinstance(scopes, list) or not scopes or any(not isinstance(x, str) or len(x.strip()) < 2 for x in scopes):
                    errors.append(f"{q}.resource_scope must be a non-empty array of scoped resource labels")
                action = op.get("action")
                if not isinstance(action, str) or action not in ACTIONS:
                    errors.append(f"{q}.action is unsupported")
                effect = op.get("effect")
                if not isinstance(effect, str) or effect not in EFFECTS:
                    errors.append(f"{q}.effect is unsupported")
                risk = op.get("risk")
                if not isinstance(risk, str) or risk not in RISKS:
                    errors.append(f"{q}.risk is unsupported")
                if not isinstance(op.get("idempotent"), bool):
                    errors.append(f"{q}.idempotent must be boolean")
                approval = op.get("approval")
                if not isinstance(approval, str) or approval not in APPROVALS:
                    errors.append(f"{q}.approval is unsupported")
                if isinstance(risk, str) and risk in {"destructive", "external"} and approval != "required":
                    errors.append(f"{q}: destructive/external operations must require approval")
                if isinstance(effect, str) and effect in {"local-write", "remote-state-change", "external-communication", "production-data-mutation"} and approval == "none":
                    errors.append(f"{q}: side-effecting operations cannot use approval='none'")
                if action in {"create", "update", "delete", "publish"} and effect in {"none", "remote-read"}:
                    errors.append(f"{q}: write action cannot declare a read-only effect")
                if risk == "read" and effect in {"local-write", "remote-state-change", "production-data-mutation"}:
                    errors.append(f"{q}: read risk cannot declare a write effect")
                for field in ("input_schema", "output_schema"):
                    _validate_io_schema(op.get(field), f"{q}.{field}", errors)
        cred = tool.get("credential_ref")
        if cred is not None and (not isinstance(cred, str) or not CREDENTIAL_RE.fullmatch(cred)):
            errors.append(f"{p}.credential_ref must be env:NAME or secret://path; raw credentials are forbidden")
        timeout = tool.get("timeout_seconds")
        if timeout is not None and (not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 3600):
            errors.append(f"{p}.timeout_seconds must be an integer from 1 to 3600")
        retry = tool.get("retry")
        if retry is not None:
            if not isinstance(retry, dict) or set(retry) != {"max_attempts", "retryable_errors"}:
                errors.append(f"{p}.retry must contain only max_attempts and retryable_errors")
            else:
                attempts = retry.get("max_attempts")
                if not isinstance(attempts, int) or isinstance(attempts, bool) or not 1 <= attempts <= 5:
                    errors.append(f"{p}.retry.max_attempts must be an integer from 1 to 5")
                if not isinstance(retry.get("retryable_errors"), list) or any(not isinstance(x, str) for x in retry["retryable_errors"]):
                    errors.append(f"{p}.retry.retryable_errors must be an array of strings")
        ev = tool.get("evidence")
        if not isinstance(ev, dict) or set(ev) - {"status", "references", "verified_at"} or not {"status", "references"} <= set(ev):
            errors.append(f"{p}.evidence must contain status and references only")
        else:
            if not isinstance(ev.get("status"), str) or ev["status"] not in EVIDENCE:
                errors.append(f"{p}.evidence.status is unsupported")
            refs = ev.get("references")
            if not isinstance(refs, list) or any(not isinstance(x, str) or not x.strip() for x in refs):
                errors.append(f"{p}.evidence.references must be an array of non-empty strings")
            if tool.get("availability") == "verified" and (ev.get("status") != "runtime-verified" or not refs):
                errors.append(f"{p}: verified availability requires runtime-verified evidence references")
            if ev.get("status") == "runtime-verified" and not refs:
                errors.append(f"{p}: runtime-verified evidence requires references")
    return errors


def validate_files() -> list[str]:
    errors: list[str] = []
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("type") != "object":
            errors.append("tool registry schema must declare a Draft 2020-12 object root")
        else:
            properties = schema.get("properties", {})
            if properties.get("default_policy", {}).get("const") != "deny":
                errors.append("tool registry schema must enforce default_policy=deny")
            tool_item = properties.get("tools", {}).get("items", {})
            tool_props = tool_item.get("properties", {}) if isinstance(tool_item, dict) else {}
            op_item = tool_props.get("operations", {}).get("items", {})
            op_props = op_item.get("properties", {}) if isinstance(op_item, dict) else {}
            for field, expected in (("risk", RISKS), ("action", ACTIONS), ("effect", EFFECTS), ("approval", APPROVALS)):
                actual = op_props.get(field, {}).get("enum")
                if not isinstance(actual, list) or set(actual) != expected:
                    errors.append(f"tool registry schema {field} enum does not match validator contract")
            required_ops = {"id", "description", "resource_scope", "action", "effect", "risk", "idempotent", "approval", "input_schema", "output_schema"}
            if set(op_item.get("required", [])) != required_ops:
                errors.append("tool registry schema operation required fields do not match validator contract")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read valid tool registry schema: {exc}")
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read valid tool registry: {exc}")
        return errors
    errors.extend(validate_registry(data))
    return errors


if __name__ == "__main__":
    issues = validate_files()
    for issue in issues:
        print(f"ERROR: {issue}")
    if issues:
        raise SystemExit(1)
    print("Tool registry validation passed (declarative manifest only; no tool execution).")
