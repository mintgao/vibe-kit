import re
import json
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest

from tests.fake_takeover_host import FakeTakeoverHost


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
    """Managed-contract and controlled-host tests; never live-host certification."""

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

    def test_post_upgrade_takeover_contract_is_closed_and_manual_fallback_only(self) -> None:
        contract = json.loads((ROOT / "agent-install.json").read_text())
        self.assertEqual(contract["schema_version"], 3)
        self.assertEqual(contract["protocol_version"], 3)
        self.assertEqual(contract["kit_version"], "0.7.0")
        self.assertEqual(
            contract["lifecycle"]["stages"],
            [
                "source-resolved",
                "planned",
                "applied",
                "upgraded",
                "activated",
                "adapted",
                "verified",
                "re-evaluated",
                "ready",
            ],
        )
        capabilities = contract["adapter"]["capabilities"]
        self.assertFalse(capabilities["same_task_reload"]["current_claim"])
        self.assertFalse(
            capabilities["automatic_successor_handoff"]["current_claim"]
        )
        self.assertEqual(capabilities["manual_new_task"]["status"], "supported")
        self.assertEqual(
            contract["activation"]["current_repository_capability"],
            "manual-fallback-only",
        )
        self.assertEqual(
            contract["takeover"]["unknown_or_inconsistent_state"], "fail-closed"
        )
        registry = contract["takeover"]["contract_registry"]
        independent_digest = hashlib.sha256(
            json.dumps(
                registry,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()
        self.assertEqual(
            independent_digest,
            contract["takeover"]["contract_registry_sha256"],
        )
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text())
        self.assertEqual(
            independent_digest,
            protocol["takeover_contract_registry_sha256"],
        )
        predecessor_mirror = contract["maintenance_bridge"]["predecessor_migrations"]
        self.assertEqual(predecessor_mirror["schema_version"], 2)
        self.assertEqual(predecessor_mirror["authority"], "target-cli-compiled")
        self.assertEqual(
            predecessor_mirror["modes"],
            ["create-pending-onboarding-if-absent", "replace-and-adopt-complete-set"],
        )
        self.assertRegex(predecessor_mirror["registry_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            contract["maintenance_bridge"]["predecessor_migrations"],
            predecessor_mirror,
        )
        self.assertEqual(protocol["predecessor_migrations"], predecessor_mirror)
        self.assertEqual(
            contract["privacy"]["takeover_repository_persistence"], False
        )

    def test_v070_lossless_leaf_and_directory_protocol_is_mirrored(self) -> None:
        cli = (ROOT / "bin/vibe").read_text()
        adr = (ROOT / "docs/decisions/0010-recoverable-upgrade-transaction.md").read_text()
        contract = json.loads((ROOT / "agent-install.json").read_text())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text())
        for token in (
            "ctypes.CDLL(None, use_errno=True)",
            "renameatx_np",
            "renameat2",
            "link-no-clobber-v1",
            "exchange-preserve-v1",
            "directory-no-clobber-v1",
            "directory_postimage_set_sha256",
            "directory_stage_set_sha256",
        ):
            self.assertIn(token, cli)
        self.assertIn("Prepared absent-parent directory units", adr)
        self.assertIn("ordinary rename/replace is never a fallback", adr)
        for reason in (
            "upgrade-leaf-atomicity-unsupported",
            "upgrade-leaf-race-preserved",
        ):
            self.assertIn(reason, contract["takeover"]["reason_codes"])
            self.assertEqual(
                contract["takeover"]["contract_registry"]["reason_stage_map"][reason],
                "applied",
            )
        self.assertIn(
            "use-supported-upgrade-filesystem",
            contract["takeover"]["next_action_codes"],
        )
        self.assertEqual(
            contract["takeover"]["contract_registry_sha256"],
            protocol["takeover_contract_registry_sha256"],
        )

    def test_controlled_activation_paths_require_positive_receipts(self) -> None:
        guide = (ROOT / "AGENT_INSTALL.md").read_text()
        plugin = (
            ROOT
            / "distribution/plugin-src/vibe-kit/skills/vibe-maintain/SKILL.md"
        ).read_text()
        normalized_guide = " ".join(guide.split())
        for receipt in ("host-reload", "host-successor-start", "manual-task-start"):
            self.assertIn(receipt, guide)
        self.assertIn("idempotent successor creation", guide)
        self.assertIn("never create a second possible successor", normalized_guide)
        self.assertIn("currently claim only the manual fallback", normalized_guide)
        self.assertIn("supplies neither same-task reload nor automatic successor", plugin)
        self.assertIn("do not say ready", plugin)
        self.assertIn("positive live conformance receipts", normalized_guide)

    def test_activation_gates_adaptation_verification_and_target_rule_routing(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text()
        onboarding = (
            ROOT / ".agents/skills/vibe-project-onboarding/SKILL.md"
        ).read_text()
        implementation = (
            ROOT / ".agents/skills/vibe-implementation-flow/SKILL.md"
        ).read_text()
        for text in (agents, onboarding, implementation):
            self.assertIn("activation", text.lower())
            self.assertIn("target", text.lower())
        self.assertIn("Only the activated task", agents)
        self.assertIn("default `./bin/vibe verify . --format json`", onboarding)
        self.assertIn("Re-evaluate", onboarding)
        self.assertIn("before editing", implementation)
        self.assertIn("apply/doctor receipt as activation evidence", implementation)

    def test_installed_takeover_contracts_are_managed_activation_critical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            installed = subprocess.run(
                [str(ROOT / "bin/vibe"), "init", str(project), "--format", "json"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            manifest = json.loads((project / ".vibe/manifest.json").read_text())
            for relative in ("AGENT_INSTALL.md", "agent-install.json"):
                with self.subTest(relative=relative):
                    self.assertTrue((project / relative).is_file())
                    self.assertIn(relative, manifest["managed_files"])
                    self.assertIn(relative, manifest["activation"]["paths"])
                    self.assertIn(relative, manifest["activation"]["runtime_discovery_roots"])

            (project / "agent-install.json").unlink()
            doctor = subprocess.run(
                [str(project / "bin/vibe"), "doctor", str(project), "--format", "json"],
                text=True, capture_output=True, check=False,
            )
            receipt = json.loads(doctor.stdout)
            self.assertEqual(doctor.returncode, 1)
            self.assertEqual(receipt["status"], "broken")
            codes = {item["code"] for item in receipt["diagnostics"]}
            self.assertIn("managed-file-missing", codes)
            self.assertIn("agent-install-contract-invalid", codes)
            validation = subprocess.run(
                [str(project / "bin/vibe"), "validate-takeover", "--format", "json"],
                input='{"secret":"VALIDATOR_SECRET_SENTINEL"}',
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(validation.returncode, 2)
            self.assertNotIn("VALIDATOR_SECRET_SENTINEL", validation.stdout)
            self.assertEqual(json.loads(validation.stdout)["status"], "error")

    def test_controlled_host_validates_activation_paths_custody_and_privacy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            installed = subprocess.run(
                [str(ROOT / "bin/vibe"), "init", str(project), "--format", "json"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            host = FakeTakeoverHost(project)

            for path in (
                "same-task-reload",
                "automatic-successor-handoff",
                "manual-new-task",
            ):
                with self.subTest(path=path):
                    code, receipt, stderr = host.validate(host.ready(path))
                    self.assertEqual(code, 0, (receipt, stderr))
                    self.assertEqual(receipt["status"], "valid")
                    self.assertFalse(receipt["host_evidence_authenticated"])
                    self.assertFalse(receipt["ready_claim"])

            wrong_task = host.ready("same-task-reload")
            wrong_task["activation"]["active_task_id"] = "wrong-task"
            self.assertEqual(host.validate(wrong_task)[0], 1)
            pre_apply = host.ready()
            pre_apply["stages"]["applied"]["evidence"][0]["sequence"] = 100
            self.assertEqual(host.validate(pre_apply)[0], 1)
            manifest_mismatch = host.ready()
            manifest_mismatch["activation"]["observed_manifest_sha256"] = "3" * 64
            self.assertEqual(host.validate(manifest_mismatch)[0], 1)
            activation_mismatch = host.ready()
            activation_mismatch["activation"]["observed_activation_set_sha256"] = "4" * 64
            self.assertEqual(host.validate(activation_mismatch)[0], 1)

            first = host.create_successor("stable-key")
            second = host.create_successor("stable-key")
            self.assertEqual(first, second)
            self.assertEqual(host.create_attempts, 1)
            self.assertIsNone(host.create_successor("ambiguous-key", ambiguous=True))
            self.assertIsNone(host.lookup_successor("ambiguous-key"))
            self.assertEqual(host.create_attempts, 2)

            replay = host.ready("manual-new-task")
            replay["goal"]["custody_history"].append(
                dict(replay["goal"]["custody_history"][-1])
            )
            self.assertEqual(host.validate(replay)[0], 1)
            wrong_project = host.ready("manual-new-task")
            wrong_project["project_root"] = "/canonical/wrong-project"
            self.assertEqual(host.validate(wrong_project)[0], 1)
            missing_transfer = host.ready("manual-new-task")
            missing_transfer["goal"]["transfer_id"] = None
            self.assertEqual(host.validate(missing_transfer)[0], 1)
            terminal_source = host.ready("automatic-successor-handoff")
            terminal_source["goal"]["custody_history"].append(
                {"state": "source-owned", "task_id": "source-task", "sequence": 99}
            )
            terminal_source["goal"]["custody"] = "source-owned"
            terminal_source["goal"]["owner_task_id"] = "source-task"
            self.assertEqual(host.validate(terminal_source)[0], 1)

            degraded = host.degraded_manual()
            code, receipt, _ = host.validate(degraded)
            self.assertEqual(code, 0, receipt)
            self.assertEqual(receipt["status"], "valid")
            serialized = json.dumps(degraded, sort_keys=True)
            self.assertNotIn(host.synthetic_goal, serialized)
            self.assertNotIn(host.synthetic_goal, json.dumps(receipt, sort_keys=True))
            for path in project.rglob("*"):
                if path.is_file():
                    self.assertNotIn(host.synthetic_goal.encode(), path.read_bytes())

    def test_controlled_host_validates_adaptation_verification_and_routing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            installed = subprocess.run(
                [str(ROOT / "bin/vibe"), "init", str(project), "--format", "json"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            host = FakeTakeoverHost(project)

            for adaptation in ("unchanged-complete", "refreshed"):
                self.assertEqual(host.validate(host.ready(adaptation=adaptation))[0], 0)
            for reason, action in (
                ("onboarding-invalid", "resolve-project-context"),
                ("onboarding-contradicted", "resolve-project-context"),
                ("adaptation-write-incomplete", "inspect-adaptation-changes"),
            ):
                value = host.block(host.ready(), "adapted", reason, action)
                self.assertEqual(host.validate(value)[0], 0, reason)
            for reason in (
                "verification-failed", "verification-skipped", "verification-error"
            ):
                value = host.block(host.ready(), "verified", reason, "fix-configured-check")
                self.assertEqual(host.validate(value)[0], 0, reason)
            for reason, action in (
                ("target-rule-blocker", "resolve-target-rule-blocker"),
                ("material-user-decision", "answer-material-decision"),
            ):
                value = host.block(host.ready(), "re-evaluated", reason, action)
                self.assertEqual(host.validate(value)[0], 0, reason)

            maintenance = host.ready(goal_kind="maintenance-only")
            self.assertEqual(host.validate(maintenance)[0], 0)
            false_ready = host.ready()
            false_ready["overall_status"] = "in-progress"
            self.assertEqual(host.validate(false_ready)[0], 1)
            partial_verification = host.ready()
            partial_verification["stages"]["verified"]["evidence"] = []
            self.assertEqual(host.validate(partial_verification)[0], 1)
            malformed_receipt = host.ready()
            malformed_receipt["stages"]["verified"]["evidence"][0][
                "raw_output"
            ] = host.synthetic_goal
            malformed_result = host.validate(malformed_receipt)
            self.assertEqual(malformed_result[0], 1)
            self.assertNotIn(host.synthetic_goal, json.dumps(malformed_result[1]))
            unknown_enum = host.ready()
            unknown_enum["goal"]["continuation"] = "completed"
            self.assertEqual(host.validate(unknown_enum)[0], 1)
            unknown_field = host.ready()
            unknown_field["goal_text"] = host.synthetic_goal
            unknown_result = host.validate(unknown_field)
            self.assertEqual(unknown_result[0], 1)
            self.assertNotIn(host.synthetic_goal, json.dumps(unknown_result[1]))
            duplicate_owner = host.ready("automatic-successor-handoff")
            duplicate_owner["completion_owner_task_id"] = duplicate_owner["activation"]["source_task_id"]
            self.assertEqual(host.validate(duplicate_owner)[0], 1)

            for index, stage in enumerate(
                ("planned", "applied", "upgraded", "activated", "adapted", "verified")
            ):
                with self.subTest(dependency=stage):
                    dependency = host.ready()
                    predecessor = (
                        "source-resolved" if stage == "planned" else
                        ("planned", "applied", "upgraded", "activated", "adapted")[index - 1]
                    )
                    dependency["stages"][predecessor]["state"] = "not-started"
                    dependency["stages"][predecessor]["evidence"] = []
                    self.assertEqual(host.validate(dependency)[0], 1)


if __name__ == "__main__":
    unittest.main()
