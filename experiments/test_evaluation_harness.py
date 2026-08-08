"""Focused regression tests for the evaluation harness."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_eval_common import (
    compact_jsonl,
    condition_instructions,
    parse_codex_jsonl,
    parse_pi_jsonl,
)
from adjudicate_novel_findings import score_novel
from evaluate_judge import discover_reviews, parse_claude_result
from experiment_runner import extract_findings
from generate_variants import generate_variant


BASE = Path(__file__).parent
RHODES_SKILL = BASE.parent / "python-rhodes-reviewer" / "SKILL.md"


class VariantTests(unittest.TestCase):
    def test_rhodes_ablation_variants_are_actually_smaller(self) -> None:
        full = generate_variant(RHODES_SKILL, "full")
        ids_only = generate_variant(RHODES_SKILL, "ids-only")
        hybrid = generate_variant(
            RHODES_SKILL,
            "hybrid",
            priority_ids=["NO-MOCK", "NO-CALL", "TOP-DOWN"],
        )
        self.assertLess(len(ids_only), len(hybrid))
        self.assertLess(len(hybrid), len(full))
        self.assertNotIn("# Python Coding Guidelines", ids_only)
        self.assertNotIn("### NO-CALL:", ids_only)
        self.assertIn("### NO-MOCK:", hybrid)

    def test_regular_and_lean_conditions_isolate_skill_guidance(self) -> None:
        lean = BASE / "skills" / "python-rhodes-reviewer-lean" / "SKILL.md"
        self.assertEqual(condition_instructions("regular", lean), "")
        instructions = condition_instructions("lean-skill", lean)
        self.assertIn("**HOIST-IO**", instructions)
        self.assertIn("lens, not as a\nfinding", instructions)


class FindingParserTests(unittest.TestCase):
    def test_accepts_numbered_and_underscore_local_model_headings(self) -> None:
        review = """## Issue 1: GLOBAL_STATE_MGMT
Details.

## 2️⃣ LOG_CFG – Import-time setup
Details.

### **NO-EVAL**: Dynamic execution

## 4. `SCHEMA-DRIFT` — Persisted shape differs
"""
        ids = {finding["id"] for finding in extract_findings(review)}
        self.assertEqual(
            ids,
            {"GLOBAL_STATE_MGMT", "LOG_CFG", "NO-EVAL", "SCHEMA-DRIFT"},
        )


class AgentEventParserTests(unittest.TestCase):
    def test_compaction_removes_incremental_events_only(self) -> None:
        raw = "\n".join(
            json.dumps({"type": event_type})
            for event_type in ("agent_start", "message_update", "message_end")
        )
        compacted = compact_jsonl(raw)
        self.assertIn("agent_start", compacted)
        self.assertIn("message_end", compacted)
        self.assertNotIn("message_update", compacted)

    def test_pi_jsonl_extracts_final_message_and_tools(self) -> None:
        raw = "\n".join(
            [
                json.dumps({"type": "session", "version": 3}),
                json.dumps(
                    {
                        "type": "tool_execution_start",
                        "toolCallId": "1",
                        "toolName": "read",
                        "args": {"path": "x.py"},
                    }
                ),
                json.dumps(
                    {
                        "type": "message_end",
                        "message": {
                            "role": "assistant",
                            "content": [{"type": "text", "text": "## NO-EVAL: Avoid eval"}],
                        },
                    }
                ),
            ]
        )
        parsed = parse_pi_jsonl(raw)
        self.assertEqual(parsed["tool_call_count"], 1)
        self.assertEqual(parsed["findings_count"], 1)
        self.assertIn("NO-EVAL", parsed["output"])

    def test_codex_jsonl_extracts_agent_message(self) -> None:
        raw = "\n".join(
            [
                json.dumps(
                    {
                        "type": "item.started",
                        "item": {"id": "cmd-1", "type": "command_execution"},
                    }
                ),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "id": "cmd-1",
                            "type": "command_execution",
                            "status": "failed",
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "type": "agent_message",
                            "text": "## NO-CALL: Prefer named method",
                        },
                    }
                ),
            ]
        )
        parsed = parse_codex_jsonl(raw)
        self.assertEqual(parsed["findings_count"], 1)
        self.assertEqual(parsed["tool_call_count"], 1)
        self.assertEqual(parsed["tool_error_count"], 1)
        self.assertIn("NO-CALL", parsed["output"])


class JudgeTests(unittest.TestCase):
    def test_scores_valid_novel_verdict_as_validated(self) -> None:
        evaluation = {
            "runs": [
                {
                    "label": "codex/model/lean-skill",
                    "condition": "lean-skill",
                    "run": 1,
                    "detected": 2,
                    "recall": 0.1,
                    "unsupported_count": 0,
                    "judgments": [
                        {"issue_id": "R-001", "detected": True},
                        {"issue_id": "R-002", "detected": True},
                    ],
                }
            ]
        }
        private = {
            "N-001": {
                "label": "codex/model/lean-skill",
                "condition": "lean-skill",
                "run": 1,
            }
        }
        scores = score_novel(
            evaluation,
            [{"verdict": "valid", "member_ids": ["N-001"]}],
            private,
        )
        self.assertEqual(scores["runs"][0]["novel_validated"], 1)

    def test_discovers_nested_and_legacy_review_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            nested = root / "pi-ollama" / "qwen" / "hybrid" / "run-2-review.md"
            legacy = root / "zero-shot" / "run-1-review.md"
            nested.parent.mkdir(parents=True)
            legacy.parent.mkdir(parents=True)
            nested.write_text("nested")
            legacy.write_text("legacy")
            found = discover_reviews(root)
            self.assertEqual(
                {(item["label"], item["run"]) for item in found},
                {("pi-ollama/qwen/hybrid", 2), ("zero-shot", 1)},
            )

    def test_parses_claude_structured_output_envelope(self) -> None:
        payload = {
            "judgments": [],
            "unsupported_findings": [],
            "novel_findings": [],
            "quality": {},
        }
        parsed = parse_claude_result(json.dumps({"structured_output": payload}))
        self.assertEqual(parsed, payload)


if __name__ == "__main__":
    unittest.main()
