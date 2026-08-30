import contextlib
import ctypes
import errno
import json
import hashlib
import importlib.machinery
import importlib.util
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin/vibe"
KIT_VERSION = (ROOT / ".vibe/core/version").read_text().strip()
KIT_ROOT = f"vibe-kit-{KIT_VERSION}"
KIT_ARCHIVE = f"{KIT_ROOT}.zip"
PLUGIN_ARCHIVE = f"vibe-kit-plugin-{KIT_VERSION}.zip"
DISTRIBUTION_ARCHIVE = f"vibe-kit-distribution-{KIT_VERSION}.zip"


def run_cli(
    cli: Path, *args: str, input_text: str = None, env: dict = None
) -> subprocess.CompletedProcess:
    command_env = os.environ.copy()
    if env:
        command_env.update(env)
    return subprocess.run(
        [sys.executable, str(cli), *args],
        text=True,
        capture_output=True,
        check=False,
        input=input_text,
        env=command_env,
    )


def copy_source(destination: Path) -> Path:
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "manifest.json"),
    )
    return destination / "bin/vibe"


def official_v050_source_fixture(destination: Path) -> Path:
    archive = subprocess.run(
        ["git", "archive", "--format=tar", "v0.5.0"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        bundle.extractall(destination)
    return destination


def load_cli_module():
    loader = importlib.machinery.SourceFileLoader("vibe_cli_test_module", str(CLI))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not create a module spec for bin/vibe")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def file_snapshot(root: Path) -> dict:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def independent_activation_digest(root: Path) -> str:
    contract = json.loads((root / "agent-install.json").read_text())
    protocol = json.loads((root / ".vibe/core/protocol.json").read_text())
    hashes = {}
    for relative in contract["activation"]["activation_paths"]:
        if relative == "AGENTS.md#managed-block":
            text = (root / "AGENTS.md").read_text()
            start = text.index("<!-- vibe-kit:managed:start -->")
            end = text.index("<!-- vibe-kit:managed:end -->", start) + len(
                "<!-- vibe-kit:managed:end -->"
            )
            content = text[start:end].encode()
        elif relative == "agent-install.json":
            normalized = json.loads((root / relative).read_text())
            normalized["activation"]["activation_set_sha256"] = "0" * 64
            content = json.dumps(
                normalized,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        else:
            content = (root / relative).read_bytes()
        hashes[relative] = hashlib.sha256(content).hexdigest()
    fingerprint = {
        "kit_version": contract["kit_version"],
        "core_protocol": protocol["core_protocol"],
        "agent_install_schema": contract["schema_version"],
        "agent_install_protocol": contract["protocol_version"],
        "adapter_name": contract["adapter"]["name"],
        "adapter_protocol": contract["adapter"]["protocol"],
    }
    canonical = json.dumps(
        {"fingerprint": fingerprint, "path_hashes": dict(sorted(hashes.items()))},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(canonical).hexdigest()


def refresh_release_checksums(release_dir: Path, artifact_relative: str) -> None:
    manifest_path = release_dir / "release-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    artifact_path = release_dir / artifact_relative
    for artifact in manifest["artifacts"]:
        if artifact["path"] == artifact_relative:
            artifact["sha256"] = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            artifact["size"] = artifact_path.stat().st_size
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    relative_paths = []
    for line in (release_dir / "SHA256SUMS").read_text().splitlines():
        _, relative = line.split("  ", 1)
        relative_paths.append(relative)
    (release_dir / "SHA256SUMS").write_text(
        "".join(
            f"{hashlib.sha256((release_dir / relative).read_bytes()).hexdigest()}  {relative}\n"
            for relative in sorted(relative_paths)
        )
    )


class VibeCliTests(unittest.TestCase):
    def feedback_signal(
        self, cli: Path, target: Path, command: str, *extra: str
    ) -> subprocess.CompletedProcess:
        return run_cli(
            cli,
            "feedback",
            command,
            "--target",
            str(target),
            "--kind",
            "workflow-gap",
            "--component",
            "doctor",
            "--title",
            "Doctor should explain the recovery path",
            "--summary",
            "Doctor reports a framework state problem without enough recovery context",
            "--expected",
            "Doctor should identify the trusted recovery action",
            "--observed",
            "The operator had to infer the correct action",
            "--impact",
            "Adoption takes longer and can produce unsafe manual edits",
            "--hypothesis",
            "The diagnostic contract lacks a recovery field",
            "--proposal",
            "Add a structured recovery action to the doctor diagnostic",
            "--workflow",
            "vibe-debug-flow",
            "--agent-role",
            "vibe-investigator",
            "--trigger",
            "work-item-close",
            *extra,
        )

    def feedback_draft(self, cli: Path, target: Path, *extra: str) -> subprocess.CompletedProcess:
        return self.feedback_signal(cli, target, "draft", *extra)

    def feedback_close(self, cli: Path, target: Path, *extra: str) -> subprocess.CompletedProcess:
        return self.feedback_signal(cli, target, "close", *extra)

    def test_init_doctor_and_work_item(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "new-project"
            result = run_cli(CLI, "init", str(target), "--name", "Demo Project")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / ".agents/skills/vibe-feature-flow/SKILL.md").is_file())
            self.assertTrue((target / ".codex/agents/vibe-qa.toml").is_file())
            self.assertTrue(
                (target / ".vibe/core/technical-decision-readiness.md").is_file()
            )
            self.assertTrue((target / ".codex/agents/vibe-tech-lead.toml").is_file())
            self.assertIn('lifecycle: "new"', (target / ".vibe/project.yaml").read_text())
            self.assertIn('name: "Demo Project"', (target / ".vibe/project.yaml").read_text())
            onboarding = json.loads((target / ".vibe/onboarding.json").read_text())
            self.assertEqual(onboarding, {"schema_version": 1, "status": "pending"})

            doctor = run_cli(CLI, "doctor", str(target))
            self.assertEqual(doctor.returncode, 0, doctor.stderr)

            item = run_cli(
                target / "bin/vibe",
                "work-item",
                "settings-page",
                "--target",
                str(target),
                "--size",
                "M",
                "--title",
                "Settings Page",
            )
            self.assertEqual(item.returncode, 0, item.stderr)
            folders = list((target / "docs/work-items").glob("*-settings-page"))
            self.assertEqual(len(folders), 1)
            brief = (folders[0] / "brief.md").read_text()
            self.assertIn("AC-1", brief)
            self.assertIn("## Technical decision readiness", brief)
            self.assertIn("- Outcome: `not-assessed`", brief)
            self.assertIn("- Gate: `blocked`", brief)
            self.assertIn("- Confirmed at: none", brief)
            self.assertTrue((folders[0] / "verification.md").is_file())

    def test_plan_is_read_only_for_init_adopt_upgrade_and_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            missing = base / "missing-project"
            init_plan = run_cli(CLI, "plan", "init", str(missing))
            self.assertEqual(init_plan.returncode, 0, init_plan.stderr)
            self.assertIn("Status: safe", init_plan.stdout)
            self.assertIn("No files were changed", init_plan.stdout)
            self.assertFalse(missing.exists())

            existing = base / "existing-project"
            existing.mkdir()
            business = existing / "app.py"
            business.write_text("print('business')\n")
            before_adopt = file_snapshot(existing)
            adopt_plan = run_cli(CLI, "plan", "adopt", str(existing))
            self.assertEqual(adopt_plan.returncode, 0, adopt_plan.stderr)
            self.assertEqual(file_snapshot(existing), before_adopt)
            adopted = run_cli(CLI, "adopt", str(existing))
            self.assertEqual(adopted.returncode, 0, adopted.stderr)
            self.assertEqual(business.read_text(), "print('business')\n")

            source_old = base / "source-old"
            source_new = base / "source-new"
            old_cli = copy_source(source_old)
            new_cli = copy_source(source_new)
            (source_old / ".vibe/core/version").write_text("0.2.0\n")
            upgrade_target = base / "upgrade-project"
            installed = run_cli(old_cli, "init", str(upgrade_target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            before_upgrade_plan = file_snapshot(upgrade_target)
            upgrade_plan = run_cli(new_cli, "plan", "upgrade", str(upgrade_target))
            self.assertEqual(upgrade_plan.returncode, 0, upgrade_plan.stderr)
            self.assertIn("Current version: 0.2.0", upgrade_plan.stdout)
            self.assertIn(f"Target version: {KIT_VERSION}", upgrade_plan.stdout)
            self.assertEqual(file_snapshot(upgrade_target), before_upgrade_plan)

            target_quality = upgrade_target / ".vibe/core/quality-gates.md"
            target_quality.write_text(target_quality.read_text() + "\nLocal edit.\n")
            source_quality = source_new / ".vibe/core/quality-gates.md"
            source_quality.write_text(source_quality.read_text() + "\nIncoming edit.\n")
            before_conflict_plan = file_snapshot(upgrade_target)
            conflict_plan = run_cli(new_cli, "plan", "upgrade", str(upgrade_target))
            self.assertEqual(conflict_plan.returncode, 2)
            self.assertIn("Status: blocked", conflict_plan.stdout)
            self.assertIn("CONFLICT", conflict_plan.stdout)
            self.assertEqual(file_snapshot(upgrade_target), before_conflict_plan)

    def test_agent_json_results_provenance_and_onboarding_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "agent-project"
            digest = "a" * 64
            provenance = (
                "--source-type",
                "github-release",
                "--source-ref",
                f"v{KIT_VERSION}",
                "--artifact-sha256",
                digest,
            )

            planned = run_cli(
                CLI, "plan", "init", str(target), "--format", "json", *provenance
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)
            plan_receipt = json.loads(planned.stdout)
            self.assertEqual(plan_receipt["schema_version"], 2)
            self.assertEqual(plan_receipt["status"], "safe")
            self.assertFalse(plan_receipt["files_changed"])
            self.assertEqual(plan_receipt["source"]["artifact_sha256"], digest)
            self.assertFalse(target.exists())

            installed = run_cli(
                CLI, "init", str(target), "--format", "json", *provenance
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            install_receipt = json.loads(installed.stdout)
            self.assertEqual(install_receipt["status"], "success")
            self.assertEqual(install_receipt["write_state"], "project-files-written")
            self.assertTrue(install_receipt["writes_performed"])
            self.assertEqual(install_receipt["onboarding"]["status"], "pending")
            self.assertEqual(install_receipt["onboarding"]["kind"], "persisted")
            self.assertRegex(
                install_receipt["source"]["payload_tree_sha256"], r"^[0-9a-f]{64}$"
            )
            self.assertEqual(install_receipt["activation"]["state"], "not-proven")
            self.assertFalse(
                install_receipt["activation"]["same_task_reload_claimed"]
            )
            self.assertFalse(
                install_receipt["activation"]["automatic_successor_handoff_claimed"]
            )
            self.assertNotIn("ready", install_receipt)
            manifest = json.loads((target / ".vibe/manifest.json").read_text())
            self.assertEqual(manifest["source"], install_receipt["source"])
            self.assertEqual(manifest["source"]["ref"], f"v{KIT_VERSION}")

            healthy = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(healthy.returncode, 0, healthy.stderr)
            healthy_result = json.loads(healthy.stdout)
            self.assertEqual(healthy_result["status"], "healthy")
            self.assertEqual(healthy_result["onboarding"]["status"], "pending")

            quality = target / ".vibe/core/quality-gates.md"
            quality.write_text(quality.read_text() + "\nLocal note.\n")
            warning = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(warning.returncode, 0, warning.stderr)
            self.assertEqual(json.loads(warning.stdout)["status"], "warning")

            (target / ".vibe/onboarding.json").write_text(
                '{"schema_version": 1, "status": "refresh-needed"}\n'
            )
            refresh_needed = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(refresh_needed.returncode, 0, refresh_needed.stderr)
            self.assertEqual(
                json.loads(refresh_needed.stdout)["onboarding"]["status"],
                "refresh-needed",
            )

            (target / ".vibe/onboarding.json").write_text("not-json\n")
            broken = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(broken.returncode, 1, broken.stderr)
            broken_result = json.loads(broken.stdout)
            self.assertEqual(broken_result["status"], "broken")
            self.assertEqual(broken_result["onboarding"]["status"], "invalid")

            incomplete_complete_states = (
                {"schema_version": 1, "status": "complete"},
                {
                    "schema_version": 1,
                    "status": "complete",
                    "updated_at": "not-a-date",
                    "evidence": ["docs/context/product.md"],
                },
                {
                    "schema_version": 1,
                    "status": "complete",
                    "updated_at": "2026-08-27T15:24:03Z",
                    "evidence": [""],
                },
            )
            for incomplete in incomplete_complete_states:
                with self.subTest(incomplete_complete=incomplete):
                    (target / ".vibe/onboarding.json").write_text(
                        json.dumps(incomplete) + "\n"
                    )
                    incomplete_result = run_cli(
                        target / "bin/vibe", "doctor", str(target), "--format", "json"
                    )
                    self.assertEqual(incomplete_result.returncode, 1)
                    incomplete_receipt = json.loads(incomplete_result.stdout)
                    self.assertEqual(incomplete_receipt["status"], "broken")
                    self.assertEqual(
                        incomplete_receipt["onboarding"]["status"], "invalid"
                    )

            invalid_target = base / "invalid-source-project"
            rejected = run_cli(
                CLI,
                "init",
                str(invalid_target),
                "--format",
                "json",
                "--source-type",
                "github-release",
                "--source-ref",
                f"v{KIT_VERSION}",
                "--artifact-sha256",
                "bad-digest",
            )
            self.assertEqual(rejected.returncode, 2)
            rejected_result = json.loads(rejected.stdout)
            self.assertEqual(rejected_result["status"], "error")
            self.assertEqual(
                rejected_result["error"]["code"], "invalid_artifact_sha256"
            )
            self.assertEqual(rejected_result["write_state"], "none")
            self.assertFalse(rejected_result["writes_performed"])
            self.assertFalse(invalid_target.exists())

            adopt_target = base / "existing"
            adopt_target.mkdir()
            (adopt_target / "business.txt").write_text("keep\n")
            adopted = run_cli(
                CLI, "adopt", str(adopt_target), "--format", "json"
            )
            self.assertEqual(adopted.returncode, 0, adopted.stderr)
            self.assertEqual(json.loads(adopted.stdout)["status"], "success")
            self.assertEqual(
                json.loads((adopt_target / ".vibe/manifest.json").read_text())["source"]["type"],
                "local-payload",
            )

            collision = base / "collision"
            conflict = collision / ".codex/agents/vibe-pm.toml"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("custom = true\n")
            blocked = run_cli(
                CLI, "plan", "adopt", str(collision), "--format", "json"
            )
            self.assertEqual(blocked.returncode, 2)
            blocked_result = json.loads(blocked.stdout)
            self.assertEqual(blocked_result["status"], "blocked")
            self.assertIn(".codex/agents/vibe-pm.toml", blocked_result["recovery"]["paths"])

    def test_upgrade_installs_pre_protocol_takeover_contracts_and_preflights_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            old_source = base / "old-source"
            old_cli = copy_source(old_source)
            (old_source / ".vibe/core/version").write_text("0.5.0\n")
            target = base / "old-project"
            installed = run_cli(old_cli, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)

            manifest_path = target / ".vibe/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            for relative in ("AGENT_INSTALL.md", "agent-install.json"):
                (target / relative).unlink()
                manifest["managed_files"].pop(relative, None)
                manifest["activation"]["path_hashes"].pop(relative, None)
                manifest["activation"]["paths"].remove(relative)
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

            before = file_snapshot(target)
            plan = run_cli(CLI, "plan", "upgrade", str(target), "--format", "json")
            self.assertEqual(plan.returncode, 0, plan.stderr)
            self.assertEqual(file_snapshot(target), before)
            entries = {item["path"]: item["action"] for item in json.loads(plan.stdout)["entries"]}
            self.assertEqual(entries["AGENT_INSTALL.md"], "create")
            self.assertEqual(entries["agent-install.json"], "create")

            upgraded = run_cli(CLI, "upgrade", str(target), "--format", "json")
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            upgraded_manifest = json.loads(manifest_path.read_text())
            for relative in ("AGENT_INSTALL.md", "agent-install.json"):
                self.assertTrue((target / relative).is_file())
                self.assertIn(relative, upgraded_manifest["managed_files"])
                self.assertIn(relative, upgraded_manifest["activation"]["paths"])
            doctor = run_cli(target / "bin/vibe", "doctor", str(target), "--format", "json")
            self.assertEqual(doctor.returncode, 0, doctor.stdout)

            collision = base / "collision"
            collision.mkdir()
            (collision / "agent-install.json").write_text('{"project": "owned"}\n')
            collision_plan = run_cli(
                CLI, "plan", "adopt", str(collision), "--format", "json"
            )
            self.assertEqual(collision_plan.returncode, 2)
            self.assertIn(
                "agent-install.json",
                json.loads(collision_plan.stdout)["recovery"]["paths"],
            )

    def test_official_v050_complete_contract_set_migrates_and_is_adopted(self) -> None:
        expected_paths = ["AGENT_INSTALL.md", "agent-install.json"]
        with tempfile.TemporaryDirectory() as temporary:
            project = official_v050_source_fixture(Path(temporary) / "project")
            (project / "business-untracked.txt").write_text("preserve me\n")
            before = file_snapshot(project)
            preserved_before = {
                relative: content
                for relative, content in before.items()
                if relative == "business-untracked.txt"
                or relative.startswith("docs/")
                or relative
                in {
                    ".vibe/project.yaml",
                    ".vibe/project-rules.md",
                    ".vibe/onboarding.json",
                }
            }

            planned = run_cli(
                CLI,
                "plan",
                "upgrade",
                str(project),
                "--format",
                "json",
                "--source-type",
                "local-payload",
                "--source-ref",
                KIT_VERSION,
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)
            self.assertEqual(file_snapshot(project), before)
            plan_receipt = json.loads(planned.stdout)
            self.assertEqual(plan_receipt["schema_version"], 2)
            self.assertEqual(plan_receipt["status"], "safe")
            migration_entries = {
                item["path"]: item
                for item in plan_receipt["entries"]
                if item["path"] in expected_paths
            }
            self.assertEqual(set(migration_entries), set(expected_paths))
            for relative in expected_paths:
                self.assertEqual(migration_entries[relative]["action"], "update")
                self.assertEqual(
                    migration_entries[relative]["note"],
                    "authenticated predecessor migration "
                    "v0.5.0-unmanaged-agent-contracts-v1; complete set",
                )
            migration = plan_receipt["compatibility_migrations"]
            self.assertEqual(len(migration), 1)
            self.assertEqual(migration[0]["phase"], "planned")
            self.assertEqual(migration[0]["paths"], expected_paths)
            self.assertEqual(
                migration[0]["registry_sha256"],
                json.loads((ROOT / ".vibe/core/protocol.json").read_text())[
                    "predecessor_migrations"
                ]["registry_sha256"],
            )

            upgraded = run_cli(
                CLI,
                "upgrade",
                str(project),
                "--format",
                "json",
                "--source-type",
                "local-payload",
                "--source-ref",
                KIT_VERSION,
            )
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            receipt = json.loads(upgraded.stdout)
            self.assertEqual(receipt["schema_version"], 2)
            self.assertEqual(receipt["status"], "success")
            self.assertEqual(receipt["write_state"], "project-files-written")
            self.assertEqual(receipt["compatibility_migrations"][0]["phase"], "applied")
            self.assertEqual(receipt["activation"]["state"], "not-proven")
            self.assertTrue(receipt["activation"]["manual_new_task_supported"])
            self.assertFalse(receipt["activation"]["same_task_reload_claimed"])
            self.assertFalse(
                receipt["activation"]["automatic_successor_handoff_claimed"]
            )

            after = file_snapshot(project)
            preserved_after = {
                relative: content
                for relative, content in after.items()
                if relative in preserved_before
            }
            self.assertEqual(preserved_after, preserved_before)
            manifest = json.loads((project / ".vibe/manifest.json").read_text())
            contract = json.loads((ROOT / "agent-install.json").read_text())
            for relative in expected_paths:
                self.assertEqual(
                    manifest["managed_files"][relative],
                    hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(),
                )
                self.assertIn(relative, manifest["activation"]["paths"])
            self.assertEqual(
                manifest["activation"]["activation_set_sha256"],
                contract["activation"]["activation_set_sha256"],
            )
            self.assertNotIn("compatibility_migrations", manifest)
            doctor = run_cli(
                project / "bin/vibe", "doctor", str(project), "--format", "json"
            )
            self.assertEqual(doctor.returncode, 0, doctor.stdout)
            self.assertEqual(json.loads(doctor.stdout)["status"], "healthy")

    def test_predecessor_source_is_excluded_and_target_channels_have_parity(self) -> None:
        source_values = (
            "absent",
            None,
            ["arbitrary", {"nested": True}],
            {"type": "github-release", "ref": "official-looking", "extra": 7},
        )
        channel_arguments = (
            ("local-payload", ("--source-ref", KIT_VERSION)),
            (
                "github-release",
                ("--source-ref", f"v{KIT_VERSION}", "--artifact-sha256", "a" * 64),
            ),
            (
                "offline-bundle",
                ("--source-ref", f"v{KIT_VERSION}", "--artifact-sha256", "b" * 64),
            ),
            ("plugin-bundled", ("--source-ref", f"v{KIT_VERSION}")),
        )
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for index, source_value in enumerate(source_values):
                with self.subTest(source=source_value):
                    project = official_v050_source_fixture(base / f"source-{index}")
                    manifest_path = project / ".vibe/manifest.json"
                    manifest = json.loads(manifest_path.read_text())
                    if source_value == "absent":
                        manifest.pop("source", None)
                    else:
                        manifest["source"] = source_value
                    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
                    decisions = []
                    for source_type, extra in channel_arguments:
                        result = run_cli(
                            CLI,
                            "plan",
                            "upgrade",
                            str(project),
                            "--format",
                            "json",
                            "--source-type",
                            source_type,
                            *extra,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        receipt = json.loads(result.stdout)
                        decisions.append(
                            (
                                receipt["status"],
                                [
                                    (item["path"], item["action"])
                                    for item in receipt["entries"]
                                    if item["path"]
                                    in {"AGENT_INSTALL.md", "agent-install.json"}
                                ],
                                receipt["compatibility_migrations"],
                            )
                        )
                    self.assertTrue(all(value == decisions[0] for value in decisions))
            for index, (source_type, extra) in enumerate(channel_arguments):
                with self.subTest(apply_channel=source_type):
                    project = official_v050_source_fixture(base / f"apply-{index}")
                    result = run_cli(
                        CLI,
                        "upgrade",
                        str(project),
                        "--format",
                        "json",
                        "--source-type",
                        source_type,
                        *extra,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    receipt = json.loads(result.stdout)
                    self.assertEqual(receipt["status"], "success")
                    self.assertEqual(
                        receipt["compatibility_migrations"][0]["phase"], "applied"
                    )

    def test_predecessor_contract_set_and_installation_fail_closed(self) -> None:
        migration_paths = {"AGENT_INSTALL.md", "agent-install.json"}

        def assert_paired_conflict(project: Path) -> None:
            before = file_snapshot(project)
            result = run_cli(
                CLI, "plan", "upgrade", str(project), "--format", "json"
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(file_snapshot(project), before)
            receipt = json.loads(result.stdout)
            entries = {
                item["path"]: item["action"] for item in receipt.get("entries", [])
            }
            self.assertTrue(migration_paths <= set(entries), receipt)
            self.assertEqual(
                {entries[path] for path in migration_paths}, {"conflict"}, receipt
            )
            self.assertTrue(
                migration_paths <= set(receipt["recovery"]["paths"]), receipt
            )

        mutations = {
            "missing-guide": lambda root: (root / "AGENT_INSTALL.md").unlink(),
            "modified-guide": lambda root: (root / "AGENT_INSTALL.md").write_text(
                "modified\n"
            ),
            "directory-guide": lambda root: (
                (root / "AGENT_INSTALL.md").unlink(),
                (root / "AGENT_INSTALL.md").mkdir(),
            ),
            "symlink-guide": lambda root: (
                (root / "AGENT_INSTALL.md").unlink(),
                (root / "AGENT_INSTALL.md").symlink_to("agent-install.json"),
            ),
            "broken-guide": lambda root: (
                (root / "AGENT_INSTALL.md").unlink(),
                (root / "AGENT_INSTALL.md").symlink_to("missing-guide"),
            ),
            "missing-agent-json": lambda root: (root / "agent-install.json").unlink(),
            "modified-agent-json": lambda root: (root / "agent-install.json").write_text(
                "{}\n"
            ),
            "directory-agent-json": lambda root: (
                (root / "agent-install.json").unlink(),
                (root / "agent-install.json").mkdir(),
            ),
            "symlink-agent-json": lambda root: (
                (root / "agent-install.json").unlink(),
                (root / "agent-install.json").symlink_to("AGENT_INSTALL.md"),
            ),
            "broken-agent-json": lambda root: (
                (root / "agent-install.json").unlink(),
                (root / "agent-install.json").symlink_to("missing-agent-json"),
            ),
            "mixed-target-agent-json": lambda root: (root / "agent-install.json").write_bytes(
                (ROOT / "agent-install.json").read_bytes()
            ),
            "wrong-version": lambda root: (root / ".vibe/version").write_text("0.4.0\n"),
            "managed-file-modified": lambda root: (
                root / ".vibe/core/quality-gates.md"
            ).write_text("modified\n"),
            "agents-missing": lambda root: (root / "AGENTS.md").unlink(),
            "agents-modified": lambda root: (root / "AGENTS.md").write_text(
                (root / "AGENTS.md").read_text().replace(
                    "<!-- vibe-kit:managed:start -->",
                    "<!-- vibe-kit:managed:start -->\nChanged managed bytes.",
                    1,
                )
            ),
            "agents-directory": lambda root: (
                (root / "AGENTS.md").unlink(),
                (root / "AGENTS.md").mkdir(),
            ),
            "agents-symlink": lambda root: (
                (root / "AGENTS.md").rename(root / "AGENTS.real.md"),
                (root / "AGENTS.md").symlink_to("AGENTS.real.md"),
            ),
            "agents-broken-symlink": lambda root: (
                (root / "AGENTS.md").unlink(),
                (root / "AGENTS.md").symlink_to("missing-agents"),
            ),
            "malformed-manifest": lambda root: (
                root / ".vibe/manifest.json"
            ).write_text("{not-json\n"),
            "duplicate-key-manifest": lambda root: (
                root / ".vibe/manifest.json"
            ).write_text(
                (root / ".vibe/manifest.json")
                .read_text()
                .replace("{", '{"schema_version": 1,', 1)
            ),
            "altered-install-identity": lambda root: self._set_manifest_field(
                root, "agents_block_hash", "0" * 64
            ),
            "official-looking-source-wrong-version": lambda root: (
                (root / ".vibe/version").write_text("0.4.0\n"),
                self._set_manifest_field(
                    root,
                    "source",
                    {"type": "github-release", "ref": "v0.5.0"},
                ),
            ),
        }
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for name, mutate in mutations.items():
                with self.subTest(mutation=name):
                    project = official_v050_source_fixture(base / name)
                    mutate(project)
                    assert_paired_conflict(project)

    def test_predecessor_intermediate_symlinks_and_apply_races_fail_closed(self) -> None:
        migration_paths = {"AGENT_INSTALL.md", "agent-install.json"}
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for relative in (".vibe", ".vibe/core", ".agents", ".agents/skills", ".codex"):
                with self.subTest(intermediate=relative):
                    project = official_v050_source_fixture(
                        base / ("link-" + relative.replace("/", "-").lstrip("."))
                    )
                    original = project / relative
                    moved = original.with_name(original.name + "-real")
                    original.rename(moved)
                    original.symlink_to(moved.name, target_is_directory=True)
                    result = run_cli(
                        CLI, "plan", "upgrade", str(project), "--format", "json"
                    )
                    self.assertEqual(result.returncode, 2, result.stderr)
                    receipt = json.loads(result.stdout)
                    if relative == ".vibe":
                        self.assertEqual(
                            receipt["next_action"]["code"],
                            "inspect-upgrade-transaction",
                        )
                        self.assertEqual(
                            receipt["recovery"]["paths"],
                            [".vibe/local/upgrade-transactions/active"],
                        )
                    else:
                        self.assertTrue(
                            migration_paths <= set(receipt["recovery"]["paths"]),
                            receipt,
                        )

            module = load_cli_module()
            pre_race = official_v050_source_fixture(base / "pre-race")
            stdout = io.StringIO()
            with mock.patch.object(
                module,
                "predecessor_migration_decision",
                side_effect=("eligible", "conflict"),
            ), contextlib.redirect_stdout(stdout):
                code = module.upgrade(
                    pre_race, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            pre_receipt = json.loads(stdout.getvalue())
            self.assertEqual(pre_receipt["write_state"], "conflict-evidence-written")
            self.assertEqual(pre_receipt["compatibility_migrations"], [])
            self.assertTrue(migration_paths <= set(pre_receipt["conflicts"]))

            post_race = official_v050_source_fixture(base / "post-race")
            original_write = module.mutate_leaf_forward

            def mutate_second_member(
                project, adapter, item, temporary
            ) -> None:
                original_write(project, adapter, item, temporary)
                if item["path"] == "AGENT_INSTALL.md":
                    (post_race / "agent-install.json").write_text("race\n")

            stdout = io.StringIO()
            with mock.patch.object(
                module, "mutate_leaf_forward", new=mutate_second_member
            ), contextlib.redirect_stdout(stdout):
                code = module.upgrade(
                    post_race, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            post_receipt = json.loads(stdout.getvalue())
            self.assertEqual(post_receipt["write_state"], "unknown-partial")
            self.assertEqual(post_receipt["compatibility_migrations"], [])
            self.assertEqual(post_receipt["transaction"]["outcome"], "unknown-partial")

    def test_adopt_receipt_reports_preserved_complete_onboarding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "existing"
            target.mkdir()
            (target / "business.txt").write_text("keep\n")
            onboarding = {
                "schema_version": 1,
                "status": "complete",
                "updated_at": "2026-08-27T15:24:03Z",
                "evidence": [
                    ".vibe/project.yaml",
                    "docs/context/product.md",
                ],
            }
            original = json.dumps(onboarding, indent=2).encode() + b"\n"
            (target / ".vibe").mkdir()
            (target / ".vibe/onboarding.json").write_bytes(original)

            adopted = run_cli(CLI, "adopt", str(target), "--format", "json")

            self.assertEqual(adopted.returncode, 0, adopted.stderr)
            receipt = json.loads(adopted.stdout)
            self.assertEqual(receipt["onboarding"], {"kind": "persisted", "status": "complete"})
            self.assertEqual((target / ".vibe/onboarding.json").read_bytes(), original)
            doctor = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            self.assertEqual(
                json.loads(doctor.stdout)["onboarding"],
                {"kind": "persisted", "status": "complete"},
            )

    def test_structured_mutation_failure_reports_unknown_partial(self) -> None:
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "partial-project"
            original_atomic_copy = module.atomic_copy
            calls = 0

            def fail_after_first_copy(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise PermissionError("simulated post-mutation denial")
                original_atomic_copy(source, destination)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(
                module, "atomic_copy", side_effect=fail_after_first_copy
            ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = module.main(["init", str(target), "--format", "json"])

            self.assertEqual(result, 2)
            self.assertEqual(stderr.getvalue(), "")
            receipt = json.loads(stdout.getvalue())
            self.assertEqual(receipt["status"], "error")
            self.assertEqual(receipt["error"]["code"], "filesystem_error")
            self.assertEqual(receipt["write_state"], "unknown-partial")
            self.assertTrue(receipt["writes_performed"])
            self.assertEqual(receipt["recovery"]["action"], "inspect-before-retry")
            self.assertTrue(target.exists())

    def test_release_package_is_reproducible_installable_and_tamper_evident(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            first = base / "release-one"
            second = base / "release-two"
            built_first = run_cli(CLI, "package", "--output", str(first))
            self.assertEqual(built_first.returncode, 0, built_first.stderr)
            built_second = run_cli(CLI, "package", "--output", str(second))
            self.assertEqual(built_second.returncode, 0, built_second.stderr)

            for filename in (KIT_ARCHIVE, PLUGIN_ARCHIVE, DISTRIBUTION_ARCHIVE):
                self.assertEqual(
                    hashlib.sha256((first / filename).read_bytes()).hexdigest(),
                    hashlib.sha256((second / filename).read_bytes()).hexdigest(),
                )
            validated = run_cli(CLI, "validate-release", str(first))
            self.assertEqual(validated.returncode, 0, validated.stderr)
            self.assertIn("Network: not used", validated.stdout)
            validated_json = run_cli(
                CLI, "validate-release", str(first), "--format", "json"
            )
            self.assertEqual(validated_json.returncode, 0, validated_json.stderr)
            validation_receipt = json.loads(validated_json.stdout)
            self.assertEqual(validation_receipt["status"], "valid")
            self.assertEqual(validation_receipt["agent_install_protocol"], 3)
            release_metadata = json.loads((first / "release-manifest.json").read_text())
            self.assertEqual(release_metadata["core_protocol"], 5)
            self.assertEqual(release_metadata["feedback_protocol"], 2)
            self.assertEqual(release_metadata["agent_install_schema"], 3)
            self.assertEqual(release_metadata["agent_install_protocol"], 3)
            self.assertEqual(release_metadata["takeover_schema"], 2)
            self.assertEqual(release_metadata["maintenance_bridge_schema"], 2)
            self.assertEqual(
                release_metadata["predecessor_migrations"],
                json.loads((ROOT / ".vibe/core/protocol.json").read_text())[
                    "predecessor_migrations"
                ],
            )
            self.assertEqual(
                release_metadata["takeover_contract_registry_sha256"],
                json.loads((ROOT / ".vibe/core/protocol.json").read_text())[
                    "takeover_contract_registry_sha256"
                ],
            )
            self.assertRegex(release_metadata["payload_tree_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(release_metadata["activation_set_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(release_metadata["adapters"]["codex"]["version"], 5)

            release_unpack = base / "release-unpacked"
            with zipfile.ZipFile(first / KIT_ARCHIVE) as archive:
                archive.extractall(release_unpack)
            release_root = release_unpack / KIT_ROOT
            self.assertIn("MIT License", (release_root / "LICENSE").read_text())
            self.assertTrue((release_root / "AGENT_INSTALL.md").is_file())
            self.assertTrue(
                (release_root / ".vibe/core/technical-decision-readiness.md").is_file()
            )
            self.assertTrue(
                (release_root / ".codex/agents/vibe-tech-lead.toml").is_file()
            )
            install_contract = json.loads((release_root / "agent-install.json").read_text())
            self.assertEqual(install_contract["schema_version"], 3)
            self.assertEqual(install_contract["protocol_version"], 3)
            self.assertEqual(install_contract["kit_version"], KIT_VERSION)
            self.assertEqual(
                install_contract["activation"]["current_repository_capability"],
                "manual-fallback-only",
            )
            self.assertEqual(
                install_contract["activation"]["activation_set_sha256"],
                release_metadata["activation_set_sha256"],
            )
            self.assertEqual(
                independent_activation_digest(release_root),
                release_metadata["activation_set_sha256"],
            )
            self.assertEqual(
                install_contract["takeover"]["contract_registry_sha256"],
                release_metadata["takeover_contract_registry_sha256"],
            )
            feedback_config = json.loads(
                (release_root / ".vibe/core/feedback.json").read_text()
            )
            self.assertEqual(feedback_config["github_repository"], "mintgao/vibe-kit")
            release_cli = release_root / "bin/vibe"
            new_target = base / "new-from-release"
            installed = run_cli(release_cli, "init", str(new_target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            doctor = run_cli(new_target / "bin/vibe", "doctor", str(new_target))
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            release_manifest = json.loads((new_target / ".vibe/manifest.json").read_text())
            self.assertIn(
                ".vibe/core/technical-decision-readiness.md",
                release_manifest["managed_files"],
            )
            self.assertIn(
                ".codex/agents/vibe-tech-lead.toml",
                release_manifest["managed_files"],
            )
            self.assertIn("AGENT_INSTALL.md", release_manifest["managed_files"])
            self.assertIn("agent-install.json", release_manifest["managed_files"])

            existing_target = base / "existing-from-release"
            existing_target.mkdir()
            existing_file = existing_target / "business.txt"
            existing_file.write_text("preserve me\n")
            before_plan = file_snapshot(existing_target)
            planned = run_cli(release_cli, "plan", "adopt", str(existing_target))
            self.assertEqual(planned.returncode, 0, planned.stderr)
            self.assertEqual(file_snapshot(existing_target), before_plan)
            adopted = run_cli(release_cli, "adopt", str(existing_target))
            self.assertEqual(adopted.returncode, 0, adopted.stderr)
            self.assertEqual(existing_file.read_text(), "preserve me\n")

            plugin_unpack = base / "plugin-unpacked"
            with zipfile.ZipFile(first / PLUGIN_ARCHIVE) as archive:
                archive.extractall(plugin_unpack)
            wrapper = plugin_unpack / "vibe-kit/skills/vibe-bootstrap/scripts/vibe_from_plugin.py"
            self.assertEqual(
                (plugin_unpack / "vibe-kit/payload/AGENT_INSTALL.md").read_bytes(),
                (release_root / "AGENT_INSTALL.md").read_bytes(),
            )
            self.assertEqual(
                (plugin_unpack / "vibe-kit/payload/agent-install.json").read_bytes(),
                (release_root / "agent-install.json").read_bytes(),
            )
            self.assertEqual(
                (first / "marketplace/plugins/vibe-kit/payload/AGENT_INSTALL.md").read_bytes(),
                (release_root / "AGENT_INSTALL.md").read_bytes(),
            )
            plugin_target = base / "new-from-plugin"
            plugin_plan = run_cli(wrapper, "plan", "init", str(plugin_target))
            self.assertEqual(plugin_plan.returncode, 0, plugin_plan.stderr)
            plugin_install = run_cli(wrapper, "init", str(plugin_target))
            self.assertEqual(plugin_install.returncode, 0, plugin_install.stderr)
            plugin_doctor = run_cli(plugin_target / "bin/vibe", "doctor", str(plugin_target))
            self.assertEqual(plugin_doctor.returncode, 0, plugin_doctor.stderr)
            plugin_manifest = json.loads((plugin_target / ".vibe/manifest.json").read_text())
            self.assertEqual(release_manifest["managed_files"], plugin_manifest["managed_files"])

            (plugin_unpack / "vibe-kit/payload/README.md").write_text("tampered\n")
            rejected_plugin = run_cli(
                wrapper, "plan", "init", str(base / "tampered-plugin-target")
            )
            self.assertEqual(rejected_plugin.returncode, 2)
            self.assertIn("payload identity does not match", rejected_plugin.stderr)

            old_payload = base / "vibe-kit-0.2-fixture"
            shutil.copytree(release_root, old_payload)
            (old_payload / ".vibe/core/version").write_text("0.2.0\n")
            old_target = base / "upgrade-from-0.2"
            old_install = run_cli(old_payload / "bin/vibe", "init", str(old_target))
            self.assertEqual(old_install.returncode, 0, old_install.stderr)
            upgrade = run_cli(release_cli, "upgrade", str(old_target))
            self.assertEqual(upgrade.returncode, 0, upgrade.stderr)
            upgraded_doctor = run_cli(old_target / "bin/vibe", "doctor", str(old_target))
            self.assertEqual(upgraded_doctor.returncode, 0, upgraded_doctor.stderr)
            self.assertIn(KIT_VERSION, upgraded_doctor.stdout)
            self.assertTrue(
                (old_target / ".vibe/core/technical-decision-readiness.md").is_file()
            )
            self.assertTrue(
                (old_target / ".codex/agents/vibe-tech-lead.toml").is_file()
            )

            old_conflict_payload = base / "vibe-kit-0.2-conflict-fixture"
            shutil.copytree(release_root, old_conflict_payload)
            (old_conflict_payload / ".vibe/core/version").write_text("0.2.0\n")
            old_quality = old_conflict_payload / ".vibe/core/quality-gates.md"
            old_quality.write_text(old_quality.read_text() + "\nOld release marker.\n")
            conflict_target = base / "conflict-from-0.2"
            conflict_install = run_cli(
                old_conflict_payload / "bin/vibe", "init", str(conflict_target)
            )
            self.assertEqual(conflict_install.returncode, 0, conflict_install.stderr)
            conflict_quality = conflict_target / ".vibe/core/quality-gates.md"
            conflict_quality.write_text(conflict_quality.read_text() + "\nLocal edit.\n")
            before_conflict_plan = file_snapshot(conflict_target)
            conflict_plan = run_cli(release_cli, "plan", "upgrade", str(conflict_target))
            self.assertEqual(conflict_plan.returncode, 2)
            self.assertEqual(file_snapshot(conflict_target), before_conflict_plan)
            conflict_upgrade = run_cli(release_cli, "upgrade", str(conflict_target))
            self.assertEqual(conflict_upgrade.returncode, 2)
            self.assertIn("Local edit.", conflict_quality.read_text())
            self.assertEqual((conflict_target / ".vibe/core/version").read_text(), "0.2.0\n")
            self.assertEqual(
                json.loads((conflict_target / ".vibe/manifest.json").read_text())["framework_version"],
                "0.2.0",
            )

            tampered = base / "tampered-release"
            shutil.copytree(first, tampered)
            archive_path = tampered / KIT_ARCHIVE
            content = archive_path.read_bytes()
            archive_path.write_bytes(content[:-1] + bytes([content[-1] ^ 0x01]))
            rejected = run_cli(CLI, "validate-release", str(tampered))
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("checksum mismatch", rejected.stderr)
            rejected_json = run_cli(
                CLI, "validate-release", str(tampered), "--format", "json"
            )
            self.assertEqual(rejected_json.returncode, 1, rejected_json.stderr)
            rejected_receipt = json.loads(rejected_json.stdout)
            self.assertEqual(rejected_receipt["status"], "invalid")
            self.assertTrue(rejected_receipt["errors"])

    def test_release_validation_rejects_unsafe_archives_and_plugin_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source_release = base / "source-release"
            built = run_cli(CLI, "package", "--output", str(source_release))
            self.assertEqual(built.returncode, 0, built.stderr)

            unsafe = base / "unsafe-release"
            shutil.copytree(source_release, unsafe)
            release_zip = unsafe / KIT_ARCHIVE
            with zipfile.ZipFile(release_zip, "r") as archive:
                original = [(info.filename, archive.read(info)) for info in archive.infolist()]
            with zipfile.ZipFile(release_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, content in original:
                    archive.writestr(name, content)
                archive.writestr(f"{KIT_ROOT}/../escape.txt", "unsafe")
            refresh_release_checksums(unsafe, KIT_ARCHIVE)
            unsafe_result = run_cli(CLI, "validate-release", str(unsafe))
            self.assertEqual(unsafe_result.returncode, 1)
            self.assertIn("unsafe archive path", unsafe_result.stderr)

            drifted = base / "drifted-release"
            shutil.copytree(source_release, drifted)
            plugin_zip = drifted / PLUGIN_ARCHIVE
            with zipfile.ZipFile(plugin_zip, "r") as archive:
                plugin_files = [(info.filename, archive.read(info)) for info in archive.infolist()]
            with zipfile.ZipFile(plugin_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, content in plugin_files:
                    if name == "vibe-kit/.codex-plugin/plugin.json":
                        plugin = json.loads(content.decode("utf-8"))
                        plugin["version"] = "9.9.9"
                        content = json.dumps(plugin).encode("utf-8")
                    archive.writestr(name, content)
            refresh_release_checksums(drifted, PLUGIN_ARCHIVE)
            drift_result = run_cli(CLI, "validate-release", str(drifted))
            self.assertEqual(drift_result.returncode, 1)
            self.assertIn("Plugin name/version does not match release", drift_result.stderr)

            identity_drifted = base / "identity-drifted-release"
            shutil.copytree(source_release, identity_drifted)
            identity_plugin_zip = identity_drifted / PLUGIN_ARCHIVE
            with zipfile.ZipFile(identity_plugin_zip, "r") as archive:
                identity_files = [
                    (info.filename, archive.read(info))
                    for info in archive.infolist()
                ]
            with zipfile.ZipFile(
                identity_plugin_zip, "w", compression=zipfile.ZIP_DEFLATED
            ) as archive:
                for name, content in identity_files:
                    if name == "vibe-kit/.codex-plugin/plugin.json":
                        plugin = json.loads(content.decode("utf-8"))
                        plugin["payload_tree_sha256"] = "0" * 64
                        content = json.dumps(plugin).encode("utf-8")
                    archive.writestr(name, content)
            refresh_release_checksums(identity_drifted, PLUGIN_ARCHIVE)
            identity_result = run_cli(
                CLI, "validate-release", str(identity_drifted)
            )
            self.assertEqual(identity_result.returncode, 1)
            self.assertIn(
                "Plugin payload-tree identity does not match release payload",
                identity_result.stderr,
            )

            unknown_state_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            unknown_state_contract["cli"]["command_statuses"]["init"].append(
                "unknown-success"
            )
            unknown_takeover_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            unknown_takeover_contract["takeover"]["reason_codes"].append(
                "unknown-reason"
            )
            broken_bridge_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            broken_bridge_contract["maintenance_bridge"][
                "maximum_installed_kit_version_exclusive"
            ] = "9.0.0"
            diagnostic_drift_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            diagnostic_drift_contract["cli"]["doctor"]["warning_registry"][
                "managed-file-hash-mismatch"
            ] = "non-blocking"
            verify_drift_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            verify_drift_contract["cli"]["verify"]["skipped_reasons"].append(
                "unknown-skip"
            )
            activation_drift_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            activation_drift_contract["activation"]["activation_set_sha256"] = (
                "0" * 64
            )
            registry_drift_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            registry_drift_contract["takeover"]["contract_registry"][
                "ready_invariants"
            ].remove("overall-ready-iff-ready-stage-satisfied")
            duplicate_key_contract = (
                (ROOT / "agent-install.json")
                .read_text()
                .replace("{", '{"schema_version": 2,', 1)
                .encode()
            )
            contract_cases = {
                "missing": (
                    None,
                    "release ZIP is missing required payload file: agent-install.json",
                ),
                "malformed": (b"{not-json\n", "agent-install.json is malformed"),
                "duplicate-key": (
                    duplicate_key_contract,
                    "agent-install.json is malformed",
                ),
                "version-drift": (
                    json.dumps(
                        {
                            **json.loads((ROOT / "agent-install.json").read_text()),
                            "kit_version": "9.9.9",
                        }
                    ).encode(),
                    "agent install contract version does not match release",
                ),
                "channel-drift": (
                    json.dumps(
                        {
                            **json.loads((ROOT / "agent-install.json").read_text()),
                            "release_channels": {"allowed_statuses": []},
                        }
                    ).encode(),
                    "agent install contract release channel does not match release status",
                ),
                "unknown-command-state": (
                    json.dumps(unknown_state_contract).encode(),
                    "agent install contract command statuses are unsupported",
                ),
                "unknown-takeover-reason": (
                    json.dumps(unknown_takeover_contract).encode(),
                    "agent install takeover enum is unsupported: reason_codes",
                ),
                "maintenance-bridge-drift": (
                    json.dumps(broken_bridge_contract).encode(),
                    "agent install maintenance bridge is unsupported",
                ),
                "diagnostic-effect-drift": (
                    json.dumps(diagnostic_drift_contract).encode(),
                    "agent install doctor diagnostic contract is unsupported",
                ),
                "verify-reason-drift": (
                    json.dumps(verify_drift_contract).encode(),
                    "agent install verify contract is unsupported",
                ),
                "activation-identity-drift": (
                    json.dumps(activation_drift_contract).encode(),
                    "agent install activation-set identity does not match payload",
                ),
                "takeover-registry-drift": (
                    json.dumps(registry_drift_contract).encode(),
                    "agent install takeover contract registry is unsupported",
                ),
            }
            contract_entry = f"{KIT_ROOT}/agent-install.json"
            for name, (replacement, expected_error) in contract_cases.items():
                with self.subTest(contract=name):
                    changed = base / f"contract-{name}"
                    shutil.copytree(source_release, changed)
                    changed_zip = changed / KIT_ARCHIVE
                    with zipfile.ZipFile(changed_zip, "r") as archive:
                        entries = [
                            (info.filename, archive.read(info))
                            for info in archive.infolist()
                            if not info.is_dir()
                        ]
                    with zipfile.ZipFile(
                        changed_zip, "w", compression=zipfile.ZIP_DEFLATED
                    ) as archive:
                        for entry_name, content in entries:
                            if entry_name == contract_entry:
                                if replacement is not None:
                                    archive.writestr(entry_name, replacement)
                                continue
                            archive.writestr(entry_name, content)
                    refresh_release_checksums(changed, KIT_ARCHIVE)
                    contract_result = run_cli(
                        CLI, "validate-release", str(changed), "--format", "json"
                    )
                    self.assertEqual(contract_result.returncode, 1)
                    contract_receipt = json.loads(contract_result.stdout)
                    self.assertIn(expected_error, contract_receipt["errors"])

    def test_predecessor_migration_mirrors_fail_closed_across_plan_and_release(self) -> None:
        mirror = {
            "schema_version": 1,
            "registry_sha256": "6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d",
            "authority": "target-cli-compiled",
            "modes": ["replace-and-adopt-complete-set"],
        }
        invalid_values = {
            "missing": "missing",
            "null": None,
            "wrong-type": [],
            "extra-field": {**mirror, "extra": True},
            "wrong-digest": {**mirror, "registry_sha256": "0" * 64},
            "uppercase-digest": {
                **mirror,
                "registry_sha256": mirror["registry_sha256"].upper(),
            },
            "wrong-authority": {**mirror, "authority": "installed-contract"},
            "wrong-mode": {**mirror, "modes": ["adopt-one-file"]},
            "boolean-schema": {**mirror, "schema_version": True},
        }
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            predecessor = official_v050_source_fixture(base / "predecessor")
            predecessor_before = file_snapshot(predecessor)
            for name, invalid in invalid_values.items():
                with self.subTest(target_agent_mirror=name):
                    source = base / f"source-{name}"
                    cli = copy_source(source)
                    contract_path = source / "agent-install.json"
                    contract = json.loads(contract_path.read_text())
                    if invalid == "missing":
                        contract["maintenance_bridge"].pop("predecessor_migrations")
                    else:
                        contract["maintenance_bridge"]["predecessor_migrations"] = invalid
                    contract_path.write_text(json.dumps(contract, indent=2) + "\n")
                    result = run_cli(
                        cli,
                        "plan",
                        "upgrade",
                        str(predecessor),
                        "--format",
                        "json",
                    )
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["status"], "error")
                    self.assertEqual(file_snapshot(predecessor), predecessor_before)

            divergent = base / "source-divergent-core"
            divergent_cli = copy_source(divergent)
            protocol_path = divergent / ".vibe/core/protocol.json"
            protocol = json.loads(protocol_path.read_text())
            protocol["predecessor_migrations"] = {
                **mirror,
                "registry_sha256": "0" * 64,
            }
            protocol_path.write_text(json.dumps(protocol, indent=2) + "\n")
            result = run_cli(
                divergent_cli,
                "plan",
                "upgrade",
                str(predecessor),
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(file_snapshot(predecessor), predecessor_before)

            release = base / "release"
            built = run_cli(CLI, "package", "--output", str(release))
            self.assertEqual(built.returncode, 0, built.stderr)
            for name, invalid in invalid_values.items():
                with self.subTest(release_manifest_mirror=name):
                    changed = base / f"release-{name}"
                    shutil.copytree(release, changed)
                    manifest_path = changed / "release-manifest.json"
                    manifest = json.loads(manifest_path.read_text())
                    if invalid == "missing":
                        manifest.pop("predecessor_migrations")
                    else:
                        manifest["predecessor_migrations"] = invalid
                    manifest_path.write_text(
                        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
                        + "\n"
                    )
                    refresh_release_checksums(changed, "release-manifest.json")
                    validation = run_cli(
                        CLI,
                        "validate-release",
                        str(changed),
                        "--format",
                        "json",
                    )
                    self.assertEqual(validation.returncode, 1, validation.stderr)
                    self.assertIn(
                        "release predecessor-migration registry mirror is unsupported",
                        json.loads(validation.stdout)["errors"],
                    )

    def test_prerelease_package_requires_clean_commit_and_records_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / "source"
            cli = copy_source(source)
            output = base / "prerelease"

            uncommitted = run_cli(
                cli,
                "package",
                "--status",
                "prerelease",
                "--output",
                str(output),
            )
            self.assertEqual(uncommitted.returncode, 2)
            self.assertIn("clean committed Git source", uncommitted.stderr)
            self.assertFalse(output.exists())

            subprocess.run(
                ["git", "init", "-b", "main"], cwd=source, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "config", "user.name", "Release Test"], cwd=source, check=True
            )
            subprocess.run(
                ["git", "config", "user.email", "release@example.invalid"],
                cwd=source,
                check=True,
            )
            subprocess.run(["git", "add", "-A"], cwd=source, check=True)
            subprocess.run(
                ["git", "commit", "-m", "fixture"],
                cwd=source,
                check=True,
                capture_output=True,
            )
            expected_ref = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=source,
                text=True,
                check=True,
                capture_output=True,
            ).stdout.strip()

            built = run_cli(
                cli,
                "package",
                "--status",
                "prerelease",
                "--output",
                str(output),
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            manifest = json.loads((output / "release-manifest.json").read_text())
            self.assertEqual(manifest["status"], "prerelease")
            self.assertEqual(manifest["source"]["ref"], expected_ref)
            self.assertEqual(manifest["source"]["tree_state"], "clean")

            bundle_unpack = base / "bundle-unpacked"
            with zipfile.ZipFile(output / DISTRIBUTION_ARCHIVE) as archive:
                archive.extractall(bundle_unpack)
            bundled_release = bundle_unpack / KIT_ROOT
            validated = run_cli(cli, "validate-release", str(bundled_release))
            self.assertEqual(validated.returncode, 0, validated.stderr)

            stable_output = base / "stable"
            stable = run_cli(
                cli,
                "package",
                "--status",
                "stable",
                "--output",
                str(stable_output),
            )
            self.assertEqual(stable.returncode, 0, stable.stderr)
            self.assertEqual(
                json.loads((stable_output / "release-manifest.json").read_text())["status"],
                "stable",
            )

            manifest["status"] = "published"
            (output / "release-manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            )
            refresh_release_checksums(output, "release-manifest.json")
            rejected = run_cli(cli, "validate-release", str(output))
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("status is missing or unsupported", rejected.stderr)

    def test_adopt_preserves_existing_project_and_detects_stack(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "existing-project"
            (target / "src").mkdir(parents=True)
            business_file = target / "src/app.ts"
            business_file.write_text("export const answer = 42;\n")
            (target / "tsconfig.json").write_text("{}\n")
            (target / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {"next": "latest", "react": "latest"},
                        "scripts": {
                            "lint": "next lint",
                            "typecheck": "tsc --noEmit",
                            "test": "vitest run",
                            "build": "next build",
                        },
                    }
                )
            )
            original_agents = "# Existing instructions\n\n- Keep this rule.\n"
            (target / "AGENTS.md").write_text(original_agents)
            project_owned = {
                ".vibe/project.yaml": b"schema_version: 7\r\ncustom: keep-me\r\n",
                ".vibe/project-rules.md": b"# Existing rules\n\n- Never replace this.\n",
                ".vibe/onboarding.json": b'{"schema_version":1,"status":"complete","custom":"keep"}\r\n',
                "docs/context/product.md": b"# Existing product truth\n",
                "docs/context/architecture.md": b"# Existing architecture truth\n",
                "docs/context/design-system.md": b"# Existing design truth\n",
                "docs/work-items/index.md": b"# Existing work index\n",
                "docs/decisions/index.md": b"# Existing decision index\n",
            }
            for relative, content in project_owned.items():
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)

            result = run_cli(CLI, "adopt", str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(business_file.read_text(), "export const answer = 42;\n")
            for relative, content in project_owned.items():
                self.assertEqual((target / relative).read_bytes(), content, relative)
            agents = (target / "AGENTS.md").read_text()
            self.assertIn("<!-- vibe-kit:managed:start -->", agents)
            self.assertIn(original_agents.strip(), agents)
            self.assertTrue((target / ".vibe/core/operating-model.md").is_file())

    def test_adopt_detects_stack_when_project_config_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "existing-project"
            target.mkdir()
            (target / "tsconfig.json").write_text("{}\n")
            (target / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {"next": "latest", "react": "latest"},
                        "scripts": {"test": "vitest run"},
                    }
                )
            )

            result = run_cli(CLI, "adopt", str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            config = (target / ".vibe/project.yaml").read_text()
            self.assertIn('lifecycle: "existing"', config)
            self.assertIn('language: "TypeScript"', config)
            self.assertIn('framework: "Next.js"', config)
            self.assertIn('test: "npm run test"', config)

    def test_adopt_stops_before_changes_on_managed_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "collision-project"
            conflict = target / ".codex/agents/vibe-pm.toml"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("custom = true\n")
            (target / "README.md").write_text("existing\n")

            result = run_cli(CLI, "adopt", str(target))
            self.assertEqual(result.returncode, 2)
            self.assertIn("stopped before making changes", result.stderr)
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse((target / ".vibe/manifest.json").exists())
            self.assertEqual(conflict.read_text(), "custom = true\n")

    def test_upgrade_updates_managed_files_and_preserves_project_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source_one = base / "source-one"
            source_two = base / "source-two"
            target = base / "target"
            cli_one = copy_source(source_one)
            cli_two = copy_source(source_two)
            (source_one / ".vibe/core/version").write_text("0.1.0\n")
            (source_two / ".vibe/core/version").write_text("0.2.0\n")
            source_one_contract_path = source_one / "agent-install.json"
            source_one_contract = json.loads(source_one_contract_path.read_text())
            source_one_contract["kit_version"] = "0.1.0"
            source_one_contract_path.write_text(
                json.dumps(source_one_contract, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            )
            source_one_contract["activation"]["activation_set_sha256"] = (
                independent_activation_digest(source_one)
            )
            source_one_contract_path.write_text(
                json.dumps(source_one_contract, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            )

            installed = run_cli(cli_one, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            custom_rules = "# My rules\n\n- Preserve me.\n"
            (target / ".vibe/project-rules.md").write_text(custom_rules)
            custom_product = "# My product context\n\nKeep this truth.\n"
            (target / "docs/context/product.md").write_text(custom_product)
            custom_onboarding = (
                b'{"schema_version":1,"status":"complete",'
                b'"updated_at":"2026-08-27",'
                b'"evidence":["docs/context/product.md"],"owner":"project"}\n'
            )
            (target / ".vibe/onboarding.json").write_bytes(custom_onboarding)
            target_agents = target / "AGENTS.md"
            target_agents.write_text(target_agents.read_text() + "\n# Local agent rule\n")

            quality_two = source_two / ".vibe/core/quality-gates.md"
            quality_two.write_text(quality_two.read_text() + "\nUpgrade marker.\n")
            source_agents = source_two / "AGENTS.md"
            source_agents.write_text(
                source_agents.read_text().replace(
                    "Do not claim completion without relevant verification evidence.",
                    "Do not claim completion without relevant verification evidence. Upgraded rule.",
                )
            )
            source_two_contract_path = source_two / "agent-install.json"
            source_two_contract = json.loads(source_two_contract_path.read_text())
            source_two_contract["kit_version"] = "0.2.0"
            source_two_contract_path.write_text(
                json.dumps(source_two_contract, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            )
            source_two_contract["activation"]["activation_set_sha256"] = (
                independent_activation_digest(source_two)
            )
            source_two_contract_path.write_text(
                json.dumps(source_two_contract, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            )
            upgraded = run_cli(cli_two, "upgrade", str(target), "--format", "json")
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            upgraded_receipt = json.loads(upgraded.stdout)
            self.assertEqual(upgraded_receipt["status"], "success")
            self.assertEqual(upgraded_receipt["write_state"], "project-files-written")
            self.assertTrue(upgraded_receipt["writes_performed"])
            self.assertEqual(upgraded_receipt["source"]["type"], "local-payload")
            self.assertIn("Upgrade marker.", (target / ".vibe/core/quality-gates.md").read_text())
            self.assertEqual((target / ".vibe/project-rules.md").read_text(), custom_rules)
            self.assertEqual((target / "docs/context/product.md").read_text(), custom_product)
            self.assertEqual((target / ".vibe/onboarding.json").read_bytes(), custom_onboarding)
            self.assertEqual((target / ".vibe/version").read_text(), "0.2.0\n")
            self.assertEqual(
                json.loads((target / ".vibe/manifest.json").read_text())["framework_version"],
                "0.2.0",
            )
            self.assertEqual((target / ".vibe/core/version").read_text(), "0.2.0\n")
            upgraded_agents = target_agents.read_text()
            self.assertIn("Upgraded rule.", upgraded_agents)
            self.assertIn("# Local agent rule", upgraded_agents)
            doctor = run_cli(target / "bin/vibe", "doctor", str(target))
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            self.assertIn("Version integrity: OK (0.2.0)", doctor.stdout)

    def test_doctor_reports_version_integrity_and_is_read_only(self) -> None:
        scenarios = {
            "installed missing": lambda target: (target / ".vibe/version").unlink(),
            "installed empty": lambda target: (target / ".vibe/version").write_text(" \n"),
            "manifest missing version": self._remove_manifest_version,
            "manifest empty version": lambda target: self._set_manifest_version(target, ""),
            "manifest mismatch": lambda target: self._set_manifest_version(target, "9.9.9"),
            "core missing": lambda target: (target / ".vibe/core/version").unlink(),
            "core empty": lambda target: (target / ".vibe/core/version").write_text("\n"),
        }
        for name, mutate in scenarios.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "version-project"
                installed = run_cli(CLI, "init", str(target))
                self.assertEqual(installed.returncode, 0, installed.stderr)
                mutate(target)
                before = file_snapshot(target)

                doctor = run_cli(target / "bin/vibe", "doctor", str(target))

                self.assertEqual(doctor.returncode, 1, doctor.stderr)
                self.assertIn("Vibe Kit version integrity failed", doctor.stderr)
                self.assertIn(".vibe/version:", doctor.stderr)
                self.assertIn("manifest.framework_version:", doctor.stderr)
                self.assertIn(".vibe/core/version:", doctor.stderr)
                self.assertIn("trusted Vibe Kit checkout", doctor.stderr)
                self.assertIn("Then rerun:", doctor.stderr)
                self.assertEqual(file_snapshot(target), before)

    def test_doctor_preserves_non_version_warning_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "warning-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            quality = target / ".vibe/core/quality-gates.md"
            quality.write_text(quality.read_text() + "\nLocal note.\n")

            doctor = run_cli(target / "bin/vibe", "doctor", str(target))

            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            self.assertEqual(doctor.stderr, "")
            self.assertIn("WARN: locally modified managed file", doctor.stdout)
            self.assertIn("Version integrity: OK", doctor.stdout)

    def test_doctor_json_classifies_activation_and_stale_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "diagnostic-project"
            installed = run_cli(CLI, "init", str(target), "--format", "json")
            self.assertEqual(installed.returncode, 0, installed.stderr)

            healthy = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(healthy.returncode, 0, healthy.stderr)
            receipt = json.loads(healthy.stdout)
            self.assertEqual(receipt["status"], "healthy")
            self.assertEqual(receipt["diagnostics"], [])
            self.assertEqual(receipt["activation"]["status"], "match")
            self.assertEqual(
                receipt["activation"]["actual_activation_set_sha256"],
                receipt["activation"]["expected_activation_set_sha256"],
            )
            self.assertRegex(receipt["manifest_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(receipt["target_fingerprint"]["kit_version"], KIT_VERSION)
            self.assertEqual(receipt["target_fingerprint"]["core_protocol"], 5)
            self.assertEqual(receipt["target_fingerprint"]["agent_install_schema"], 3)
            self.assertEqual(receipt["target_fingerprint"]["manifest_sha256"], receipt["manifest_sha256"])

            quality = target / ".vibe/core/quality-gates.md"
            original_quality = quality.read_bytes()
            quality.write_bytes(original_quality + b"\nlocal change\n")
            changed = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(changed.returncode, 0, changed.stderr)
            changed_receipt = json.loads(changed.stdout)
            self.assertEqual(changed_receipt["status"], "warning")
            self.assertEqual(changed_receipt["activation"]["status"], "mismatch")
            diagnostic = next(
                item
                for item in changed_receipt["diagnostics"]
                if item["code"] == "managed-file-hash-mismatch"
            )
            self.assertEqual(diagnostic["level"], "warning")
            self.assertEqual(diagnostic["readiness_effect"], "blocking")
            self.assertEqual(diagnostic["path"], ".vibe/core/quality-gates.md")
            self.assertEqual(changed.stderr, "")
            quality.write_bytes(original_quality)

            stale_skill = target / ".agents/skills/vibe-retired/SKILL.md"
            stale_skill.parent.mkdir(parents=True)
            stale_skill.write_text(
                "---\nname: vibe-retired\ndescription: Retired fixture skill.\n---\n"
            )
            stale = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(stale.returncode, 0, stale.stderr)
            stale_receipt = json.loads(stale.stdout)
            stale_codes = [item["code"] for item in stale_receipt["diagnostics"]]
            self.assertIn("stale-runtime-path-preserved", stale_codes)
            self.assertIn(
                ".agents/skills/vibe-retired/SKILL.md",
                stale_receipt["activation"]["stale_runtime_paths"],
            )

            manifest_path = target / ".vibe/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            legacy = target / "legacy/retained.txt"
            legacy.parent.mkdir()
            legacy.write_text("retained\n")
            manifest["managed_files"]["legacy/retained.txt"] = hashlib.sha256(
                legacy.read_bytes()
            ).hexdigest()
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
            nonruntime = run_cli(
                target / "bin/vibe", "doctor", str(target), "--format", "json"
            )
            self.assertEqual(nonruntime.returncode, 0, nonruntime.stderr)
            nonruntime_receipt = json.loads(nonruntime.stdout)
            nonruntime_diagnostic = next(
                item
                for item in nonruntime_receipt["diagnostics"]
                if item["code"] == "stale-nonruntime-path-preserved"
            )
            self.assertEqual(nonruntime_diagnostic["readiness_effect"], "non-blocking")

    @staticmethod
    def _remove_manifest_version(target: Path) -> None:
        path = target / ".vibe/manifest.json"
        manifest = json.loads(path.read_text())
        manifest.pop("framework_version")
        path.write_text(json.dumps(manifest, indent=2) + "\n")

    @staticmethod
    def _set_manifest_version(target: Path, version: str) -> None:
        path = target / ".vibe/manifest.json"
        manifest = json.loads(path.read_text())
        manifest["framework_version"] = version
        path.write_text(json.dumps(manifest, indent=2) + "\n")

    @staticmethod
    def _set_manifest_field(target: Path, key: str, value: object) -> None:
        path = target / ".vibe/manifest.json"
        manifest = json.loads(path.read_text())
        manifest[key] = value
        path.write_text(json.dumps(manifest, indent=2) + "\n")

    def test_upgrade_is_atomic_when_managed_file_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source_one = base / "source-one"
            source_two = base / "source-two"
            target = base / "target"
            cli_one = copy_source(source_one)
            cli_two = copy_source(source_two)

            installed = run_cli(cli_one, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            target_quality = target / ".vibe/core/quality-gates.md"
            target_quality.write_text(target_quality.read_text() + "\nLocal edit.\n")

            source_quality = source_two / ".vibe/core/quality-gates.md"
            source_quality.write_text(source_quality.read_text() + "\nIncoming edit.\n")
            source_operating = source_two / ".vibe/core/operating-model.md"
            source_operating.write_text(source_operating.read_text() + "\nShould not apply.\n")
            before_operating = (target / ".vibe/core/operating-model.md").read_text()

            upgraded = run_cli(cli_two, "upgrade", str(target))
            self.assertEqual(upgraded.returncode, 2)
            self.assertIn("Upgrade aborted", upgraded.stderr)
            self.assertIn("Local edit.", target_quality.read_text())
            self.assertNotIn("Incoming edit.", target_quality.read_text())
            self.assertEqual((target / ".vibe/core/operating-model.md").read_text(), before_operating)
            candidates = list((target / ".vibe/conflicts").rglob("*.incoming"))
            self.assertTrue(candidates)

    def test_verify_runs_selected_commands_and_reports_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "verify-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            (target / ".vibe/project.yaml").write_text(
                "schema_version: 1\n"
                "commands:\n"
                '  lint: "true"\n'
                '  typecheck: ""\n'
                '  test: "false"\n'
                '  build: ""\n'
            )

            lint = run_cli(target / "bin/vibe", "verify", str(target), "--only", "lint")
            self.assertEqual(lint.returncode, 0, lint.stderr)
            all_checks = run_cli(target / "bin/vibe", "verify", str(target))
            self.assertEqual(all_checks.returncode, 1)
            self.assertIn("Verification failed", all_checks.stderr)

    def test_verify_json_reports_full_matrix_bounded_redacted_output_and_skips(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "verify-json-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            failing = (
                "python3 -c \"import sys; print('sk-test_abcdefghijklmnop'); "
                "print('" + ("x" * 17000) + "'); print('sk-test_abcdefghijklmnop'); "
                "print('" + str(target) + "'); "
                "sys.exit(3)\""
            )
            (target / ".vibe/project.yaml").write_text(
                "schema_version: 1\ncommands:\n"
                + f"  lint: {json.dumps('true')}\n"
                + '  typecheck: ""\n'
                + f"  test: {json.dumps(failing)}\n"
                + f"  build: {json.dumps('true')}\n"
            )

            result = run_cli(
                target / "bin/vibe", "verify", str(target), "--format", "json"
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(result.stderr, "")
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["schema_version"], 2)
            self.assertEqual(receipt["status"], "failed")
            self.assertEqual(
                [check["name"] for check in receipt["checks"]],
                ["lint", "typecheck", "test", "build"],
            )
            self.assertEqual(
                [check["outcome"] for check in receipt["checks"]],
                ["passed", "unconfigured", "failed", "passed"],
            )
            self.assertEqual(
                receipt["selection"],
                {"mode": "default", "requested": [], "coverage": "all-configured"},
            )
            failed = receipt["checks"][2]
            self.assertEqual(failed["exit_code"], 3)
            self.assertTrue(failed["output"]["stdout_truncated"])
            self.assertNotIn("sk-test_abcdefghijklmnop", failed["output"]["stdout_tail"])
            self.assertIn("[REDACTED]", failed["output"]["stdout_tail"])
            self.assertNotIn(str(target), failed["output"]["stdout_tail"])

            partial = run_cli(
                target / "bin/vibe",
                "verify",
                str(target),
                "--only",
                "test",
                "--only",
                "test",
                "--format",
                "json",
            )
            self.assertEqual(partial.returncode, 1, partial.stderr)
            partial_receipt = json.loads(partial.stdout)
            self.assertEqual(
                partial_receipt["selection"],
                {"mode": "only", "requested": ["test"], "coverage": "partial"},
            )
            self.assertEqual(len(partial_receipt["checks"]), 1)

            module = load_cli_module()
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(
                module.subprocess, "run", side_effect=OSError("fixture start failure")
            ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                return_code = module.verify(target, [], "json")
            self.assertEqual(return_code, 2)
            self.assertEqual(stderr.getvalue(), "")
            blocked = json.loads(stdout.getvalue())
            self.assertEqual(blocked["status"], "blocked")
            self.assertEqual(blocked["summary"]["skipped"], 3)
            self.assertTrue(
                all(
                    check["reason_code"] == "process-start-failed"
                    for check in blocked["checks"]
                    if check["configured"]
                )
            )

    def test_feedback_deduplicates_dismisses_and_resurfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "feedback-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)

            first = self.feedback_draft(
                target / "bin/vibe", target, "--severity", "medium", "--confidence", "high"
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("Network: not used", first.stdout)
            report_dirs = list((target / ".vibe/local/feedback").glob("fb-*"))
            self.assertEqual(len(report_dirs), 1)
            report_id = report_dirs[0].name
            self.assertEqual(
                (target / ".vibe/local/.gitignore").read_text(), "*\n!.gitignore\n"
            )

            repeated = self.feedback_draft(
                target / "bin/vibe", target, "--severity", "medium", "--confidence", "high"
            )
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertIn("reused existing candidate", repeated.stdout)
            state_path = report_dirs[0] / "state.json"
            self.assertEqual(json.loads(state_path.read_text())["occurrence_count"], 2)

            dismissed = run_cli(
                target / "bin/vibe",
                "feedback",
                "dismiss",
                report_id,
                "--target",
                str(target),
                "--reason",
                "Not actionable at the current severity",
            )
            self.assertEqual(dismissed.returncode, 0, dismissed.stderr)
            suppressed = self.feedback_draft(
                target / "bin/vibe", target, "--severity", "medium", "--confidence", "high"
            )
            self.assertEqual(suppressed.returncode, 0, suppressed.stderr)
            self.assertIn("suppressed by prior dismissal", suppressed.stdout)

            resurfaced = self.feedback_draft(
                target / "bin/vibe", target, "--severity", "high", "--confidence", "high"
            )
            self.assertEqual(resurfaced.returncode, 0, resurfaced.stderr)
            self.assertIn("resurfaced with material change", resurfaced.stdout)
            self.assertEqual(len(list((target / ".vibe/local/feedback").glob("fb-*"))), 1)
            state = json.loads(state_path.read_text())
            self.assertEqual(state["status"], "review-ready")
            self.assertEqual(state["occurrence_count"], 4)

    def test_feedback_mode_defaults_preserves_choices_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "mode-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            project = target / ".vibe/project.yaml"
            original = project.read_text()

            default = run_cli(target / "bin/vibe", "feedback", "mode", "--target", str(target))
            self.assertEqual(default.returncode, 0, default.stderr)
            self.assertIn("Feedback mode: ask", default.stdout)
            self.assertIn("Source: project", default.stdout)

            missing_text = re.sub(r"\nfeedback:\n  mode: .*\n?", "\n", original)
            project.write_text(missing_text)
            missing = run_cli(target / "bin/vibe", "feedback", "mode", "--target", str(target))
            self.assertEqual(missing.returncode, 0, missing.stderr)
            self.assertIn("Feedback mode: ask", missing.stdout)
            self.assertIn("Source: default-missing", missing.stdout)

            for choice in ("local", "off"):
                project.write_text(original.replace('mode: "ask"', f'mode: "{choice}"'))
                selected = run_cli(
                    target / "bin/vibe", "feedback", "mode", "--target", str(target)
                )
                self.assertEqual(selected.returncode, 0, selected.stderr)
                self.assertIn(f"Feedback mode: {choice}", selected.stdout)

            project.write_text(original.replace('mode: "ask"', 'mode: "local"'))
            incoming_source = Path(temporary) / "incoming-source"
            incoming_cli = copy_source(incoming_source)
            (incoming_source / ".vibe/core/version").write_text("0.4.1\n")
            upgraded = run_cli(incoming_cli, "upgrade", str(target))
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            self.assertIn('mode: "local"', project.read_text())
            preserved = run_cli(
                target / "bin/vibe", "feedback", "mode", "--target", str(target)
            )
            self.assertIn("Feedback mode: local", preserved.stdout)

            invalid_variants = (
                original.replace('mode: "ask"', 'mode: "auto"'),
                original + 'feedback:\n  mode: "ask"\n',
                original.replace('  mode: "ask"', '\tmode: "ask"'),
            )
            for invalid in invalid_variants:
                with self.subTest(invalid=invalid[-32:]):
                    project.write_text(invalid)
                    mode = run_cli(
                        target / "bin/vibe", "feedback", "mode", "--target", str(target)
                    )
                    self.assertEqual(mode.returncode, 2)
                    doctor = run_cli(target / "bin/vibe", "doctor", str(target))
                    self.assertEqual(doctor.returncode, 1)

    def test_feedback_close_is_mode_aware_and_prompts_only_on_material_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)

            off_target = base / "off-project"
            self.assertEqual(run_cli(CLI, "init", str(off_target)).returncode, 0)
            off_config = off_target / ".vibe/project.yaml"
            off_config.write_text(off_config.read_text().replace('mode: "ask"', 'mode: "off"'))
            off = self.feedback_close(off_target / "bin/vibe", off_target)
            self.assertEqual(off.returncode, 0, off.stderr)
            self.assertEqual(off.stdout, "")
            self.assertFalse((off_target / ".vibe/local/feedback").exists())

            local_target = base / "local-project"
            self.assertEqual(run_cli(CLI, "init", str(local_target)).returncode, 0)
            local_config = local_target / ".vibe/project.yaml"
            local_config.write_text(
                local_config.read_text().replace('mode: "ask"', 'mode: "local"')
            )
            local = self.feedback_close(local_target / "bin/vibe", local_target)
            self.assertEqual(local.returncode, 0, local.stderr)
            self.assertIn("Feedback saved locally", local.stdout)
            self.assertNotIn("exact GitHub Issue payload", local.stdout)
            local_state = json.loads(
                next((local_target / ".vibe/local/feedback").glob("fb-*/state.json")).read_text()
            )
            self.assertEqual(local_state["attention"]["status"], "handled-local")
            local_repeated = self.feedback_close(local_target / "bin/vibe", local_target)
            self.assertEqual(local_repeated.returncode, 0, local_repeated.stderr)
            self.assertEqual(local_repeated.stdout, "")

            ask_target = base / "ask-project"
            self.assertEqual(run_cli(CLI, "init", str(ask_target)).returncode, 0)
            first = self.feedback_close(ask_target / "bin/vibe", ask_target)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("Vibe Kit feedback READY — local only", first.stdout)
            self.assertIn("--- exact GitHub Issue payload ---", first.stdout)
            self.assertIn("回复“提交”即可", first.stdout)
            state_path = next(
                (ask_target / ".vibe/local/feedback").glob("fb-*/state.json")
            )
            state = json.loads(state_path.read_text())
            self.assertEqual(state["state_schema_version"], 2)
            self.assertEqual(state["attention"]["status"], "presented")
            self.assertIsNotNone(state["attention"]["last_presented"]["review_hash"])

            repeated = self.feedback_close(ask_target / "bin/vibe", ask_target)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertEqual(repeated.stdout, "")

            changed = self.feedback_close(
                ask_target / "bin/vibe", ask_target, "--evidence", "A second project showed the same gap"
            )
            self.assertEqual(changed.returncode, 0, changed.stderr)
            self.assertIn("Vibe Kit feedback READY", changed.stdout)
            self.assertIn("Dedupe: MATERIAL RESURFACE", changed.stdout)
            changed_state = json.loads(state_path.read_text())
            self.assertEqual(changed_state["attention"]["revision"], 2)

            unchanged_again = self.feedback_close(
                ask_target / "bin/vibe", ask_target, "--evidence", "A second project showed the same gap"
            )
            self.assertEqual(unchanged_again.returncode, 0, unchanged_again.stderr)
            self.assertEqual(unchanged_again.stdout, "")

            legacy = json.loads(state_path.read_text())
            legacy.pop("state_schema_version")
            legacy.pop("attention")
            state_path.write_text(json.dumps(legacy))
            legacy_close = self.feedback_close(
                ask_target / "bin/vibe", ask_target, "--evidence", "A second project showed the same gap"
            )
            self.assertEqual(legacy_close.returncode, 0, legacy_close.stderr)
            self.assertEqual(legacy_close.stdout, "")
            legacy_material = self.feedback_close(
                ask_target / "bin/vibe", ask_target, "--severity", "high"
            )
            self.assertEqual(legacy_material.returncode, 0, legacy_material.stderr)
            self.assertIn("Vibe Kit feedback READY", legacy_material.stdout)

    def test_feedback_revise_invalidates_approval_and_security_blocks_public_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "revise-project"
            self.assertEqual(run_cli(CLI, "init", str(target)).returncode, 0)
            first = self.feedback_close(target / "bin/vibe", target)
            self.assertEqual(first.returncode, 0, first.stderr)
            report_dir = next((target / ".vibe/local/feedback").glob("fb-*"))
            report_id = report_dir.name
            old_hash = re.search(r"Review hash: (sha256:[a-f0-9]{64})", first.stdout)
            self.assertIsNotNone(old_hash)

            revised = run_cli(
                target / "bin/vibe",
                "feedback",
                "revise",
                report_id,
                "--target",
                str(target),
                "--input",
                "-",
                input_text=json.dumps(
                    {"proposal": "Add a recovery action and a concise diagnostic example"}
                ),
            )
            self.assertEqual(revised.returncode, 0, revised.stderr)
            new_hash = re.search(r"Review hash: (sha256:[a-f0-9]{64})", revised.stdout)
            self.assertIsNotNone(new_hash)
            self.assertNotEqual(old_hash.group(1), new_hash.group(1))
            self.assertIn("Dedupe: REVISED LOCAL CANDIDATE", revised.stdout)

            marker = base / "gh-called"
            fake_bin = base / "fake-bin"
            fake_bin.mkdir()
            fake_gh = fake_bin / "gh"
            fake_gh.write_text(
                "#!/bin/sh\n"
                f"touch {marker}\n"
                "exit 0\n"
            )
            fake_gh.chmod(0o755)
            env = {"PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", "")}
            stale = run_cli(
                target / "bin/vibe",
                "feedback",
                "submit",
                report_id,
                "--target",
                str(target),
                "--confirm",
                old_hash.group(1),
                env=env,
            )
            self.assertEqual(stale.returncode, 2)
            self.assertFalse(marker.exists())

            privacy_upgrade = self.feedback_close(
                target / "bin/vibe",
                target,
                "--evidence",
                "Later evidence shows the report requires a private disclosure path",
                "--security-sensitive",
            )
            self.assertEqual(privacy_upgrade.returncode, 0, privacy_upgrade.stderr)
            self.assertIn("PUBLIC SUBMISSION BLOCKED", privacy_upgrade.stdout)
            self.assertNotIn("--- exact GitHub Issue payload ---", privacy_upgrade.stdout)
            self.assertNotRegex(privacy_upgrade.stdout, r"Review hash: sha256:")
            upgraded_report = json.loads((report_dir / "report.json").read_text())
            self.assertEqual(
                upgraded_report["privacy"]["public_submission"], "blocked"
            )
            blocked_old_approval = run_cli(
                target / "bin/vibe",
                "feedback",
                "submit",
                report_id,
                "--target",
                str(target),
                "--confirm",
                new_hash.group(1),
                env=env,
            )
            self.assertEqual(blocked_old_approval.returncode, 2)
            self.assertFalse(marker.exists())

            sensitive_target = base / "sensitive-project"
            self.assertEqual(run_cli(CLI, "init", str(sensitive_target)).returncode, 0)
            sensitive = self.feedback_close(
                sensitive_target / "bin/vibe", sensitive_target, "--security-sensitive"
            )
            self.assertEqual(sensitive.returncode, 0, sensitive.stderr)
            self.assertIn("PUBLIC SUBMISSION BLOCKED", sensitive.stdout)
            self.assertNotIn("--- exact GitHub Issue payload ---", sensitive.stdout)
            self.assertNotRegex(sensitive.stdout, r"Review hash: sha256:")
            sensitive_id = next(
                (sensitive_target / ".vibe/local/feedback").glob("fb-*")
            ).name
            blocked_check = run_cli(
                sensitive_target / "bin/vibe",
                "feedback",
                "check",
                sensitive_id,
                "--target",
                str(sensitive_target),
                env=env,
            )
            self.assertEqual(blocked_check.returncode, 2)
            self.assertFalse(marker.exists())
            blocked_submit = run_cli(
                sensitive_target / "bin/vibe",
                "feedback",
                "submit",
                sensitive_id,
                "--target",
                str(sensitive_target),
                "--confirm",
                "sha256:" + "0" * 64,
                env=env,
            )
            self.assertEqual(blocked_submit.returncode, 2)
            self.assertFalse(marker.exists())

    def test_feedback_redacts_identifiers_and_blocks_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "private-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            payload = {
                "kind": "documentation",
                "component": "docs",
                "title": "Private-project onboarding gap",
                "summary": f"At {target}/src, owner@example.com followed https://internal.example/runbook",
                "expected": "The public workflow should explain the generic step",
                "observed": "The private-project maintainer needed a private path",
                "impact": "The reusable workflow could not be followed",
                "hypothesis": "The generic documentation omits one prerequisite",
                "proposal": "Document the prerequisite without project details",
                "reproduction": [f"Open {target}/README.md"],
                "evidence": ["The same generic prerequisite was missing twice"],
                "workflow": "vibe-project-onboarding",
                "agent_role": "vibe-pm",
                "severity": "medium",
                "confidence": "high",
                "trigger": "work-item-close",
            }
            drafted = run_cli(
                target / "bin/vibe",
                "feedback",
                "draft",
                "--target",
                str(target),
                "--input",
                "-",
                input_text=json.dumps(payload),
            )
            self.assertEqual(drafted.returncode, 0, drafted.stderr)
            report_path = next((target / ".vibe/local/feedback").glob("fb-*/report.json"))
            report_text = report_path.read_text()
            self.assertNotIn(str(target), report_text)
            self.assertNotIn("owner@example.com", report_text)
            self.assertNotIn("internal.example", report_text)
            self.assertNotIn("private-project", report_text.lower())
            report = json.loads(report_text)
            self.assertEqual(report["privacy"]["status"], "redacted")

            synthetic_secrets = (
                "-----BEGIN " + "PRIVATE KEY-----",
                "gh" + "p_" + ("a" * 32),
                "gl" + "pat-" + ("b" * 24),
                "AK" + "IA" + ("C" * 16),
                "sk_" + "live_" + ("d" * 24),
                "xo" + "xb-" + ("123456789012-" + "e" * 16),
                "npm" + "_" + ("f" * 36),
                "pypi" + "-" + ("g" * 48),
                "AI" + "za" + ("h" * 35),
                "S" + "G." + ("i" * 16) + "." + ("j" * 16),
                "S" + "K" + ("0" * 32),
                "ey" + "J" + ("k" * 12) + "." + ("l" * 16) + "." + ("m" * 16),
                "s" + "k-" + ("n" * 24),
                "api_" + "key = " + ("o" * 24),
            )
            for synthetic_secret in synthetic_secrets:
                with self.subTest(secret_prefix=synthetic_secret[:8]):
                    unsafe = dict(payload)
                    unsafe["summary"] = "Synthetic credential " + synthetic_secret
                    blocked = run_cli(
                        target / "bin/vibe",
                        "feedback",
                        "draft",
                        "--target",
                        str(target),
                        "--input",
                        "-",
                        input_text=json.dumps(unsafe),
                    )
                    self.assertEqual(blocked.returncode, 2)
                    self.assertIn("public feedback is blocked", blocked.stderr)
            self.assertEqual(len(list((target / ".vibe/local/feedback").glob("fb-*"))), 1)

    def test_feedback_review_hash_and_github_submit_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "feedback-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            drafted = self.feedback_draft(target / "bin/vibe", target)
            self.assertEqual(drafted.returncode, 0, drafted.stderr)
            report_dir = next((target / ".vibe/local/feedback").glob("fb-*"))
            report_id = report_dir.name

            feedback_config = target / ".vibe/core/feedback.json"
            config = json.loads(feedback_config.read_text())
            config["github_repository"] = ""
            feedback_config.write_text(json.dumps(config, indent=2) + "\n")

            local_review = run_cli(
                target / "bin/vibe",
                "feedback",
                "review",
                report_id,
                "--target",
                str(target),
            )
            self.assertEqual(local_review.returncode, 0, local_review.stderr)
            self.assertIn("Target: <not configured>", local_review.stdout)
            self.assertIn("No network was used", local_review.stdout)

            review = run_cli(
                target / "bin/vibe",
                "feedback",
                "review",
                report_id,
                "--target",
                str(target),
                "--repo",
                "owner/vibe-kit",
            )
            self.assertEqual(review.returncode, 0, review.stderr)
            match = re.search(r"Review hash: (sha256:[a-f0-9]{64})", review.stdout)
            self.assertIsNotNone(match)
            review_hash = match.group(1)

            fake_bin = base / "fake-bin"
            fake_bin.mkdir()
            fake_gh = fake_bin / "gh"
            fake_gh.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, pathlib, sys\n"
                "args = sys.argv[1:]\n"
                "state = pathlib.Path(os.environ['FAKE_GH_STATE'])\n"
                "count = pathlib.Path(os.environ['FAKE_GH_COUNT'])\n"
                "body = pathlib.Path(os.environ['FAKE_GH_BODY'])\n"
                "if args[:2] == ['auth', 'status']:\n"
                "    raise SystemExit(0)\n"
                "if args[:2] == ['issue', 'list']:\n"
                "    print(json.dumps([{'number': 7, 'url': 'https://github.com/owner/vibe-kit/issues/7', 'title': 'existing', 'state': 'OPEN'}] if state.exists() else []))\n"
                "    raise SystemExit(0)\n"
                "if args[:2] == ['issue', 'create']:\n"
                "    body.write_text(sys.stdin.read())\n"
                "    current = int(count.read_text()) if count.exists() else 0\n"
                "    count.write_text(str(current + 1))\n"
                "    state.write_text('created')\n"
                "    print('https://github.com/owner/vibe-kit/issues/7')\n"
                "    raise SystemExit(0)\n"
                "raise SystemExit(9)\n"
            )
            fake_gh.chmod(0o755)
            env = {
                "PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", ""),
                "FAKE_GH_STATE": str(base / "gh-state"),
                "FAKE_GH_COUNT": str(base / "gh-count"),
                "FAKE_GH_BODY": str(base / "gh-body"),
            }

            unconfirmed = run_cli(
                target / "bin/vibe",
                "feedback",
                "submit",
                report_id,
                "--target",
                str(target),
                "--repo",
                "owner/vibe-kit",
                env=env,
            )
            self.assertEqual(unconfirmed.returncode, 2)
            self.assertFalse((base / "gh-state").exists())

            submitted = run_cli(
                target / "bin/vibe",
                "feedback",
                "submit",
                report_id,
                "--target",
                str(target),
                "--repo",
                "owner/vibe-kit",
                "--confirm",
                review_hash,
                env=env,
            )
            self.assertEqual(submitted.returncode, 0, submitted.stderr)
            self.assertIn("Feedback submitted", submitted.stdout)
            self.assertEqual((base / "gh-count").read_text(), "1")
            self.assertIn("vibe-kit-feedback:fingerprint=", (base / "gh-body").read_text())

            repeated = run_cli(
                target / "bin/vibe",
                "feedback",
                "submit",
                report_id,
                "--target",
                str(target),
                "--repo",
                "owner/vibe-kit",
                "--confirm",
                review_hash,
                env=env,
            )
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertIn("already covered", repeated.stdout)
            self.assertEqual((base / "gh-count").read_text(), "1")

            report_path = report_dir / "report.json"
            report = json.loads(report_path.read_text())
            report["signal"]["proposal"] = "A changed proposal invalidates approval"
            report_path.write_text(json.dumps(report))
            stale = run_cli(
                target / "bin/vibe",
                "feedback",
                "submit",
                report_id,
                "--target",
                str(target),
                "--repo",
                "owner/vibe-kit",
                "--confirm",
                review_hash,
                env=env,
            )
            self.assertEqual(stale.returncode, 2)
            self.assertIn("missing or stale", stale.stderr)
            self.assertEqual((base / "gh-count").read_text(), "1")

    def test_feedback_remote_failure_does_not_persist_or_echo_raw_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "failure-project"
            installed = run_cli(CLI, "init", str(target))
            self.assertEqual(installed.returncode, 0, installed.stderr)
            drafted = self.feedback_draft(target / "bin/vibe", target)
            self.assertEqual(drafted.returncode, 0, drafted.stderr)
            report_dir = next((target / ".vibe/local/feedback").glob("fb-*"))
            review = run_cli(
                target / "bin/vibe",
                "feedback",
                "review",
                report_dir.name,
                "--target",
                str(target),
            )
            review_hash = re.search(
                r"Review hash: (sha256:[a-f0-9]{64})", review.stdout
            )
            self.assertIsNotNone(review_hash)

            fake_bin = base / "fake-bin"
            fake_bin.mkdir()
            fake_gh = fake_bin / "gh"
            fake_gh.write_text(
                "#!/bin/sh\n"
                "if [ \"$1 $2\" = \"auth status\" ]; then exit 0; fi\n"
                "echo 'opaque-remote-secret-marker' >&2\n"
                "exit 9\n"
            )
            fake_gh.chmod(0o755)
            env = {"PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", "")}
            failed = run_cli(
                target / "bin/vibe",
                "feedback",
                "submit",
                report_dir.name,
                "--target",
                str(target),
                "--confirm",
                review_hash.group(1),
                env=env,
            )
            self.assertEqual(failed.returncode, 1)
            combined = failed.stdout + failed.stderr + (report_dir / "state.json").read_text()
            self.assertNotIn("opaque-remote-secret-marker", combined)
            state = json.loads((report_dir / "state.json").read_text())
            self.assertEqual(state["submission"]["category"], "remote-duplicate-check")

    def test_feedback_uncertain_create_requires_explicit_remote_recheck(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "uncertain-project"
            self.assertEqual(run_cli(CLI, "init", str(target)).returncode, 0)
            self.assertEqual(self.feedback_draft(target / "bin/vibe", target).returncode, 0)
            report_dir = next((target / ".vibe/local/feedback").glob("fb-*"))
            review = run_cli(
                target / "bin/vibe",
                "feedback",
                "review",
                report_dir.name,
                "--target",
                str(target),
            )
            review_hash = re.search(
                r"Review hash: (sha256:[a-f0-9]{64})", review.stdout
            )
            self.assertIsNotNone(review_hash)

            fake_bin = base / "fake-bin"
            fake_bin.mkdir()
            fake_gh = fake_bin / "gh"
            fake_gh.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, pathlib, sys\n"
                "args = sys.argv[1:]\n"
                "count = pathlib.Path(os.environ['FAKE_GH_COUNT'])\n"
                "if args[:2] == ['auth', 'status']:\n"
                "    raise SystemExit(0)\n"
                "if args[:2] == ['issue', 'list']:\n"
                "    print(json.dumps([]))\n"
                "    raise SystemExit(0)\n"
                "if args[:2] == ['issue', 'create']:\n"
                "    current = int(count.read_text()) if count.exists() else 0\n"
                "    count.write_text(str(current + 1))\n"
                "    print('opaque-create-secret-marker', file=sys.stderr)\n"
                "    raise SystemExit(9)\n"
                "raise SystemExit(8)\n"
            )
            fake_gh.chmod(0o755)
            count_path = base / "create-count"
            env = {
                "PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", ""),
                "FAKE_GH_COUNT": str(count_path),
            }
            submit_args = (
                "feedback",
                "submit",
                report_dir.name,
                "--target",
                str(target),
                "--confirm",
                review_hash.group(1),
            )
            uncertain = run_cli(target / "bin/vibe", *submit_args, env=env)
            self.assertEqual(uncertain.returncode, 1)
            self.assertEqual(count_path.read_text(), "1")
            state_path = report_dir / "state.json"
            combined = uncertain.stdout + uncertain.stderr + state_path.read_text()
            self.assertNotIn("opaque-create-secret-marker", combined)
            self.assertEqual(json.loads(state_path.read_text())["status"], "submission-unknown")

            blind_retry = run_cli(target / "bin/vibe", *submit_args, env=env)
            self.assertEqual(blind_retry.returncode, 2)
            self.assertIn("run feedback check", blind_retry.stderr)
            self.assertEqual(count_path.read_text(), "1")

            checked = run_cli(
                target / "bin/vibe",
                "feedback",
                "check",
                report_dir.name,
                "--target",
                str(target),
                env=env,
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(json.loads(state_path.read_text())["status"], "review-ready")
            checked_retry = run_cli(target / "bin/vibe", *submit_args, env=env)
            self.assertEqual(checked_retry.returncode, 1)
            self.assertEqual(count_path.read_text(), "2")

    def test_v070_official_v030_bridge_is_exact_create_only_and_preserves_onboarding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            project = base / "official-v030"
            archive = subprocess.run(
                ["git", "archive", "--format=tar", "v0.3.0"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            project.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
                bundle.extractall(project)
            before = file_snapshot(project)

            planned = run_cli(
                CLI, "plan", "upgrade", str(project), "--format", "json",
                "--source-type", "local-payload", "--source-ref", KIT_VERSION,
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)
            self.assertEqual(file_snapshot(project), before)
            plan_receipt = json.loads(planned.stdout)
            self.assertEqual(plan_receipt["schema_version"], 2)
            self.assertEqual(plan_receipt["onboarding_bridge"]["state"], "planned")
            self.assertEqual(
                plan_receipt["onboarding_bridge"]["family"],
                "official-v0.3.0-pre-onboarding-v1",
            )

            upgraded = run_cli(
                CLI, "upgrade", str(project), "--format", "json",
                "--source-type", "local-payload", "--source-ref", KIT_VERSION,
            )
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            receipt = json.loads(upgraded.stdout)
            self.assertEqual(receipt["transaction"]["outcome"], "committed")
            self.assertEqual(receipt["onboarding_bridge"]["state"], "applied")
            self.assertEqual(
                (project / ".vibe/onboarding.json").read_bytes(),
                b'{"schema_version":1,"status":"pending"}\n',
            )
            doctor = run_cli(
                project / "bin/vibe", "doctor", str(project), "--format", "json"
            )
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)

    def test_v070_upgrade_write_failure_rolls_back_and_committed_cleanup_recovers(self) -> None:
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            rolled_back_target = base / "rolled-back"
            self.assertEqual(run_cli(CLI, "init", str(rolled_back_target)).returncode, 0)
            before = file_snapshot(rolled_back_target)
            original_write = module.mutate_leaf_forward
            writes = 0

            def fail_second_write(project, adapter, item, temporary):
                nonlocal writes
                writes += 1
                if writes == 2:
                    raise PermissionError("controlled write failure")
                return original_write(project, adapter, item, temporary)

            output = io.StringIO()
            with mock.patch.object(
                module, "mutate_leaf_forward", new=fail_second_write
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    rolled_back_target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(receipt["write_state"], "rolled-back")
            self.assertEqual(receipt["installation_state"], "predecessor")
            self.assertEqual(file_snapshot(rolled_back_target), before)

            committed_target = base / "committed"
            self.assertEqual(run_cli(CLI, "init", str(committed_target)).returncode, 0)
            original_remove = module.remove_transaction_control
            attempts = 0

            def fail_first_cleanup(target):
                nonlocal attempts
                attempts += 1
                if attempts == 1:
                    raise PermissionError("controlled cleanup failure")
                return original_remove(target)

            output = io.StringIO()
            with mock.patch.object(
                module, "remove_transaction_control", side_effect=fail_first_cleanup
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    committed_target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(receipt["installation_state"], "target")
            self.assertEqual(receipt["transaction"]["outcome"], "committed")
            self.assertTrue(
                (committed_target / ".vibe/local/upgrade-transactions/active").is_dir()
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                recovery_code = module.recover_upgrade(committed_target, "json")
            self.assertEqual(recovery_code, 0)
            recovery = json.loads(output.getvalue())
            self.assertEqual(recovery["transaction"]["outcome"], "committed")
            self.assertEqual(recovery["installation_state"], "target")
            self.assertFalse(
                (committed_target / ".vibe/local/upgrade-transactions/active").exists()
            )

    def test_v070_transaction_control_symlink_blocks_without_any_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "project"
            external = base / "external-control"
            self.assertEqual(run_cli(CLI, "init", str(target)).returncode, 0)
            external.mkdir()
            control = target / ".vibe/local/upgrade-transactions"
            control.parent.mkdir(parents=True, exist_ok=True)
            if control.exists():
                control.rmdir()
            control.symlink_to(external, target_is_directory=True)
            before = file_snapshot(target)

            commands = [
                run_cli(
                    CLI, "plan", "upgrade", str(target), "--format", "json",
                    "--source-type", "local-payload", "--source-ref", KIT_VERSION,
                ),
                run_cli(
                    CLI, "upgrade", str(target), "--format", "json",
                    "--source-type", "local-payload", "--source-ref", KIT_VERSION,
                ),
                run_cli(
                    target / "bin/vibe", "recover-upgrade", str(target),
                    "--format", "json",
                ),
                run_cli(
                    target / "bin/vibe", "doctor", str(target), "--format", "json"
                ),
            ]
            self.assertEqual([item.returncode for item in commands], [2, 2, 2, 1])
            for command in commands:
                receipt = json.loads(command.stdout)
                self.assertEqual(receipt["write_state"], "none")
                self.assertFalse(receipt["writes_performed"])
                self.assertEqual(receipt["installation_state"], "unknown")
                self.assertEqual(
                    receipt["next_action"]["code"], "inspect-upgrade-transaction"
                )
            self.assertEqual(file_snapshot(target), before)
            self.assertEqual(list(external.iterdir()), [])
            self.assertTrue(control.is_symlink())

    def test_v070_publication_plan_and_validation_are_closed_and_offline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / "source"
            cli = copy_source(source)
            subprocess.run(
                ["git", "init", "-b", "main"], cwd=source, check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Release Test"],
                cwd=source, check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "release@example.invalid"],
                cwd=source, check=True,
            )
            subprocess.run(["git", "add", "-A"], cwd=source, check=True)
            subprocess.run(
                ["git", "commit", "-m", "v0.7 publication fixture"],
                cwd=source, check=True, capture_output=True,
            )
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=source, check=True,
                text=True, capture_output=True,
            ).stdout.strip()
            candidate = base / "candidate"
            built = run_cli(
                cli, "package", "--status", "prerelease", "--output", str(candidate)
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            distribution_sha = hashlib.sha256(
                (candidate / DISTRIBUTION_ARCHIVE).read_bytes()
            ).hexdigest()
            body_sha = hashlib.sha256(
                (source / "docs/releases/0.7.0.md").read_bytes()
            ).hexdigest()
            allowed_operations = [
                "fast-forward-main",
                "create-or-confirm-annotated-tag",
                "create-or-confirm-prerelease",
                "upload-or-confirm-five-assets",
                "read-back-publication",
                "download-and-verify-public-assets",
                "conditionally-comment-and-close-issues-1-through-5",
            ]
            publish_operations = allowed_operations[:-1]
            request = {
                "schema_version": 1,
                "kind": "vibe-kit-publication",
                "repository": {
                    "owner": "mintgao",
                    "name": "vibe-kit",
                    "canonical_url": "https://github.com/mintgao/vibe-kit",
                },
                "version": "0.7.0",
                "source_commit": commit,
                "main": {
                    "branch": "main",
                    "expected_old_oid": "a" * 40,
                    "target_oid": commit,
                    "policy": "fast-forward-cas-only",
                },
                "tag": {
                    "name": "v0.7.0",
                    "object_type": "tag",
                    "expected_tag_object_oid": "b" * 40,
                    "target_commit": commit,
                    "tagger_name": "Release Test",
                    "tagger_email": "release@example.invalid",
                    "tagger_timestamp": "2026-08-31T12:00:00Z",
                    "tagger_timezone": "+0800",
                    "message_sha256": "c" * 64,
                },
                "release": {
                    "title": "Vibe Kit v0.7.0",
                    "body_sha256": body_sha,
                    "body_source_path": "docs/releases/0.7.0.md",
                    "draft": False,
                    "prerelease": True,
                    "generated_notes": False,
                    "platform_immutability_required": False,
                },
                "assets": [],
                "asset_set_sha256": "0" * 64,
                "local_gates": {
                    "source_clean": True,
                    "source_commit_verified": True,
                    "qa_passed": True,
                    "package_a_sha256": distribution_sha,
                    "package_b_sha256": distribution_sha,
                    "byte_identical": True,
                    "validate_release_passed": True,
                },
                "remote_snapshot": {
                    "observed_at": "2026-08-31T12:01:00Z",
                    "main_oid": "a" * 40,
                    "tag_state": "absent",
                    "tag_oid": None,
                    "release_state": "absent",
                    "release_id": None,
                    "asset_set": [],
                },
                "operations": [
                    {
                        "sequence": index,
                        "operation_id": f"publish-{index}",
                        "kind": kind,
                        "natural_key": f"mintgao/vibe-kit:{kind}",
                        "expected_precondition": {
                            "kind": "exact-remote-snapshot",
                            "identity_sha256": hashlib.sha256(kind.encode()).hexdigest(),
                        },
                        "max_write_attempts": 2,
                    }
                    for index, kind in enumerate(publish_operations)
                ],
                "authorization_scope": {
                    "repository": "mintgao/vibe-kit",
                    "version": "0.7.0",
                    "release_kind": "prerelease",
                    "allowed_operations": allowed_operations,
                    "destructive_operations_allowed": False,
                },
                "issue_closeout_policy": {
                    "issues": [1, 2, 3, 4, 5],
                    "requires_public_verification": True,
                    "requires_separate_closeout_intent": True,
                    "requires_separate_closeout_authorization": True,
                },
                "recovery_policy": {
                    "read_back_before_retry": True,
                    "delete": False,
                    "replace": False,
                    "force": False,
                },
            }
            request_path = base / "request.json"
            request_path.write_text(json.dumps(request, indent=2) + "\n")
            candidate_before = file_snapshot(candidate)
            planned = run_cli(
                cli, "publication-plan", "--phase", "publish",
                "--request", str(request_path), "--candidate", str(candidate),
                "--format", "json",
            )
            self.assertEqual(planned.returncode, 0, planned.stdout + planned.stderr)
            self.assertEqual(file_snapshot(candidate), candidate_before)
            plan = json.loads(planned.stdout)
            self.assertEqual(plan["status"], "safe")
            self.assertFalse(plan["network_used"])
            intent = plan["intent"]
            intent_path = base / "intent.json"
            intent_path.write_text(json.dumps(intent, indent=2) + "\n")

            assets = [
                {
                    **item,
                    "id": index + 1,
                    "url": f"https://github.com/mintgao/vibe-kit/releases/download/v0.7.0/{item['name']}",
                    "write_state": "confirmed-complete",
                    "read_back": True,
                }
                for index, item in enumerate(intent["assets"])
            ]
            receipt = {
                "schema_version": 1,
                "kind": "vibe-kit-publication-receipt",
                "intent_sha256": plan["intent_sha256"],
                "authorization_id": "authorization-v070",
                "host_operation_id": "host-operation-v070",
                "repository": "mintgao/vibe-kit",
                "remote_write_state": "confirmed-complete",
                "verification_state": "passed",
                "main": {
                    "branch": "main", "expected_old_oid": "a" * 40,
                    "target_oid": commit, "observed_oid": commit,
                    "write_state": "confirmed-complete", "read_back": True,
                },
                "tag": {
                    "name": "v0.7.0", "expected_tag_object_oid": "b" * 40,
                    "observed_ref_oid": "b" * 40, "peeled_commit": commit,
                    "write_state": "confirmed-complete", "read_back": True,
                },
                "release": {
                    "id": 70,
                    "url": "https://github.com/mintgao/vibe-kit/releases/tag/v0.7.0",
                    "tag": "v0.7.0", "title": "Vibe Kit v0.7.0",
                    "body_sha256": body_sha, "draft": False, "prerelease": True,
                    "immutable": "unknown", "write_state": "confirmed-complete",
                    "read_back": True,
                },
                "assets": assets,
                "operations": [
                    {
                        "sequence": item["sequence"],
                        "operation_id": item["operation_id"],
                        "kind": item["kind"],
                        "natural_key": item["natural_key"],
                        "write_attempts": 1,
                        "initial_response": "definite-success",
                        "read_back_result": "match",
                        "outcome": (
                            "uploaded" if item["kind"] == "upload-or-confirm-five-assets"
                            else "created"
                        ),
                        "remote_object_id": f"remote-{item['sequence']}",
                        "error": None,
                    }
                    for item in intent["operations"]
                ],
                "downloads": [
                    {
                        "name": item["name"], "size": item["size"],
                        "sha256": item["sha256"], "matched": True,
                    }
                    for item in intent["assets"]
                ],
                "validate_release": {"status": "valid", "receipt_sha256": "d" * 64},
                "smokes": [
                    {"name": "direct-init-doctor", "status": "passed", "evidence_sha256": "e" * 64},
                    {"name": "plugin-bundled", "status": "passed", "evidence_sha256": "f" * 64},
                ],
                "limitations": ["Host authenticity is retained as live public evidence."],
                "issue_closeout": None,
                "error": None,
            }
            receipt_path = base / "receipt.json"
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
            validated = run_cli(
                cli, "validate-publication", "--intent", str(intent_path),
                "--receipt", str(receipt_path), "--candidate", str(candidate),
                "--format", "json",
            )
            self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
            validation = json.loads(validated.stdout)
            self.assertEqual(validation["status"], "valid")
            self.assertFalse(validation["network_used"])
            self.assertFalse(validation["host_evidence_authenticated"])

            duplicate_asset = json.loads(json.dumps(receipt))
            duplicate_asset["assets"].append(dict(duplicate_asset["assets"][0]))
            receipt_path.write_text(json.dumps(duplicate_asset, indent=2) + "\n")
            rejected_asset_duplicate = run_cli(
                cli, "validate-publication", "--intent", str(intent_path),
                "--receipt", str(receipt_path), "--candidate", str(candidate),
                "--format", "json",
            )
            self.assertEqual(rejected_asset_duplicate.returncode, 1)
            self.assertEqual(
                json.loads(rejected_asset_duplicate.stdout)["status"], "invalid"
            )

            duplicate_download = json.loads(json.dumps(receipt))
            duplicate_download["downloads"].append(
                dict(duplicate_download["downloads"][0])
            )
            receipt_path.write_text(json.dumps(duplicate_download, indent=2) + "\n")
            rejected_download_duplicate = run_cli(
                cli, "validate-publication", "--intent", str(intent_path),
                "--receipt", str(receipt_path), "--candidate", str(candidate),
                "--format", "json",
            )
            self.assertEqual(rejected_download_duplicate.returncode, 1)
            self.assertEqual(
                json.loads(rejected_download_duplicate.stdout)["status"], "invalid"
            )

            receipt["downloads"][0]["matched"] = False
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
            rejected = run_cli(
                cli, "validate-publication", "--intent", str(intent_path),
                "--receipt", str(receipt_path), "--candidate", str(candidate),
                "--format", "json",
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertEqual(json.loads(rejected.stdout)["status"], "invalid")

    def test_v070_interrupted_prepare_recovers_and_tampered_stage_stays_fail_closed(self) -> None:
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            interrupted = base / "interrupted"
            self.assertEqual(run_cli(CLI, "init", str(interrupted)).returncode, 0)
            before = file_snapshot(interrupted)
            with module.ProjectRootFD(interrupted) as project:
                change = module.upgrade_change(
                    project,
                    0,
                    ".vibe/version",
                    (KIT_VERSION + "\n").encode(),
                    0o644,
                )
            original_private_bytes = module.write_private_bytes

            def interrupt_stage(project, relative, content):
                if "/stage/" in relative:
                    raise KeyboardInterrupt("controlled interruption")
                return original_private_bytes(project, relative, content)

            with mock.patch.object(
                module, "write_private_bytes", side_effect=interrupt_stage
            ):
                with self.assertRaises(KeyboardInterrupt):
                    module.prepare_transaction_state(
                        interrupted, KIT_VERSION, KIT_VERSION, [change]
                    )
            kind, shape = module.active_transaction_state(interrupted)
            self.assertEqual(kind, "unprepared")
            self.assertIsNotNone(shape["transaction_id"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = module.recover_upgrade(interrupted, "json")
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["installation_state"], "predecessor")
            self.assertEqual(file_snapshot(interrupted), before)

            diverged = base / "diverged-unprepared"
            self.assertEqual(run_cli(CLI, "init", str(diverged)).returncode, 0)
            with module.ProjectRootFD(diverged) as project:
                change = module.upgrade_change(
                    project, 0, ".vibe/version", (KIT_VERSION + "\n").encode(), 0o644
                )
            with mock.patch.object(
                module, "write_private_bytes", side_effect=interrupt_stage
            ):
                with self.assertRaises(KeyboardInterrupt):
                    module.prepare_transaction_state(
                        diverged, KIT_VERSION, KIT_VERSION, [change]
                    )
            active_diverged = diverged / ".vibe/local/upgrade-transactions/active"
            evidence_before = file_snapshot(active_diverged)
            (diverged / ".vibe/version").write_text("external-divergence\n")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = module.recover_upgrade(diverged, "json")
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(receipt["status"], "blocked")
            self.assertEqual(receipt["write_state"], "none")
            self.assertFalse(receipt["writes_performed"])
            self.assertEqual(receipt["installation_state"], "unknown")
            self.assertEqual(receipt["transaction"]["outcome"], "unknown-partial")
            self.assertEqual(receipt["transaction"]["failed_path"], ".vibe/version")
            self.assertEqual(
                receipt["next_action"]["code"], "inspect-upgrade-transaction"
            )
            self.assertEqual(file_snapshot(active_diverged), evidence_before)
            self.assertEqual(
                (diverged / ".vibe/version").read_text(), "external-divergence\n"
            )

            tampered = base / "tampered"
            self.assertEqual(run_cli(CLI, "init", str(tampered)).returncode, 0)
            with module.ProjectRootFD(tampered) as project:
                change = module.upgrade_change(
                    project,
                    0,
                    ".vibe/version",
                    (KIT_VERSION + "\n").encode(),
                    0o644,
                )
            module.prepare_transaction_state(
                tampered, KIT_VERSION, KIT_VERSION, [change]
            )
            active = tampered / ".vibe/local/upgrade-transactions/active"
            (active / "stage/0000").write_bytes(b"tampered\n")
            target_before_recovery = (tampered / ".vibe/version").read_bytes()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = module.recover_upgrade(tampered, "json")
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(receipt["transaction"]["outcome"], "unknown-partial")
            self.assertEqual(receipt["write_state"], "none")
            self.assertEqual(
                (tampered / ".vibe/version").read_bytes(), target_before_recovery
            )
            self.assertTrue(active.is_dir())

    def test_v070_commit_marker_is_irreversible_and_target_cas_rechecks_leaf(self) -> None:
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            committed = base / "commit-event-failure"
            self.assertEqual(run_cli(CLI, "init", str(committed)).returncode, 0)
            original_append = module.append_transaction_event

            def fail_commit_event(project, transaction_id, phase, previous):
                if phase == "commit-complete":
                    raise PermissionError("controlled commit event failure")
                return original_append(project, transaction_id, phase, previous)

            output = io.StringIO()
            with mock.patch.object(
                module, "append_transaction_event", side_effect=fail_commit_event
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    committed, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(receipt["installation_state"], "target")
            self.assertEqual(receipt["transaction"]["outcome"], "committed")
            self.assertEqual(
                receipt["summary"],
                "Target upgrade committed; transaction cleanup remains and must be finalized with recover-upgrade.",
            )
            active = committed / ".vibe/local/upgrade-transactions/active"
            self.assertTrue((active / "commit.json").is_file())
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                recovery_code = module.recover_upgrade(committed, "json")
            self.assertEqual(recovery_code, 0)
            recovery = json.loads(output.getvalue())
            self.assertEqual(recovery["installation_state"], "target")
            self.assertEqual(recovery["transaction"]["outcome"], "committed")
            self.assertFalse(active.exists())

            raced = base / "cas-race"
            self.assertEqual(run_cli(CLI, "init", str(raced)).returncode, 0)
            original_exchange = module.LeafAtomicityAdapter.exchange
            injected = False
            external_manifest = b'{"external":"writer"}\n'

            def race_manifest(instance, source_parent, source, destination_parent, destination):
                nonlocal injected
                if destination == "manifest.json" and not injected:
                    injected = True
                    (raced / ".vibe/manifest.json").write_bytes(external_manifest)
                return original_exchange(
                    instance, source_parent, source, destination_parent, destination
                )

            output = io.StringIO()
            with mock.patch.object(
                module.LeafAtomicityAdapter, "exchange", new=race_manifest
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    raced, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertTrue(injected)
            self.assertEqual(receipt["transaction"]["outcome"], "unknown-partial")
            self.assertEqual(receipt["installation_state"], "unknown")
            self.assertEqual(
                receipt["next_action"]["code"], "inspect-upgrade-transaction"
            )
            self.assertEqual((raced / ".vibe/manifest.json").read_bytes(), external_manifest)
            self.assertFalse(
                (raced / ".vibe/local/upgrade-transactions/active/commit.json").exists()
            )

    def test_v070_final_leaf_rename_window_races_are_losslessly_preserved(self) -> None:
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)

            onboarding_target = base / "onboarding-race"
            archive = subprocess.run(
                ["git", "archive", "--format=tar", "v0.3.0"],
                cwd=ROOT, check=True, capture_output=True,
            ).stdout
            onboarding_target.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
                bundle.extractall(onboarding_target)
            external_onboarding = b'{"schema_version":1,"status":"complete","evidence":["external"]}\n'
            original_link = module.ProjectRootFD.link_no_clobber
            linked = False

            def link_race(instance, source, destination):
                nonlocal linked
                if destination == ".vibe/onboarding.json" and not linked:
                    linked = True
                    (onboarding_target / ".vibe/onboarding.json").write_bytes(
                        external_onboarding
                    )
                return original_link(instance, source, destination)

            output = io.StringIO()
            with mock.patch.object(
                module.ProjectRootFD, "link_no_clobber", new=link_race
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    onboarding_target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertTrue(linked, output.getvalue())
            self.assertEqual(receipt["error"]["code"], "upgrade_leaf_race_preserved")
            self.assertEqual(receipt["transaction"]["outcome"], "unknown-partial")
            self.assertEqual(receipt["write_state"], "unknown-partial")
            self.assertEqual(
                receipt["next_action"]["code"], "inspect-upgrade-transaction"
            )
            self.assertEqual(
                (onboarding_target / ".vibe/onboarding.json").read_bytes(),
                external_onboarding,
            )
            self.assertFalse(
                (onboarding_target / ".vibe/local/upgrade-transactions/active/commit.json").exists()
            )

            manifest_target = base / "manifest-race"
            self.assertEqual(run_cli(CLI, "init", str(manifest_target)).returncode, 0)
            external_manifest = b'{"external":"rename-window"}\n'
            original_exchange = module.LeafAtomicityAdapter.exchange
            exchanged = False

            def exchange_race(instance, source_parent, source, destination_parent, destination):
                nonlocal exchanged
                if destination == "manifest.json" and not exchanged:
                    exchanged = True
                    (manifest_target / ".vibe/manifest.json").write_bytes(
                        external_manifest
                    )
                return original_exchange(
                    instance, source_parent, source, destination_parent, destination
                )

            output = io.StringIO()
            with mock.patch.object(
                module.LeafAtomicityAdapter, "exchange", new=exchange_race
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    manifest_target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertTrue(exchanged)
            self.assertEqual(receipt["error"]["code"], "upgrade_leaf_race_preserved")
            self.assertEqual(receipt["installation_state"], "unknown")
            self.assertEqual(receipt["transaction"]["failure_kind"], "external-leaf-race-preserved")
            self.assertEqual(
                (manifest_target / ".vibe/manifest.json").read_bytes(),
                external_manifest,
            )

            rollback_target = base / "onboarding-rollback-race"
            rollback_target.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
                bundle.extractall(rollback_target)
            original_mutate = module.mutate_leaf_forward
            original_no_replace = module.LeafAtomicityAdapter.no_replace
            rollback_raced = False
            rollback_external = b'{"schema_version":1,"status":"complete","evidence":["rollback-race"]}\n'

            def fail_after_onboarding(project, adapter, item, temporary):
                if item["path"] == ".vibe/manifest.json":
                    raise PermissionError("force absent-leaf rollback")
                return original_mutate(project, adapter, item, temporary)

            def race_absent_rollback(instance, source_parent, source, destination_parent, destination):
                nonlocal rollback_raced
                if source == "onboarding.json" and not rollback_raced:
                    rollback_raced = True
                    (rollback_target / ".vibe/onboarding.json").write_bytes(
                        rollback_external
                    )
                return original_no_replace(
                    instance, source_parent, source, destination_parent, destination
                )

            output = io.StringIO()
            with mock.patch.object(
                module, "mutate_leaf_forward", new=fail_after_onboarding
            ), mock.patch.object(
                module.LeafAtomicityAdapter, "no_replace", new=race_absent_rollback
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    rollback_target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertTrue(rollback_raced)
            self.assertEqual(receipt["error"]["code"], "upgrade_leaf_race_preserved")
            self.assertEqual(receipt["transaction"]["outcome"], "unknown-partial")
            self.assertEqual(
                (rollback_target / ".vibe/onboarding.json").read_bytes(),
                rollback_external,
            )

    def test_v070_absent_parent_directory_unit_is_prepared_and_no_clobber(self) -> None:
        module = load_cli_module()

        def official_v060_project(path: Path) -> None:
            archive = subprocess.run(
                ["git", "archive", "--format=tar", "v0.6.0"],
                cwd=ROOT, check=True, capture_output=True,
            ).stdout
            path.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
                bundle.extractall(path)

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            committed = base / "directory-unit-committed"
            official_v060_project(committed)
            original_remove = module.remove_transaction_control
            attempts = 0

            def retain_committed_control(target):
                nonlocal attempts
                attempts += 1
                if attempts == 1:
                    raise PermissionError("retain exact committed journal")
                return original_remove(target)

            output = io.StringIO()
            with mock.patch.object(
                module, "remove_transaction_control", new=retain_committed_control
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    committed, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(receipt["transaction"]["outcome"], "committed")
            active = committed / ".vibe/local/upgrade-transactions/active"
            intent = json.loads((active / "intent.json").read_text())
            prepared = json.loads((active / "prepared.json").read_text())
            capabilities = json.loads((active / "capabilities.json").read_text())
            commit = json.loads((active / "commit.json").read_text())
            self.assertEqual(len(intent["directory_units"]), 1)
            unit = intent["directory_units"][0]
            self.assertEqual(unit["final_root"], ".agents/skills/vibe-release")
            self.assertEqual(unit["protocol"], "directory-no-clobber-v1")
            self.assertEqual(unit["directories"][0]["mode"], 0o755)
            self.assertEqual(set(unit["parent_object"]), {"device", "inode"})
            self.assertEqual(
                prepared["directory_postimage_set_sha256"],
                intent["directory_postimage_set_sha256"],
            )
            self.assertEqual(
                commit["directory_postimage_set_sha256"],
                intent["directory_postimage_set_sha256"],
            )
            self.assertEqual(
                capabilities["probe_set_sha256"],
                hashlib.sha256(
                    json.dumps(
                        {
                            "leaf_capability_probes": intent["leaf_capability_probes"],
                            "directory_capability_probes": intent["directory_capability_probes"],
                        },
                        sort_keys=True, separators=(",", ":"),
                    ).encode()
                ).hexdigest(),
            )
            self.assertTrue(
                (committed / ".agents/skills/vibe-release/SKILL.md").is_file()
            )
            prepared_bytes = (active / "prepared.json").read_bytes()
            invalid_prepared = dict(prepared)
            invalid_prepared["directory_postimage_set_sha256"] = "0" * 64
            (active / "prepared.json").write_text(
                json.dumps(invalid_prepared, sort_keys=True, separators=(",", ":"))
                + "\n"
            )
            invalid_kind, _ = module.active_transaction_state(committed)
            self.assertEqual(invalid_kind, "invalid")
            (active / "prepared.json").write_bytes(prepared_bytes)
            valid_kind, _ = module.active_transaction_state(committed)
            self.assertEqual(valid_kind, "committed")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                recovery_code = module.recover_upgrade(committed, "json")
            self.assertEqual(recovery_code, 0)
            self.assertFalse(active.exists())

            raced = base / "directory-unit-race"
            official_v060_project(raced)
            original_no_replace = module.LeafAtomicityAdapter.no_replace
            injected = False

            def directory_race(instance, source_parent, source, destination_parent, destination):
                nonlocal injected
                if destination == "vibe-release" and not injected:
                    injected = True
                    external = raced / ".agents/skills/vibe-release"
                    external.mkdir()
                    (external / "external.txt").write_text("third-party\n")
                return original_no_replace(
                    instance, source_parent, source, destination_parent, destination
                )

            output = io.StringIO()
            with mock.patch.object(
                module.LeafAtomicityAdapter, "no_replace", new=directory_race
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    raced, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertTrue(injected)
            self.assertEqual(
                receipt["error"]["code"], "upgrade_directory_race_preserved"
            )
            self.assertEqual(receipt["transaction"]["outcome"], "unknown-partial")
            self.assertEqual(
                receipt["transaction"]["failure_kind"],
                "external-directory-race-preserved",
            )
            self.assertEqual(receipt["write_state"], "unknown-partial")
            self.assertTrue(receipt["writes_performed"])
            self.assertEqual(receipt["installation_state"], "unknown")
            self.assertEqual(
                receipt["transaction"]["failed_path"],
                ".agents/skills/vibe-release",
            )
            self.assertEqual(
                receipt["next_action"]["code"], "inspect-upgrade-transaction"
            )
            self.assertEqual(
                (raced / ".agents/skills/vibe-release/external.txt").read_text(),
                "third-party\n",
            )
            self.assertFalse(
                (raced / ".vibe/local/upgrade-transactions/active/commit.json").exists()
            )

            for winner_kind in ("file", "symlink"):
                raced_entry = base / f"directory-unit-{winner_kind}-race"
                official_v060_project(raced_entry)
                injected = False

                def entry_race(
                    instance, source_parent, source, destination_parent,
                    destination,
                ):
                    nonlocal injected
                    if destination == "vibe-release" and not injected:
                        injected = True
                        winner = raced_entry / ".agents/skills/vibe-release"
                        if winner_kind == "file":
                            winner.write_bytes(b"third-party-file\n")
                        else:
                            winner.symlink_to("third-party-symlink-target")
                    return original_no_replace(
                        instance, source_parent, source,
                        destination_parent, destination,
                    )

                output = io.StringIO()
                with mock.patch.object(
                    module.LeafAtomicityAdapter,
                    "no_replace",
                    new=entry_race,
                ), contextlib.redirect_stdout(output):
                    code = module.upgrade(
                        raced_entry, "json", "local-payload", KIT_VERSION, None
                    )
                self.assertEqual(code, 2, output.getvalue())
                receipt = json.loads(output.getvalue())
                self.assertTrue(injected)
                self.assertEqual(receipt["status"], "error")
                self.assertEqual(receipt["write_state"], "unknown-partial")
                self.assertTrue(receipt["writes_performed"])
                self.assertEqual(receipt["installation_state"], "unknown")
                self.assertEqual(
                    receipt["error"]["code"],
                    "upgrade_directory_race_preserved",
                )
                self.assertEqual(
                    receipt["transaction"]["outcome"], "unknown-partial"
                )
                self.assertEqual(receipt["transaction"]["phase"], "invalid")
                self.assertEqual(
                    receipt["transaction"]["failed_path"],
                    ".agents/skills/vibe-release",
                )
                self.assertEqual(
                    receipt["transaction"]["failure_kind"],
                    "external-directory-race-preserved",
                )
                self.assertEqual(
                    receipt["next_action"]["code"],
                    "inspect-upgrade-transaction",
                )
                active = (
                    raced_entry
                    / ".vibe/local/upgrade-transactions/active"
                )
                self.assertTrue(active.is_dir())
                evidence = file_snapshot(active)
                winner = raced_entry / ".agents/skills/vibe-release"
                if winner_kind == "file":
                    self.assertEqual(winner.read_bytes(), b"third-party-file\n")
                else:
                    self.assertTrue(winner.is_symlink())
                    self.assertEqual(
                        os.readlink(winner), "third-party-symlink-target"
                    )

                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    recovery_code = module.recover_upgrade(raced_entry, "json")
                self.assertEqual(recovery_code, 2)
                recovery = json.loads(output.getvalue())
                self.assertEqual(recovery["status"], "blocked")
                self.assertEqual(recovery["write_state"], "none")
                self.assertFalse(recovery["writes_performed"])
                self.assertEqual(recovery["installation_state"], "unknown")
                self.assertEqual(
                    recovery["error"]["code"],
                    "upgrade_directory_race_preserved",
                )
                self.assertEqual(
                    recovery["transaction"]["failed_path"],
                    ".agents/skills/vibe-release",
                )
                self.assertEqual(
                    recovery["transaction"]["failure_kind"],
                    "external-directory-race-preserved",
                )
                self.assertEqual(file_snapshot(active), evidence)

                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    doctor_code = module.doctor(raced_entry, "json")
                self.assertEqual(doctor_code, 1)
                doctor = json.loads(output.getvalue())
                self.assertEqual(doctor["status"], "broken")
                self.assertEqual(doctor["write_state"], "none")
                self.assertFalse(doctor["writes_performed"])
                self.assertIn(
                    "upgrade-transaction-active",
                    [item["code"] for item in doctor["diagnostics"]],
                )
                if winner_kind == "file":
                    self.assertEqual(winner.read_bytes(), b"third-party-file\n")
                else:
                    self.assertEqual(
                        os.readlink(winner), "third-party-symlink-target"
                    )

    def test_v070_leaf_atomicity_adapter_real_and_missing_symbol_paths(self) -> None:
        module = load_cli_module()
        adapter = module.leaf_atomicity_api_preflight()
        self.assertIn(adapter.system, ("Darwin", "Linux"))

        class MissingLibrary:
            pass

        with self.assertRaises(module.VibeError) as caught:
            module.LeafAtomicityAdapter(system=adapter.system, library=MissingLibrary())
        self.assertEqual(caught.exception.code, "upgrade_leaf_atomicity_unsupported")

        symbol = "renameatx_np" if adapter.system == "Darwin" else "renameat2"

        class UnsupportedFunction:
            def __call__(self, *args):
                ctypes.set_errno(errno.ENOSYS)
                return -1

        class UnsupportedLibrary:
            pass

        library = UnsupportedLibrary()
        setattr(library, symbol, UnsupportedFunction())
        unsupported = module.LeafAtomicityAdapter(
            system=adapter.system, library=library
        )
        with self.assertRaises(OSError) as syscall:
            unsupported.exchange(1, "a", 1, "b")
        mapped = module.atomicity_os_error(syscall.exception)
        self.assertIsInstance(mapped, module.VibeError)
        self.assertEqual(mapped.code, "upgrade_leaf_atomicity_unsupported")

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            self.assertEqual(run_cli(CLI, "init", str(target)).returncode, 0)
            before = file_snapshot(target)
            output = io.StringIO()
            with mock.patch.object(
                module, "transaction_platform_supported", return_value=False
            ), contextlib.redirect_stdout(output):
                plan_code = module.plan(
                    "upgrade", target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(plan_code, 2)
            plan_receipt = json.loads(output.getvalue())
            self.assertEqual(plan_receipt["status"], "blocked")
            self.assertEqual(
                plan_receipt["error"]["code"],
                "upgrade_leaf_atomicity_unsupported",
            )
            self.assertEqual(
                plan_receipt["next_action"]["code"],
                "use-supported-upgrade-filesystem",
            )
            self.assertEqual(file_snapshot(target), before)
            output = io.StringIO()
            with mock.patch.object(
                module, "transaction_platform_supported", return_value=False
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(receipt["status"], "blocked")
            self.assertEqual(
                receipt["error"]["code"], "upgrade_leaf_atomicity_unsupported"
            )
            self.assertEqual(
                receipt["next_action"]["code"],
                "use-supported-upgrade-filesystem",
            )
            self.assertEqual(receipt["write_state"], "none")
            self.assertFalse(receipt["writes_performed"])
            self.assertEqual(file_snapshot(target), before)

            output = io.StringIO()
            with mock.patch.object(
                module,
                "leaf_capability_probe",
                side_effect=module.VibeError(
                    "mock filesystem rejected required flags",
                    "upgrade_leaf_atomicity_unsupported",
                ),
            ), contextlib.redirect_stdout(output):
                code = module.upgrade(
                    target, "json", "local-payload", KIT_VERSION, None
                )
            self.assertEqual(code, 2)
            receipt = json.loads(output.getvalue())
            self.assertEqual(
                receipt["error"]["code"], "upgrade_leaf_atomicity_unsupported"
            )
            self.assertEqual(receipt["write_state"], "transaction-control-written")
            self.assertTrue(receipt["writes_performed"])
            self.assertEqual(receipt["installation_state"], "predecessor")
            self.assertFalse(
                (target / ".vibe/local/upgrade-transactions/active").exists()
            )
            self.assertEqual(file_snapshot(target), before)

    def test_v070_prepared_directory_crash_and_partial_cleanup_resume(self) -> None:
        module = load_cli_module()

        def official_v060_project(path: Path) -> None:
            archive = subprocess.run(
                ["git", "archive", "--format=tar", "v0.6.0"],
                cwd=ROOT, check=True, capture_output=True,
            ).stdout
            path.mkdir()
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
                bundle.extractall(path)

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            interrupted = base / "before-directory-publication"
            official_v060_project(interrupted)
            before = file_snapshot(interrupted)

            def interrupt_directory(*args, **kwargs):
                raise KeyboardInterrupt("after prepared before directory publication")

            with mock.patch.object(
                module, "publish_directory_unit", side_effect=interrupt_directory
            ):
                with self.assertRaises(KeyboardInterrupt):
                    module.upgrade(
                        interrupted, "json", "local-payload", KIT_VERSION, None
                    )
            kind, _ = module.active_transaction_state(interrupted)
            self.assertEqual(kind, "prepared")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = module.recover_upgrade(interrupted, "json")
            self.assertEqual(code, 0, output.getvalue())
            self.assertEqual(file_snapshot(interrupted), before)

            partial = base / "partial-directory-cleanup"
            official_v060_project(partial)
            before = file_snapshot(partial)
            original_mutate = module.mutate_leaf_forward
            original_remove_tree = module.ProjectRootFD.remove_tree
            cleanup_interrupted = False

            def fail_after_directory(project, adapter, item, temporary):
                if item["path"] == ".vibe/manifest.json":
                    raise PermissionError("force rollback after directory publication")
                return original_mutate(project, adapter, item, temporary)

            def interrupt_private_cleanup(
                instance, relative, expected_parent=None
            ):
                nonlocal cleanup_interrupted
                if module.DIRECTORY_STAGE_PREFIX in relative and not cleanup_interrupted:
                    cleanup_interrupted = True
                    private_skill = partial / relative / "SKILL.md"
                    self.assertTrue(private_skill.is_file())
                    private_skill.unlink()
                    raise KeyboardInterrupt("partial prepared-tree cleanup")
                return original_remove_tree(instance, relative, expected_parent)

            with mock.patch.object(
                module, "mutate_leaf_forward", new=fail_after_directory
            ), mock.patch.object(
                module.ProjectRootFD, "remove_tree", new=interrupt_private_cleanup
            ):
                with self.assertRaises(KeyboardInterrupt):
                    module.upgrade(
                        partial, "json", "local-payload", KIT_VERSION, None
                    )
            self.assertTrue(cleanup_interrupted)
            cleanup_markers = list(
                (partial / ".vibe/local/upgrade-transactions/active/directory-cleanup").glob("*.json")
            )
            self.assertEqual(len(cleanup_markers), 1)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = module.recover_upgrade(partial, "json")
            self.assertEqual(code, 0, output.getvalue())
            self.assertEqual(file_snapshot(partial), before)

            reauthenticated = base / "parent-reauthentication"
            (reauthenticated / "managed/.vibe-stage").mkdir(parents=True)
            (reauthenticated / "managed/.vibe-stage/prepared.txt").write_text(
                "prepared\n"
            )
            with module.ProjectRootFD(reauthenticated) as project:
                parent_object = project.directory_object("managed")
                (reauthenticated / "managed").rename(
                    reauthenticated / "detached-managed"
                )
                (reauthenticated / "managed/.vibe-stage").mkdir(parents=True)
                external = reauthenticated / "managed/.vibe-stage/external.txt"
                external.write_text("external\n")
                with self.assertRaises(module.VibeError) as caught:
                    project.remove_tree("managed/.vibe-stage", parent_object)
            self.assertEqual(
                caught.exception.code, "upgrade_directory_race_preserved"
            )
            self.assertEqual(external.read_text(), "external\n")
            self.assertEqual(
                (
                    reauthenticated
                    / "detached-managed/.vibe-stage/prepared.txt"
                ).read_text(),
                "prepared\n",
            )

    def test_v070_closeout_intent_is_exact_monotonic_and_separately_authorized(self) -> None:
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            parent_sha = "1" * 64
            closeout_id = hashlib.sha256(
                json.dumps(
                    {
                        "schema_version": 1,
                        "repository": "mintgao/vibe-kit",
                        "version": "0.7.0",
                        "parent_publication_intent_sha256": parent_sha,
                        "issues": [1, 2, 3, 4, 5],
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            ).hexdigest()
            observations = [
                ("open", "absent", None),
                ("open", "exact", 102),
                ("closed", "exact", 103),
                ("open", "absent", None),
                ("closed", "exact", 105),
            ]
            issues = []
            snapshot_items = []
            for number, (state, marker_state, comment_id) in enumerate(
                observations, start=1
            ):
                marker = f"<!-- vibe-kit:v0.7.0:issue-{number}:{closeout_id} -->"
                body = f"{marker}\nVerified evidence for issue #{number}.\n"
                body_sha = hashlib.sha256(body.encode()).hexdigest()
                issues.append({
                    "issue_number": number,
                    "comment_body": body,
                    "observed_state": state,
                    "observed_matching_comment_id": comment_id,
                    "criterion_evidence_sha256": str(number) * 64,
                })
                snapshot_items.append({
                    "issue_number": number,
                    "state": state,
                    "marker_state": marker_state,
                    "matching_comment_id": comment_id,
                    "matching_comment_body_sha256": (
                        body_sha if marker_state == "exact" else None
                    ),
                })
            operations = []
            for number, snapshot_item in enumerate(snapshot_items, start=1):
                snapshot_sha = hashlib.sha256(
                    json.dumps(
                        snapshot_item, sort_keys=True, separators=(",", ":")
                    ).encode()
                ).hexdigest()
                for offset, kind in enumerate(
                    ("create-exact-evidence-comment", "close-issue")
                ):
                    comment = offset == 0
                    operations.append({
                        "sequence": 2 * (number - 1) + offset,
                        "operation_id": f"issue-{number}-{'comment' if comment else 'close'}",
                        "issue_number": number,
                        "kind": kind,
                        "natural_key": (
                            f"issue:{number}:marker:{closeout_id}"
                            if comment else f"issue:{number}:state:closed"
                        ),
                        "expected_precondition": {
                            "kind": "issue-closeout-monotonic-resume",
                            "initial_snapshot_sha256": snapshot_sha,
                            "allowed_observations": (
                                ["open-absent", "open-exact", "closed-exact"]
                                if comment else ["open-exact", "closed-exact"]
                            ),
                        },
                        "max_write_attempts": 2,
                    })
            scope = {
                "repository": "mintgao/vibe-kit",
                "issues": [1, 2, 3, 4, 5],
                "allowed_operations": [
                    "create-exact-evidence-comment", "close-issue"
                ],
                "destructive_operations_allowed": False,
                "requires_separate_closeout_authorization": True,
            }
            request = {
                "parent_publication_intent_sha256": parent_sha,
                "publication_receipt_sha256": "2" * 64,
                "verification_receipt_sha256": "3" * 64,
                "repository": {
                    "owner": "mintgao",
                    "name": "vibe-kit",
                    "canonical_url": "https://github.com/mintgao/vibe-kit",
                },
                "issues": issues,
                "remote_snapshot": {
                    "observed_at": "2026-08-31T13:00:00Z",
                    "issues": snapshot_items,
                },
                "operations": operations,
                "authorization_scope": scope,
            }
            request_path = base / "closeout-request.json"
            request_path.write_text(json.dumps(request, indent=2) + "\n")
            planned = run_cli(
                CLI, "publication-plan", "--phase", "issue-closeout",
                "--request", str(request_path), "--format", "json",
            )
            self.assertEqual(planned.returncode, 0, planned.stdout + planned.stderr)
            result = json.loads(planned.stdout)
            self.assertEqual(result["status"], "safe")
            intent = result["intent"]
            self.assertEqual(intent["closeout_id"], closeout_id)
            self.assertEqual(intent["operations"], operations)
            self.assertEqual(intent["authorization_scope"], scope)
            self.assertEqual(len(result["comment_bodies"]), 5)

            authorization = {
                "closeout_authorization_id": "closeout-authorization-v070",
                "repository": "mintgao/vibe-kit",
                "issues": [1, 2, 3, 4, 5],
                "allowed_operations": [
                    "create-exact-evidence-comment", "close-issue"
                ],
                "closeout_intent_sha256": result["intent_sha256"],
                "destructive_operations_allowed": False,
            }
            self.assertEqual(
                module.validate_closeout_authorization(authorization, intent), []
            )
            divergent_authorization = dict(authorization)
            divergent_authorization["issues"] = [1, 2, 3, 4]
            self.assertTrue(
                module.validate_closeout_authorization(
                    divergent_authorization, intent
                )
            )

            request["remote_snapshot"]["issues"][0].update({
                "state": "closed",
                "marker_state": "absent",
            })
            request["issues"][0]["observed_state"] = "closed"
            request_path.write_text(json.dumps(request, indent=2) + "\n")
            rejected = run_cli(
                CLI, "publication-plan", "--phase", "issue-closeout",
                "--request", str(request_path), "--format", "json",
            )
            self.assertEqual(rejected.returncode, 2)
            rejected_result = json.loads(rejected.stdout)
            self.assertEqual(rejected_result["status"], "blocked")
            self.assertIsNone(rejected_result["intent_sha256"])


if __name__ == "__main__":
    unittest.main()
