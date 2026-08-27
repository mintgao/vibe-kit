import contextlib
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
            self.assertEqual(plan_receipt["schema_version"], 1)
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
            self.assertEqual(validation_receipt["agent_install_protocol"], 1)
            release_metadata = json.loads((first / "release-manifest.json").read_text())
            self.assertEqual(release_metadata["core_protocol"], 3)
            self.assertEqual(release_metadata["feedback_protocol"], 2)
            self.assertEqual(release_metadata["agent_install_protocol"], 1)
            self.assertEqual(release_metadata["adapters"]["codex"]["version"], 3)

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
            self.assertEqual(install_contract["protocol_version"], 1)
            self.assertEqual(install_contract["kit_version"], KIT_VERSION)
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

            unknown_state_contract = json.loads(
                (ROOT / "agent-install.json").read_text()
            )
            unknown_state_contract["cli"]["command_statuses"]["init"].append(
                "unknown-success"
            )
            contract_cases = {
                "missing": (
                    None,
                    "release ZIP is missing required payload file: agent-install.json",
                ),
                "malformed": (b"{not-json\n", "agent-install.json is malformed"),
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


if __name__ == "__main__":
    unittest.main()
