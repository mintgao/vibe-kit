"""Synthetic closed-profile and workflow evidence for ADR0024, not live publication."""
import argparse
import contextlib
import copy
import io
import json
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from tests.test_cli import ROOT, load_cli_module, profile_test_intent, profile_test_receipt, passing_command

ISSUES = [20, 22, 23]
CRITERIA = ["AC-" + str(number) for number in range(1, 13)]
SMOKES = ('public-direct-init-doctor', 'public-plugin-bundled-plan-init-doctor', 'public-upgrade-v0.3-to-v0.12.0', 'public-upgrade-v0.5-to-v0.12.0', 'public-upgrade-v0.6-to-v0.12.0', 'public-upgrade-v0.7-to-v0.12.0', 'public-upgrade-v0.8-to-v0.12.0', 'public-upgrade-v0.9-to-v0.12.0', 'public-upgrade-v0.10.0-to-v0.12.0', 'public-upgrade-v0.10.1-to-v0.12.0', 'public-upgrade-v0.11.0-to-v0.12.0', 'public-repeat-upgrade-v0.12.0', 'public-onboarding-exact-integer-entrypoints', 'public-focused-entry-evidence-python-node', 'public-inspect-run-evidence-separation', 'public-inspect-run-interruption-readonly', 'public-inspect-run-wrong-run-isolation')


