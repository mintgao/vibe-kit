"""Behavioral evidence for ADR 0020: the v0.10.0 publication profile, its schema-3
closeout, the advanced bridge/predecessor-migration boundary and the managed-guide
version drift check. No host-authentication or live-publication claims."""
import copy
import json
import re
import unittest

from tests.test_cli import ROOT, load_cli_module, profile_test_intent, profile_test_receipt

CLOSEOUT_ISSUES = [8, 9, 10, 11, 12, 13]


class V010PublicationProfileTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()

    def profile(self):
        return self.m.PUBLICATION_PROFILES[4]

    def test_profile_is_closed_and_pinned(self):
        profile = self.profile()
        self.assertEqual(profile["schema"], 4)
        self.assertEqual(profile["version"], "0.10.0")
        self.assertEqual(profile["tag"], "v0.10.0")
        self.assertEqual(profile["title"], "Vibe Kit v0.10.0")
        self.assertEqual(profile["profile"], "vibe-kit-v0.10.0-prerelease")
        self.assertEqual(profile["body_path"], "docs/releases/0.10.0.md")
        self.assertEqual(profile["direct"], "vibe-kit-0.10.0.zip")
        self.assertEqual(profile["distribution"], "vibe-kit-distribution-0.10.0.zip")
        self.assertEqual(profile["plugin"], "vibe-kit-plugin-0.10.0.zip")
        self.assertEqual(
            profile["issue_policy"],
            {
                "mode": "after-public-verification",
                "issues": CLOSEOUT_ISSUES,
                "allowed_operations": ["create-exact-evidence-comment", "close-issue"],
            },
        )
        self.assertEqual(profile["post_criteria"], ["AC-1", "AC-2", "AC-3", "AC-4", "AC-5", "AC-6", "AC-7"])
        self.assertEqual(sorted(profile["requirements"]), sorted(profile["states"]))
        self.assertEqual(profile["states"]["AC-7"], "not-runnable-before-publication")
        self.assertEqual(profile["states"]["AC-CLOSE.1"], "not-runnable-before-publication")
        self.assertEqual(profile["requirements"]["AC-CLOSE.1"], "issue-closeout")
        self.assertEqual(profile["requirements"]["AC-7"], "live-read-back")
        self.assertEqual(
            set(profile["kinds"]),
            {"prepublication-qa", "configured-checks", "python-3.9", "clean-build", "release-gate-evidence", "postpublication-acceptance"},
        )
        for kind in profile["kinds"].values():
            self.assertTrue(kind.startswith("vibe-kit-v0.10-"), kind)
        self.assertEqual(
            list(profile["smokes"]),
            [
                "public-direct-init-doctor",
                "public-plugin-bundled-plan-init-doctor",
                "public-upgrade-v0.3-to-v0.10",
                "public-upgrade-v0.5-to-v0.10",
                "public-upgrade-v0.6-to-v0.10",
                "public-upgrade-v0.7-to-v0.10",
                "public-upgrade-v0.8-to-v0.10",
                "public-upgrade-v0.9-to-v0.10",
            ],
        )
        self.assertEqual(profile["authorization_fields"], ("authorization_source_ref", "bound_at"))
        self.assertEqual(self.m.validate_profile_intent(profile_test_intent(self.m, 4), profile=profile), [])

    def test_profile_intent_receipt_and_authorization_acceptance(self):
        profile = self.profile()
        intent = profile_test_intent(self.m, 4)
        receipt = profile_test_receipt(self.m, intent, 4)
        digest = self.m.canonical_json_sha256
        self.assertEqual(self.m.validate_publication_intent(intent), [])
        self.assertEqual(self.m.validate_publication_receipt_shape(receipt, intent), [])
        authorization = {
            "authorization_id": receipt["authorization_id"],
            "repository": "mintgao/vibe-kit",
            "version": "0.10.0",
            "release_kind": "prerelease",
            "allowed_operations": list(self.m.V080_PUBLICATION_ALLOWED_OPERATIONS),
            "publication_intent_sha256": digest(intent),
            "host_operation_id": receipt["host_operation_id"],
            "authorization_source_ref": "task:accepted",
            "bound_at": "2026-09-22T00:00:00Z",
        }
        self.assertEqual(self.m.validate_profile_authorization(authorization, intent, profile=profile), [])
        for mutate in (
            lambda value: value.pop("authorization_source_ref"),
            lambda value: value.update(bound_at="not-a-time"),
            lambda value: value.update(version="0.9.0"),
        ):
            bad = copy.deepcopy(authorization)
            mutate(bad)
            self.assertTrue(self.m.validate_profile_authorization(bad, intent, profile=profile))

    def test_historical_profiles_reject_a_v010_candidate(self):
        intent = profile_test_intent(self.m, 4)
        for schema in (2, 3, 5):
            self.assertTrue(
                self.m.validate_profile_intent(intent, profile=self.m.PUBLICATION_PROFILES[schema]),
                f"a v0.10.0 candidate must not pass the schema-{schema} profile",
            )
        self.assertNotEqual(
            self.m.validate_publication_intent(dict(intent, schema_version=5)),
            [],
            "a v0.10.0 candidate must not pass the schema-5 dispatch",
        )
        self.assertEqual(
            self.m.validate_publication_intent(dict(intent, schema_version=6)),
            ["publication intent schema/profile is unsupported"],
        )
        self.assertTrue(
            self.m.validate_publication_receipt_shape(
                profile_test_receipt(self.m, profile_test_intent(self.m, 3), 3), intent
            )
        )
        # the historical entry points keep their own acceptance
        self.assertEqual(
            self.m.validate_profile_intent(profile_test_intent(self.m, 3), profile=self.m.PUBLICATION_PROFILES[3]), []
        )
        self.assertEqual(
            self.m.validate_profile_intent(profile_test_intent(self.m, 2), profile=self.m.PUBLICATION_PROFILES[2]), []
        )

    def test_publication_schemas_and_identity_are_mirrored_everywhere(self):
        contract = json.loads((ROOT / "agent-install.json").read_text())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text())
        expected = (5, 5, 3)
        self.assertEqual(
            (
                contract["publication"]["intent_schema"],
                contract["publication"]["receipt_schema"],
                contract["publication"]["issue_closeout_intent_schema"],
            ),
            expected,
        )
        self.assertEqual(
            (
                protocol["publication_intent_schema"],
                protocol["publication_receipt_schema"],
                protocol["issue_closeout_intent_schema"],
            ),
            expected,
        )
        self.assertEqual(
            (
                self.m.PUBLICATION_INTENT_SCHEMA,
                self.m.PUBLICATION_RECEIPT_SCHEMA,
                self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA,
            ),
            expected,
        )
        self.assertEqual(contract["kit_version"], "0.10.1")
        self.assertEqual((ROOT / ".vibe/core/version").read_text().strip(), "0.10.1")
        self.assertEqual((ROOT / ".vibe/version").read_text().strip(), "0.10.1")
        plugin = json.loads(
            (ROOT / "distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json").read_text()
        )
        self.assertEqual(plugin["version"], "0.10.1")

    def test_bridge_bound_and_predecessor_migration_advance_to_the_current_target(self):
        contract = json.loads((ROOT / "agent-install.json").read_text())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text())
        bridge = contract["maintenance_bridge"]
        self.assertEqual(bridge["maximum_installed_kit_version_exclusive"], "0.10.1")
        self.assertEqual(bridge["minimum_installed_kit_version"], "0.2.0")
        self.assertEqual(bridge["supported_installed_agent_protocols"], [0, 1, 2, 3])
        self.assertEqual(bridge["target_agent_install_schema"], 4)
        self.assertEqual(bridge["target_agent_install_protocol"], 4)
        entry = self.m.PREDECESSOR_MIGRATION_REGISTRY["entries"][3]
        self.assertEqual(entry["target"]["framework_version"], "0.10.1")
        self.assertEqual(entry["predecessor"]["framework_version"], "0.5.0")
        self.assertEqual(
            self.m.PREDECESSOR_MIGRATION_REGISTRY_SHA256,
            self.m.EXPECTED_PREDECESSOR_MIGRATION_REGISTRY_SHA256,
        )
        self.assertEqual(
            bridge["predecessor_migrations"]["registry_sha256"],
            self.m.PREDECESSOR_MIGRATION_REGISTRY_SHA256,
        )
        self.assertEqual(protocol["predecessor_migrations"], bridge["predecessor_migrations"])


