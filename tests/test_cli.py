import json
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin/vibe"


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
    def feedback_draft(self, cli: Path, target: Path, *extra: str) -> subprocess.CompletedProcess:
        return run_cli(
            cli,
            "feedback",
            "draft",
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

    def test_init_doctor_and_work_item(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "new-project"
            result = run_cli(CLI, "init", str(target), "--name", "Demo Project")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / ".agents/skills/vibe-feature-flow/SKILL.md").is_file())
            self.assertTrue((target / ".codex/agents/vibe-qa.toml").is_file())
            self.assertIn('lifecycle: "new"', (target / ".vibe/project.yaml").read_text())
            self.assertIn('name: "Demo Project"', (target / ".vibe/project.yaml").read_text())

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
            self.assertIn("AC-1", (folders[0] / "brief.md").read_text())
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
            self.assertIn("Target version: 0.3.0", upgrade_plan.stdout)
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

    def test_release_package_is_reproducible_installable_and_tamper_evident(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            first = base / "release-one"
            second = base / "release-two"
            built_first = run_cli(CLI, "package", "--output", str(first))
            self.assertEqual(built_first.returncode, 0, built_first.stderr)
            built_second = run_cli(CLI, "package", "--output", str(second))
            self.assertEqual(built_second.returncode, 0, built_second.stderr)

            for filename in (
                "vibe-kit-0.3.0.zip",
                "vibe-kit-plugin-0.3.0.zip",
                "vibe-kit-distribution-0.3.0.zip",
            ):
                self.assertEqual(
                    hashlib.sha256((first / filename).read_bytes()).hexdigest(),
                    hashlib.sha256((second / filename).read_bytes()).hexdigest(),
                )
            validated = run_cli(CLI, "validate-release", str(first))
            self.assertEqual(validated.returncode, 0, validated.stderr)
            self.assertIn("Network: not used", validated.stdout)

            release_unpack = base / "release-unpacked"
            with zipfile.ZipFile(first / "vibe-kit-0.3.0.zip") as archive:
                archive.extractall(release_unpack)
            release_root = release_unpack / "vibe-kit-0.3.0"
            self.assertIn("MIT License", (release_root / "LICENSE").read_text())
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
            with zipfile.ZipFile(first / "vibe-kit-plugin-0.3.0.zip") as archive:
                archive.extractall(plugin_unpack)
            wrapper = plugin_unpack / "vibe-kit/skills/vibe-bootstrap/scripts/vibe_from_plugin.py"
            plugin_target = base / "new-from-plugin"
            plugin_plan = run_cli(wrapper, "plan", "init", str(plugin_target))
            self.assertEqual(plugin_plan.returncode, 0, plugin_plan.stderr)
            plugin_install = run_cli(wrapper, "init", str(plugin_target))
            self.assertEqual(plugin_install.returncode, 0, plugin_install.stderr)
            plugin_doctor = run_cli(plugin_target / "bin/vibe", "doctor", str(plugin_target))
            self.assertEqual(plugin_doctor.returncode, 0, plugin_doctor.stderr)
            release_manifest = json.loads((new_target / ".vibe/manifest.json").read_text())
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
            self.assertIn("0.3.0", upgraded_doctor.stdout)

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
            archive_path = tampered / "vibe-kit-0.3.0.zip"
            content = archive_path.read_bytes()
            archive_path.write_bytes(content[:-1] + bytes([content[-1] ^ 0x01]))
            rejected = run_cli(CLI, "validate-release", str(tampered))
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("checksum mismatch", rejected.stderr)

    def test_release_validation_rejects_unsafe_archives_and_plugin_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source_release = base / "source-release"
            built = run_cli(CLI, "package", "--output", str(source_release))
            self.assertEqual(built.returncode, 0, built.stderr)

            unsafe = base / "unsafe-release"
            shutil.copytree(source_release, unsafe)
            release_zip = unsafe / "vibe-kit-0.3.0.zip"
            with zipfile.ZipFile(release_zip, "r") as archive:
                original = [(info.filename, archive.read(info)) for info in archive.infolist()]
            with zipfile.ZipFile(release_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, content in original:
                    archive.writestr(name, content)
                archive.writestr("vibe-kit-0.3.0/../escape.txt", "unsafe")
            refresh_release_checksums(unsafe, "vibe-kit-0.3.0.zip")
            unsafe_result = run_cli(CLI, "validate-release", str(unsafe))
            self.assertEqual(unsafe_result.returncode, 1)
            self.assertIn("unsafe archive path", unsafe_result.stderr)

            drifted = base / "drifted-release"
            shutil.copytree(source_release, drifted)
            plugin_zip = drifted / "vibe-kit-plugin-0.3.0.zip"
            with zipfile.ZipFile(plugin_zip, "r") as archive:
                plugin_files = [(info.filename, archive.read(info)) for info in archive.infolist()]
            with zipfile.ZipFile(plugin_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, content in plugin_files:
                    if name == "vibe-kit/.codex-plugin/plugin.json":
                        plugin = json.loads(content.decode("utf-8"))
                        plugin["version"] = "9.9.9"
                        content = json.dumps(plugin).encode("utf-8")
                    archive.writestr(name, content)
            refresh_release_checksums(drifted, "vibe-kit-plugin-0.3.0.zip")
            drift_result = run_cli(CLI, "validate-release", str(drifted))
            self.assertEqual(drift_result.returncode, 1)
            self.assertIn("Plugin name/version does not match release", drift_result.stderr)

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
            with zipfile.ZipFile(output / "vibe-kit-distribution-0.3.0.zip") as archive:
                archive.extractall(bundle_unpack)
            bundled_release = bundle_unpack / "vibe-kit-0.3.0"
            validated = run_cli(cli, "validate-release", str(bundled_release))
            self.assertEqual(validated.returncode, 0, validated.stderr)

            manifest["status"] = "stable"
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
            upgraded = run_cli(cli_two, "upgrade", str(target))
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            self.assertIn("Upgrade marker.", (target / ".vibe/core/quality-gates.md").read_text())
            self.assertEqual((target / ".vibe/project-rules.md").read_text(), custom_rules)
            self.assertEqual((target / "docs/context/product.md").read_text(), custom_product)
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


if __name__ == "__main__":
    unittest.main()
