import contextlib
import copy
import errno
import hashlib
import io
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from tests.test_cli import CLI, ROOT, load_cli_module, profile_test_intent, profile_test_receipt, run_cli


class PublicationInputOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.candidate = self.base / "candidate"
        self.candidate.mkdir()
        self.intent = self.base / "intent.json"
        self.receipt = self.base / "input.json"
        self.authorization = self.base / "authorization.json"
        for path in (self.intent, self.receipt, self.authorization):
            path.write_bytes(b'{"schema_version": 1}\n')
        self.arguments = ["validate-publication", "--intent", str(self.intent),
                          "--receipt", str(self.receipt), "--candidate", str(self.candidate),
                          "--format", "json"]

    def invoke(self, *extra):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = self.m.main(self.arguments + list(extra))
        return code, json.loads(output.getvalue())

    def test_valid_invalid_and_error_leave_input_bytes_unchanged(self):
        for status, code in (("valid", 0), ("invalid", 1)):
            with self.subTest(status=status):
                def validator(*args):
                    self.m.print_json(self.m.result_envelope("validate-publication", status))
                    return code
                before = self.receipt.read_bytes()
                with mock.patch.object(self.m, "validate_publication", validator):
                    observed, envelope = self.invoke()
                self.assertEqual((observed, envelope["status"]), (code, status))
                self.assertEqual(self.receipt.read_bytes(), before)
                self.assertEqual(sorted(p.name for p in self.base.iterdir()),
                                 ["authorization.json", "candidate", "input.json", "intent.json"])
        self.intent.write_bytes(b"invalid json\n")
        before = self.receipt.read_bytes()
        code, value = self.invoke("--result-receipt", str(self.base / "error.json"))
        self.assertEqual((code, value["status"]), (2, "error"))
        self.assertEqual(self.receipt.read_bytes(), before)
        self.assertEqual(json.loads((self.base / "error.json").read_bytes())["status"], "error")

    def test_distinct_result_is_create_only_private_and_only_outer_result(self):
        destination = self.base / "result.json"
        def validator(*args):
            with contextlib.redirect_stdout(io.StringIO()):
                self.m.print_json({"command": "validate-release", "status": "valid"})
            self.m.print_json(self.m.result_envelope("validate-publication", "valid"))
            return 0
        with mock.patch.object(self.m, "validate_publication", validator):
            code, value = self.invoke("--result-receipt", str(destination))
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(destination.read_bytes()), value)
        self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o600)
        before = destination.read_bytes()
        code, value = self.invoke("--result-receipt", str(destination))
        self.assertEqual(code, 2)
        self.assertEqual(destination.read_bytes(), before)
        self.assertEqual(value["error"]["code"], "result_receipt_exists")

    def test_aliases_candidate_descendants_and_unsafe_parents_reject_before_temporary(self):
        symlink = self.base / "symlink.json"
        symlink.symlink_to(self.receipt)
        hardlink = self.base / "hardlink.json"
        os.link(self.receipt, hardlink)
        parent_link = self.base / "linked-parent"
        parent_link.symlink_to(self.candidate, target_is_directory=True)
        aliases = [self.receipt, self.base / "child" / ".." / "input.json", symlink,
                   hardlink, self.candidate / "result.json", parent_link / "result.json",
                   self.base / "missing" / "result.json", self.intent, self.authorization]
        if sys.platform == "darwin":
            aliases.append(self.base / "INPUT.JSON")
        for destination in aliases:
            with self.subTest(destination=destination):
                before = self.receipt.read_bytes()
                code, value = self.invoke("--authorization", str(self.authorization),
                                          "--result-receipt", str(destination))
                self.assertEqual(code, 2)
                self.assertEqual(value["status"], "error")
                self.assertEqual(self.receipt.read_bytes(), before)
                self.assertEqual(list(self.base.rglob(".vibe-evidence-*")), [])

    def test_competing_final_creation_is_never_replaced(self):
        destination = self.base / "race.json"
        original = self.m.os.link
        def competing_link(src, dst, **kwargs):
            destination.write_bytes(b"competing writer\n")
            return original(src, dst, **kwargs)
        def validator(*args):
            self.m.print_json(self.m.result_envelope("validate-publication", "valid"))
            return 0
        with mock.patch.object(self.m, "validate_publication", validator), \
             mock.patch.object(self.m.os, "link", competing_link), \
             mock.patch.object(self.m.os, "supports_dir_fd", self.m.os.supports_dir_fd | {competing_link}):
            code, value = self.invoke("--result-receipt", str(destination))
        self.assertEqual((code, value["status"]), (2, "error"))
        self.assertEqual(destination.read_bytes(), b"competing writer\n")
        self.assertEqual(list(self.base.glob(".vibe-evidence-*")), [])

    def test_main_clears_context_on_returns_and_parse_failures(self):
        stale = self.base / "stale.json"
        self.m.RECEIPT_CONTEXT[0] = (stale, self.base)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.m.main(["unknown-command"])
        self.assertIsNone(self.m.RECEIPT_CONTEXT[0])
        self.assertFalse(stale.exists())
        self.invoke()
        self.assertIsNone(self.m.RECEIPT_CONTEXT[0])
        self.assertFalse(stale.exists())

    def test_actual_profile_validation_preserves_inputs_and_only_publishes_outer_result(self):
        # Real closed profile validation and local file hashes; the nested
        # release validator is controlled, so this is not a release gate.
        profile = self.m.PUBLICATION_PROFILES[6]
        intent = profile_test_intent(self.m, 6)
        for asset in intent["assets"]:
            data = ("synthetic local artifact " + asset["name"]).encode()
            (self.candidate / asset["name"]).write_bytes(data)
            asset.update(size=len(data), sha256=hashlib.sha256(data).hexdigest())
        intent["asset_set_sha256"] = self.m.canonical_json_sha256(intent["assets"])
        for asset, operation in zip(intent["assets"], intent["operations"][3]["asset_operations"]):
            operation.update(size=asset["size"], sha256=asset["sha256"])
            identity = {"schema_version": 6, "profile": profile["profile"],
                        "parent_operation_id": intent["operations"][3]["operation_id"],
                        "natural_key": operation["natural_key"],
                        "remote_snapshot_sha256": intent["remote_snapshot_sha256"],
                        "asset": asset, "initial_observation": {"state": "absent", "id": None,
                        "size": None, "sha256": None, "download_url": None}}
            operation["expected_precondition"]["identity_sha256"] = self.m.canonical_json_sha256(identity)
        receipt = profile_test_receipt(self.m, intent, 6)
        authorization = {"authorization_id": receipt["authorization_id"], "repository": "mintgao/vibe-kit",
                         "version": "0.11.0", "release_kind": "prerelease",
                         "allowed_operations": list(self.m.V080_PUBLICATION_ALLOWED_OPERATIONS),
                         "publication_intent_sha256": self.m.canonical_json_sha256(intent),
                         "host_operation_id": receipt["host_operation_id"],
                         "authorization_source_ref": "test:existing-bound-authorization",
                         "bound_at": "2026-10-13T00:00:00Z"}
        self.intent.write_text(json.dumps(intent))
        self.authorization.write_text(json.dumps(authorization))
        def nested_validator(*args):
            self.m.print_json(self.m.result_envelope("validate-release", "valid"))
            return 0
        for invalid in (False, True):
            for explicit_output in (False, True):
                candidate_receipt = copy.deepcopy(receipt)
                if invalid:
                    candidate_receipt["downloads"][0]["matched"] = False
                self.receipt.write_text(json.dumps(candidate_receipt) + "\n")
                before = self.receipt.read_bytes()
                destination = self.base / (str(invalid) + str(explicit_output) + ".result.json")
                extra = ["--authorization", str(self.authorization)]
                if explicit_output:
                    extra += ["--result-receipt", str(destination)]
                with mock.patch.object(self.m, "validate_release", nested_validator), \
                     mock.patch.object(self.m, "publish_exclusive_bytes", wraps=self.m.publish_exclusive_bytes) as publication:
                    code, value = self.invoke(*extra)
                expected = 1 if invalid or sys.version_info[:2] != (3, 9) else 0
                self.assertEqual(code, expected, value.get("errors"))
                self.assertEqual(value["status"], "invalid" if expected else "valid")
                self.assertEqual(self.receipt.read_bytes(), before)
                self.assertEqual(publication.call_count, int(explicit_output))
                if explicit_output:
                    self.assertEqual(json.loads(destination.read_bytes())["command"], "validate-publication")


