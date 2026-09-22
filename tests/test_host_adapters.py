"""Host adapters: registry mirrors, payload selection, per-selection installs and upgrades."""

import copy
import importlib.machinery
import importlib.util
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

from tests.fake_takeover_host import FakeTakeoverHost

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
            "--source-type", "local-payload", "--source-ref", "0.10.0",
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
                    contract["hosts"][host]["conformance"], entry["conformance"]
                )
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
        self.assertIn("`hermes` | 1 | none | verified", guide)
        for selector in MODULE.HOST_PAYLOAD_SELECTORS["codex"]:
            self.assertIn(selector, guide)
        self.assertIn("declared per host in the host registry", guide)

    def test_hermes_conformance_label_follows_its_record(self):
        entry = MODULE.HOST_REGISTRY["hermes"]["conformance"]
        self.assertIn(entry["label"], MODULE.HOST_CONFORMANCE_LABELS)
        self.assertEqual(entry["label"], "verified")
        self.assertEqual(
            entry["evidence"],
            ["docs/work-items/20260921-host-adapters/conformance.md"],
        )
        for reference in entry["evidence"]:
            self.assertTrue((ROOT / reference).is_file(), reference)

    def test_guide_publishes_the_hermes_role_mapping_and_host_differences(self):
        guide = " ".join((ROOT / "AGENT_INSTALL.md").read_text(encoding="utf-8").split())
        roles = sorted(
            match.group(1)
            for path in sorted((ROOT / ".codex/agents").glob("vibe-*.toml"))
            for match in [re.match(r'name = "([a-z_]+)"', path.read_text(encoding="utf-8"))]
            if match
        )
        self.assertEqual(len(roles), 6)
        self.assertIn("Kit role | Hermes mapping", guide)
        mapping = guide.split("Kit role | Hermes mapping", 1)[1].split(
            "Host differences that change", 1
        )[0]
        for role in roles:
            self.assertIn(f"`{role}`", mapping)
        differences = guide.split("Host differences that change", 1)[1]
        self.assertIn("Approval prompts", differences)
        self.assertIn("Subagent budget", differences)
        self.assertIn("host approval prompt", differences)
        self.assertIn("sequential-perspective", differences)
        self.assertIn(
            "Any host that can start a new task in the same project may own the successor task",
            guide,
        )

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
                "--source-type", "local-payload", "--source-ref", "0.10.0",
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
                "--source-type", "local-payload", "--source-ref", "0.10.0",
                "--host", "bogus",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown host", result.stdout + result.stderr)
            self.assertFalse((Path(directory) / "bogus").exists())

    def source_arguments(self):
        return [
            "--source-type", "local-payload",
            "--source-ref", MODULE.framework_version(ROOT),
        ]

    def test_takeover_validation_accepts_registered_hosts_and_fails_closed(self):
        for hosts, expected in ((None, "codex"), ("hermes", "hermes")):
            with self.subTest(hosts=hosts):
                with tempfile.TemporaryDirectory() as directory:
                    target = self.install(directory, hosts=hosts)
                    host = FakeTakeoverHost(target)
                    fingerprint = host.context["target_fingerprint"]
                    self.assertEqual(fingerprint["adapter_name"], expected)
                    self.assertEqual(
                        fingerprint["adapter_protocol"],
                        MODULE.HOST_REGISTRY[expected]["protocol"],
                    )
                    code, receipt, _ = host.validate(host.ready("manual-new-task"))
                    self.assertEqual(code, 0, json.dumps(receipt, ensure_ascii=False)[:400])
                    self.assertEqual(receipt["status"], "valid")
                    for label, mutate in (
                        (
                            "unknown host",
                            lambda value: value["target_fingerprint"].update(
                                adapter_name="bogus"
                            ),
                        ),
                        (
                            "unknown protocol",
                            lambda value: value["target_fingerprint"].update(
                                adapter_protocol=99
                            ),
                        ),
                        (
                            "absent host",
                            lambda value: value["target_fingerprint"].update(
                                adapter_name=None
                            ),
                        ),
                    ):
                        with self.subTest(hosts=hosts, mutation=label):
                            value = copy.deepcopy(host.ready("manual-new-task"))
                            mutate(value)
                            code, receipt, _ = host.validate(value)
                            self.assertNotEqual(code, 0)
                            self.assertEqual(receipt["status"], "invalid")
                            errors = receipt["errors"]
                            self.assertIsInstance(errors, list)
                            codes = [
                                str(item.get("code"))
                                for item in errors
                                if isinstance(item, dict)
                            ]
                            self.assertIn("activation-identities-match-target", codes)

    def test_upgrade_from_pre_change_install_maps_to_codex_additively(self):
        with tempfile.TemporaryDirectory() as directory:
            predecessor = Path(directory) / "predecessor"
            predecessor.mkdir()
            archive = subprocess.run(
                ["git", "archive", "--format=tar", "v0.8.0"],
                cwd=str(ROOT), check=True, capture_output=True,
            ).stdout
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
                bundle.extractall(predecessor)
            target = Path(directory) / "target"
            installed = subprocess.run(
                [sys.executable, str(predecessor / "bin/vibe"), "init", str(target), "--format", "json"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            before_manifest = json.loads(
                (target / ".vibe/manifest.json").read_text(encoding="utf-8")
            )
            before_contract = json.loads(
                (target / "agent-install.json").read_text(encoding="utf-8")
            )
            self.assertIsNone(before_manifest.get("hosts"))
            self.assertNotIn("selected_hosts", before_contract["activation"])

            owned = "\n<!-- owner -->\nProject policy stays: café 中文.\n"
            with (target / "AGENTS.md").open("a") as stream:
                stream.write(owned)
            upgraded = self.run_cli(
                "upgrade", str(target), "--format", "json", *self.source_arguments()
            )
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            manifest = json.loads(
                (target / ".vibe/manifest.json").read_text(encoding="utf-8")
            )
            contract = json.loads(
                (target / "agent-install.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["hosts"], ["codex"])
            self.assertEqual(contract["activation"]["selected_hosts"], ["codex"])
            self.assertEqual(contract["adapter"], {"name": "codex", "protocol": 7})
            self.assertTrue((target / ".codex/agents/vibe-tech-lead.toml").is_file())
            self.assertTrue(
                (target / "AGENTS.md").read_text(encoding="utf-8").endswith(owned)
            )
            doctor = self.run_cli("doctor", str(target))
            self.assertEqual(doctor.returncode, 0, doctor.stdout)

    def test_stale_deselected_payload_and_incoherent_selection_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.install(directory, hosts="hermes")
            stray = target / ".codex/agents"
            stray.mkdir(parents=True)
            (stray / "vibe-tech-lead.toml").write_bytes(
                (ROOT / ".codex/agents/vibe-tech-lead.toml").read_bytes()
            )
            doctor = self.run_cli("doctor", str(target), "--format", "json")
            receipt = json.loads(doctor.stdout)
            self.assertEqual(receipt["status"], "warning")
            stale = [
                item
                for item in receipt["diagnostics"]
                if item["code"] == "stale-runtime-path-preserved"
            ]
            self.assertEqual(
                [item["path"] for item in stale], [".codex/agents/vibe-tech-lead.toml"]
            )
            self.assertEqual(stale[0]["readiness_effect"], "blocking")
            (stray / "vibe-tech-lead.toml").unlink()

            manifest_path = target / ".vibe/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for recorded, message in ((["codex"], "incoherent"), (["bogus"], "unknown host")):
                with self.subTest(recorded=recorded):
                    manifest["hosts"] = recorded
                    manifest_path.write_text(
                        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    doctor = self.run_cli("doctor", str(target), "--format", "json")
                    self.assertNotEqual(doctor.returncode, 0)
                    self.assertIn(
                        "host-selection-incoherent",
                        {item["code"] for item in json.loads(doctor.stdout)["diagnostics"]},
                    )
                    refused = self.run_cli(
                        "upgrade", str(target), "--format", "json", *self.source_arguments()
                    )
                    self.assertNotEqual(refused.returncode, 0)
                    self.assertIn(message, refused.stdout + refused.stderr)
                    manifest["hosts"] = ["hermes"]
                    manifest_path.write_text(
                        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
            restored = self.run_cli("doctor", str(target))
            self.assertEqual(restored.returncode, 0, restored.stdout)


if __name__ == "__main__":
    unittest.main()