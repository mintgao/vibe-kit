"""Synthetic closed-profile and workflow evidence for ADR0022, not live publication."""
import argparse
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from tests.test_cli import ROOT, load_cli_module, profile_test_intent, profile_test_receipt

ISSUES = [14, 15, 16, 17, 18]
CRITERIA = ["AC-" + str(number) for number in range(1, 10)] + ["AC-10.1", "AC-10.2", "AC-10.3"]
SMOKES = ("public-direct-init-doctor", "public-plugin-bundled-plan-init-doctor", "public-upgrade-v0.3-to-v0.11.0", "public-upgrade-v0.5-to-v0.11.0", "public-upgrade-v0.6-to-v0.11.0", "public-upgrade-v0.7-to-v0.11.0", "public-upgrade-v0.8-to-v0.11.0", "public-upgrade-v0.9-to-v0.11.0", "public-upgrade-v0.10.0-to-v0.11.0", "public-upgrade-v0.10.1-to-v0.11.0", "public-repeat-upgrade-v0.11.0")


class V110PublicationTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.profile = self.m.PUBLICATION_PROFILES[6]
        self.parent = profile_test_intent(self.m, 6)
        self.publication = profile_test_receipt(self.m, self.parent, 6)
        self.digest = self.m.canonical_json_sha256
        self.authorization = {"authorization_id": self.publication["authorization_id"], "repository": "mintgao/vibe-kit", "version": "0.11.0", "release_kind": "prerelease", "allowed_operations": list(self.m.V080_PUBLICATION_ALLOWED_OPERATIONS), "publication_intent_sha256": self.digest(self.parent), "host_operation_id": self.publication["host_operation_id"], "authorization_source_ref": "task:existing-exact-user-request", "bound_at": "2026-10-12T00:00:00Z"}
        self.validation = self.m.result_envelope("validate-publication", "valid", profile=self.profile["profile"], version="0.11.0", intent_sha256=self.digest(self.parent), authorization_id=self.authorization["authorization_id"], host_operation_id=self.authorization["host_operation_id"], remote_write_state="confirmed-complete", verification_state="passed", errors=[], network_used=False, host_evidence_authenticated=False)
        self.acceptance = {"schema_version": 1, "kind": self.profile["kinds"]["postpublication-acceptance"], "execution_id": "independent-synthetic-acceptance", "executor_role": "independent-qa", "started_at": "2026-10-12T00:00:00Z", "finished_at": "2026-10-12T00:01:00Z", "repository": "mintgao/vibe-kit", "version": "0.11.0", "profile": self.profile["profile"], "source_commit": self.parent["source_commit"], "source_tree_oid": "a" * 40, "publication_intent_sha256": self.digest(self.parent), "authorization_id": self.authorization["authorization_id"], "host_operation_id": self.authorization["host_operation_id"], "validate_publication_result_sha256": self.digest(self.validation), "criteria": [{"criterion_id": name, "state": "passed", "evidence_refs": [{"kind": "local-gate-receipt" if name != "AC-10.2" else "validate-publication", "sha256": "a" * 64}]} for name in CRITERIA[:-1]], "status": "passed", "error": None}

    def test_exact_identity_ordered_acceptance_smokes_and_phase_separation(self):
        profile = self.profile
        self.assertEqual((profile["schema"], profile["version"], profile["tag"], profile["title"], profile["profile"], profile["body_path"]), (6, "0.11.0", "v0.11.0", "Vibe Kit v0.11.0", "vibe-kit-v0.11.0-prerelease", "docs/releases/0.11.0.md"))
        self.assertEqual(profile["smokes"], SMOKES)
        self.assertEqual(list(profile["states"]), CRITERIA)
        self.assertEqual(list(profile["requirements"]), CRITERIA)
        self.assertEqual(profile["post_criteria"], CRITERIA[:-1])
        self.assertEqual([profile["states"][name] for name in CRITERIA], ["passed"] * 10 + ["not-runnable-before-publication"] * 2)
        self.assertEqual([profile["requirements"][name] for name in CRITERIA], ["none"] * 10 + ["live-read-back", "issue-closeout"])
        self.assertEqual(profile["issue_policy"], {"mode": "after-public-verification", "issues": ISSUES, "allowed_operations": ["create-exact-evidence-comment", "close-issue"]})
        self.assertIsNone(self.publication["issue_closeout"])
        self.assertEqual(self.m.validate_publication_intent(self.parent), [])
        self.assertEqual(self.m.validate_publication_receipt_shape(self.publication, self.parent), [])
        self.assertEqual(self.m.validate_profile_authorization(self.authorization, self.parent, profile=profile), [])
        self.assertEqual(self.m.validate_profile_postpublication_acceptance(self.acceptance, self.parent, self.authorization, "a" * 40, profile=profile), [])
        premature = copy.deepcopy(self.acceptance)
        premature["criteria"].append({"criterion_id": "AC-10.3", "state": "passed", "evidence_refs": [{"kind": "local-gate-receipt", "sha256": "a" * 64}]})
        self.assertTrue(self.m.validate_profile_postpublication_acceptance(premature, self.parent, self.authorization, "a" * 40, profile=profile))

    def test_historical_profiles_keep_their_verdicts_and_reject_cross_profile(self):
        for schema in (2, 3, 4, 5):
            old = profile_test_intent(self.m, schema)
            receipt = profile_test_receipt(self.m, old, schema)
            self.assertEqual(self.m.validate_publication_intent(old), [])
            self.assertEqual(self.m.validate_publication_receipt_shape(receipt, old), [])
            self.assertTrue(self.m.validate_profile_intent(self.parent, profile=self.m.PUBLICATION_PROFILES[schema]))
            self.assertTrue(self.m.validate_publication_receipt_shape(receipt, self.parent))
            self.assertTrue(self.m.validate_publication_receipt_shape(self.publication, old))
        for mutation in (lambda v: v.update(schema_version=6.0), lambda v: v.update(version="0.10.1"), lambda v: v["assets"].pop(), lambda v: v["operations"][0].update(natural_key="wrong"), lambda v: v["issue_closeout_policy"]["issues"].reverse()):
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
        identifier = self.m.profile_closeout_id(parent_digest, version="0.11.0", schema=4, issues=ISSUES)
        issues, snapshots, operations = [], [], []
        for index, number in enumerate(ISSUES):
            body = "Verified mapped criterion evidence. " + f"<!-- vibe-kit:v0.11.0:issue-{number}:{identifier} -->"
            exact = resume and index == 0
            comment_id = 114 if exact else None
            issues.append({"issue_number": number, "comment_body": body, "observed_state": "closed" if exact else "open", "observed_matching_comment_id": comment_id, "criterion_evidence_sha256": "b" * 64})
            snapshot = {"issue_number": number, "state": "closed" if exact else "open", "marker_state": "exact" if exact else "absent", "matching_comment_id": comment_id, "matching_comment_body_sha256": self.m.sha256_text(body) if exact else None}
            snapshots.append(snapshot)
            for offset, kind in enumerate(("create-exact-evidence-comment", "close-issue")):
                operations.append({"sequence": 2 * index + offset, "operation_id": f"issue-{number}-{'comment' if offset == 0 else 'close'}", "issue_number": number, "kind": kind, "natural_key": f"issue:{number}:marker:{identifier}" if offset == 0 else f"issue:{number}:state:closed", "expected_precondition": {"kind": "issue-closeout-monotonic-resume", "initial_snapshot_sha256": self.digest(snapshot), "allowed_observations": ["open-absent", "open-exact", "closed-exact"] if offset == 0 else ["open-exact", "closed-exact"]}, "max_write_attempts": 2})
        return {"parent_publication_intent_sha256": parent_digest, "publication_receipt_sha256": self.digest(self.publication), "verification_receipt_sha256": self.digest(self.acceptance), "repository": self.m.publication_repository(), "issues": issues, "remote_snapshot": {"observed_at": "2026-10-12T00:02:00Z", "issues": snapshots}, "operations": operations, "authorization_scope": {"repository": "mintgao/vibe-kit", "issues": ISSUES, "allowed_operations": ["create-exact-evidence-comment", "close-issue"], "destructive_operations_allowed": False, "requires_separate_closeout_authorization": True}}, identifier

    def build(self, request):
        return self.m.build_v110_closeout_intent(request, self.parent, self.publication, self.authorization, self.acceptance, self.validation)

    def test_schema4_closeout_exact_order_markers_parent_binding_and_resume(self):
        self.assertEqual(self.m.validate_v110_closeout_parent(self.parent, self.publication, self.authorization, self.acceptance, self.validation), [])
        request, identifier = self.request()
        intent, bodies = self.build(request)
        self.assertEqual(intent["schema_version"], 4)
        self.assertEqual([item["issue_number"] for item in intent["issues"]], ISSUES)
        self.assertEqual([item["operation_id"] for item in intent["operations"]], [f"issue-{number}-{kind}" for number in ISSUES for kind in ("comment", "close")])
        self.assertEqual(len(intent["operations"]), 10)
        for number in ISSUES:
            self.assertIn(f"<!-- vibe-kit:v0.11.0:issue-{number}:{identifier} -->", bodies[str(number)])
        resumed, unused = self.request(resume=True)
        self.assertEqual(self.build(resumed)[0]["issues"][0]["observed_state"], "closed")
        for mutation in (lambda v: v["issues"].reverse(), lambda v: v["operations"].reverse(), lambda v: v["issues"][0].update(issue_number=13), lambda v: v["issues"][0].update(comment_body="wrong marker"), lambda v: v.update(publication_receipt_sha256="0" * 64), lambda v: v.update(parent_publication_intent_sha256="0" * 64), lambda v: v["operations"][0].update(max_write_attempts=3), lambda v: v["remote_snapshot"]["issues"][0].update(marker_state="duplicate")):
            value = copy.deepcopy(request)
            mutation(value)
            with self.assertRaises(self.m.VibeError):
                self.build(value)
        wrong_parent = profile_test_intent(self.m, 5)
        self.assertTrue(self.m.validate_v110_closeout_parent(wrong_parent, self.publication, self.authorization, self.acceptance, self.validation))
        bad_validation = dict(self.validation, host_operation_id="other")
        self.assertTrue(self.m.validate_v110_closeout_parent(self.parent, self.publication, self.authorization, self.acceptance, bad_validation))

    def test_closeout_complete_requires_each_pair_and_partial_uncertain_is_honest(self):
        request, identifier = self.request()
        intent, unused = self.build(request)
        authorization = {"closeout_authorization_id": "separate-exact-issue-authorization", "repository": "mintgao/vibe-kit", "issues": ISSUES, "allowed_operations": ["create-exact-evidence-comment", "close-issue"], "closeout_intent_sha256": self.digest(intent), "destructive_operations_allowed": False, "authorization_source_ref": "task:existing-separate-issue-closeout-request", "bound_at": "2026-10-12T00:02:00Z"}
        receipt = {"schema_version": 4, "kind": "vibe-kit-issue-closeout-receipt", "closeout_id": identifier, "closeout_intent_sha256": self.digest(intent), "closeout_authorization_id": authorization["closeout_authorization_id"], "overall_state": "confirmed-complete", "items": [{"issue_number": number, "expected_initial_state": "open", "comment_body_sha256": intent["issues"][index]["comment_body_sha256"], "comment_id": 100 + number, "comment_url": f"https://github.com/mintgao/vibe-kit/issues/{number}#issuecomment-{100 + number}", "comment_write_state": "confirmed-after-uncertain", "close_write_state": "read-matched", "observed_post_state": "closed", "read_back": True, "error": None} for index, number in enumerate(ISSUES)]}
        self.assertEqual(self.m.validate_v110_closeout_receipt(receipt, intent, authorization), [])
        malformed_items = [receipt["items"] + [None], receipt["items"] + ["extra"],
                           receipt["items"] + [{}], receipt["items"][:-1],
                           receipt["items"][:2] + [None] + receipt["items"][3:],
                           receipt["items"][:2] + ["wrong"] + receipt["items"][3:],
                           receipt["items"][:2] + [{}] + receipt["items"][3:]]
        for index, items in enumerate(malformed_items):
            with self.subTest(malformed_item_case=index):
                value = copy.deepcopy(receipt)
                value["items"] = items
                self.assertTrue(self.m.validate_v110_closeout_receipt(value, intent, authorization))
        partial = copy.deepcopy(receipt)
        partial["overall_state"] = "confirmed-partial"
        for item in partial["items"][1:]:
            item.update(comment_id=None, comment_url=None, comment_write_state="not-attempted", close_write_state="not-attempted", observed_post_state=None, read_back=False)
        self.assertEqual(self.m.validate_v110_closeout_receipt(partial, intent, authorization), [])
        partial["overall_state"] = "confirmed-complete"
        self.assertTrue(self.m.validate_v110_closeout_receipt(partial, intent, authorization))
        partial["overall_state"] = "uncertain"
        partial["items"][1]["comment_write_state"] = "uncertain"
        self.assertEqual(self.m.validate_v110_closeout_receipt(partial, intent, authorization), [])
        for mutation in (lambda v: v["items"].reverse(), lambda v: v.update(schema_version=3), lambda v: v["items"][0].update(read_back=False), lambda v: v["items"][0].update(comment_url="https://example.invalid")):
            value = copy.deepcopy(receipt)
            mutation(value)
            self.assertTrue(self.m.validate_v110_closeout_receipt(value, intent, authorization))
        bad_auth = dict(authorization, closeout_intent_sha256="0" * 64)
        self.assertTrue(self.m.validate_v110_closeout_receipt(receipt, intent, bad_auth))
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
            self.assertEqual(json.loads(output.getvalue())["intent"]["schema_version"], 4)

    def test_current_mirrors_homepages_and_prospective_outcome_contract(self):
        contract = json.loads((ROOT / "agent-install.json").read_bytes())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_bytes())
        self.assertEqual((self.m.PUBLICATION_INTENT_SCHEMA, self.m.PUBLICATION_RECEIPT_SCHEMA, self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA), (6, 6, 4))
        self.assertEqual((contract["publication"]["intent_schema"], contract["publication"]["receipt_schema"], contract["publication"]["issue_closeout_intent_schema"]), (6, 6, 4))
        self.assertEqual((protocol["publication_intent_schema"], protocol["publication_receipt_schema"], protocol["issue_closeout_intent_schema"]), (6, 6, 4))
        for name in ("README.md", "README.zh-CN.md"):
            homepage = (ROOT / name).read_text()
            self.assertIn('releases/tag/v0.10.1', homepage)
            self.assertIn('0.11.0', homepage)
            self.assertIn('all-configured', homepage)
            self.assertIn('Unverified', homepage)
        template = (ROOT / ".vibe/core/templates/work-item-brief.md").read_text()
        for column in ("Approved outcome / AC reference", "This stage covers", "State", "Evidence", "Next action", "Role owner", "Blocker / waiting condition"):
            self.assertIn(column, template)
        contract_text = (ROOT / ".vibe/core/operating-model.md").read_text()
        for text in ("Source Pass plus external", "export Unverified", "completes only the source stage", "already-authorized actionable diagnosis", "S remains lightweight", "historical", "custody", "independent", "not a new QA result enum", "Static scenarios"):
            self.assertIn(text, contract_text)
        # Explicitly synthetic coverage: source Pass cannot erase outstanding stages.
        rows = [("docs/work-items/example/brief.md#AC-1", "source", "Pass", "implementation.md", "verify API", "QA", "none"), ("docs/work-items/example/brief.md#AC-2", "API", "Blocked", "verification.md", "request external permission", "Host executor", "permission grant"), ("docs/work-items/example/brief.md#AC-3", "export", "Unverified", "none", "verify export after API", "QA", "API pass")]
        self.assertFalse(all(row[2] in ("Pass", "Not applicable") for row in rows))
        self.assertTrue(all(row[0] and row[4] and row[5] and row[6] for row in rows))