class V010CloseoutTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.digest = "a" * 64

    def closeout_request(self):
        identifier = self.m.profile_closeout_id(
            self.digest, version="0.10.0", schema=3, issues=CLOSEOUT_ISSUES
        )
        issues, snapshots, operations = [], [], []
        for index, number in enumerate(CLOSEOUT_ISSUES):
            body = (
                f"Problem fixed; regression test; public v0.10.0. "
                f"<!-- vibe-kit:v0.10.0:issue-{number}:{identifier} -->"
            )
            issues.append(
                {
                    "issue_number": number,
                    "comment_body": body,
                    "observed_state": "open",
                    "observed_matching_comment_id": None,
                    "criterion_evidence_sha256": "b" * 64,
                }
            )
            snapshot = {
                "issue_number": number,
                "state": "open",
                "marker_state": "absent",
                "matching_comment_id": None,
                "matching_comment_body_sha256": None,
            }
            snapshots.append(snapshot)
            for offset, kind in enumerate(["create-exact-evidence-comment", "close-issue"]):
                comment = offset == 0
                operations.append(
                    {
                        "sequence": 2 * index + offset,
                        "operation_id": f"issue-{number}-{'comment' if comment else 'close'}",
                        "issue_number": number,
                        "kind": kind,
                        "natural_key": (
                            f"issue:{number}:marker:{identifier}"
                            if comment
                            else f"issue:{number}:state:closed"
                        ),
                        "expected_precondition": {
                            "kind": "issue-closeout-monotonic-resume",
                            "initial_snapshot_sha256": self.m.canonical_json_sha256(snapshot),
                            "allowed_observations": (
                                ["open-absent", "open-exact", "closed-exact"]
                                if comment
                                else ["open-exact", "closed-exact"]
                            ),
                        },
                        "max_write_attempts": 2,
                    }
                )
        request = {
            "parent_publication_intent_sha256": self.digest,
            "publication_receipt_sha256": "c" * 64,
            "verification_receipt_sha256": "d" * 64,
            "repository": self.m.publication_repository(),
            "issues": issues,
            "remote_snapshot": {"observed_at": "2026-09-22T00:00:00Z", "issues": snapshots},
            "operations": operations,
            "authorization_scope": {
                "repository": "mintgao/vibe-kit",
                "issues": CLOSEOUT_ISSUES,
                "allowed_operations": ["create-exact-evidence-comment", "close-issue"],
                "destructive_operations_allowed": False,
                "requires_separate_closeout_authorization": True,
            },
        }
        return request, identifier

    def test_closeout_intent_is_schema_3_over_the_ordered_issue_set(self):
        request, identifier = self.closeout_request()
        intent, bodies = self.m.build_profile_closeout_intent(
            request, version="0.10.0", schema=3, issue_numbers=CLOSEOUT_ISSUES, parent_digest=self.digest
        )
        self.assertEqual(intent["schema_version"], 3)
        self.assertEqual([item["issue_number"] for item in intent["issues"]], CLOSEOUT_ISSUES)
        self.assertEqual(len(intent["operations"]), 12)
        self.assertEqual([item["sequence"] for item in intent["operations"]], list(range(12)))
        self.assertEqual(len(bodies), 6)
        for number in CLOSEOUT_ISSUES:
            self.assertIn(f"<!-- vibe-kit:v0.10.0:issue-{number}:{identifier} -->", bodies[str(number)])
        self.assertEqual(intent["authorization_scope"]["issues"], CLOSEOUT_ISSUES)
        # the v0.7/v0.9 graphs stay closed against this request
        with self.assertRaises(self.m.VibeError):
            self.m.build_closeout_intent(request)
        for mutate in (
            lambda value: value["issues"].reverse(),
            lambda value: value["operations"].reverse(),
            lambda value: value["remote_snapshot"]["issues"][0].update(state="closed"),
            lambda value: value["remote_snapshot"]["issues"][0].update(marker_state="duplicate"),
            lambda value: value["operations"][0].update(max_write_attempts=3),
        ):
            bad = copy.deepcopy(request)
            mutate(bad)
            with self.assertRaises(self.m.VibeError):
                self.m.build_profile_closeout_intent(
                    bad, version="0.10.0", schema=3, issue_numbers=CLOSEOUT_ISSUES, parent_digest=self.digest
                )

    def test_closeout_receipt_acceptance_and_rejection(self):
        request, identifier = self.closeout_request()
        intent, _ = self.m.build_profile_closeout_intent(
            request, version="0.10.0", schema=3, issue_numbers=CLOSEOUT_ISSUES, parent_digest=self.digest
        )
        authorization = {
            "closeout_authorization_id": "close-auth",
            "repository": "mintgao/vibe-kit",
            "issues": CLOSEOUT_ISSUES,
            "allowed_operations": ["create-exact-evidence-comment", "close-issue"],
            "closeout_intent_sha256": self.m.canonical_json_sha256(intent),
            "destructive_operations_allowed": False,
            "authorization_source_ref": "task:existing-user-request",
            "bound_at": "2026-09-22T00:00:00Z",
        }
        self.assertEqual(self.m.validate_profile_closeout_authorization(authorization, intent, schema=3), [])
        receipt = {
            "schema_version": 3,
            "kind": "vibe-kit-issue-closeout-receipt",
            "closeout_id": identifier,
            "closeout_intent_sha256": self.m.canonical_json_sha256(intent),
            "closeout_authorization_id": "close-auth",
            "overall_state": "confirmed-complete",
            "items": [
                {
                    "issue_number": number,
                    "expected_initial_state": "open",
                    "comment_body_sha256": intent["issues"][index]["comment_body_sha256"],
                    "comment_id": 100 + number,
                    "comment_url": f"https://github.com/mintgao/vibe-kit/issues/{number}#issuecomment-{100 + number}",
                    "comment_write_state": "created",
                    "close_write_state": "read-matched",
                    "observed_post_state": "closed",
                    "read_back": True,
                    "error": None,
                }
                for index, number in enumerate(CLOSEOUT_ISSUES)
            ],
        }
        self.assertEqual(self.m.validate_v100_closeout_receipt(receipt, intent, authorization), [])
        for mutate in (
            lambda value: value["items"].reverse(),
            lambda value: value["items"][0].update(read_back=False),
            lambda value: value["items"][0].update(comment_url="https://example.invalid"),
            lambda value: value.update(schema_version=2),
            lambda value: value["items"][0].update(close_write_state="updated"),
            lambda value: value["items"].pop(),
        ):
            bad = copy.deepcopy(receipt)
            mutate(bad)
            self.assertTrue(
                self.m.validate_v100_closeout_receipt(bad, intent, authorization),
                "a mutated v0.10.0 closeout receipt must be rejected",
            )


class ManagedGuideDriftTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()
        self.guide = (ROOT / "AGENT_INSTALL.md").read_text()
        self.version = self.m.framework_version(ROOT)

    def test_framework_version_is_the_release_version(self):
        self.assertEqual(self.version, "0.10.1")

    def test_managed_guide_version_literals_agree_with_the_framework_version(self):
        sites = {
            "identification line": r"This document is the Agent-host-facing adoption and maintenance entry point for\s+Vibe Kit (?P<version>\d+\.\d+\.\d+)\.",
            "activation notice": r"> Vibe Kit 文件已升级到 (?P<version>\d+\.\d+\.\d+)，",
            "publication boundary": r"presents the closed v(?P<version>\d+\.\d+\.\d+) schema-(?P<schema>\d+) Pre-release",
        }
        for name, pattern in sites.items():
            match = re.search(pattern, self.guide)
            if match is None:
                self.fail(f"the managed guide no longer carries its {name}")
                continue
            self.assertEqual(
                match.group("version"),
                self.version,
                f"the managed guide's {name} version literal diverged from the framework version",
            )
            if "schema" in match.groupdict():
                self.assertEqual(match.group("schema"), str(self.m.PUBLICATION_INTENT_SCHEMA))

    def test_managed_guide_names_no_future_version(self):
        current = tuple(int(part) for part in self.version.split("."))
        for literal in re.findall(r"\d+\.\d+\.\d+", self.guide):
            self.assertLessEqual(
                tuple(int(part) for part in literal.split(".")),
                current,
                f"the managed guide names the future version {literal}",
            )
