"""Synthetic schema-8 contracts for ADR0026; these are not release/host receipts."""
import contextlib
import copy
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest import mock

from tests.test_cli import (
    ROOT, load_cli_module, passing_command, profile_test_intent, profile_test_receipt,
)

CRITERIA = ["AC-" + str(number) for number in range(1, 11)]
SMOKES = (
    "public-direct-init-doctor", "public-plugin-bundled-plan-init-doctor",
    "public-upgrade-v0.3-to-v0.13.0", "public-upgrade-v0.5-to-v0.13.0",
    "public-upgrade-v0.6-to-v0.13.0", "public-upgrade-v0.7-to-v0.13.0",
    "public-upgrade-v0.8-to-v0.13.0", "public-upgrade-v0.9-to-v0.13.0",
    "public-upgrade-v0.10.0-to-v0.13.0", "public-upgrade-v0.10.1-to-v0.13.0",
    "public-upgrade-v0.11.0-to-v0.13.0", "public-upgrade-v0.12.0-to-v0.13.0",
    "public-repeat-upgrade-v0.13.0", "public-onboarding-exact-integer-entrypoints",
    "public-focused-entry-evidence-python-node", "public-inspect-run-evidence-separation",
    "public-inspect-run-interruption-readonly", "public-inspect-run-wrong-run-isolation",
    "public-extension-contract-templates-python-node", "public-upgrade-compatibility-readonly-python-node",
)
ASSETS = ["SHA256SUMS", "release-manifest.json", "vibe-kit-0.13.0.zip",
          "vibe-kit-distribution-0.13.0.zip", "vibe-kit-plugin-0.13.0.zip"]