class EqualityAwareUpgradeTests(unittest.TestCase):
    def test_equal_images_satisfy_either_expectation_and_modes_still_matter(self):
        m = load_cli_module()
        pre = m.bytes_identity("regular", b"same", 0o644)
        post = m.bytes_identity("regular", b"changed", 0o644)
        intent = {"changes": [{"slot": "0", "path": "a", "preimage": pre, "postimage": pre},
                              {"slot": "1", "path": "b", "preimage": pre, "postimage": post}]}
        project = mock.Mock()
        project.read.side_effect = [("regular", b"same", 0o644), ("regular", b"changed", 0o644)]
        self.assertEqual(m.transaction_installation_state_project(project, intent, "target"), ("target", []))
        project.read.side_effect = [("regular", b"same", 0o644), ("regular", b"same", 0o644)]
        self.assertEqual(m.transaction_installation_state_project(project, intent, "predecessor"), ("predecessor", []))
        project.read.side_effect = [("regular", b"same", 0o600), ("regular", b"same", 0o644)]
        self.assertEqual(m.transaction_installation_state_project(project, intent, "target"), ("unknown", ["a"]))

    def test_two_same_version_upgrades_commit_truthfully_without_residue(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary).resolve() / "project"
            result = run_cli(CLI, "init", str(project), "--format", "json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for unused in range(2):
                result = run_cli(CLI, "upgrade", str(project), "--format", "json")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                value = json.loads(result.stdout)
                self.assertEqual(value["transaction"]["outcome"], "committed")
                self.assertEqual(value["installation_state"], "target")
                self.assertTrue(value["writes_performed"])
                self.assertFalse((project / ".vibe/local/upgrade-transactions/active").exists())
            doctor = run_cli(project / "bin/vibe", "doctor", str(project), "--format", "json")
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)


class VerificationDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.target = self.base / "project"
        (self.target / ".vibe").mkdir(parents=True)

    def config(self, commands=None, settings=""):
        commands = commands or {"test": "printf 'success-marker'"}
        data = "schema_version: 1\ncommands:\n" + "".join("  " + name + ": " + json.dumps(commands.get(name, "")) + "\n" for name in self.m.VERIFY_ORDER)
        (self.target / ".vibe/project.yaml").write_text(data + settings)

    def invoke(self, *extra):
        return run_cli(CLI, "verify", str(self.target), "--format", "json", *extra)

    def snapshot(self, envelope=None, artifacts=False):
        locator, findings = self.m.read_verify_locator(self.target)
        self.assertEqual(findings, [])
        value, findings = self.m.read_verify_execution(self.target, locator["run_id"], envelope, artifacts=artifacts)
        self.assertEqual(findings, [])
        return value

    def test_four_policy_progress_combinations_and_default_has_no_body_on_disk(self):
        for progress in (True, False):
            for policy in ("failures", "all-configured"):
                with self.subTest(progress=progress, policy=policy):
                    self.target = self.base / (str(progress) + policy)
                    (self.target / ".vibe").mkdir(parents=True)
                    self.config(settings='checks:\n  log_policy: "' + policy + '"\n  progress: ' + str(progress).lower() + '\n')
                    result = self.invoke()
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    envelope = json.loads(result.stdout)
                    self.assertEqual("full" in envelope["checks"][2]["output"], policy == "all-configured")
                    self.assertEqual((self.target / ".vibe/local/verify/runs").exists(), progress)
                    self.assertFalse(list(self.target.rglob("result.json")))
                    if progress:
                        value = self.snapshot(envelope, artifacts=True)
                        self.assertEqual(value["state"], "finished")
                        self.assertEqual(value["checks"][2]["log"]["availability"], "available" if policy == "all-configured" else "not-selected")
                        raw = (self.target / ".vibe/local/verify/runs" / value["run_id"] / "progress.json").read_text()
                        self.assertNotIn("success-marker", raw)
                        self.assertNotIn("stdout_tail", raw)
                    if policy == "failures":
                        self.assertFalse(list(self.target.rglob("*.log")))
                    else:
                        self.assertTrue(list(self.target.rglob("*.log")))

    def test_complete_success_layout_sanitization_and_deterministic_receipts(self):
        import shlex
        code = "import sys; print('FIRST'); print('x'*22000); print('ghp_'+'A'*32); print('LAST'); sys.stderr.write('BEGIN\\n'+'y'*22000+'\\nEND'); sys.stdout.write('\\x7f\\x85\\x1b[31mRED\\x1b[0m'); sys.stdout.write('-----BEGIN PRIVATE KEY-----\\nsecret-body\\n-----END PRIVATE KEY-----\\n'); sys.stdout.write('-----BEGIN RSA PRIVATE KEY-----\\nunterminated-secret')"
        command = shlex.quote(sys.executable) + " -c " + shlex.quote(code)
        self.config({"test": command}, 'checks:\n  log_policy: "all-configured"\n')
        receipts = []
        for index in range(2):
            destination = self.target / ("receipt" + str(index) + ".json")
            result = self.invoke("--receipt", str(destination))
            self.assertEqual(result.returncode, 0, result.stderr)
            envelope = json.loads(result.stdout)
            value = self.snapshot(envelope, artifacts=True)
            check = envelope["checks"][2]
            self.assertTrue(check["output"]["stdout_truncated"])
            full = check["output"]["full"]
            content = (self.target / full["path"]).read_bytes()
            self.assertTrue(content.startswith(b"=== stdout ===\nFIRST\n"))
            self.assertIn(b"\n=== stderr ===\nBEGIN\n", content)
            self.assertTrue(content.endswith(b"\nEND"))
            self.assertIn(b"LAST", content)
            self.assertNotIn(b"ghp_", content)
            self.assertNotIn(b"secret-body", content)
            self.assertNotIn(b"unterminated-secret", content)
            self.assertNotIn(b"\x7f", content)
            self.assertNotIn(b"\xc2\x85", content)
            self.assertNotIn(b"\x1b", content)
            self.assertEqual(hashlib.sha256(content).hexdigest(), full["sha256"])
            self.assertEqual(value["checks"][2]["log"]["bytes"], len(content))
            self.assertEqual(stat.S_IMODE((self.target / full["path"]).stat().st_mode), 0o600)
            receipts.append(destination.read_bytes())
        self.assertEqual(receipts[0], receipts[1])
        self.assertEqual(len(list((self.target / ".vibe/local/verify/logs/sha256").glob("*.log"))), 1)
        for directory in (self.target / ".vibe/local/verify").rglob("*"):
            if directory.is_dir():
                self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)
        self.assertEqual(value["result"]["receipt"]["scope"], "project")

    def test_storage_failures_and_hard_links_leave_project_verdict_and_later_checks(self):
        self.config({"test": "printf complete", "build": "true"}, 'checks:\n  log_policy: "all-configured"\n')
        first = self.invoke()
        full = json.loads(first.stdout)["checks"][2]["output"]["full"]
        os.link(self.target / full["path"], self.base / "extra-link")
        second = self.invoke()
        self.assertEqual(second.returncode, 0, second.stderr)
        envelope = json.loads(second.stdout)
        self.assertNotIn("full", envelope["checks"][2]["output"])
        value = self.snapshot(envelope)
        self.assertEqual(value["checks"][2]["log"]["availability"], "unavailable")
        self.assertEqual(value["checks"][3]["outcome"], "passed")
        output = io.StringIO()
        with mock.patch.object(self.m.VerifyPrivateStore, "log", side_effect=OSError(errno.ENOSPC, "sensitive error")), contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            code = self.m.verify(self.target, [], "json", "all-configured")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["checks"][3]["outcome"], "passed")
        value = self.snapshot(json.loads(output.getvalue()))
        self.assertEqual(value["checks"][2]["log"]["reason"], "resource-exhausted")

    def test_progress_failure_is_independent_from_logs_and_receipt_failure_is_nonzero(self):
        self.config(settings='checks:\n  log_policy: "all-configured"\n')
        output = io.StringIO()
        errors = io.StringIO()
        with mock.patch.object(self.m.VerifyPrivateStore, "metadata", side_effect=PermissionError()), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = self.m.verify(self.target, [], "json")
        self.assertEqual(code, 0)
        self.assertIn("full", json.loads(output.getvalue())["checks"][2]["output"])
        self.assertIn("progress=unavailable", errors.getvalue())
        result = self.invoke("--receipt", str(self.base / "missing" / "receipt.json"))
        self.assertEqual(result.returncode, 2)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["status"], "error")
        value = self.snapshot(envelope)
        self.assertEqual(value["checks"][2]["outcome"], "passed")
        self.assertEqual(value["result"]["receipt"]["availability"], "unavailable")
        self.assertFalse((self.base / "missing").exists())

    def test_progress_memory_failures_preserve_later_checks_logs_receipt_and_release_store(self):
        for phase in ("constructor", "initial-snapshot", "locator", "after-check", "terminal"):
            with self.subTest(phase=phase):
                self.target = self.base / phase
                (self.target / ".vibe").mkdir(parents=True)
                self.config({"lint": "true", "test": "printf later > later-marker"},
                            'checks:\n  log_policy: "all-configured"\n')
                original_init = self.m.VerifyPrivateStore.__init__
                original_metadata = self.m.VerifyPrivateStore.metadata
                stores, triggered = [], []
                def initialize(store, target):
                    if phase == "constructor" and not triggered:
                        triggered.append(True)
                        raise MemoryError("controlled optional-store exhaustion")
                    original_init(store, target)
                    stores.append(store)
                def metadata(store, path, value):
                    fault = ((phase == "initial-snapshot" and path.endswith("progress.json"))
                             or (phase == "locator" and path.endswith("latest.json"))
                             or (phase == "after-check" and path.endswith("progress.json")
                                 and value["checks"][0]["state"] == "finished")
                             or (phase == "terminal" and value.get("state") == "finished"))
                    if fault and not triggered:
                        triggered.append(True)
                        raise MemoryError("controlled optional-store exhaustion")
                    return original_metadata(store, path, value)
                output, errors = io.StringIO(), io.StringIO()
                receipt = self.target / "receipt.json"
                with mock.patch.object(self.m.VerifyPrivateStore, "__init__", initialize), \
                     mock.patch.object(self.m.VerifyPrivateStore, "metadata", metadata), \
                     contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                    code = self.m.main(["verify", str(self.target), "--format", "json", "--receipt", str(receipt)])
                self.assertTrue(triggered)
                self.assertEqual(code, 0)
                envelope = json.loads(output.getvalue())
                self.assertEqual(envelope["status"], "passed")
                self.assertEqual((self.target / "later-marker").read_text(), "later")
                self.assertEqual(envelope["checks"][0]["outcome"], "passed")
                self.assertEqual(envelope["checks"][2]["outcome"], "passed")
                self.assertIn("full", envelope["checks"][2]["output"])
                self.assertEqual(json.loads(receipt.read_bytes())["status"], "passed")
                self.assertIn("progress=unavailable reason=resource-exhausted", errors.getvalue())
                self.assertNotIn("controlled optional-store exhaustion", errors.getvalue())
                self.assertTrue(all(store.project.fd == -1 for store in stores))

    def test_metadata_memory_failure_closes_descriptors_and_owned_temporary(self):
        store = self.m.VerifyPrivateStore(self.target)
        self.addCleanup(store.close)
        for phase in ("temporary-name", "serialization"):
            with self.subTest(phase=phase):
                original_open, original_dup, original_close = os.open, os.dup, os.close
                original_dumps = json.dumps
                owned = set()
                def opened(*args, **kwargs):
                    descriptor = original_open(*args, **kwargs)
                    owned.add(descriptor)
                    return descriptor
                def duplicated(*args, **kwargs):
                    descriptor = original_dup(*args, **kwargs)
                    owned.add(descriptor)
                    return descriptor
                def closed(descriptor):
                    owned.discard(descriptor)
                    return original_close(descriptor)
                def serialized(*args, **kwargs):
                    if phase == "serialization":
                        raise MemoryError("controlled metadata serialization exhaustion")
                    return original_dumps(*args, **kwargs)
                with mock.patch.object(self.m.os, "open", opened), \
                     mock.patch.object(self.m.os, "dup", duplicated), \
                     mock.patch.object(self.m.os, "close", closed), \
                     mock.patch.object(self.m.json, "dumps", serialized), \
                     mock.patch.object(self.m.secrets, "token_hex", side_effect=MemoryError() if phase == "temporary-name" else ["a" * 32]):
                    with self.assertRaises(MemoryError):
                        store.metadata(".vibe/local/verify/runs/memory-case/progress.json", {})
                self.assertEqual(owned, set())
                self.assertFalse(list(self.target.rglob(".vibe-evidence-*")))

    def test_checks_config_rejects_duplicate_malformed_and_unknown_values_before_running(self):
        variants = ['checks:\n  progress: 1\n', 'checks:\n  log_policy: "other"\n',
                    'checks: {"progress": false}\n', 'checks: []\n',
                    'checks :\n  progress: false\n', '  checks:\n    progress: false\n',
                    'checks:\n  progress: true\n  progress: false\n',
                    'checks:\n  requires: {"test": [], "test": []}\n',
                    'checks:\n  requires:\n    test: []\n    test: []\n',
                    'checks:\n  progress: true\nchecks:\n  progress: false\n',
                    'checks:\n  unknown: true\n']
        for settings in variants:
            with self.subTest(settings=settings):
                self.config({"test": "touch ran"}, settings)
                result = self.invoke()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.target / "ran").exists())
                self.assertFalse((self.target / ".vibe/local/verify/runs").exists())

    def test_schema_reader_rejects_tamper_unknowns_envelope_mismatch_and_duplicate_json(self):
        self.config(settings='checks:\n  log_policy: "all-configured"\n')
        result = self.invoke()
        envelope = json.loads(result.stdout)
        value = self.snapshot(envelope, artifacts=True)
        for mutation in (lambda v: v.update(unknown=True),
                         lambda v: v.update(schema_version=True),
                         lambda v: v.update(updated_at="2026-13-01T00:00:00.000000Z"),
                         lambda v: v["checks"][2]["log"].update(bytes=True),
                         lambda v: v["checks"][2]["log"].update(path="../escape"),
                         lambda v: v["result"].update(status=["passed"]),
                         lambda v: v["interruption"] is None and v.update(interruption={"reason": "sigterm"})):
            candidate = copy.deepcopy(value)
            mutation(candidate)
            candidate["metadata_sha256"] = self.m.canonical_json_sha256({k: v for k, v in candidate.items() if k != "metadata_sha256"})
            self.assertTrue(self.m.validate_verify_execution(candidate))
        modified = copy.deepcopy(envelope)
        modified["status"] = "failed"
        self.assertTrue(self.m.validate_verify_execution(value, modified, root=self.target))
        full_path = self.target / value["checks"][2]["log"]["path"]
        full_path.write_bytes(b"tampered")
        unused, findings = self.m.read_verify_execution(self.target, value["run_id"], envelope, artifacts=True)
        self.assertTrue(findings)
        path = self.target / ".vibe/local/verify/runs" / value["run_id"] / "progress.json"
        path.write_bytes(b'{"schema_version":1,"schema_version":1}')
        unused, findings = self.m.read_verify_execution(self.target, value["run_id"])
        self.assertTrue(findings)
        # Bad/missing progress does not rewrite or independently invalidate the envelope.
        self.assertEqual(envelope["status"], "passed")

    def test_execution_reader_rejects_leading_zero_version_components(self):
        self.config()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        value = self.snapshot(json.loads(result.stdout))
        for version in ("00.011.0", "01.11.0", "0.01.0", "0.11.00", "0.11.0\n", "٠.11.0"):
            with self.subTest(version=version):
                candidate = copy.deepcopy(value)
                candidate["kit_version"] = version
                candidate["metadata_sha256"] = self.m.canonical_json_sha256({key: item for key, item in candidate.items() if key != "metadata_sha256"})
                self.assertIn({"code": "execution-version", "path": "$.kit_version"},
                              self.m.validate_verify_execution(candidate))
        for version in ("0.11.0", "0.0.0", "10.20.30"):
            candidate = copy.deepcopy(value)
            candidate["kit_version"] = version
            candidate["metadata_sha256"] = self.m.canonical_json_sha256({key: item for key, item in candidate.items() if key != "metadata_sha256"})
            self.assertEqual(self.m.validate_verify_execution(candidate), [])

    def test_unsafe_common_parent_is_unavailable_without_fallback(self):
        self.config(settings='checks:\n  log_policy: "all-configured"\n')
        outside = self.base / "outside"
        outside.mkdir()
        (self.target / ".vibe/local").symlink_to(outside, target_is_directory=True)
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("progress=unavailable", result.stderr)
        self.assertIn("log=unavailable", result.stderr)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertNotIn("full", json.loads(result.stdout)["checks"][2]["output"])

    def test_slow_silent_check_has_before_check_metadata_and_handled_signals(self):
        import shlex
        for signum in (signal.SIGINT, signal.SIGTERM):
            with self.subTest(signal=signum):
                self.target = self.base / str(signum)
                (self.target / ".vibe").mkdir(parents=True)
                self.config({"lint": "true", "test": "exec " + shlex.quote(sys.executable) + " -c " + shlex.quote("import time; time.sleep(20)"), "build": "touch never"})
                process = subprocess.Popen([sys.executable, str(CLI), "verify", str(self.target), "--format", "json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                deadline = time.monotonic() + 10
                active = None
                while time.monotonic() < deadline:
                    locator, findings = self.m.read_verify_locator(self.target)
                    if not findings:
                        active, findings = self.m.read_verify_execution(self.target, locator["run_id"])
                        if active and active["current_check"] == "test":
                            break
                    time.sleep(0.02)
                self.assertIsNotNone(active)
                self.assertEqual(active["current_check"], "test")
                self.assertEqual(active["checks"][0]["outcome"], "passed")
                self.assertEqual(active["checks"][2]["state"], "running")
                self.assertIsNone(active["result"])
                process.send_signal(signum)
                stdout, stderr = process.communicate(timeout=5)
                self.assertEqual(process.returncode, 2, stderr.decode())
                envelope = json.loads(stdout)
                self.assertEqual(envelope["status"], "blocked")
                value = self.snapshot(envelope)
                self.assertEqual(value["state"], "incomplete")
                self.assertEqual(value["interruption"]["descendants"], "not-proven")
                self.assertEqual(value["interruption"]["direct_child"], "reaped")
                self.assertEqual(value["checks"][2]["state"], "interrupted")
                self.assertEqual(value["checks"][3]["state"], "not-started")
                self.assertFalse((self.target / "never").exists())
                self.assertNotIn(b"time.sleep", stderr)

    def test_sigkill_leaves_last_observation_without_result(self):
        import shlex
        self.config({"test": "exec " + shlex.quote(sys.executable) + " -c " + shlex.quote("import time; time.sleep(0.7)")})
        process = subprocess.Popen([sys.executable, str(CLI), "verify", str(self.target), "--format", "json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deadline = time.monotonic() + 10
        value = None
        while time.monotonic() < deadline:
            locator, findings = self.m.read_verify_locator(self.target)
            if not findings:
                value, findings = self.m.read_verify_execution(self.target, locator["run_id"])
                if value and value["current_check"] == "test":
                    break
            time.sleep(0.02)
        self.assertIsNotNone(value)
        process.kill()
        stdout, unused = process.communicate(timeout=3)
        self.assertEqual(stdout, b"")
        last, findings = self.m.read_verify_execution(self.target, value["run_id"])
        self.assertEqual(findings, [])
        self.assertEqual(last["state"], "running")
        self.assertIsNone(last["result"])

    def test_concurrent_runs_content_reuse_and_locator_last_publication_order(self):
        import concurrent.futures
        import threading
        self.config(settings='checks:\n  log_policy: "all-configured"\n')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda unused: self.invoke(), range(4)))
        run_ids = []
        identities = []
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("log=available", result.stderr)
            envelope = json.loads(result.stdout)
            run_id = next(part[4:] for part in result.stderr.split() if part.startswith("run="))
            run_ids.append(run_id)
            value, findings = self.m.read_verify_execution(self.target, run_id, envelope, artifacts=True)
            self.assertEqual(findings, [])
            self.assertEqual(value["state"], "finished")
            identities.append(envelope["checks"][2]["output"]["full"])
        self.assertEqual(len(set(run_ids)), 4)
        self.assertTrue(all(identity == identities[0] for identity in identities))
        held = threading.Event()
        release = threading.Event()
        original = self.m.VerifyPrivateStore.metadata
        first_id = []
        def delayed(store, path, value):
            if path.endswith("latest.json") and threading.current_thread().name == "first-run":
                first_id.append(value["run_id"])
                held.set()
                self.assertTrue(release.wait(5))
            return original(store, path, value)
        selection = {"mode": "default", "requested": [], "coverage": "all-configured"}
        progress_objects = []
        def first():
            progress_objects.append(self.m.VerifyProgress(self.target, self.m.VERIFY_ORDER, {"test": "true"}, self.m.VERIFY_ORDER, selection, "failures", True))
        with mock.patch.object(self.m.VerifyPrivateStore, "metadata", delayed), contextlib.redirect_stderr(io.StringIO()):
            thread = threading.Thread(target=first, name="first-run")
            thread.start()
            self.assertTrue(held.wait(5))
            second = self.m.VerifyProgress(self.target, self.m.VERIFY_ORDER, {"test": "true"}, self.m.VERIFY_ORDER, selection, "failures", True)
            before, findings = self.m.read_verify_locator(self.target)
            self.assertEqual(findings, [])
            self.assertEqual(before["run_id"], second.value["run_id"])
            release.set()
            thread.join(5)
            self.assertFalse(thread.is_alive())
            after, findings = self.m.read_verify_locator(self.target)
            self.assertEqual(findings, [])
            self.assertEqual(after["run_id"], first_id[0])
            self.assertLessEqual(after["started_at"], before["started_at"])
            second.close()
            progress_objects[0].close()

    def test_external_receipt_identity_and_cross_parent_fixed_envelopes(self):
        self.config(settings='checks:\n  log_policy: "all-configured"\n')
        receipts = []
        for index in range(2):
            self.target = self.base / ("parent" + str(index)) / "project"
            (self.target / ".vibe").mkdir(parents=True)
            self.config(settings='checks:\n  log_policy: "all-configured"\n')
            destination = self.base / ("external" + str(index) + ".json")
            result = self.invoke("--receipt", str(destination))
            self.assertEqual(result.returncode, 0, result.stderr)
            envelope = json.loads(result.stdout)
            value = self.snapshot(envelope, artifacts=True)
            self.assertEqual(value["result"]["receipt"]["scope"], "external")
            self.assertIsNone(value["result"]["receipt"]["path"])
            raw = destination.read_bytes()
            unused, findings = self.m.read_verify_execution(self.target, value["run_id"], envelope, artifacts=True, external_receipt=raw)
            self.assertEqual(findings, [])
            unused, findings = self.m.read_verify_execution(self.target, value["run_id"], envelope, artifacts=True, external_receipt=b"changed")
            self.assertTrue(findings)
            receipts.append(raw)
        self.assertEqual(receipts[0], receipts[1])

    def test_runner_error_and_process_start_failures_preserve_prior_checks(self):
        self.config({"lint": "true", "test": "true", "build": "touch not-started"})
        original = self.m.capture_verify_check
        def fail_test(command, target, runner):
            if command == "true" and len(records) == 1:
                raise RuntimeError("sensitive runner exception")
            records.append(command)
            return original(command, target, runner)
        records = []
        output, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(self.m, "capture_verify_check", fail_test), contextlib.redirect_stdout(output), contextlib.redirect_stderr(stderr):
            code = self.m.verify(self.target, [], "json")
        self.assertEqual(code, 2)
        envelope = json.loads(output.getvalue())
        self.assertEqual(envelope["checks"][0]["outcome"], "passed")
        value = self.snapshot(envelope)
        self.assertEqual(value["state"], "incomplete")
        self.assertEqual(value["interruption"]["reason"], "runner-error")
        self.assertEqual(value["checks"][2]["state"], "not-started")
        self.assertNotIn("sensitive runner exception", stderr.getvalue())
        self.assertFalse((self.target / "not-started").exists())
        output = io.StringIO()
        with mock.patch.object(self.m, "capture_verify_check", side_effect=OSError("private start error")), contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            code = self.m.verify(self.target, [], "json")
        self.assertEqual(code, 2)
        envelope = json.loads(output.getvalue())
        value = self.snapshot(envelope)
        self.assertEqual(value["state"], "finished")
        self.assertIsNone(value["interruption"])
        self.assertTrue(all(check["state"] == "not-started" and check["reason_code"] == "process-start-failed" for check in value["checks"] if check["configured"]))

    def test_interrupted_explicit_receipt_and_surviving_descendant_have_no_cancellation_claim(self):
        import shlex
        child_code = "from pathlib import Path; import time; Path('descendant-started').write_text('yes'); time.sleep(0.8); Path('descendant-survived').write_text('yes')"
        command = shlex.quote(sys.executable) + " -c " + shlex.quote(child_code) + " & wait"
        self.config({"lint": "true", "test": command, "build": "touch never"}, 'checks:\n  log_policy: "all-configured"\n')
        receipt = self.target / "blocked.json"
        process = subprocess.Popen([sys.executable, str(CLI), "verify", str(self.target), "--format", "json", "--receipt", str(receipt)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and not (self.target / "descendant-started").exists():
            time.sleep(0.02)
        self.assertTrue((self.target / "descendant-started").exists())
        process.terminate()
        stdout, stderr = process.communicate(timeout=5)
        self.assertEqual(process.returncode, 2, stderr.decode())
        envelope = json.loads(stdout)
        self.assertEqual(envelope["status"], "blocked")
        value = self.snapshot(envelope, artifacts=True)
        self.assertEqual(value["state"], "incomplete")
        self.assertEqual(value["result"]["receipt"]["availability"], "available")
        self.assertEqual(json.loads(receipt.read_bytes())["status"], "blocked")
        self.assertEqual(value["checks"][0]["log"]["availability"], "available")
        self.assertEqual(value["checks"][2]["log"]["availability"], "incomplete")
        self.assertEqual(value["interruption"]["descendants"], "not-proven")
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline and not (self.target / "descendant-survived").exists():
            time.sleep(0.02)
        self.assertTrue((self.target / "descendant-survived").exists())
        self.assertFalse((self.target / "never").exists())

    def test_private_modes_under_permissive_umask_and_nested_git_exclusion(self):
        self.config(settings='checks:\n  log_policy: "all-configured"\n')
        original = os.umask(0)
        try:
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
                code = self.m.verify(self.target, [], "json")
        finally:
            os.umask(original)
        self.assertEqual(code, 0)
        envelope = json.loads(output.getvalue())
        value = self.snapshot(envelope, artifacts=True)
        for path in (self.target / ".vibe/local").rglob("*"):
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700 if path.is_dir() else 0o600)
        initialized = subprocess.run(["git", "init", str(self.target)], capture_output=True)
        self.assertEqual(initialized.returncode, 0)
        progress = ".vibe/local/verify/runs/" + value["run_id"] + "/progress.json"
        checked = subprocess.run(["git", "check-ignore", progress, value["checks"][2]["log"]["path"]], cwd=self.target, capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(len(checked.stdout.splitlines()), 2)
        future = "2999-01-01T00:00:00.000000Z"
        self.assertEqual(self.m.verify_timestamp(future), future)

    def test_terminal_interruption_preserves_complete_outcomes_and_binds_blocked_receipt(self):
        self.config({"test": "true"}, 'checks:\n  log_policy: "all-configured"\n')
        original = self.m.write_verify_receipt
        calls = []
        def signal_during_receipt(envelope, destination, target):
            value = original(envelope, destination, target)
            calls.append(envelope["status"])
            if len(calls) == 1:
                os.kill(os.getpid(), signal.SIGTERM)
            return value
        receipt = self.target / "late-interruption.json"
        old_handler = signal.getsignal(signal.SIGTERM)
        output = io.StringIO()
        with mock.patch.object(self.m, "write_verify_receipt", signal_during_receipt), contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            self.m.RECEIPT_CONTEXT[0] = (receipt, self.target)
            code = self.m.verify(self.target, [], "json")
        self.assertEqual(code, 2)
        self.assertEqual(signal.getsignal(signal.SIGTERM), old_handler)
        envelope = json.loads(output.getvalue())
        self.assertEqual(envelope["status"], "blocked")
        self.assertEqual(envelope["summary"]["passed"], 1)
        self.assertEqual(envelope["summary"]["skipped"], 0)
        value = self.snapshot(envelope, artifacts=True)
        self.assertEqual(value["state"], "incomplete")
        self.assertEqual(value["checks"][2]["state"], "finished")
        self.assertEqual(value["interruption"]["reason"], "sigterm")
        self.assertEqual(value["interruption"]["direct_child"], "reaped")
        self.assertEqual(json.loads(receipt.read_bytes())["status"], "blocked")
        self.assertEqual(calls, ["passed", "blocked"])

    def test_terminal_metadata_interruption_is_reconciled_before_json_delivery(self):
        self.config({"test": "true"})
        original = self.m.VerifyPrivateStore.metadata
        triggered = []
        def signal_during_metadata(store, path, value):
            if path.endswith("progress.json") and value.get("state") == "finished" and not triggered:
                triggered.append(True)
                os.kill(os.getpid(), signal.SIGINT)
            return original(store, path, value)
        output = io.StringIO()
        with mock.patch.object(self.m.VerifyPrivateStore, "metadata", signal_during_metadata), contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            code = self.m.verify(self.target, [], "json")
        self.assertEqual(code, 2)
        envelope = json.loads(output.getvalue())
        value = self.snapshot(envelope)
        self.assertEqual(envelope["status"], "blocked")
        self.assertEqual(value["state"], "incomplete")
        self.assertEqual(value["result"]["receipt"]["availability"], "not-requested")
        self.assertEqual(value["interruption"]["direct_child"], "reaped")
        self.assertEqual(value["checks"][2]["outcome"], "passed")

    def terminal_transition(self, number, *, progress="available", receipt_mode="available"):
        # Read-only tracing changes scheduling only; no production function is
        # patched. Send a real signal immediately before the delivery arm runs.
        label = str(number) + progress + receipt_mode
        self.target = self.base / label
        (self.target / ".vibe").mkdir(parents=True)
        self.config({"test": "printf transition-marker"})
        outside = self.base / (label + "-outside")
        if progress == "unavailable":
            outside.mkdir()
            (outside / "sentinel").write_text("preserved")
            (self.target / ".vibe/local").symlink_to(outside, target_is_directory=True)
        receipt = self.target / ("missing/receipt.json" if receipt_mode == "unavailable" else "receipt.json")
        arguments = ["verify", str(self.target), "--format", "json"]
        if progress == "disabled":
            arguments.append("--no-progress")
        if receipt_mode != "none":
            arguments += ["--receipt", str(receipt)]
        transition = next(index + 1 for index, line in enumerate(CLI.read_text().splitlines())
                          if line.strip() == "runner.delivering = True")
        sent = []
        def trace(frame, event, arg):
            if (event == "line" and frame.f_code is self.m.verify.__code__
                    and frame.f_lineno == transition and not sent):
                sent.append(True)
                os.kill(os.getpid(), number)
            return trace
        previous_trace = sys.gettrace()
        previous_handlers = {value: signal.getsignal(value) for value in (signal.SIGINT, signal.SIGTERM)}
        output, errors = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                sys.settrace(trace)
                code = self.m.main(arguments)
        finally:
            sys.settrace(previous_trace)
        self.assertTrue(sent)
        self.assertEqual(code, 2)
        self.assertEqual(sys.gettrace(), previous_trace)
        self.assertEqual({value: signal.getsignal(value) for value in previous_handlers}, previous_handlers)
        envelope = json.loads(output.getvalue())
        self.assertEqual(envelope["status"], "error" if receipt_mode == "unavailable" else "blocked")
        self.assertEqual(envelope["summary"]["passed"], 1)
        self.assertEqual(envelope["summary"]["skipped"], 0)
        self.assertEqual(envelope["checks"][2]["outcome"], "passed")
        self.assertEqual(output.getvalue().count("\n"), 1)
        if receipt_mode == "available":
            self.assertEqual(json.loads(receipt.read_bytes())["status"], "blocked")
        else:
            self.assertFalse(receipt.exists())
        if progress == "available":
            value = self.snapshot(envelope, artifacts=True)
            self.assertEqual(value["state"], "incomplete")
            self.assertEqual(value["interruption"]["reason"], "sigterm" if number == signal.SIGTERM else "sigint")
            self.assertEqual(value["interruption"]["descendants"], "not-proven")
            self.assertEqual(value["checks"][2]["state"], "finished")
        elif progress == "disabled":
            self.assertFalse((self.target / ".vibe/local/verify/runs").exists())
        else:
            self.assertEqual(sorted(path.name for path in outside.iterdir()), ["sentinel"])
            self.assertEqual((outside / "sentinel").read_text(), "preserved")
            self.assertIn("progress=unavailable", errors.getvalue())
        self.assertFalse(list(self.target.rglob("result.json")))
        self.assertIsNone(self.m.RECEIPT_CONTEXT[0])

    def test_observed_terminal_transition_sigterm_sigint_binds_nonpassing_output(self):
        for number in (signal.SIGTERM, signal.SIGINT):
            with self.subTest(signal=number):
                self.terminal_transition(number)

    def test_observed_terminal_transition_is_independent_of_optional_artifacts(self):
        for progress, receipt_mode in (("available", "none"), ("available", "unavailable"),
                                       ("disabled", "available"), ("unavailable", "available")):
            with self.subTest(progress=progress, receipt=receipt_mode):
                self.terminal_transition(signal.SIGTERM, progress=progress, receipt_mode=receipt_mode)

    def terminal_backpressure(self, number, *, progress=True, receipt_mode="available"):
        import select
        import shlex
        label = str(number) + str(progress) + receipt_mode
        self.target = self.base / label
        (self.target / ".vibe").mkdir(parents=True)
        commands = {}
        for name in self.m.VERIFY_ORDER:
            code = 'from pathlib import Path; print("x" * 300000); Path("done-' + name + '").write_text("done")'
            commands[name] = "exec " + shlex.quote(sys.executable) + " -c " + shlex.quote(code)
        self.config(commands, 'checks:\n  output_limit_bytes: 300000\n')
        receipt = self.target / ("missing/receipt.json" if receipt_mode == "unavailable" else "receipt.json")
        arguments = [sys.executable, str(CLI), "verify", str(self.target), "--format", "json"]
        if not progress:
            arguments.append("--no-progress")
        if receipt_mode != "none":
            arguments += ["--receipt", str(receipt)]
        process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.monotonic() + 10
            observed, locator = None, None
            while time.monotonic() < deadline:
                if progress:
                    locator, unused = self.m.read_verify_locator(self.target)
                    if locator:
                        observed, unused = self.m.read_verify_execution(self.target, locator["run_id"])
                    terminal = observed and observed["state"] == "finished"
                else:
                    terminal = all((self.target / ("done-" + name)).is_file() for name in self.m.VERIFY_ORDER)
                if terminal and select.select([process.stdout], [], [], 0)[0] and process.poll() is None:
                    break
                time.sleep(0.01)
            self.assertTrue(terminal, "terminal backpressure premise was not observed")
            self.assertIsNone(process.poll())
            # Leave stdout undrained until the handled signal reaches the real CLI.
            os.kill(process.pid, number)
            # The interrupted fd writer must stop without a consumer draining
            # its pipe or a shutdown flush resuming the undelivered suffix.
            process.wait(timeout=3)
            stdout, stderr = process.communicate(timeout=5)
            self.assertEqual(process.returncode, 2, stderr.decode("utf-8", errors="replace"))
            self.assertGreater(len(stdout), 0)
            with self.assertRaises(json.JSONDecodeError):
                json.loads(stdout)
            self.assertEqual(stdout.count(b"\n"), 0, "no replacement JSON may be appended")
            self.assertIn(b"delivery=incomplete", stderr)
            self.assertTrue(all((self.target / ("done-" + name)).is_file() for name in self.m.VERIFY_ORDER))
            envelope = json.loads(receipt.read_bytes()) if receipt_mode == "available" else None
            if envelope is not None:
                self.assertEqual(envelope["status"], "blocked")
                self.assertEqual(envelope["summary"]["passed"], 4)
                self.assertEqual(envelope["summary"]["skipped"], 0)
            else:
                self.assertFalse(receipt.exists())
            if progress:
                value, findings = self.m.read_verify_execution(self.target, locator["run_id"], envelope, artifacts=True)
                self.assertEqual(findings, [])
                self.assertEqual(value["state"], "incomplete")
                self.assertEqual(value["interruption"]["reason"], "sigterm" if number == signal.SIGTERM else "sigint")
                self.assertEqual(value["interruption"]["descendants"], "not-proven")
                self.assertEqual(value["result"]["status"], "error" if receipt_mode == "unavailable" else "blocked")
                self.assertEqual(value["result"]["exit_code"], 2)
                self.assertEqual(value["result"]["receipt"]["availability"],
                                 {"available": "available", "none": "not-requested", "unavailable": "unavailable"}[receipt_mode])
                self.assertTrue(all(check["state"] == "finished" and check["outcome"] == "passed" for check in value["checks"]))
            else:
                self.assertFalse((self.target / ".vibe/local/verify/runs").exists())
            self.assertFalse(list(self.target.rglob("*.log")))
            self.assertFalse(list(self.target.rglob("result.json")))
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate(timeout=5)

    def test_terminal_stdout_backpressure_sigterm_and_sigint_are_incomplete(self):
        for number in (signal.SIGTERM, signal.SIGINT):
            with self.subTest(signal=number):
                self.terminal_backpressure(number)

    def test_terminal_stdout_backpressure_preserves_diagnostic_availability_boundaries(self):
        for number, progress, receipt_mode in ((signal.SIGTERM, True, "none"),
                                             (signal.SIGTERM, True, "unavailable"),
                                             (signal.SIGTERM, False, "available"),
                                             (signal.SIGINT, False, "none")):
            with self.subTest(signal=number, progress=progress, receipt=receipt_mode):
                self.terminal_backpressure(number, progress=progress, receipt_mode=receipt_mode)

    def test_output_producing_slow_check_has_metadata_and_split_secret_is_sanitized(self):
        import shlex
        code = "import os,sys,time; print('slow-first',flush=True); sys.stdout.write('ghp_'); sys.stdout.flush(); time.sleep(0.4); sys.stdout.write('A'*32+'\\n'); sys.stdout.flush(); os.write(2,b'bad-utf8:\\xff'); print('slow-last')"
        self.config({"test": "exec " + shlex.quote(sys.executable) + " -c " + shlex.quote(code)}, 'checks:\n  log_policy: "all-configured"\n')
        process = subprocess.Popen([sys.executable, str(CLI), "verify", str(self.target), "--format", "json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deadline = time.monotonic() + 10
        running = None
        while time.monotonic() < deadline:
            locator, findings = self.m.read_verify_locator(self.target)
            if not findings:
                running, findings = self.m.read_verify_execution(self.target, locator["run_id"])
                if running and running["current_check"] == "test":
                    break
            time.sleep(0.02)
        self.assertIsNotNone(running)
        self.assertEqual(running["checks"][2]["state"], "running")
        self.assertEqual(running["checks"][2]["log"]["availability"], "pending")
        stdout, stderr = process.communicate(timeout=5)
        self.assertEqual(process.returncode, 0, stderr.decode())
        envelope = json.loads(stdout)
        value = self.snapshot(envelope, artifacts=True)
        raw = (self.target / value["checks"][2]["log"]["path"]).read_bytes()
        self.assertIn(b"slow-first", raw)
        self.assertIn(b"slow-last", raw)
        self.assertNotIn(b"ghp_", raw)
        self.assertIn(b"[REDACTED]", raw)
        self.assertIn("bad-utf8:�".encode(), raw)
        metadata = (self.target / ".vibe/local/verify/runs" / value["run_id"] / "progress.json").read_bytes()
        self.assertNotIn(b"slow-first", metadata)
        self.assertNotIn(b"ghp_", metadata)