class V120PublicationTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.profile = self.m.PUBLICATION_PROFILES[7]
        self.parent = profile_test_intent(self.m, 7)
        self.publication = profile_test_receipt(self.m, self.parent, 7)
        self.digest = self.m.canonical_json_sha256
        self.authorization = {"authorization_id": self.publication["authorization_id"], "repository": "mintgao/vibe-kit", "version": "0.12.0", "release_kind": "prerelease", "allowed_operations": list(self.m.V080_PUBLICATION_ALLOWED_OPERATIONS), "publication_intent_sha256": self.digest(self.parent), "host_operation_id": self.publication["host_operation_id"], "authorization_source_ref": "task:existing-exact-user-request", "bound_at": "2026-10-12T00:00:00Z"}
        self.validation = self.m.result_envelope("validate-publication", "valid", profile=self.profile["profile"], version="0.12.0", intent_sha256=self.digest(self.parent), authorization_id=self.authorization["authorization_id"], host_operation_id=self.authorization["host_operation_id"], remote_write_state="confirmed-complete", verification_state="passed", errors=[], network_used=False, host_evidence_authenticated=False)
        self.acceptance = {"schema_version": 1, "kind": self.profile["kinds"]["postpublication-acceptance"], "execution_id": "independent-synthetic-acceptance", "executor_role": "independent-qa", "started_at": "2026-10-12T00:00:00Z", "finished_at": "2026-10-12T00:01:00Z", "repository": "mintgao/vibe-kit", "version": "0.12.0", "profile": self.profile["profile"], "source_commit": self.parent["source_commit"], "source_tree_oid": "a" * 40, "publication_intent_sha256": self.digest(self.parent), "authorization_id": self.authorization["authorization_id"], "host_operation_id": self.authorization["host_operation_id"], "validate_publication_result_sha256": self.digest(self.validation), "criteria": [{"criterion_id": name, "state": "passed", "evidence_refs": [{"kind": "local-gate-receipt" if name != "AC-10" else "validate-publication", "sha256": "a" * 64}]} for name in CRITERIA[:-2]], "status": "passed", "error": None}

    def test_exact_identity_ordered_acceptance_smokes_and_phase_separation(self):
        profile = self.profile
        self.assertEqual((profile["schema"], profile["version"], profile["tag"], profile["title"], profile["profile"], profile["body_path"]), (7, "0.12.0", "v0.12.0", "Vibe Kit v0.12.0", "vibe-kit-v0.12.0-prerelease", "docs/releases/0.12.0.md"))
        self.assertEqual(profile["smokes"], SMOKES)
        self.assertEqual(list(profile["states"]), CRITERIA)
        self.assertEqual(list(profile["requirements"]), CRITERIA)
        self.assertEqual(profile["post_criteria"], CRITERIA[:-2])
        self.assertEqual([profile["states"][name] for name in CRITERIA], ["passed"] * 8 + ["not-runnable-before-publication"] * 4)
        self.assertEqual([profile["requirements"][name] for name in CRITERIA], ["none"] * 8 + ["live-read-back", "public-smoke", "issue-closeout", "project-upgrade"])
        self.assertEqual(profile["issue_policy"], {"mode": "after-public-verification", "issues": ISSUES, "allowed_operations": ["create-exact-evidence-comment", "close-issue"]})
        self.assertIsNone(self.publication["issue_closeout"])
        self.assertEqual(self.m.validate_publication_intent(self.parent), [])
        self.assertEqual(self.m.validate_publication_receipt_shape(self.publication, self.parent), [])
        self.assertEqual(self.m.validate_profile_authorization(self.authorization, self.parent, profile=profile), [])
        self.assertEqual(self.m.validate_profile_postpublication_acceptance(self.acceptance, self.parent, self.authorization, "a" * 40, profile=profile), [])
        premature = copy.deepcopy(self.acceptance)
        premature["criteria"].append({"criterion_id": "AC-11", "state": "passed", "evidence_refs": [{"kind": "local-gate-receipt", "sha256": "a" * 64}]})
        self.assertTrue(self.m.validate_profile_postpublication_acceptance(premature, self.parent, self.authorization, "a" * 40, profile=profile))

    def test_historical_profiles_keep_their_verdicts_and_reject_cross_profile(self):
        for schema in (2, 3, 4, 5, 6):
            old = profile_test_intent(self.m, schema)
            receipt = profile_test_receipt(self.m, old, schema)
            self.assertEqual(self.m.validate_publication_intent(old), [])
            self.assertEqual(self.m.validate_publication_receipt_shape(receipt, old), [])
            self.assertTrue(self.m.validate_profile_intent(self.parent, profile=self.m.PUBLICATION_PROFILES[schema]))
            self.assertTrue(self.m.validate_publication_receipt_shape(receipt, self.parent))
            self.assertTrue(self.m.validate_publication_receipt_shape(self.publication, old))
        for mutation in (lambda v: v.update(schema_version=7.0), lambda v: v.update(version="0.10.1"), lambda v: v["assets"].pop(), lambda v: v["operations"][0].update(natural_key="wrong"), lambda v: v["issue_closeout_policy"]["issues"].reverse()):
            value = copy.deepcopy(self.parent)
            mutation(value)
            self.assertTrue(self.m.validate_publication_intent(value))
        for mutation in (lambda v: v.pop("authorization_source_ref"), lambda v: v.update(bound_at="invalid"), lambda v: v.update(publication_intent_sha256="0" * 64), lambda v: v.update(allowed_operations=["close-issue"])):
            value = copy.deepcopy(self.authorization)
            mutation(value)
            self.assertTrue(self.m.validate_profile_authorization(value, self.parent, profile=self.profile))
        value = copy.deepcopy(self.publication)
        value["smokes"][-1]["name"] = "public-repeat-upgrade-v0.10.1"
        self.assertTrue(self.m.validate_publication_receipt_shape(value, self.parent))

    def request(self, resume=False):
        parent_digest = self.digest(self.parent)
        identifier = self.m.profile_closeout_id(parent_digest, version="0.12.0", schema=5, issues=ISSUES)
        issues, snapshots, operations = [], [], []
        for index, number in enumerate(ISSUES):
            body = "Verified mapped criterion evidence. " + f"<!-- vibe-kit:v0.12.0:issue-{number}:{identifier} -->"
            exact = resume and index == 0
            comment_id = 114 if exact else None
            issues.append({"issue_number": number, "comment_body": body, "observed_state": "closed" if exact else "open", "observed_matching_comment_id": comment_id, "criterion_evidence_sha256": "b" * 64})
            snapshot = {"issue_number": number, "state": "closed" if exact else "open", "marker_state": "exact" if exact else "absent", "matching_comment_id": comment_id, "matching_comment_body_sha256": self.m.sha256_text(body) if exact else None}
            snapshots.append(snapshot)
            for offset, kind in enumerate(("create-exact-evidence-comment", "close-issue")):
                operations.append({"sequence": 2 * index + offset, "operation_id": f"issue-{number}-{'comment' if offset == 0 else 'close'}", "issue_number": number, "kind": kind, "natural_key": f"issue:{number}:marker:{identifier}" if offset == 0 else f"issue:{number}:state:closed", "expected_precondition": {"kind": "issue-closeout-monotonic-resume", "initial_snapshot_sha256": self.digest(snapshot), "allowed_observations": ["open-absent", "open-exact", "closed-exact"] if offset == 0 else ["open-exact", "closed-exact"]}, "max_write_attempts": 2})
        return {"parent_publication_intent_sha256": parent_digest, "publication_receipt_sha256": self.digest(self.publication), "verification_receipt_sha256": self.digest(self.acceptance), "repository": self.m.publication_repository(), "issues": issues, "remote_snapshot": {"observed_at": "2026-10-12T00:02:00Z", "issues": snapshots}, "operations": operations, "authorization_scope": {"repository": "mintgao/vibe-kit", "issues": ISSUES, "allowed_operations": ["create-exact-evidence-comment", "close-issue"], "destructive_operations_allowed": False, "requires_separate_closeout_authorization": True}}, identifier

    def build(self, request):
        return self.m.build_v120_closeout_intent(request, self.parent, self.publication, self.authorization, self.acceptance, self.validation)

    def test_schema5_closeout_exact_order_markers_parent_binding_and_resume(self):
        self.assertEqual(self.m.validate_v120_closeout_parent(self.parent, self.publication, self.authorization, self.acceptance, self.validation), [])
        request, identifier = self.request()
        intent, bodies = self.build(request)
        self.assertEqual(intent["schema_version"], 5)
        self.assertEqual([item["issue_number"] for item in intent["issues"]], ISSUES)
        self.assertEqual([item["operation_id"] for item in intent["operations"]], [f"issue-{number}-{kind}" for number in ISSUES for kind in ("comment", "close")])
        self.assertEqual(len(intent["operations"]), 6)
        for number in ISSUES:
            self.assertIn(f"<!-- vibe-kit:v0.12.0:issue-{number}:{identifier} -->", bodies[str(number)])
        resumed, unused = self.request(resume=True)
        self.assertEqual(self.build(resumed)[0]["issues"][0]["observed_state"], "closed")
        for mutation in (lambda v: v["issues"].reverse(), lambda v: v["operations"].reverse(), lambda v: v["issues"][0].update(issue_number=21), lambda v: v["issues"][0].update(comment_body="wrong marker"), lambda v: v.update(publication_receipt_sha256="0" * 64), lambda v: v.update(parent_publication_intent_sha256="0" * 64), lambda v: v["operations"][0].update(max_write_attempts=3), lambda v: v["remote_snapshot"]["issues"][0].update(marker_state="duplicate")):
            value = copy.deepcopy(request)
            mutation(value)
            with self.assertRaises(self.m.VibeError):
                self.build(value)
        wrong_parent = profile_test_intent(self.m, 6)
        self.assertTrue(self.m.validate_v120_closeout_parent(wrong_parent, self.publication, self.authorization, self.acceptance, self.validation))
        bad_validation = dict(self.validation, host_operation_id="other")
        self.assertTrue(self.m.validate_v120_closeout_parent(self.parent, self.publication, self.authorization, self.acceptance, bad_validation))

    def test_closeout_complete_requires_each_pair_and_partial_uncertain_is_honest(self):
        request, identifier = self.request()
        intent, unused = self.build(request)
        authorization = {"closeout_authorization_id": "separate-exact-issue-authorization", "repository": "mintgao/vibe-kit", "issues": ISSUES, "allowed_operations": ["create-exact-evidence-comment", "close-issue"], "closeout_intent_sha256": self.digest(intent), "destructive_operations_allowed": False, "authorization_source_ref": "task:existing-separate-issue-closeout-request", "bound_at": "2026-10-12T00:02:00Z"}
        receipt = {"schema_version": 5, "kind": "vibe-kit-issue-closeout-receipt", "closeout_id": identifier, "closeout_intent_sha256": self.digest(intent), "closeout_authorization_id": authorization["closeout_authorization_id"], "overall_state": "confirmed-complete", "items": [{"issue_number": number, "expected_initial_state": "open", "comment_body_sha256": intent["issues"][index]["comment_body_sha256"], "comment_id": 100 + number, "comment_url": f"https://github.com/mintgao/vibe-kit/issues/{number}#issuecomment-{100 + number}", "comment_write_state": "confirmed-after-uncertain", "close_write_state": "read-matched", "observed_post_state": "closed", "read_back": True, "error": None} for index, number in enumerate(ISSUES)]}
        self.assertEqual(self.m.validate_v120_closeout_receipt(receipt, intent, authorization), [])
        malformed_items = [receipt["items"] + [None], receipt["items"] + ["extra"],
                           receipt["items"] + [{}], receipt["items"][:-1],
                           receipt["items"][:2] + [None] + receipt["items"][3:],
                           receipt["items"][:2] + ["wrong"] + receipt["items"][3:],
                           receipt["items"][:2] + [{}] + receipt["items"][3:]]
        for index, items in enumerate(malformed_items):
            with self.subTest(malformed_item_case=index):
                value = copy.deepcopy(receipt)
                value["items"] = items
                self.assertTrue(self.m.validate_v120_closeout_receipt(value, intent, authorization))
        partial = copy.deepcopy(receipt)
        partial["overall_state"] = "confirmed-partial"
        for item in partial["items"][1:]:
            item.update(comment_id=None, comment_url=None, comment_write_state="not-attempted", close_write_state="not-attempted", observed_post_state=None, read_back=False)
        self.assertEqual(self.m.validate_v120_closeout_receipt(partial, intent, authorization), [])
        partial["overall_state"] = "confirmed-complete"
        self.assertTrue(self.m.validate_v120_closeout_receipt(partial, intent, authorization))
        partial["overall_state"] = "uncertain"
        partial["items"][1]["comment_write_state"] = "uncertain"
        self.assertEqual(self.m.validate_v120_closeout_receipt(partial, intent, authorization), [])
        for mutation in (lambda v: v["items"].reverse(), lambda v: v.update(schema_version=3), lambda v: v.update(schema_version=5.0), lambda v: v.update(schema_version="5"), lambda v: v["items"][0].update(read_back=False), lambda v: v["items"][0].update(comment_url="https://example.invalid")):
            value = copy.deepcopy(receipt)
            mutation(value)
            self.assertTrue(self.m.validate_v120_closeout_receipt(value, intent, authorization))
        bad_auth = dict(authorization, closeout_intent_sha256="0" * 64)
        self.assertTrue(self.m.validate_v120_closeout_receipt(receipt, intent, bad_auth))
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            values = {"request": request, "parent_intent": self.parent, "publication_receipt": self.publication, "publication_authorization": self.authorization, "acceptance_receipt": self.acceptance, "validation_result": self.validation, "closeout_authorization": authorization, "closeout_receipt": receipt}
            packet = {}
            for key, value in values.items():
                packet[key] = key + ".json"
                (base / packet[key]).write_text(json.dumps(value))
            (base / "packet.json").write_text(json.dumps(packet))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = self.m.issue_closeout_command(argparse.Namespace(packet=base / "packet.json"))
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["intent"]["schema_version"], 5)

    def test_current_mirrors_exact_kinds_and_semantic_mapping_are_declared(self):
        contract = json.loads((ROOT / "agent-install.json").read_bytes())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_bytes())
        self.assertEqual((self.m.PUBLICATION_INTENT_SCHEMA, self.m.PUBLICATION_RECEIPT_SCHEMA, self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA), (8, 8, 5))
        self.assertEqual(tuple(contract["publication"][name] for name in ("intent_schema", "receipt_schema", "issue_closeout_intent_schema")), (8, 8, 5))
        self.assertEqual(tuple(protocol[name] for name in ("publication_intent_schema", "publication_receipt_schema", "issue_closeout_intent_schema")), (8, 8, 5))
        for kind in ("prepublication-qa", "configured-checks", "python-3.9", "clean-build", "release-gate-evidence", "postpublication-acceptance"):
            self.assertEqual(self.profile["kinds"][kind], "vibe-kit-v0.12.0-" + kind)
        decision = (ROOT / "docs/decisions/0024-v0-12-publication-and-separate-closeout.md").read_text()
        for text in ("#20: AC1 plus public-onboarding-exact-integer-entrypoints", "#22: AC2 plus public-focused-entry-evidence-python-node", "#23: AC3 plus all3 public-inspect-run smokes", "digest alone does not authenticate semantic truth"):
            self.assertIn(text, decision)
        for relative in ("AGENT_INSTALL.md", ".agents/skills/vibe-release/SKILL.md"):
            text = (ROOT / relative).read_text()
            self.assertIn("schema-7", text)
            self.assertIn("schema-5", text)
            self.assertIn("[20,22,23]", text)
        for relative in ("README.md", "README.zh-CN.md"):
            text = (ROOT / relative).read_text()
            self.assertRegex(text, r"releases/tag/v0\.(?:11|12)\.0")
            self.assertIn("0.12.0", text)
            self.assertIn("inspect-run", text)
        notes = (ROOT / self.profile["body_path"]).read_text()
        for asset in self.parent["assets"]:
            self.assertIn(asset["name"], notes)

    def test_schema7_rejects_noninteger_unknown_and_cross_profile_dispatch(self):
        for schema in (7.0, "7", True, False, None, 99, [], {}):
            with self.subTest(schema=schema):
                value = copy.deepcopy(self.parent)
                value["schema_version"] = schema
                self.assertTrue(self.m.validate_publication_intent(value))
                receipt = copy.deepcopy(self.publication)
                receipt["schema_version"] = schema
                self.assertTrue(self.m.validate_publication_receipt_shape(receipt, self.parent))
        for mutation in (lambda v: v.update(unknown=True),
                         lambda v: v["assets"].__setitem__(4, copy.deepcopy(v["assets"][3])),
                         lambda v: v["assets"].reverse(),
                         lambda v: v["operations"][3]["asset_operations"][0].update(operation_id="asset-99"),
                         lambda v: v["operations"][4].update(max_write_attempts=2),
                         lambda v: v["operations"][5].update(natural_key="mintgao/vibe-kit:release:v0.11.0:public-assets")):
            value = copy.deepcopy(self.parent)
            mutation(value)
            self.assertTrue(self.m.validate_publication_intent(value))
        for mutation in (lambda v: v["smokes"].reverse(), lambda v: v["smokes"].pop(),
                         lambda v: v.update(issue_closeout={}), lambda v: v.update(schema_version=6)):
            value = copy.deepcopy(self.publication)
            mutation(value)
            self.assertTrue(self.m.validate_publication_receipt_shape(value, self.parent))

    def test_qa_mapping_has_eight_prepasses_and_later_upgrade_only_in_schema7(self):
        qa = {key: copy.deepcopy(self.acceptance[key]) for key in
              ("schema_version", "execution_id", "executor_role", "started_at", "finished_at", "repository", "version", "profile", "source_commit", "source_tree_oid", "status", "error")}
        qa.update(kind=self.profile["kinds"]["prepublication-qa"], asset_set_sha256=self.parent["asset_set_sha256"],
                  commands=[passing_command(0, "postmerge-release-gate", ["./bin/vibe", "verify", ".", "--format", "json"])],
                  criterion_mapping=[{"criterion_id": name, "state": self.profile["states"][name],
                    "evidence_command_sequences": [0] if index < 8 else [],
                    "postpublication_requirement": self.profile["requirements"][name]}
                    for index, name in enumerate(CRITERIA)])
        validate = lambda value: self.m.validate_profile_qa_receipt(value, self.parent["source_commit"], "a" * 40, profile=self.profile)
        self.assertEqual(validate(qa), [])
        for mutate in (lambda v: v["criterion_mapping"][8].update(state="passed"),
                       lambda v: v["criterion_mapping"][-1].update(postpublication_requirement="final-claim-gate"),
                       lambda v: v["criterion_mapping"].reverse()):
            bad = copy.deepcopy(qa)
            mutate(bad)
            self.assertTrue(validate(bad))
        self.assertEqual(self.profile["requirements"]["AC-12"], "project-upgrade")
        for schema in (2, 3, 4, 5, 6):
            self.assertNotIn("project-upgrade", self.m.PUBLICATION_PROFILES[schema]["requirements"].values())
        self.assertEqual(self.m.validate_v120_closeout_parent(self.parent, self.publication, self.authorization, self.acceptance, self.validation), [])
        for mutate in (lambda v: v["criteria"].append({"criterion_id": "AC-11", "state": "passed", "evidence_refs": [{"kind": "public-smoke", "sha256": "a" * 64}]}),
                       lambda v: v["criteria"].reverse()):
            bad = copy.deepcopy(self.acceptance)
            mutate(bad)
            self.assertTrue(self.m.validate_v120_closeout_parent(self.parent, self.publication, self.authorization, bad, self.validation))

    def test_separate_closeout_schema_and_authorization_are_strict(self):
        request, unused = self.request()
        intent, bodies = self.build(request)
        expected_id = self.digest({"schema_version": 5, "repository": "mintgao/vibe-kit", "version": "0.12.0",
            "parent_publication_intent_sha256": self.digest(self.parent), "issues": ISSUES})
        self.assertEqual(intent["closeout_id"], expected_id)
        for number in ISSUES:
            self.assertEqual(bodies[str(number)].count(f"<!-- vibe-kit:v0.12.0:issue-{number}:{expected_id} -->"), 1)
        auth = {"closeout_authorization_id": "bound-closeout", "repository": "mintgao/vibe-kit", "issues": ISSUES,
                "allowed_operations": ["create-exact-evidence-comment", "close-issue"], "closeout_intent_sha256": self.digest(intent),
                "destructive_operations_allowed": False, "authorization_source_ref": "task:existing-separate-scope", "bound_at": "2026-10-28T00:00:00Z"}
        self.assertEqual(self.m.validate_profile_closeout_authorization(auth, intent, schema=5), [])
        for mutate in (lambda v: v.pop("authorization_source_ref"), lambda v: v.update(bound_at="invalid"),
                       lambda v: v.update(issues=[20, 21, 22, 23, 26]), lambda v: v.update(destructive_operations_allowed=True),
                       lambda v: v.update(allowed_operations=["close-issue"])):
            bad = copy.deepcopy(auth)
            mutate(bad)
            self.assertTrue(self.m.validate_profile_closeout_authorization(bad, intent, schema=5))
        for number in (21, 24, 25, 26):
            bad = copy.deepcopy(request)
            bad["issues"][0]["issue_number"] = number
            with self.assertRaises(self.m.VibeError):
                self.build(bad)

    def test_merged_source_already_target_uses_read_match_with_zero_writes(self):
        intent = copy.deepcopy(self.parent)
        intent["main"]["expected_old_oid"] = intent["source_commit"]
        intent["remote_snapshot"]["main"]["observed_oid"] = intent["source_commit"]
        snapshot_sha = self.digest(intent["remote_snapshot"])
        intent["remote_snapshot_sha256"] = snapshot_sha
        for operation in intent["operations"]:
            initial = self.m.profile_operation_initial_observation(intent["remote_snapshot"], operation["kind"], profile=self.profile)
            operation["expected_precondition"].update(remote_snapshot_sha256=snapshot_sha,
                identity_sha256=self.digest(self.m.profile_operation_identity(operation["kind"], operation["natural_key"], snapshot_sha, initial, profile=self.profile)))
            for child, asset in zip(operation["asset_operations"], intent["assets"]):
                identity = {"schema_version": 7, "profile": self.profile["profile"], "parent_operation_id": operation["operation_id"],
                    "natural_key": child["natural_key"], "remote_snapshot_sha256": snapshot_sha, "asset": asset,
                    "initial_observation": {"state": "absent", "id": None, "size": None, "sha256": None, "download_url": None}}
                child["expected_precondition"].update(remote_snapshot_sha256=snapshot_sha, identity_sha256=self.digest(identity))
        self.assertEqual(self.m.validate_publication_intent(intent), [])
        receipt = profile_test_receipt(self.m, intent, 7)
        receipt["main"]["expected_old_oid"] = intent["source_commit"]
        self.assertEqual(receipt["operations"][0]["attempts"], [])
        self.assertEqual(receipt["operations"][0]["outcome"], "read-matched")
        self.assertEqual(self.m.validate_publication_receipt_shape(receipt, intent), [])

    def test_schema7_uncertainty_readback_and_bounded_retry_contract(self):
        def observation(state, oid):
            return {"observed_at": "2026-10-28T00:01:00Z", "state": state, "oid": oid}
        attempts = [{"attempt_number": 1, "pre_write_observation": observation("preimage", "0" * 40),
            "response": "timeout", "read_back_observation": observation("preimage", "0" * 40)},
            {"attempt_number": 2, "pre_write_observation": observation("preimage", "0" * 40),
             "response": "definite-success", "read_back_observation": observation("target", "1" * 40)}]
        validate = lambda value: self.m.validate_profile_attempts(value, "main", profile=self.profile)
        self.assertEqual(validate(attempts), [])
        for state, oid in (("unknown", None), ("divergent", "9" * 40), ("target", "1" * 40)):
            bad = copy.deepcopy(attempts)
            bad[0]["read_back_observation"] = observation(state, oid)
            self.assertTrue(validate(bad))
        for response in ("permission-denied", "definite-failure", "execution-error"):
            bad = copy.deepcopy(attempts)
            bad[0]["response"] = response
            self.assertTrue(validate(bad))
        self.assertTrue(validate(attempts + [copy.deepcopy(attempts[-1])]))
        bad = copy.deepcopy(self.parent)
        bad["remote_snapshot"]["asset_list_complete"] = False
        self.assertTrue(self.m.validate_publication_intent(bad))

    def test_schema7_local_gate_and_plan_dispatch_are_profile_bound(self):
        # Synthetic local evidence tests field/dispatch contracts only; no release gate runs.
        common = {key: copy.deepcopy(self.acceptance[key]) for key in
            ("schema_version", "started_at", "finished_at", "repository", "version", "profile", "source_commit", "source_tree_oid")}
        qa = {**common, "kind": self.profile["kinds"]["prepublication-qa"], "execution_id": "synthetic-qa",
            "executor_role": "independent-qa", "asset_set_sha256": self.parent["asset_set_sha256"],
            "commands": [passing_command(0, "qa-focused")],
            "criterion_mapping": [{"criterion_id": name, "state": self.profile["states"][name],
                "evidence_command_sequences": [0] if index < 8 else [],
                "postpublication_requirement": self.profile["requirements"][name]}
                for index, name in enumerate(CRITERIA)], "status": "passed", "error": None}
        configured = {**common, "kind": self.profile["kinds"]["configured-checks"], "execution_id": "synthetic-configured",
            "executor_role": "independent-qa", "commands": [passing_command(0, "default-verify", ["./bin/vibe", "verify", ".", "--format", "json"])],
            "checks": [{"name": name, "configured": name == "test", "status": "passed" if name == "test" else "not-configured",
                "exit_code": 0 if name == "test" else None, "result_sha256": "a" * 64 if name == "test" else None}
                for name in self.m.VERIFY_ORDER], "status": "passed", "error": None}
        python = {**common, "kind": self.profile["kinds"]["python-3.9"], "execution_id": "synthetic-python39",
            "executor_role": "release-build-host", "interpreter": {"implementation": "CPython", "major": 3, "minor": 9,
                "patch": 6, "platform": "controlled-fixture", "executable_name": "python3.9"},
            "commands": [passing_command(index, name) for index, name in enumerate(("python39-default-verify",
                "python39-publication-focused-tests", "python39-package-a", "python39-validate-release-a", "python39-package-b", "python39-validate-release-b"))],
            "status": "passed", "error": None}
        builds = [{**common, "kind": self.profile["kinds"]["clean-build"], "execution_id": "synthetic-build-" + name,
            "executor_role": "release-build-host", "build_id": name, "checkout_id": "checkout-" + name,
            "output_id": "output-" + name, "source_clean": True, "interpreter": python["interpreter"],
            "package_command": passing_command(0, "package-" + name), "assets": self.parent["assets"],
            "asset_set_sha256": self.parent["asset_set_sha256"], "validate_release_command": passing_command(1, "validate-" + name),
            "validate_release_result_sha256": "b" * 64, "status": "passed", "error": None} for name in ("A", "B")]
        bundle = {"schema_version": 1, "kind": self.profile["kinds"]["release-gate-evidence"], "repository": "mintgao/vibe-kit",
            "version": "0.12.0", "profile": self.profile["profile"], "source_commit": self.parent["source_commit"],
            "source_tree_oid": common["source_tree_oid"], "generated_at": common["finished_at"], "qa": qa,
            "configured_checks": configured, "python_3_9": python, "builds": builds,
            "receipt_sha256s": {"qa": self.digest(qa), "configured_checks": self.digest(configured), "python_3_9": self.digest(python),
                "build_a": self.digest(builds[0]), "build_b": self.digest(builds[1])}}
        validate = lambda value: self.m.validate_profile_release_gate_bundle(value, self.parent["source_commit"], profile=self.profile)
        self.assertEqual(validate(bundle), ([], common["source_tree_oid"], self.parent["assets"]))
        for field, target, value in (("qa", "state", "passed"), ("build_b", "checkout_id", "checkout-A"),
                                     ("python_3_9", "minor", 10)):
            bad = copy.deepcopy(bundle)
            if field == "qa":
                bad["qa"]["criterion_mapping"][8][target] = value
                bad["receipt_sha256s"][field] = self.digest(bad[field])
            elif field == "build_b":
                bad["builds"][1][target] = value
                bad["receipt_sha256s"][field] = self.digest(bad["builds"][1])
            else:
                bad[field]["interpreter"][target] = value
                bad["receipt_sha256s"][field] = self.digest(bad[field])
            self.assertTrue(validate(bad)[0])
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            candidate, comparison = base / "candidate", base / "comparison"
            manifest = {"kit_version": "0.12.0", "status": "prerelease", "source": {"tree_state": "clean", "ref": self.parent["source_commit"]}}
            for destination in (candidate, comparison):
                destination.mkdir()
                (destination / "release-manifest.json").write_text(json.dumps(manifest))
            request = copy.deepcopy(self.parent)
            request["release"]["body_sha256"] = self.m.sha256(ROOT / self.profile["body_path"])
            request["local_gates"]["release_gate_evidence_sha256"] = self.digest(bundle)
            request_path, gate_path = base / "request.json", base / "gates.json"
            request_path.write_text(json.dumps(request))
            gate_path.write_text(json.dumps(bundle))
            for comparison_path, evidence_path, missing in ((comparison, gate_path, None), (None, None, "requires --comparison-candidate")):
                output = io.StringIO()
                with mock.patch.object(self.m, "publication_assets", return_value=copy.deepcopy(request["assets"])), \
                     mock.patch.object(self.m, "validate_release", return_value=0), \
                     mock.patch.object(self.m, "validate_profile_release_gate_bundle", wraps=self.m.validate_profile_release_gate_bundle) as gate, \
                     contextlib.redirect_stdout(output):
                    code = self.m.publication_plan("publish", request_path, candidate, comparison_path, evidence_path, "json")
                result = json.loads(output.getvalue())
                self.assertEqual(gate.call_args.kwargs["profile"], self.profile)
                if missing:
                    self.assertEqual((code, result["status"]), (2, "blocked"))
                    self.assertTrue(any(missing in error for error in result["errors"]))
                elif sys.version_info[:2] == (3, 9):
                    self.assertEqual((code, result["status"]), (0, "safe"), result["errors"])
                    self.assertEqual(result["intent"]["schema_version"], 7)
                else:
                    self.assertEqual((code, result["status"]), (2, "blocked"))
