"""Focused real-entry and bounded historical-evidence scenarios for ADR0023."""
import contextlib
import copy
import errno
import hashlib
import io
import json
import os
import posixpath
from pathlib import Path
import re
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from unittest import mock

from tests.test_cli import CLI, ROOT, load_cli_module, run_cli, profile_test_intent


def node_runtime():
    return os.environ.get("CODEX_TASK_WORKSPACE_NODE") or shutil.which("node")


def snapshot_tree(root):
    result = {}
    for path in sorted(root.rglob("*")):
        info = path.lstat()
        relative = path.relative_to(root).as_posix()
        if stat.S_ISREG(info.st_mode):
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    digest.update(chunk)
            value = digest.hexdigest()
        elif stat.S_ISLNK(info.st_mode):
            value = os.readlink(path)
        else:
            value = None
        result[relative] = (stat.S_IFMT(info.st_mode), stat.S_IMODE(info.st_mode), info.st_size if stat.S_ISREG(info.st_mode) else None, value)
    return result


class OnboardingExactVersionTests(unittest.TestCase):
    def test_exact_version_table_and_real_doctor_upgrade_plan(self):
        m = load_cli_module()
        missing = object()
        versions = (True, False, 1.0, 1.5, "1", None, missing, 0, 1, 2)
        for kind in ("python", "node"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                target = Path(directory).resolve() / kind
                target.mkdir()
                if kind == "python":
                    (target / "pyproject.toml").write_text('[project]\nname="fixture"\nversion="0.1.0"\n')
                else:
                    (target / "package.json").write_text('{"name":"fixture","private":true,"scripts":{"test":"node test.cjs"}}\n')
                result = run_cli(CLI, "adopt", str(target), "--format", "json")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                state = target / ".vibe/onboarding.json"
                for status in ("pending", "refresh-needed", "complete"):
                    for version in versions:
                        body = {"status": status, "private": "PRIVATE-ONBOARDING-BODY", "updated_at": "2026-10-28", "evidence": ["README.md"]}
                        if version is not missing:
                            body["schema_version"] = version
                        state.write_text(json.dumps(body) + "\n")
                        before = state.read_bytes()
                        if type(version) is int and version == 1:
                            self.assertEqual(m.onboarding_readiness(target), (status, []))
                        else:
                            with self.assertRaises(m.VibeError) as raised:
                                m.onboarding_readiness(target)
                            self.assertEqual(raised.exception.code, "invalid_onboarding_state")
                            self.assertNotIn("PRIVATE-ONBOARDING-BODY", str(raised.exception))
                        self.assertEqual(state.read_bytes(), before)
                    for version in (True, 1.0, 1):
                        state.write_text(json.dumps({"schema_version": version, "status": status, "updated_at": "2026-10-28", "evidence": ["README.md"], "private": "PRIVATE-ONBOARDING-BODY"}) + "\n")
                        before = state.read_bytes()
                        for arguments in (("doctor", str(target)), ("plan", "upgrade", str(target))):
                            result = run_cli(CLI, *arguments, "--format", "json")
                            value = json.loads(result.stdout)
                            if type(version) is int:
                                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                            else:
                                self.assertNotEqual(result.returncode, 0)
                                self.assertIn("invalid", result.stdout)
                            self.assertNotIn("PRIVATE-ONBOARDING-BODY", result.stdout + result.stderr)
                            self.assertEqual(state.read_bytes(), before)
                for body in ([], None, 1, True, "PRIVATE-ONBOARDING-BODY"):
                    state.write_text(json.dumps(body))
                    with self.assertRaises(m.VibeError):
                        m.onboarding_readiness(target)
                state.write_text('{"schema_version":1,"status":"complete"}')
                with self.assertRaises(m.VibeError):
                    m.onboarding_readiness(target)
                state.unlink()
                self.assertEqual(m.onboarding_readiness(target)[0], "review-required")
                self.assertFalse(state.exists())


class AffectedEntryEvidenceTests(unittest.TestCase):
    def execute(self, args, cwd):
        result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
        print("ENTRY-EVIDENCE " + json.dumps({"command": args, "returncode": result.returncode,
              "stdout": result.stdout[-2048:], "stderr": result.stderr[-2048:]}, sort_keys=True))
        return result

    def test_python_real_discovery_detects_stale_origin_and_arguments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "tests").mkdir()
            (root / "old.py").write_text('def check(*args):\n    return {"origin": __name__, "args": list(args)}\n')
            (root / "new.py").write_text('def check(*args):\n    return {"origin": __name__, "args": list(args)}\n')
            adapter = root / "adapter.py"
            adapter.write_text('from old import check\ndef observe():\n    return check("test", "focused")\n')
            direct = 'import unittest\nfrom new import check\nclass Direct(unittest.TestCase):\n    def test_direct(self):\n        self.assertEqual(check("test", "focused"), {"origin":"new","args":["test","focused"]})\n'
            live = 'import unittest, json\nfrom adapter import observe\nimport adapter, inspect\nclass Live(unittest.TestCase):\n    def test_origin_and_arguments(self):\n        value=observe(); print(json.dumps({"observation":value,"file":inspect.getsourcefile(adapter.check)},sort_keys=True))\n        self.assertEqual(inspect.getsourcefile(adapter.check).rsplit("/",1)[-1], "new.py")\n        self.assertEqual(value["origin"], "new")\n        self.assertEqual(value["args"], ["test","focused"])\n'
            historical = 'import unittest\nfrom old import check\nclass Historical(unittest.TestCase):\n    def test_historical(self):\n        self.assertEqual(check("legacy"), {"origin":"old","args":["legacy"]})\n'
            (root / "tests/test_direct.py").write_text(direct)
            (root / "tests/test_live.py").write_text(live)
            history = root / "tests/test_historical.py"
            history.write_text(historical)
            before = history.read_bytes()
            base = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p"]
            self.assertEqual(self.execute(base + ["test_direct.py", "-v"], root).returncode, 0)
            stale = self.execute(base + ["test_live.py", "-v"], root)
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn('"origin": "old"', stale.stdout)
            adapter.write_text('from new import check\ndef observe():\n    return check("test", "WRONG")\n')
            wrong = self.execute(base + ["test_live.py", "-v"], root)
            self.assertNotEqual(wrong.returncode, 0)
            self.assertIn('"origin": "new"', wrong.stdout)
            self.assertIn('"WRONG"', wrong.stdout)
            adapter.write_text('from new import check\ndef observe():\n    return check("test", "focused")\n')
            self.assertEqual(self.execute(base + ["test_live.py", "-v"], root).returncode, 0)
            self.assertEqual(self.execute(base + ["test_historical.py", "-v"], root).returncode, 0)
            self.assertEqual(history.read_bytes(), before)

    def test_node_real_package_script_detects_stale_origin_and_arguments(self):
        node = node_runtime()
        if node is None:
            self.skipTest("Node runtime unavailable: Node acceptance is not executed")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for name in ("old", "new"):
                (root / (name + ".cjs")).write_text('exports.check=(...args)=>({origin:__filename,args});\n')
            adapter = root / "adapter.cjs"
            adapter.write_text('const {check}=require("./old.cjs"); exports.observe=(args)=>check(...args);\n')
            (root / "observer.cjs").write_text('const assert=require("node:assert/strict"); const value=require("./adapter.cjs").observe(process.argv.slice(2)); console.log(JSON.stringify(value)); assert.equal(value.origin,require.resolve("./new.cjs")); assert.deepEqual(value.args,["--focused"]);\n')
            (root / "direct.cjs").write_text('require("node:assert/strict").deepEqual(require("./new.cjs").check("--focused"),{origin:require.resolve("./new.cjs"),args:["--focused"]});\n')
            history = root / "historical.cjs"
            history.write_text('require("node:assert/strict").deepEqual(require("./old.cjs").check("legacy"),{origin:require.resolve("./old.cjs"),args:["legacy"]});\n')
            before = history.read_bytes()
            (root / "package.json").write_text(json.dumps({"private": True, "scripts": {"test": shlex.quote(node) + " observer.cjs"}}))
            self.assertEqual(self.execute([node, "direct.cjs"], root).returncode, 0)
            script = [node, "--run", "test", "--", "--focused"]
            stale = self.execute(script, root)
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn(str(root / 'old.cjs'), stale.stdout)
            adapter.write_text('const {check}=require("./new.cjs"); exports.observe=()=>check("WRONG");\n')
            wrong = self.execute(script, root)
            self.assertNotEqual(wrong.returncode, 0)
            self.assertIn(str(root / 'new.cjs'), wrong.stdout)
            self.assertIn('"WRONG"', wrong.stdout)
            adapter.write_text('const {check}=require("./new.cjs"); exports.observe=(args)=>check(...args);\n')
            self.assertEqual(self.execute(script, root).returncode, 0)
            self.assertEqual(self.execute([node, "historical.cjs"], root).returncode, 0)
            self.assertEqual(history.read_bytes(), before)


class InspectRunTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.target = self.base / "project"
        (self.target / ".vibe").mkdir(parents=True)

    def produce(self, *, text="observed", only=False, status=0, receipt=True, logs=True, all_checks=False, external=False):
        command = shlex.quote(sys.executable) + " -c " + shlex.quote("import sys; print(" + repr(text) + "); sys.exit(" + str(status) + ")")
        commands = {name: command if all_checks or name == "test" else "" for name in self.m.VERIFY_ORDER}
        (self.target / ".vibe/project.yaml").write_text("schema_version: 1\ncommands:\n" + "".join("  " + key + ": " + json.dumps(value) + "\n" for key, value in commands.items()))
        receipt_path = (self.base if external else self.target) / ("receipt-" + str(len(list(self.base.rglob("receipt-*")))) + ".json")
        if receipt:
            self.m.RECEIPT_CONTEXT[0] = (receipt_path, self.target)
        output = io.StringIO()
        with mock.patch.object(self.m, "observe_toolchain", return_value={"python": "3.9.0", "node": None, "pnpm": None}), contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            code = self.m.verify(self.target, ["test"] if only else [], "json", "all-configured" if logs else "failures")
        envelope = json.loads(output.getvalue())
        locator, errors = self.m.read_verify_locator(self.target)
        self.assertEqual(errors, [])
        run_id = locator["run_id"]
        path = self.target / ".vibe/local/verify/runs" / run_id / "progress.json"
        snapshot = json.loads(path.read_bytes())
        return run_id, receipt_path if receipt else None, envelope, snapshot, path

    def publish_metadata(self, path, value):
        value["metadata_sha256"] = self.m.canonical_json_sha256({key: item for key, item in value.items() if key != "metadata_sha256"})
        path.write_text(json.dumps(value, sort_keys=True) + "\n")
        path.chmod(0o600)

    def rebind(self, receipt_path, envelope, metadata, path, *, raw=None):
        raw = raw if raw is not None else self.m.receipt_bytes(envelope, self.target)
        receipt_path.write_bytes(raw)
        receipt_path.chmod(0o600)
        metadata["result"]["envelope_sha256"] = self.m.canonical_json_sha256(self.m.root_relative_receipt(envelope, self.target))
        metadata["result"]["receipt"]["sha256"] = hashlib.sha256(raw).hexdigest()
        self.publish_metadata(path, metadata)

    def inspect(self, run_id, receipt=None, *, target=None, guard=True):
        target = self.target if target is None else target
        before = snapshot_tree(target) if Path(target).is_dir() else None
        output = io.StringIO()
        errors = io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(contextlib.redirect_stdout(output))
            stack.enter_context(contextlib.redirect_stderr(errors))
            if guard:
                for name in ("verify", "doctor", "observe_toolchain", "write_receipt_artifact", "write_verify_receipt"):
                    stack.enter_context(mock.patch.object(self.m, name, side_effect=AssertionError("inspection execution/write tripwire")))
                stack.enter_context(mock.patch.object(self.m.subprocess, "run", side_effect=AssertionError("inspection subprocess tripwire")))
                stack.enter_context(mock.patch.object(self.m.subprocess, "Popen", side_effect=AssertionError("inspection subprocess tripwire")))
                stack.enter_context(mock.patch.object(self.m.os, "kill", side_effect=AssertionError("inspection process-control tripwire")))
            code = self.m.main(["inspect-run", str(target), "--run-id", run_id, "--format", "json"] + (["--final-receipt", str(receipt)] if receipt is not None else []))
        value = json.loads(output.getvalue())
        self.assertEqual(errors.getvalue(), "")
        self.assertLessEqual(len(output.getvalue().encode()), 32768)
        self.assertEqual(set(value), {"schema_version", "command", "status", "inspection"})
        facts = value["inspection"]
        self.assertEqual(set(facts), {"schema_version", "run_id", "metadata", "receipt", "binding", "coverage", "artifact_scope", "artifacts", "historical_receipt_verdict", "historical_run_verdict", "candidate_applicability", "project_origin", "liveness", "findings", "next_actions"})
        self.assertEqual((facts["candidate_applicability"], facts["project_origin"], facts["liveness"]), ("unproven", "not-attested", "not-assessed"))
        self.assertLessEqual(len(facts["findings"]), 64)
        self.assertLessEqual(len(facts["artifacts"]), 4)
        self.assertTrue(set(facts["next_actions"]).issubset(self.m.INSPECT_NEXT_ACTIONS))
        self.assertNotIn("PRIVATE-MARKER", output.getvalue())
        if before is not None:
            self.assertEqual(snapshot_tree(target), before)
        return code, value, facts

    def test_default_full_partial_nonpassing_and_missing_envelope(self):
        run, receipt, envelope, metadata, path = self.produce()
        code, value, facts = self.inspect(run)
        self.assertEqual((code, value["status"], facts["binding"], facts["coverage"], facts["artifact_scope"]), (0, "inspected", "matched", "all-configured", "receipt"))
        self.assertEqual((facts["historical_receipt_verdict"], facts["historical_run_verdict"]), ("passed", "passed"))
        self.assertEqual([item["state"] for item in facts["artifacts"]], ["not-referenced", "not-referenced", "verified", "not-referenced"])
        (self.target / "current-source.py").write_text("changed after historical execution\n")
        self.assertEqual(self.inspect(run)[2]["candidate_applicability"], "unproven")
        run, receipt, _, _, _ = self.produce(only=True)
        code, _, facts = self.inspect(run)
        self.assertEqual((code, facts["coverage"], facts["historical_run_verdict"]), (0, "partial", "not-passed"))
        run, receipt, _, _, _ = self.produce(status=7)
        self.assertEqual(self.inspect(run)[2]["historical_run_verdict"], "not-passed")
        run, _, envelope, metadata, path = self.produce(receipt=False, logs=False)
        code, _, facts = self.inspect(run)
        self.assertEqual((code, facts["receipt"]["state"], facts["artifact_scope"], facts["historical_run_verdict"]), (0, "not-supplied", "metadata", "unverified"))
        wrapper = self.target / "wrapper.json"
        wrapper.write_bytes(self.m.receipt_bytes(envelope, self.target)); wrapper.chmod(0o600)
        self.assertEqual(self.inspect(run, wrapper)[2]["historical_run_verdict"], "passed")

    def test_missing_invalid_metadata_preserves_independent_receipt_and_no_fallback(self):
        run, receipt, envelope, metadata, path = self.produce()
        original = path.read_bytes()
        for raw in (None, b'{"PRIVATE-MARKER":true}', b'not-json PRIVATE-MARKER', b'\xff', b'{"schema_version":1,"schema_version":1}'):
            if raw is None:
                path.unlink()
            else:
                path.write_bytes(raw); path.chmod(0o600)
            code, value, facts = self.inspect(run, receipt)
            self.assertEqual((code, value["status"], facts["historical_receipt_verdict"], facts["historical_run_verdict"]), (1, "invalid", "passed", "unverified"))
        path.write_bytes(original); path.chmod(0o600)
        bad = self.target / "bad.json"; bad.write_bytes(b'PRIVATE-MARKER'); bad.chmod(0o600)
        code, _, facts = self.inspect(run, bad)
        self.assertEqual((code, facts["receipt"]["state"], facts["artifact_scope"]), (1, "invalid", "metadata"))
        self.assertEqual(self.inspect("wrong-PRIVATE-MARKER", receipt)[2]["run_id"], None)
        self.assertEqual(self.inspect("verify-" + "f" * 32, receipt)[0], 1)

    def test_external_explicit_copy_and_selected_scope(self):
        run, receipt, _, metadata, _ = self.produce(external=True)
        self.assertEqual(self.inspect(run)[2]["receipt"]["state"], "not-supplied")
        self.assertEqual(self.inspect(run, receipt)[2]["historical_run_verdict"], "passed")
        run, original, _, metadata, _ = self.produce()
        copied = self.target / "copy.json"; copied.write_bytes(original.read_bytes()); copied.chmod(0o600)
        original.unlink(); os.mkfifo(original, 0o600)
        original_open = self.m.os.open
        def tripwire(name, *args, **kwargs):
            if name == original.name:
                raise AssertionError("unselected original receipt was reopened")
            return original_open(name, *args, **kwargs)
        with mock.patch.object(self.m.os, "open", tripwire), mock.patch.object(self.m.os, "supports_dir_fd", self.m.os.supports_dir_fd | {tripwire}):
            code, _, facts = self.inspect(run, copied)
        self.assertEqual((code, facts["binding"], facts["historical_run_verdict"]), (0, "matched", "passed"))
        self.assertIn("inspection-original-receipt-path-not-inspected", [item["code"] for item in facts["findings"]])
        self.assertEqual(self.inspect(run)[0], 1)

    def test_conflicting_valid_receipt_owns_only_four_logs(self):
        older, first, _, _, _ = self.produce(text="first log", all_checks=True)
        run, second, _, metadata, path = self.produce(text="second log", all_checks=True)
        with mock.patch.object(self.m, "inspection_log", wraps=self.m.inspection_log) as reads:
            code, _, facts = self.inspect(run, first)
        self.assertEqual(reads.call_count, 4)
        first_hashes = {item["output"]["full"]["sha256"] for item in json.loads(first.read_bytes())["checks"]}
        self.assertTrue({item["sha256"] for item in facts["artifacts"]}.issubset(first_hashes))
        self.assertEqual((code, facts["artifact_scope"], facts["binding"], facts["historical_receipt_verdict"], facts["historical_run_verdict"]), (1, "receipt", "mismatch", "passed", "unverified"))
        self.assertIn("inspection-metadata-artifacts-not-inspected", [item["code"] for item in facts["findings"]])
        # Irrelevant conflicting metadata declarations must not erase receipt truth.
        for item in metadata["checks"]:
            item["log"]["bytes"] = self.m.INSPECT_LOG_LIMIT + 1
        self.publish_metadata(path, metadata)
        self.assertEqual(self.inspect(run, first)[2]["historical_receipt_verdict"], "passed")

    def test_complete_receipt_closed_shape_and_raw_binding_drift(self):
        run, receipt, envelope, metadata, path = self.produce()
        original = receipt.read_bytes()
        normalized = json.loads(original)
        mutations = [lambda v: v.update(schema_version=True), lambda v: v.update(schema_version=2.0), lambda v: v.update(target="/foreign/PRIVATE-MARKER"), lambda v: v.update(PRIVATE_MARKER="PRIVATE-MARKER"), lambda v: v.pop("toolchain"), lambda v: v["summary"].update(passed=True), lambda v: v["summary"].update(passed=4), lambda v: v["checks"][2].update(exit_code=True), lambda v: v["checks"][2].update(exit_code=2**63), lambda v: v["checks"][2].update(configured=1), lambda v: v["checks"][2].update(required=False), lambda v: v["checks"][2].update(provenance={"kind":"host","task_id":None,"operation_id":None}), lambda v: v["checks"][2]["output"].update(stdout_truncated=1), lambda v: v["checks"][2]["output"]["full"].update(path="../PRIVATE-MARKER"), lambda v: v["default_order"].reverse(), lambda v: v["checks"].pop(), lambda v: v["selection"].update(coverage="partial"), lambda v: v["toolchain"].update(python={"PRIVATE-MARKER":1})]
        for mutate in mutations:
            candidate = copy.deepcopy(normalized); mutate(candidate)
            receipt.write_text(json.dumps(candidate)); receipt.chmod(0o600)
            code, _, facts = self.inspect(run, receipt)
            self.assertEqual((code, facts["receipt"]["state"], facts["receipt"]["result_status"]), (1, "invalid", None))
        for raw in (b'{"schema_version":2,"schema_version":2}', b'NaN', b'{"status":Infinity}', b'\xff', b'{"schema_version":2', b'{"PRIVATE-MARKER": [', b'['*10000+b'"PRIVATE-MARKER"'+b']'*10000):
            receipt.write_bytes(raw)
            code, _, facts = self.inspect(run, receipt)
            self.assertEqual((code, facts["receipt"]["state"]), (1, "invalid"))
        receipt.write_bytes(original + b" \n")
        code, _, facts = self.inspect(run, receipt)
        self.assertEqual((code, facts["binding"], facts["receipt"]["state"], facts["historical_receipt_verdict"]), (1, "mismatch", "valid", "passed"))
        receipt.write_bytes(original)
        metadata["result"]["envelope_sha256"] = "0" * 64; self.publish_metadata(path, metadata)
        self.assertEqual(self.inspect(run, receipt)[2]["binding"], "mismatch")

    def test_running_blocked_error_and_environment_receipt_combinations(self):
        run, receipt, envelope, metadata, path = self.produce(logs=False)
        base = copy.deepcopy(metadata)
        metadata.update(state="running", ended_at=None, result=None)
        self.publish_metadata(path, metadata)
        self.assertEqual(self.inspect(run)[2]["metadata"]["run_state"], "running")
        self.assertEqual(self.inspect(run)[2]["historical_run_verdict"], "unverified")
        metadata = copy.deepcopy(base)
        metadata["state"] = "incomplete"
        metadata["interruption"] = {"reason":"sigterm","requested_at":metadata["updated_at"],"direct_child":"reaped","descendants":"not-proven"}
        envelope["status"] = "blocked"; metadata["result"].update(status="blocked",exit_code=2)
        self.rebind(receipt, envelope, metadata, path)
        code, _, facts = self.inspect(run)
        self.assertEqual((code, facts["receipt"]["result_status"], facts["historical_run_verdict"]), (0, "blocked", "not-passed"))
        metadata = copy.deepcopy(base)
        metadata["result"].update(status="error",exit_code=2); envelope["status"]="error"
        self.rebind(receipt,envelope,metadata,path)
        self.assertEqual(self.inspect(run)[2]["historical_run_verdict"], "not-passed")
        value = json.loads(receipt.read_bytes()); value["status"]="blocked"
        self.assertEqual(self.m.validate_complete_verify_receipt(value), [])
        value["status"]="error"
        self.assertEqual(self.m.validate_complete_verify_receipt(value), [])
        limited = value["checks"][2]; limited.update(outcome="environment-limited",exit_code=1,reason_code="toolchain-mismatch",environment={"expectations":{"node":{"expected":">=99","observed":None}},"observed":value["toolchain"]})
        value["summary"].update(passed=0, **{"environment-limited":1})
        self.assertEqual(self.m.validate_complete_verify_receipt(value), [])
        limited["environment"]["expectations"]["PRIVATE-MARKER"]={"expected":"secret","observed":None}
        self.assertTrue(self.m.validate_complete_verify_receipt(value))

    def test_log_integrity_size_and_metadata_count_preflight(self):
        run, receipt, envelope, metadata, path = self.produce()
        log = metadata["checks"][2]["log"]
        actual = self.target / log["path"]
        original = actual.read_bytes()
        for mode in ("changed", "missing", "hardlink", "permissions"):
            if actual.exists():
                actual.unlink()
            actual.write_bytes(original); actual.chmod(0o600)
            extra = self.base / "linked"
            if extra.exists(): extra.unlink()
            if mode == "changed": actual.write_bytes(b"PRIVATE-MARKER")
            elif mode == "missing": actual.unlink()
            elif mode == "hardlink": os.link(actual, extra)
            else: actual.chmod(0o644)
            code, _, facts = self.inspect(run)
            self.assertEqual(code, 1)
            self.assertNotEqual(facts["historical_run_verdict"], "passed")
        actual.unlink(); actual.write_bytes(original); actual.chmod(0o600)
        log["bytes"] += 1; self.publish_metadata(path,metadata)
        code, _, facts = self.inspect(run)
        self.assertEqual((code,facts["binding"],facts["historical_receipt_verdict"]),(1,"mismatch","passed"))
        log["bytes"] = self.m.INSPECT_LOG_LIMIT + 1; self.publish_metadata(path,metadata)
        with mock.patch.object(self.m,"inspection_log",side_effect=AssertionError("oversized declared log must not open")):
            code,_,facts=self.inspect(run)
        self.assertEqual((code,facts["artifacts"][2]["state"]),(1,"unavailable"))
        receipt.unlink()
        with mock.patch.object(self.m,"inspection_log",side_effect=AssertionError("metadata oversized log must not open")):
            self.assertEqual(self.inspect(run)[0],1)

    def test_receipt_at_and_over_limit_and_streaming_log_limit(self):
        run,receipt,envelope,metadata,path=self.produce()
        raw=receipt.read_bytes(); padded=raw+b" "*(self.m.INSPECT_RECEIPT_LIMIT-len(raw))
        self.rebind(receipt,envelope,metadata,path,raw=padded)
        self.assertEqual(self.inspect(run)[0],0)
        receipt.write_bytes(padded+b" ")
        self.assertEqual(self.inspect(run)[2]["receipt"]["state"],"unavailable")
        # Exercise the real 64 MiB boundary without retaining a log body in the reader.
        data_path=self.target/"sized.log"
        block=b"x"*65536; digest=hashlib.sha256()
        with data_path.open("wb") as handle:
            for _ in range(self.m.INSPECT_LOG_LIMIT//len(block)):
                handle.write(block);digest.update(block)
        full={"path":".vibe/local/verify/logs/sha256/"+digest.hexdigest()+".log","sha256":digest.hexdigest()}
        final=self.target/full["path"]; data_path.rename(final);final.chmod(0o600)
        envelope["checks"][2]["output"]["full"]=full
        metadata["checks"][2]["log"].update(path=full["path"],sha256=full["sha256"],bytes=self.m.INSPECT_LOG_LIMIT)
        self.rebind(receipt,envelope,metadata,path)
        self.assertEqual(self.inspect(run)[2]["artifacts"][2]["bytes"],self.m.INSPECT_LOG_LIMIT)
        with final.open("ab") as handle:handle.write(b"x")
        self.assertEqual(self.inspect(run)[2]["artifacts"][2]["state"],"unavailable")

    def test_short_growth_and_changed_identity_reads_close_descriptors(self):
        leaf=self.target/"leaf.json";leaf.write_bytes(b"abcdef");leaf.chmod(0o600)
        parent=os.open(self.target,os.O_RDONLY|os.O_DIRECTORY)
        self.addCleanup(os.close,parent)
        original_read=self.m.os.read
        for mode in ("short","growth","identity"):
            reads=[]
            def read(fd,n):
                if mode=="short":return b"" if reads else (reads.append(True) or b"a")
                if mode=="growth":return b"x"*n
                return original_read(fd,n)
            original_stat=self.m.os.fstat
            stats=[]
            def fstat(fd):
                value=original_stat(fd);stats.append(value)
                if mode=="identity" and len(stats)>1:
                    value=mock.Mock(wraps=value)
                    for name in ("st_dev","st_ino","st_mode","st_uid","st_nlink","st_size","st_mtime_ns","st_ctime_ns"):
                        setattr(value,name,getattr(stats[-1],name))
                    value.st_ino+=1
                return value
            with mock.patch.object(self.m.os,"read",read),mock.patch.object(self.m.os,"fstat",fstat),mock.patch.object(self.m.os,"close",wraps=self.m.os.close) as close:
                with self.assertRaises(self.m.InspectionReadError):
                    self.m.inspection_private_leaf(parent,leaf.name,6,retain=True)
                self.assertEqual(close.call_count,1)

    def test_symlink_unsafe_types_owner_unsupported_and_pinned_rename(self):
        run,receipt,envelope,metadata,path=self.produce()
        link=self.base/"root-link";link.symlink_to(self.target,target_is_directory=True)
        self.assertEqual(self.inspect(run,receipt,target=link)[0],2)
        self.assertEqual(self.inspect(run,receipt,target=link/".vibe"/"..")[0],2)
        alias=self.target/"alias.json";alias.symlink_to(receipt)
        self.assertEqual(self.inspect(run,alias)[0],1)
        alias.unlink();os.link(receipt,alias)
        self.assertEqual(self.inspect(run,alias)[0],1)
        alias.unlink(); os.mkfifo(alias,0o600)
        self.assertEqual(self.inspect(run,alias)[0],1)
        alias.unlink();alias.mkdir()
        self.assertEqual(self.inspect(run,alias)[0],1)
        alias.rmdir()
        parentlink=self.base/"parent-link";parentlink.symlink_to(self.target,target_is_directory=True)
        self.assertEqual(self.inspect(run,parentlink/receipt.name)[0],1)
        with mock.patch.object(self.m.os,"supports_dir_fd",set()):
            self.assertEqual(self.inspect(run,receipt)[0],2)
        with mock.patch.object(self.m.os,"getuid",return_value=os.getuid()+1):
            self.assertEqual(self.inspect(run,receipt)[0],1)
        # Replace the root pathname after snapshot reading. Relative explicit input
        # captured from cwd must still use the original pinned project descriptor.
        reader=self.m._read_verify_execution_snapshot
        root=self.target; moved=self.base/"moved";cwd=Path.cwd()
        def rename_after_read(*args,**kwargs):
            value=reader(*args,**kwargs)
            root.rename(moved);root.mkdir()
            (root/receipt.name).write_bytes(b"PRIVATE-MARKER");(root/receipt.name).chmod(0o600)
            return value
        output=io.StringIO()
        try:
            os.chdir(root)
            with mock.patch.object(self.m,"_read_verify_execution_snapshot",rename_after_read),mock.patch.object(self.m,"open_existing_directory_nofollow",wraps=self.m.open_existing_directory_nofollow) as reopen,contextlib.redirect_stdout(output):
                code=self.m.main(["inspect-run",".","--run-id",run,"--final-receipt",receipt.name,"--format","json"])
            self.assertEqual(code,0,output.getvalue())
            self.assertEqual(reopen.call_count,1,"internal explicit receipt must never reopen a pathname after pinning")
            self.assertEqual(json.loads(output.getvalue())["inspection"]["historical_run_verdict"],"passed")
        finally:
            os.chdir(cwd)


    def test_private_parent_symlinks_and_resource_failures_are_bounded(self):
        run,receipt,_,_,path=self.produce()
        logs=self.target/".vibe/local/verify/logs/sha256"
        moved=self.base/"held-logs";logs.rename(moved);logs.symlink_to(moved,target_is_directory=True)
        code,_,facts=self.inspect(run,receipt)
        self.assertEqual((code,facts["artifacts"][2]["state"]),(1,"unavailable"))
        logs.unlink();moved.rename(logs)
        run_parent=path.parent;held=self.base/"held-run";run_parent.rename(held);run_parent.symlink_to(held,target_is_directory=True)
        code,_,facts=self.inspect(run,receipt)
        self.assertEqual((code,facts["metadata"]["state"],facts["historical_receipt_verdict"]),(1,"unavailable","passed"))
        run_parent.unlink();held.rename(run_parent)
        with mock.patch.object(self.m,"inspection_log",side_effect=OSError(errno.ENOTSUP,"PRIVATE-MARKER")):
            code,_,facts=self.inspect(run,receipt)
        self.assertEqual(code,2)
        self.assertIn("inspection-unsupported-filesystem",[item["code"] for item in facts["findings"]])
        closed=[];original_close=self.m.ProjectRootFD.close
        def close(project):
            closed.append(project.fd);return original_close(project)
        with mock.patch.object(self.m.ProjectRootFD,"close",close),mock.patch.object(self.m,"inspection_private_leaf",side_effect=MemoryError("PRIVATE-MARKER")):
            code,_,facts=self.inspect(run,receipt)
        self.assertEqual(code,2)
        self.assertGreaterEqual(len(closed),2)
        for descriptor in closed:
            with self.assertRaises(OSError):os.fstat(descriptor)
        with mock.patch.object(self.m,"inspection_log",wraps=self.m.inspection_log) as reads:
            # No receipt selected: metadata alone owns available logs.
            code,_,facts=self.inspect(run, self.target/"missing-explicit.json")
        self.assertEqual((code,facts["artifact_scope"],facts["artifacts"][2]["state"]),(1,"metadata","verified"))
        self.assertEqual(reads.call_count,1)



    def test_pinned_root_constructor_closes_owned_duplicate_on_initial_fstat_failure(self):
        original=os.open(self.target,os.O_RDONLY|os.O_DIRECTORY)
        self.addCleanup(os.close,original)
        duplicate=self.m.os.dup
        for error in (OSError(errno.EIO,"PRIVATE-MARKER"),MemoryError("PRIVATE-MARKER")):
            acquired=[]
            def dup(descriptor):
                value=duplicate(descriptor);acquired.append(value);return value
            with mock.patch.object(self.m.os,"dup",dup),mock.patch.object(self.m.os,"fstat",side_effect=error):
                with self.assertRaises(type(error)):
                    self.m.ProjectRootFD(self.target,descriptor=original)
            self.assertEqual(len(acquired),1)
            with self.assertRaises(OSError):os.fstat(acquired[0])
            self.assertTrue(stat.S_ISDIR(os.fstat(original).st_mode))


    def test_copied_consistent_evidence_is_not_origin_attestation(self):
        run,receipt,_,_,_=self.produce()
        copied=self.base/"copy";shutil.copytree(self.target,copied)
        code,_,facts=self.inspect(run,copied/receipt.name,target=copied)
        self.assertEqual((code,facts["historical_run_verdict"],facts["project_origin"]),(0,"passed","not-attested"))
        (copied/receipt.name).write_bytes(b"PRIVATE-MARKER")
        self.assertEqual(self.inspect(run,copied/receipt.name)[0],1)

    def test_main_stale_context_parse_failures_and_fixed_registry(self):
        run,receipt,_,_,_=self.produce()
        destination=self.target/"must-not-exist.json"
        self.m.RECEIPT_CONTEXT[0]=(destination,self.target)
        self.inspect(run,receipt)
        self.assertFalse(destination.exists());self.assertIsNone(self.m.RECEIPT_CONTEXT[0])
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
            self.m.main(["inspect-run",str(self.target),"--run-id",run,"--receipt",str(receipt)])
        self.assertIsNone(self.m.RECEIPT_CONTEXT[0])
        contract=json.loads((ROOT/"agent-install.json").read_text())
        self.assertEqual(contract["cli"]["inspect_run"],self.m.INSPECT_RUN_CONTRACT)
        self.assertEqual(contract["cli"]["command_statuses"]["inspect-run"],list(self.m.AGENT_COMMAND_STATUSES["inspect-run"]))
        doc=(ROOT/"docs/verification-observability.md").read_text()
        self.assertEqual(len(self.m.INSPECT_FINDING_CODES),15)
        for name in self.m.INSPECT_FINDING_CODES+self.m.INSPECT_NEXT_ACTIONS:self.assertIn(name,doc)



class CurrentUnpublishedIdentityTests(unittest.TestCase):
    def test_real_013_package_is_rejected_by_exact_schema6_publication_plan(self):
        m=load_cli_module()
        self.assertEqual(m.framework_version(ROOT),"0.13.0")
        self.assertEqual(m.PUBLICATION_PROFILES[6]["version"],"0.11.0")
        self.assertEqual(sorted(m.PUBLICATION_PROFILES),[2,3,4,5,6,7,8])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve();candidate=root/"candidate"
            built=run_cli(CLI,"package","--status","release-candidate-unpublished","--output",str(candidate))
            self.assertEqual(built.returncode,0,built.stdout+built.stderr)
            manifest=json.loads((candidate/"release-manifest.json").read_bytes())
            self.assertEqual((manifest["kit_version"],manifest["status"]),("0.13.0","release-candidate-unpublished"))
            reference=".agents/skills/vibe-implementation-flow/references/affected-entry-evidence.md"
            self.assertIn(reference,manifest["payload_files"])
            for archive,prefix in ((candidate/"vibe-kit-0.13.0.zip","vibe-kit-0.13.0/"),(candidate/"vibe-kit-plugin-0.13.0.zip","vibe-kit/payload/")):
                with zipfile.ZipFile(archive) as bundle:
                    self.assertIn("Node package script",bundle.read(prefix+reference).decode())
                    for skill in ("vibe-implementation-flow","vibe-verification-flow"):
                        relative=".agents/skills/"+skill+"/SKILL.md"
                        content=bundle.read(prefix+relative).decode()
                        link=re.search(r"\[Python and Node example\]\(([^)]+)\)",content).group(1)
                        resolved=posixpath.normpath(posixpath.join(posixpath.dirname(relative),link))
                        self.assertEqual(resolved,reference)
                        self.assertIn(prefix+resolved,bundle.namelist())
            request=profile_test_intent(m,6)
            self.assertEqual(m.validate_publication_intent(request),[])
            path=root/"request.json";path.write_text(json.dumps(request))
            result=run_cli(CLI,"publication-plan","--phase","publish","--request",str(path),"--candidate",str(candidate),"--format","json")
            value=json.loads(result.stdout)
            self.assertEqual((result.returncode,value["status"]),(2,"blocked"))
            self.assertIn("publication candidate must be the exact 0.11.0 prerelease",value["errors"])


class RealSlowRunInspectionTests(unittest.TestCase):
    def test_python_and_node_normal_handled_and_abrupt_runs(self):
        node=node_runtime()
        if node is None:self.skipTest("Node runtime unavailable: required Node acceptance not executed")
        m=load_cli_module()
        for kind in ("python","node"):
            for interruption in (None,signal.SIGTERM,signal.SIGINT,signal.SIGKILL):
                with self.subTest(kind=kind,signal=interruption),tempfile.TemporaryDirectory() as directory:
                    target=Path(directory).resolve()/"project";(target/".vibe").mkdir(parents=True)
                    marker=target/"started"
                    if kind=="python":
                        script=target/"slow.py";script.write_text('from pathlib import Path\nimport time\np=Path("started")\nwith p.open("a") as h: h.write("owned-python-start\\n")\nprint("PRIVATE-MARKER",flush=True)\ntime.sleep(0.6)\n')
                        command="exec "+shlex.quote(sys.executable)+" "+shlex.quote(str(script))
                    else:
                        script=target/"slow.cjs";script.write_text('require("node:fs").appendFileSync("started","owned-node-start\\n"); console.log("PRIVATE-MARKER"); setTimeout(()=>{},600);\n')
                        (target/"package.json").write_text('{"name":"slow-fixture","private":true}')
                        command="exec "+shlex.quote(node)+" "+shlex.quote(str(script))
                    (target/".vibe/project.yaml").write_text('schema_version: 1\ncommands:\n  test: '+json.dumps(command)+'\n')
                    receipt=target/"final.json"
                    process=subprocess.Popen([sys.executable,str(CLI),"verify",str(target),"--progress","--log-policy","all-configured","--receipt",str(receipt),"--format","json"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    try:
                        deadline=time.monotonic()+8
                        while (not marker.exists() or marker.stat().st_size==0) and process.poll() is None and time.monotonic()<deadline:time.sleep(0.01)
                        self.assertTrue(marker.exists(),"owned slow check did not start")
                        locator,findings=m.read_verify_locator(target);self.assertEqual(findings,[])
                        run=locator["run_id"]
                        if interruption is not None:process.send_signal(interruption)
                        stdout,stderr=process.communicate(timeout=8)
                    finally:
                        if process.poll() is None:
                            process.kill();process.communicate(timeout=8)
                    self.assertIn("run="+run,stderr)
                    self.assertEqual(marker.read_text().splitlines(),["owned-"+kind+"-start"])
                    before=snapshot_tree(target)
                    result=run_cli(CLI,"inspect-run",str(target),"--run-id",run,"--format","json")
                    facts=json.loads(result.stdout)["inspection"]
                    self.assertEqual(snapshot_tree(target),before)
                    self.assertEqual(marker.read_text().splitlines(),["owned-"+kind+"-start"])
                    self.assertNotIn("PRIVATE-MARKER",result.stdout+result.stderr)
                    self.assertEqual(facts["liveness"],"not-assessed")
                    if interruption is None:
                        self.assertEqual((process.returncode,facts["historical_run_verdict"]),(0,"passed"))
                        self.assertEqual(len(stdout.splitlines()),1)
                    elif interruption==signal.SIGKILL:
                        self.assertEqual(facts["metadata"]["run_state"],"running")
                        self.assertEqual(facts["historical_run_verdict"],"unverified")
                        self.assertFalse(receipt.exists());self.assertEqual(stdout,"")
                    else:
                        self.assertEqual((process.returncode,facts["metadata"]["run_state"],facts["historical_run_verdict"]),(2,"incomplete","not-passed"))
                        self.assertEqual(json.loads(stdout)["status"],"blocked")
                    print("SLOW-RUN-EVIDENCE "+json.dumps({"kind":kind,"signal":interruption,"run_id":run,"verify_exit":process.returncode,"inspect_exit":result.returncode,"run_verdict":facts["historical_run_verdict"]},sort_keys=True))


if __name__=="__main__":
    unittest.main()
