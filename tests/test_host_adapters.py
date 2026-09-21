"""Host adapters: registry mirrors, payload selection, per-selection installs and upgrades."""

import copy
import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "bin/vibe"


def load_module():
    loader = importlib.machinery.SourceFileLoader("vibe_host_adapters_cli", str(CLI))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = load_module()


class HostAdapterTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(CLI), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )

    def install(self, directory, hosts=None):
        target = Path(directory) / "project"
        arguments = [
            "init", str(target), "--format", "json",
            "--source-type", "local-payload", "--source-ref", "0.9.0",
        ]
        if hosts is not None:
            arguments += ["--host", hosts]
        result = self.run_cli(*arguments)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return target

    def test_registry_mirrors_stay_coherent(self):
        contract = json.loads((ROOT / "agent-install.json").read_text(encoding="utf-8"))
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text(encoding="utf-8"))
        self.assertEqual(set(contract["hosts"]), set(MODULE.HOST_REGISTRY))
        for host, entry in MODULE.HOST_REGISTRY.items():
            with self.subTest(host=host):
                self.assertEqual(contract["hosts"][host]["protocol"], entry["protocol"])
                self.assertEqual(protocol["adapters"][host]["version"], entry["protocol"])
                self.assertEqual(contract["hosts"][host]["capabilities"], entry["capabilities"])
                self.assertEqual(contract["hosts"][host]["payload"], entry["payload"])
        self.assertEqual(
            contract["activation"]["selected_hosts"], sorted(MODULE.HOST_REGISTRY)
        )

    def test_validator_rejects_unknown_host_and_selection(self):
        contract = json.loads((ROOT / "agent-install.json").read_text(encoding="utf-8"))
        self.assertEqual(MODULE.validate_agent_install_contract_shape(copy.deepcopy(contract)), [])
        mutated = copy.deepcopy(contract)
        mutated["hosts"]["bogus"] = mutated["hosts"]["hermes"]
        self.assertTrue(MODULE.validate_agent_install_contract_shape(mutated))
        mutated = copy.deepcopy(contract)
        mutated["activation"]["selected_hosts"] = ["bogus"]
        self.assertTrue(MODULE.validate_agent_install_contract_shape(mutated))
        mutated = copy.deepcopy(contract)
        mutated["adapter"]["protocol"] = 99
        self.assertTrue(MODULE.validate_agent_install_contract_shape(mutated))

    def test_managed_set_partitions_by_host(self):
        everything = MODULE.managed_source_files(ROOT)
        hermes = MODULE.managed_source_files(ROOT, ["hermes"])
        codex = MODULE.managed_source_files(ROOT, ["codex"])
        self.assertIn(ROOT / ".codex/agents/vibe-tech-lead.toml", everything)
        self.assertNotIn(ROOT / ".codex/agents/vibe-tech-lead.toml", hermes)
        self.assertIn(ROOT / ".codex/agents/vibe-tech-lead.toml", codex)
        self.assertIn(ROOT / ".agents/skills/vibe-feedback-flow/agents/openai.yaml", codex)
        self.assertNotIn(ROOT / ".agents/skills/vibe-feedback-flow/agents/openai.yaml", hermes)
        self.assertIn(ROOT / "AGENT_INSTALL.md", hermes)
        with self.assertRaises(MODULE.VibeError):
            MODULE.managed_source_files(ROOT, ["probe"])

    def test_guide_publishes_host_registry(self):
        guide = " ".join((ROOT / "AGENT_INSTALL.md").read_text(encoding="utf-8").split())
        self.assertIn("`codex` | 7 |", guide)
        self.assertIn("`hermes` | 1 | none | supported, unverified", guide)
        for selector in MODULE.HOST_PAYLOAD_SELECTORS["codex"]:
            self.assertIn(selector, guide)
        self.assertIn("declared per host in the host registry", guide)

    def test_install_selection_matrix_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            hermes = self.install(directory, hosts="hermes")
            self.assertFalse((hermes / ".codex").exists())
            self.assertFalse((hermes / ".agents/skills/vibe-feedback-flow/agents").exists())
            manifest = json.loads((hermes / ".vibe/manifest.json").read_text(encoding="utf-8"))
            contract = json.loads((hermes / "agent-install.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["hosts"], ["hermes"])
            self.assertEqual(contract["activation"]["selected_hosts"], ["hermes"])
            self.assertEqual(contract["adapter"]["name"], "hermes")
            doctor = self.run_cli("doctor", str(hermes))
            self.assertEqual(doctor.returncode, 0, doctor.stdout)
            upgraded = self.run_cli(
                "upgrade", str(hermes), "--format", "json",
                "--source-type", "local-payload", "--source-ref", "0.9.0",
            )
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            self.assertFalse((hermes / ".codex").exists())
        with tempfile.TemporaryDirectory() as directory:
            default = self.install(directory)
            tomls = sorted((default / ".codex/agents").glob("vibe-*.toml"))
            self.assertEqual(len(tomls), 6)
            openai = default / ".agents/skills/vibe-feedback-flow/agents/openai.yaml"
            self.assertTrue(openai.is_file())
        with tempfile.TemporaryDirectory() as directory:
            both = self.install(directory, hosts="codex,hermes")
            manifest = json.loads((both / ".vibe/manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["hosts"], ["codex", "hermes"])
            doctor = self.run_cli("doctor", str(both))
            self.assertEqual(doctor.returncode, 0, doctor.stdout)
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(
                "init", str(Path(directory) / "bogus"), "--format", "json",
                "--source-type", "local-payload", "--source-ref", "0.9.0",
                "--host", "bogus",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown host", result.stdout + result.stderr)
            self.assertFalse((Path(directory) / "bogus").exists())


if __name__ == "__main__":
    unittest.main()