class V130PublicationTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.profile = self.m.PUBLICATION_PROFILES[8]
        self.intent = profile_test_intent(self.m, 8)
        self.receipt = profile_test_receipt(self.m, self.intent, 8)
        self.digest = self.m.canonical_json_sha256
        self.authorization = {
            "authorization_id": self.receipt["authorization_id"], "repository": "mintgao/vibe-kit",
            "version": "0.13.0", "release_kind": "prerelease",
            "allowed_operations": list(self.m.V080_PUBLICATION_ALLOWED_OPERATIONS),
            "publication_intent_sha256": self.digest(self.intent),
            "host_operation_id": self.receipt["host_operation_id"],
            "authorization_source_ref": "synthetic:already-authorized-scope",
            "bound_at": "2026-10-29T00:00:00Z",
        }
        self.common = {
            "schema_version": 1, "started_at": "2026-10-29T00:00:00Z",
            "finished_at": "2026-10-29T00:01:00Z", "repository": "mintgao/vibe-kit",
            "version": "0.13.0", "profile": self.profile["profile"],
            "source_commit": self.intent["source_commit"], "source_tree_oid": "a" * 40,
        }

    def synthetic_bundle(self):
        # Fixed synthetic source/commands exercise validation, never a real H/M gate.
        common, profile = self.common, self.profile
        qa = {**common, "kind": profile["kinds"]["prepublication-qa"], "execution_id": "synthetic-qa",
              "executor_role": "independent-qa", "asset_set_sha256": self.intent["asset_set_sha256"],
              "commands": [passing_command(0, "synthetic-focused")],
              "criterion_mapping": [{"criterion_id": name, "state": profile["states"][name],
                  "evidence_command_sequences": [0] if index < 8 else [],
                  "postpublication_requirement": profile["requirements"][name]}
                  for index, name in enumerate(CRITERIA)], "status": "passed", "error": None}
        configured = {**common, "kind": profile["kinds"]["configured-checks"],
            "execution_id": "synthetic-configured", "executor_role": "independent-qa",
            "commands": [passing_command(0, "synthetic-default", ["./bin/vibe", "verify", ".", "--format", "json"])],
            "checks": [{"name": name, "configured": name == "test",
                "status": "passed" if name == "test" else "not-configured",
                "exit_code": 0 if name == "test" else None,
                "result_sha256": "a" * 64 if name == "test" else None}
                for name in self.m.VERIFY_ORDER], "status": "passed", "error": None}
        python = {**common, "kind": profile["kinds"]["python-3.9"], "execution_id": "synthetic-python39",
            "executor_role": "release-build-host", "interpreter": {"implementation": "CPython",
                "major": 3, "minor": 9, "patch": 6, "platform": "controlled-fixture",
                "executable_name": "python3.9"},
            "commands": [passing_command(index, name) for index, name in enumerate((
                "python39-default-verify", "python39-publication-focused-tests", "python39-package-a",
                "python39-validate-release-a", "python39-package-b", "python39-validate-release-b"))],
            "status": "passed", "error": None}
        builds = [{**common, "kind": profile["kinds"]["clean-build"],
            "execution_id": "synthetic-build-" + name, "executor_role": "release-build-host",
            "build_id": name, "checkout_id": "checkout-" + name, "output_id": "output-" + name,
            "source_clean": True, "interpreter": copy.deepcopy(python["interpreter"]),
            "package_command": passing_command(0, "synthetic-package-" + name),
            "assets": copy.deepcopy(self.intent["assets"]), "asset_set_sha256": self.intent["asset_set_sha256"],
            "validate_release_command": passing_command(1, "synthetic-validate-" + name),
            "validate_release_result_sha256": "b" * 64, "status": "passed", "error": None}
            for name in ("A", "B")]
        return {"schema_version": 1, "kind": profile["kinds"]["release-gate-evidence"],
            "repository": "mintgao/vibe-kit", "version": "0.13.0", "profile": profile["profile"],
            "source_commit": common["source_commit"], "source_tree_oid": common["source_tree_oid"],
            "generated_at": common["finished_at"], "qa": qa, "configured_checks": configured,
            "python_3_9": python, "builds": builds, "receipt_sha256s": {
                "qa": self.digest(qa), "configured_checks": self.digest(configured),
                "python_3_9": self.digest(python), "build_a": self.digest(builds[0]),
                "build_b": self.digest(builds[1])}}

    def invoke(self, argv):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = self.m.main(argv)
        return code, json.loads(output.getvalue())

    def test_exact_profile_assets_graph_and_current_protocol_mirrors(self):
        self.assertEqual(tuple(self.profile[name] for name in
            ("schema", "version", "tag", "title", "profile", "body_path")),
            (8, "0.13.0", "v0.13.0", "Vibe Kit v0.13.0", "vibe-kit-v0.13.0-prerelease", "docs/releases/0.13.0.md"))
        self.assertEqual([item["name"] for item in self.intent["assets"]], ASSETS)
        self.assertEqual(self.profile["smokes"], SMOKES)
        self.assertEqual(self.m.validate_publication_intent(self.intent), [])
        self.assertEqual(self.m.validate_publication_receipt_shape(self.receipt, self.intent), [])
        keys = ["mintgao/vibe-kit:main", "mintgao/vibe-kit:tag:v0.13.0",
                "mintgao/vibe-kit:release:v0.13.0", "mintgao/vibe-kit:release:v0.13.0:assets",
                "mintgao/vibe-kit:publication:v0.13.0:read-back", "mintgao/vibe-kit:release:v0.13.0:public-assets"]
        self.assertEqual([op["natural_key"] for op in self.intent["operations"]], keys)
        self.assertEqual([op["operation_id"] for op in self.intent["operations"]], ["publish-" + str(i) for i in range(6)])
        self.assertEqual([op["max_write_attempts"] for op in self.intent["operations"]], [2, 2, 2, 2, 0, 0])
        children = self.intent["operations"][3]["asset_operations"]
        self.assertEqual([item["natural_key"] for item in children],
                         ["mintgao/vibe-kit:release:v0.13.0:asset:" + name for name in ASSETS])
        contract = json.loads((ROOT / "agent-install.json").read_text())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text())
        self.assertEqual((self.m.PUBLICATION_INTENT_SCHEMA, self.m.PUBLICATION_RECEIPT_SCHEMA,
                          self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA), (8, 8, 5))
        self.assertEqual([contract["publication"][key] for key in
            ("intent_schema", "receipt_schema", "issue_closeout_intent_schema")], [8, 8, 5])
        self.assertEqual([protocol[key] for key in
            ("publication_intent_schema", "publication_receipt_schema", "issue_closeout_intent_schema")], [8, 8, 5])
        self.assertEqual((contract["schema_version"], contract["protocol_version"],
                          protocol["core_protocol"], protocol["adapters"]["codex"]["version"],
                          protocol["adapters"]["hermes"]["version"]), (4, 5, 7, 7, 1))

    def test_schema8_is_exact_integer_and_historical_profiles_remain_isolated(self):
        for schema in (8.0, "8", True, False, None, 9, [], {}):
            with self.subTest(schema=schema):
                value = copy.deepcopy(self.intent)
                value["schema_version"] = schema
                self.assertTrue(self.m.validate_publication_intent(value))
                receipt = copy.deepcopy(self.receipt)
                receipt["schema_version"] = schema
                self.assertTrue(self.m.validate_publication_receipt_shape(receipt, self.intent))
        self.assertTrue(self.m.validate_publication_intent_v1(self.intent))
        self.assertTrue(self.m.validate_publication_receipt_shape_v1(self.receipt))
        for schema in (2, 3, 4, 5, 6, 7):
            old = profile_test_intent(self.m, schema)
            receipt = profile_test_receipt(self.m, old, schema)
            self.assertEqual(self.m.validate_publication_intent(old), [])
            self.assertEqual(self.m.validate_publication_receipt_shape(receipt, old), [])
            self.assertTrue(self.m.validate_profile_intent(self.intent, profile=self.m.PUBLICATION_PROFILES[schema]))
            self.assertTrue(self.m.validate_publication_receipt_shape(receipt, self.intent))
            self.assertTrue(self.m.validate_publication_receipt_shape(self.receipt, old))
        self.assertEqual(self.m.PUBLICATION_PROFILES[7]["version"], "0.12.0")
        self.assertEqual(self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA, 5)

    def test_closed_assets_natural_keys_preconditions_and_no_issue_policy(self):
        for mutate in (
            lambda v: v.update(unknown=True), lambda v: v.update(version="0.12.0"),
            lambda v: v["assets"].__setitem__(4, copy.deepcopy(v["assets"][3])),
            lambda v: v["assets"].reverse(), lambda v: v["operations"][0].update(natural_key="wrong"),
            lambda v: v["operations"][0]["expected_precondition"].update(identity_sha256="0" * 64),
            lambda v: v["operations"][3]["asset_operations"][0].update(operation_id="asset-99"),
            lambda v: v["operations"][3]["asset_operations"][0]["expected_precondition"].update(identity_sha256="0" * 64),
            lambda v: v["operations"][4].update(max_write_attempts=2),
            lambda v: v["issue_closeout_policy"].update(mode="after-public-verification", issues=[20]),
            lambda v: v["remote_snapshot"].update(asset_list_complete=False),
            lambda v: v["remote_snapshot"]["main"].update(observed_oid="9" * 40),
        ):
            value = copy.deepcopy(self.intent)
            mutate(value)
            self.assertTrue(self.m.validate_publication_intent(value))
        self.assertEqual(self.profile["issue_policy"], {"mode": "none", "issues": [], "allowed_operations": []})
        self.assertIsNone(self.receipt["issue_closeout"])
        for mutate in (lambda v: v.update(issue_closeout={}), lambda v: v["smokes"].pop(),
                       lambda v: v["smokes"].reverse(), lambda v: v["smokes"][-1].update(name="public-direct-init-doctor")):
            value = copy.deepcopy(self.receipt)
            mutate(value)
            self.assertTrue(self.m.validate_publication_receipt_shape(value, self.intent))

    def test_authorization_binds_existing_source_time_intent_and_operation_set(self):
        validate = lambda value: self.m.validate_profile_authorization(value, self.intent, profile=self.profile)
        self.assertEqual(validate(self.authorization), [])
        for mutate in (lambda v: v.pop("authorization_source_ref"), lambda v: v.update(bound_at="invalid"),
                       lambda v: v.update(authorization_source_ref=""), lambda v: v.update(version="0.12.0"),
                       lambda v: v.update(publication_intent_sha256="0" * 64),
                       lambda v: v.update(allowed_operations=["close-issue"]), lambda v: v.update(extra=True)):
            value = copy.deepcopy(self.authorization)
            mutate(value)
            self.assertTrue(validate(value))

    def test_ten_criteria_have_eight_prepasses_and_no_future_closeout_or_upgrade(self):
        self.assertEqual(list(self.profile["states"]), CRITERIA)
        self.assertEqual(list(self.profile["requirements"]), CRITERIA)
        self.assertEqual(self.profile["post_criteria"], CRITERIA)
        self.assertEqual(list(self.profile["states"].values()), ["passed"] * 8 + ["not-runnable-before-publication"] * 2)
        self.assertEqual(list(self.profile["requirements"].values()), ["none"] * 8 + ["live-read-back", "public-smoke"])
        for kind, value in self.profile["kinds"].items():
            self.assertEqual(value, "vibe-kit-v0.13.0-" + kind)
        qa = self.synthetic_bundle()["qa"]
        validate_qa = lambda value: self.m.validate_profile_qa_receipt(value, self.common["source_commit"],
            self.common["source_tree_oid"], profile=self.profile)
        self.assertEqual(validate_qa(qa), [])
        for mutate in (lambda v: v["criterion_mapping"][8].update(state="passed"),
                       lambda v: v["criterion_mapping"][-1].update(postpublication_requirement="project-upgrade"),
                       lambda v: v["criterion_mapping"].append(copy.deepcopy(v["criterion_mapping"][-1]))):
            value = copy.deepcopy(qa)
            mutate(value)
            self.assertTrue(validate_qa(value))
        acceptance = {**self.common, "kind": self.profile["kinds"]["postpublication-acceptance"],
            "execution_id": "synthetic-postpublication", "executor_role": "independent-qa",
            "publication_intent_sha256": self.digest(self.intent),
            "authorization_id": self.authorization["authorization_id"],
            "host_operation_id": self.authorization["host_operation_id"],
            "validate_publication_result_sha256": "c" * 64,
            "criteria": [{"criterion_id": name, "state": "passed", "evidence_refs": [
                {"kind": "public-smoke" if name == "AC-10" else "local-gate-receipt", "sha256": "a" * 64}]}
                for name in CRITERIA], "status": "passed", "error": None}
        validate = lambda value: self.m.validate_profile_postpublication_acceptance(value, self.intent,
            self.authorization, self.common["source_tree_oid"], profile=self.profile)
        self.assertEqual(validate(acceptance), [])
        for mutate in (lambda v: v["criteria"].pop(), lambda v: v["criteria"].reverse(),
                       lambda v: v["criteria"][-1].update(state="blocked"),
                       lambda v: v["criteria"].append({"criterion_id": "AC-11", "state": "passed", "evidence_refs": []})):
            value = copy.deepcopy(acceptance)
            mutate(value)
            self.assertTrue(validate(value))

    def test_gate_bundle_rejects_same_build_execution_and_cross_profile_receipts(self):
        bundle = self.synthetic_bundle()
        validate = lambda value: self.m.validate_profile_release_gate_bundle(value, self.intent["source_commit"], profile=self.profile)
        self.assertEqual(validate(bundle), ([], self.common["source_tree_oid"], self.intent["assets"]))
        for field in ("execution_id", "checkout_id", "output_id"):
            value = copy.deepcopy(bundle)
            value["builds"][1][field] = value["builds"][0][field]
            value["receipt_sha256s"]["build_b"] = self.digest(value["builds"][1])
            self.assertTrue(validate(value)[0])
        value = copy.deepcopy(bundle)
        value["qa"]["version"] = "0.12.0"
        value["receipt_sha256s"]["qa"] = self.digest(value["qa"])
        self.assertTrue(validate(value)[0])
        value = copy.deepcopy(bundle)
        value["python_3_9"]["interpreter"]["minor"] = 10
        value["receipt_sha256s"]["python_3_9"] = self.digest(value["python_3_9"])
        self.assertTrue(validate(value)[0])

    def test_merged_main_read_match_and_uncertain_retries_remain_bounded(self):
        intent = copy.deepcopy(self.intent)
        intent["main"]["expected_old_oid"] = intent["source_commit"]
        intent["remote_snapshot"]["main"]["observed_oid"] = intent["source_commit"]
        snapshot_sha = self.digest(intent["remote_snapshot"])
        intent["remote_snapshot_sha256"] = snapshot_sha
        for operation in intent["operations"]:
            initial = self.m.profile_operation_initial_observation(intent["remote_snapshot"], operation["kind"], profile=self.profile)
            operation["expected_precondition"].update(remote_snapshot_sha256=snapshot_sha,
                identity_sha256=self.digest(self.m.profile_operation_identity(operation["kind"], operation["natural_key"], snapshot_sha, initial, profile=self.profile)))
            for child, asset in zip(operation["asset_operations"], intent["assets"]):
                identity = {"schema_version": 8, "profile": self.profile["profile"],
                    "parent_operation_id": operation["operation_id"], "natural_key": child["natural_key"],
                    "remote_snapshot_sha256": snapshot_sha, "asset": asset,
                    "initial_observation": {"state": "absent", "id": None, "size": None, "sha256": None, "download_url": None}}
                child["expected_precondition"].update(remote_snapshot_sha256=snapshot_sha, identity_sha256=self.digest(identity))
        self.assertEqual(self.m.validate_publication_intent(intent), [])
        receipt = profile_test_receipt(self.m, intent, 8)
        receipt["main"]["expected_old_oid"] = intent["source_commit"]
        self.assertEqual(self.m.validate_publication_receipt_shape(receipt, intent), [])
        self.assertEqual(receipt["operations"][0]["attempts"], [])
        self.assertEqual(receipt["operations"][0]["outcome"], "read-matched")
        def observed(state, oid):
            return {"observed_at": "2026-10-29T00:00:00Z", "state": state, "oid": oid}
        attempts = [{"attempt_number": 1, "pre_write_observation": observed("preimage", "0" * 40),
            "response": "timeout", "read_back_observation": observed("preimage", "0" * 40)},
            {"attempt_number": 2, "pre_write_observation": observed("preimage", "0" * 40),
            "response": "definite-success", "read_back_observation": observed("target", "1" * 40)}]
        validate = lambda value: self.m.validate_profile_attempts(value, "main", profile=self.profile)
        self.assertEqual(validate(attempts), [])
        for state, oid in (("unknown", None), ("divergent", "9" * 40), ("target", "1" * 40)):
            value = copy.deepcopy(attempts)
            value[0]["read_back_observation"] = observed(state, oid)
            self.assertTrue(validate(value))
        for response in ("permission-denied", "definite-failure", "execution-error"):
            value = copy.deepcopy(attempts)
            value[0]["response"] = response
            self.assertTrue(validate(value))
        self.assertTrue(validate(attempts + [copy.deepcopy(attempts[-1])]))
        child = copy.deepcopy(receipt["operations"][3]["asset_receipts"][0])
        child["precondition_sha256"] = "0" * 64
        changed = copy.deepcopy(receipt)
        changed["operations"][3]["asset_receipts"][0] = child
        self.assertTrue(self.m.validate_publication_receipt_shape(changed, intent))

    def test_real_main_plan_dispatch_requires_both_candidates_and_bound_gate(self):
        bundle = self.synthetic_bundle()
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            candidates = [base / "candidate", base / "comparison"]
            manifest = {"kit_version": "0.13.0", "status": "prerelease",
                        "source": {"tree_state": "clean", "ref": self.intent["source_commit"]}}
            for candidate in candidates:
                candidate.mkdir()
                (candidate / "release-manifest.json").write_text(json.dumps(manifest))
            request = copy.deepcopy(self.intent)
            request["release"]["body_sha256"] = self.m.sha256(ROOT / self.profile["body_path"])
            request["local_gates"]["release_gate_evidence_sha256"] = self.digest(bundle)
            paths = {"request": base / "request.json", "gates": base / "gates.json"}
            paths["request"].write_text(json.dumps(request))
            paths["gates"].write_text(json.dumps(bundle))
            argv = ["publication-plan", "--phase", "publish", "--request", str(paths["request"]),
                    "--candidate", str(candidates[0]), "--format", "json"]
            with mock.patch.object(self.m, "publication_assets", return_value=copy.deepcopy(request["assets"])), \
                 mock.patch.object(self.m, "validate_release", return_value=0):
                code, missing = self.invoke(argv)
                self.assertEqual((code, missing["status"]), (2, "blocked"))
                self.assertTrue(any("requires --comparison-candidate" in error for error in missing["errors"]))
                self.assertTrue(any("requires --release-gate-evidence" in error for error in missing["errors"]))
                code, value = self.invoke(argv + ["--comparison-candidate", str(candidates[1]),
                                                "--release-gate-evidence", str(paths["gates"])])
                expected = (0, "safe") if sys.version_info[:2] == (3, 9) else (2, "blocked")
                self.assertEqual((code, value["status"]), expected, value["errors"])
                if code == 0:
                    self.assertEqual(value["intent"]["schema_version"], 8)

    def test_real_main_validation_keeps_inputs_readonly_and_result_create_only(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            candidate = base / "candidate"
            candidate.mkdir()
            paths = {}
            for name, value in (("intent", self.intent), ("receipt", self.receipt), ("authorization", self.authorization)):
                paths[name] = base / (name + ".json")
                paths[name].write_text(json.dumps(value))
            argv = ["validate-publication", "--intent", str(paths["intent"]), "--receipt", str(paths["receipt"]),
                    "--authorization", str(paths["authorization"]), "--candidate", str(candidate), "--format", "json"]
            before = {path: path.read_bytes() for path in paths.values()}
            result = base / "result.json"
            with mock.patch.object(self.m, "publication_assets", return_value=copy.deepcopy(self.intent["assets"])), \
                 mock.patch.object(self.m, "validate_release", return_value=0):
                code, value = self.invoke(argv)
                expected = (0, "valid") if sys.version_info[:2] == (3, 9) else (1, "invalid")
                self.assertEqual((code, value["status"]), expected, value["errors"])
                self.assertEqual(value["profile"], "vibe-kit-v0.13.0-prerelease")
                self.assertFalse(result.exists())
                code, value = self.invoke(argv + ["--result-receipt", str(result)])
                self.assertEqual(stat.S_IMODE(result.stat().st_mode), 0o600)
                self.assertEqual(json.loads(result.read_bytes())["profile"], self.profile["profile"])
                saved = result.read_bytes()
                code, value = self.invoke(argv + ["--result-receipt", str(result)])
                self.assertEqual((code, value["error"]["code"]), (2, "result_receipt_exists"))
                self.assertEqual(result.read_bytes(), saved)
                for destination in (paths["receipt"], paths["intent"], paths["authorization"], candidate / "result.json"):
                    code, value = self.invoke(argv + ["--result-receipt", str(destination)])
                    self.assertEqual((code, value["error"]["code"]), (2, "result_receipt_alias"))
            self.assertEqual({path: path.read_bytes() for path in paths.values()}, before)

    def test_schema8_parent_cannot_enter_any_issue_closeout_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            packet = {}
            for key in ("request", "parent_intent", "publication_receipt", "publication_authorization",
                        "acceptance_receipt", "validation_result"):
                packet[key] = key + ".json"
                value = self.intent if key == "parent_intent" else {}
                (base / packet[key]).write_text(json.dumps(value))
            path = base / "packet.json"
            path.write_text(json.dumps(packet))
            code, value = self.invoke(["issue-closeout", "--packet", str(path), "--format", "json"])
            self.assertEqual(code, 2)
            self.assertIn("schema-7 (v0.12.0) parent", value["error"]["message"])
            self.assertEqual(self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA, 5)


if __name__ == "__main__":
    unittest.main()
