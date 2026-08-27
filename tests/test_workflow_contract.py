import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / ".vibe/core/technical-decision-readiness.md"


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text
    )
    if not match:
        raise AssertionError(f"missing section: {heading}")
    return match.group("body")


def readiness_fields(text: str) -> dict:
    body = section(text, "Technical decision readiness")
    fields = {}
    for name, value in re.findall(r"(?m)^- ([^:]+):\s*(.+)$", body):
        fields[name] = value.strip().strip("`")
    return fields


class WorkflowContractTests(unittest.TestCase):
    """Static managed-contract tests; these do not certify live Agent behavior."""

    def test_core_declares_complete_fail_closed_state_model(self) -> None:
        core = CORE_PATH.read_text()
        outcome_body = core.split("`Outcome` is exactly one of:", 1)[1].split(
            "`Gate` is exactly", 1
        )[0]
        outcomes = re.findall(r"(?m)^- `([^`]+)`$", outcome_body)
        self.assertEqual(
            outcomes,
            [
                "not-assessed",
                "decision-required",
                "covered-by-accepted-decision",
                "no-new-durable-decision",
                "decision-accepted",
            ],
        )
        for value in (
            "`blocked` or `implementation-ready`",
            "`not-required`, `independent-agent`, or",
            "`not-required`, `pending`,",
            "Status: Accepted",
            "The contract fails closed.",
            "ISO-8601 confirmation time",
        ):
            self.assertIn(value, core)

    def test_work_item_template_initializes_all_fields_blocked(self) -> None:
        template = (ROOT / ".vibe/core/templates/work-item-brief.md").read_text()
        self.assertEqual(
            readiness_fields(template),
            {
                "Outcome": "not-assessed",
                "Trigger evidence": "none",
                "Decision owner": "none",
                "Governing decision": "none",
                "Review mode": "not-required",
                "Review result": "not-required",
                "Review evidence": "none",
                "Material product decisions": "none",
                "Open blockers": "none",
                "Gate": "blocked",
                "Gate owner": "Workflow orchestrator",
                "Confirmed at": "none",
                "Confirmation basis": "none",
                "Readiness history": "none",
            },
        )

    def test_implementation_entry_points_apply_one_canonical_contract(self) -> None:
        paths = {
            "feature": ROOT / ".agents/skills/vibe-feature-flow/SKILL.md",
            "debug": ROOT / ".agents/skills/vibe-debug-flow/SKILL.md",
            "implementation": ROOT / ".agents/skills/vibe-implementation-flow/SKILL.md",
            "verification": ROOT / ".agents/skills/vibe-verification-flow/SKILL.md",
        }
        for name, path in paths.items():
            with self.subTest(workflow=name):
                content = path.read_text()
                self.assertIn(".vibe/core/technical-decision-readiness.md", content)
                self.assertNotIn("## State and release rules", content)

        feature = paths["feature"].read_text()
        self.assertLess(feature.index("vibe_tech_lead"), feature.index("vibe_rd"))
        self.assertIn("While blocked, do not edit application/shared code", feature)

        debug = paths["debug"].read_text()
        self.assertIn("root-cause confirmation alone does not release implementation", debug)

        implementation = paths["implementation"].read_text()
        self.assertIn("even when the user asks directly for implementation", implementation)
        self.assertLess(
            implementation.index("preflight size"),
            implementation.index("Use one writer"),
        )
        self.assertIn("reopen readiness", implementation)

        verification = paths["verification"].read_text()
        self.assertIn("static string assertions are not evidence", verification)

    def test_static_trigger_vocabulary_covers_high_risk_boundaries(self) -> None:
        core = CORE_PATH.read_text().lower()
        for trigger in (
            "durable or shared contract",
            "cross-component or cross-system boundary",
            "schema, protocol, version, api, or compatibility",
            "migration or irreversible state",
            "authentication, permissions, security, privacy",
            "rollback, recovery, crash behavior, or failure consistency",
            "material long-term trade-off",
        ):
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, core)
        self.assertIn("local, reversible choices", core)
        self.assertIn("reclassify to m or l before editing", core)

    def test_role_prompts_preserve_author_review_writer_authority(self) -> None:
        pm = (ROOT / ".codex/agents/vibe-pm.toml").read_text()
        tech_lead = (ROOT / ".codex/agents/vibe-tech-lead.toml").read_text()
        rd = (ROOT / ".codex/agents/vibe-rd.toml").read_text()
        qa = (ROOT / ".codex/agents/vibe-qa.toml").read_text()

        self.assertIn('sandbox_mode = "read-only"', tech_lead)
        self.assertIn("Perform exactly the assigned mode: author or reviewer", tech_lead)
        self.assertIn("review the exact persisted decision evidence", tech_lead)
        self.assertIn("Do not author substantive replacements", tech_lead)
        self.assertIn("without choosing", pm.lower())
        self.assertIn("architecture, trade-offs, migration, recovery", pm)
        self.assertIn("gate is `implementation-ready`", rd)
        self.assertIn("stop before editing application/shared code", rd)
        self.assertIn("do not retroactively manufacture decision evidence", qa.lower())
        self.assertIn("or treat QA as the gate", qa)

    def test_native_and_sequential_host_evidence_are_not_conflated(self) -> None:
        core = CORE_PATH.read_text()
        specialist = " ".join(section(core, "Specialist execution").split())
        self.assertIn("different read-only Tech Lead instance", specialist)
        self.assertIn("Review mode: sequential-perspective", specialist)
        self.assertIn(
            "Capability limitation: identity-isolated independent reviewer unavailable",
            specialist,
        )
        self.assertIn("must not be described as", specialist)
        self.assertIn("`independent-agent` review", specialist)

    def test_distribution_docs_disclose_static_behavior_limit(self) -> None:
        readme = (ROOT / "README.md").read_text()
        chinese_readme = (ROOT / "README.zh-CN.md").read_text()
        self.assertIn(
            "Documentation string tests cannot replace this kind of behavioral evidence",
            readme,
        )
        self.assertIn(
            "does not currently parse work-item readiness or mechanically prevent file writes",
            readme,
        )
        self.assertIn("文档字符串测试不能替代这类行为证据", chinese_readme)
        self.assertIn(
            "当前不会解析 work-item 状态或机械阻止文件写入",
            chinese_readme,
        )


if __name__ == "__main__":
    unittest.main()
