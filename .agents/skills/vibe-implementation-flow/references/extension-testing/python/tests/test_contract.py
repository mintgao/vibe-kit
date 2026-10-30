import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).absolute().parents[1]))
from adapter import observe, module
BASE = Path(__file__).absolute().parents[2]


def integrity(root, index):
    actual = {p.name for p in root.iterdir()}
    if actual != set(index):
        return False
    return all(p.is_file() and not p.is_symlink()
               and hashlib.sha256(p.read_bytes()).hexdigest() == index[p.name][0]
               and stat.S_IMODE(p.stat().st_mode) == index[p.name][1]
               for p in root.iterdir())


class Contract(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((BASE / "receipt.json").read_text())

    def test_receipt_contract(self):
        observed = observe(self.receipt)
        print("EXTENSION-ENTRY " + json.dumps(observed, sort_keys=True))
        self.assertEqual(observed["findings"], [])
        self.assertEqual(observed["origin"], str(module.cli_path()))
        self.assertEqual(observed["arguments"], ["receipt", "default"])
        self.assertEqual(Path(observed["helper_origin"]).name, "new_helper.py")
        self.assertEqual(observed["helper_module"], "new_helper")
        for version in (True, 2.0):
            value = copy.deepcopy(self.receipt); value["schema_version"] = version
            self.assertIn("$", observe(value)["findings"])
        for field in self.receipt:
            value = copy.deepcopy(self.receipt); del value[field]
            self.assertIn("$", observe(value)["findings"])
        value = copy.deepcopy(self.receipt); value["extra"] = True
        self.assertIn("$", observe(value)["findings"])
        value = copy.deepcopy(self.receipt)
        value["checks"].pop(0); value["summary"]["unconfigured"] -= 1
        self.assertEqual(value["summary"], {
            name: sum(check["outcome"] == name for check in value["checks"])
            for name in self.receipt["summary"]
        })
        findings = observe(value)["findings"]
        self.assertIn("$.checks", findings)
        self.assertIn("$.summary", findings)

        value = copy.deepcopy(self.receipt); value["summary"]["passed"] = 1
        findings = observe(value)["findings"]
        self.assertIn("$.summary", findings)
        self.assertNotIn("$.checks", findings)

        value = copy.deepcopy(self.receipt); value["cli_invoked"] = False
        findings = observe(value)["findings"]
        self.assertIn("$", findings)
        self.assertNotIn("$.summary", findings)
        for mutate, path in [
            (lambda x: x["selection"].update(coverage="partial"), "$.selection"),
            (lambda x: x.update(cli_invoked=False), "$"),
            (lambda x: x["checks"][0]["provenance"].update(kind="agent"), "$.checks[0].provenance"),
            (lambda x: x["checks"][0].update(outcome="Pass"), "$.checks[0]"),
            (lambda x: x["checks"].reverse(), "$.checks"),
            (lambda x: x["default_order"].pop(), "$.default_order")]:
            value = copy.deepcopy(self.receipt); mutate(value)
            self.assertIn(path, observe(value)["findings"])
        reordered = copy.deepcopy(self.receipt)
        reordered["default_order"].reverse(); reordered["checks"].reverse()
        self.assertEqual(observe(reordered)["findings"], [])
        partial = copy.deepcopy(self.receipt)
        partial["selection"] = {"mode":"only", "requested":["test"], "coverage":"partial"}
        partial["checks"] = [partial["checks"][2]]; partial["summary"]["unconfigured"] = 1
        self.assertEqual(observe(partial)["findings"], [])
        self.assertNotEqual(partial["selection"]["coverage"], "all-configured")

    def test_inert_semantics_and_integrity_separate(self):
        frozen = hashlib.sha256((BASE / "receipt.json").read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            good, bad = [], []
            for content in (None, b"{bad", b'{"status":"Fail"}', b'{"status":"Pass"}'):
                p = root / "doctor.json"
                if p.exists(): p.unlink()
                index = {}
                if content is not None:
                    p.write_bytes(content); p.chmod(0o600)
                    index[p.name] = (hashlib.sha256(content).hexdigest(), 0o600)
                # Each semantic variant has its OWN valid output index. Source/input stays frozen.
                good.append(integrity(root, index))
                try: decoded = json.loads(p.read_text()) if p.exists() else {}
                except ValueError: decoded = {}
                bad.append(integrity(root, index) and decoded.get("status") == "Pass")
            self.assertEqual(good, [True] * 4)
            self.assertNotEqual(len(set(bad)), 1, "bad semantic consumer must be detected")
            p.write_bytes(b"changed"); self.assertFalse(integrity(root, index))
            p.write_bytes(content); p.chmod(0o700); self.assertFalse(integrity(root, index))
            p.chmod(0o600); (root / "undeclared").write_text("x")
            self.assertFalse(integrity(root, index)); (root / "undeclared").unlink()
            p.unlink(); self.assertFalse(integrity(root, index))
        self.assertEqual(hashlib.sha256((BASE / "receipt.json").read_bytes()).hexdigest(), frozen)

    def test_doctor_lifecycle(self):
        from adapter import SNAPSHOT
        value=os.environ.get('VIBE_EXTENSION_DOCTOR_OUTPUT')
        output=Path(value) if value else Path('designated-doctor-output-not-provided')
        expected=os.environ.get('EXTENSION_DOCTOR')=='generated'
        if not expected:self.assertFalse(output.exists())
        self.assertEqual(output.exists(), expected)
        self.assertEqual(SNAPSHOT['state'],'generated' if expected else 'absent')
        self.assertTrue(SNAPSHOT['before_helper_import'])
        if output.exists():
            self.assertEqual(SNAPSHOT['sha256'],hashlib.sha256(output.read_bytes()).hexdigest())
            value=json.loads(output.read_text());self.assertEqual(value['command'],'doctor')
        else:self.assertIsNone(SNAPSHOT['sha256'])
        print('DOCTOR-LIFECYCLE '+json.dumps({'state':SNAPSHOT['state'],'loader':'unittest-discovery','observed_at':'before-helper-import','sha256':SNAPSHOT['sha256']}))
        self.assertEqual(observe(self.receipt)['findings'], [])
