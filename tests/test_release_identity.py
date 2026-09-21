"""Release identity and managed-contract consistency; structural evidence only.

These checks are the regression gate for the identity mirrors that `main` violated on
2026-09-08: a release-payload edit without regenerated mirrors leaves `./bin/vibe package`
failing while `doctor` still reports healthy.
"""
import json
import re
import tempfile
import unittest
from pathlib import Path

from tests.test_cli import ROOT, CLI, run_cli, load_cli_module


CONTRACT = ROOT / "agent-install.json"
MANIFEST = ROOT / ".vibe/manifest.json"
PLUGIN_MANIFEST = ROOT / "distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json"
REGENERATION = (
    "Regenerate the release identity mirrors with the repository procedure: recompute "
    "payload_tree_sha256(ROOT) and source_activation_identity(ROOT), generate the manifest "
    "through a production `init --source-type local-payload --source-ref <version>` install in "
    "a disposable directory, then update the Plugin manifest payload digest and "
    ".vibe/manifest.json source/activation mirrors in the same change."
)
HOST_NEUTRAL_ACTION = "create a new task in the same project"


class ReleaseIdentityTests(unittest.TestCase):
    """Identity mirrors, package buildability, and contract-text agreement."""

    def setUp(self) -> None:
        self.module = load_cli_module()

    def test_payload_identity_mirrors_match_the_tree(self) -> None:
        digest = self.module.payload_tree_sha256(ROOT)
        declared = json.loads(PLUGIN_MANIFEST.read_text())["payload_tree_sha256"]
        mirrored = json.loads(MANIFEST.read_text())["source"]["payload_tree_sha256"]
        self.assertEqual(declared, digest, f"Plugin payload identity is stale. {REGENERATION}")
        self.assertEqual(mirrored, digest, f"Manifest source payload identity is stale. {REGENERATION}")

    def test_release_package_builds_from_the_current_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            built = run_cli(CLI, "package", "--output", str(Path(directory) / "release"))
            self.assertEqual(built.returncode, 0, built.stderr)

    def test_activation_identity_mirrors_match_the_recomputed_identity(self) -> None:
        digest = self.module.source_activation_identity(ROOT)["activation_set_sha256"]
        declared = json.loads(CONTRACT.read_text())["activation"]["activation_set_sha256"]
        mirrored = json.loads(MANIFEST.read_text())["activation"]["activation_set_sha256"]
        self.assertEqual(declared, digest, f"Contract activation identity is stale. {REGENERATION}")
        self.assertEqual(mirrored, digest, f"Manifest activation identity is stale. {REGENERATION}")

    def test_takeover_schema_references_agree_with_the_installed_contract(self) -> None:
        declared = json.loads(CONTRACT.read_text())["takeover"]["schema_version"]
        block = (ROOT / "AGENTS.md").read_text()
        self.assertEqual(
            re.findall(r"takeover schema (\d+)", block),
            [],
            "the managed block references the takeover schema the installed contract declares "
            "instead of a hard-coded number (ADR 0015)",
        )
        for reference in re.findall(r"takeover schema (\d+)", (ROOT / "AGENT_INSTALL.md").read_text()):
            self.assertEqual(
                int(reference),
                declared,
                f"AGENT_INSTALL.md names takeover schema {reference}; the installed contract declares {declared}",
            )

    def test_manual_fallback_action_is_host_neutral(self) -> None:
        surfaces = (
            "AGENT_INSTALL.md",
            "README.md",
            "README.zh-CN.md",
            "bin/vibe",
            "distribution/plugin-src/vibe-kit/skills/vibe-bootstrap/SKILL.md",
            "distribution/plugin-src/vibe-kit/skills/vibe-maintain/SKILL.md",
            "AGENTS.md",
        )
        for relative in surfaces:
            with self.subTest(relative=relative):
                text = (ROOT / relative).read_text()
                self.assertNotIn("Codex task", text)
                self.assertNotIn("Codex 任务", text)
        for relative in ("AGENT_INSTALL.md", "AGENTS.md"):
            with self.subTest(required=relative):
                text = (ROOT / relative).read_text()
                self.assertIn(HOST_NEUTRAL_ACTION, text)
                self.assertIn("host-neutral", text)

    def test_installed_contract_states_the_host_neutral_manual_path(self) -> None:
        guide = " ".join((ROOT / "AGENT_INSTALL.md").read_text().split())
        self.assertIn("host-neutral", guide)
        self.assertIn("host that can start a new task in the same project", guide)
        self.assertIn("describe the host that installed or adopted", guide)


if __name__ == "__main__":
    unittest.main()
