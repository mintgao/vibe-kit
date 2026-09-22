"""Behavioral evidence for ADR 0021: the v0.10.1 publication profile (schema 5),
its no-closeout issue policy, the advanced maintenance-bridge and
predecessor-migration boundary, the published Hermes `verified` label, and the
schema-5 shared-helper parity. No host-authentication or live-publication claims.
"""
import argparse
import copy
import json
import re
import tempfile
import unittest
from pathlib import Path

from tests.test_cli import ROOT, load_cli_module, profile_test_intent, profile_test_receipt

SMOKES = (
    "public-direct-init-doctor",
    "public-plugin-bundled-plan-init-doctor",
    "public-upgrade-v0.3-to-v0.10.1",
    "public-upgrade-v0.5-to-v0.10.1",
    "public-upgrade-v0.6-to-v0.10.1",
    "public-upgrade-v0.7-to-v0.10.1",
    "public-upgrade-v0.8-to-v0.10.1",
    "public-upgrade-v0.9-to-v0.10.1",
    "public-upgrade-v0.10.0-to-v0.10.1",
)
CRITERIA = ["AC-1", "AC-2", "AC-3", "AC-4", "AC-5", "AC-6"]


class V011PublicationProfileTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()

    def profile(self):
        return self.m.PUBLICATION_PROFILES[5]

    def test_profile_is_closed_and_pinned(self):
        profile = self.profile()
        self.assertEqual(profile["schema"], 5)
        self.assertEqual(profile["version"], "0.10.1")
        self.assertEqual(profile["tag"], "v0.10.1")
        self.assertEqual(profile["title"], "Vibe Kit v0.10.1")
        self.assertEqual(profile["profile"], "vibe-kit-v0.10.1-prerelease")
        self.assertEqual(profile["body_path"], "docs/releases/0.10.1.md")
        self.assertEqual(profile["direct"], "vibe-kit-0.10.1.zip")
        self.assertEqual(profile["distribution"], "vibe-kit-distribution-0.10.1.zip")
        self.assertEqual(profile["plugin"], "vibe-kit-plugin-0.10.1.zip")
        self.assertEqual(
            profile["issue_policy"],
            {"mode": "none", "issues": [], "allowed_operations": []},
        )
        self.assertEqual(profile["post_criteria"], CRITERIA)
        self.assertEqual(sorted(profile["requirements"]), sorted(profile["states"]))
        self.assertEqual(profile["states"]["AC-6"], "not-runnable-before-publication")
        self.assertEqual(profile["requirements"]["AC-6"], "live-read-back")
        for criterion in CRITERIA[:5]:
            self.assertEqual(profile["states"][criterion], "passed")
            self.assertEqual(profile["requirements"][criterion], "none")
        self.assertEqual(
            set(profile["kinds"]),
            {"prepublication-qa", "configured-checks", "python-3.9", "clean-build", "release-gate-evidence", "postpublication-acceptance"},
        )
        for kind in profile["kinds"].values():
            self.assertTrue(kind.startswith("vibe-kit-v0.10.1-"), kind)
        self.assertEqual(list(profile["smokes"]), list(SMOKES))
        self.assertEqual(profile["authorization_fields"], ("authorization_source_ref", "bound_at"))
        self.assertEqual(self.m.validate_profile_intent(profile_test_intent(self.m, 5), profile=profile), [])

    def test_profile_intent_receipt_and_authorization_acceptance(self):
        profile = self.profile()
        intent = profile_test_intent(self.m, 5)
        receipt = profile_test_receipt(self.m, intent, 5)
        digest = self.m.canonical_json_sha256
        self.assertEqual(self.m.validate_publication_intent(intent), [])
        self.assertEqual(self.m.validate_publication_receipt_shape(receipt, intent), [])
        authorization = {
            "authorization_id": receipt["authorization_id"],
            "repository": "mintgao/vibe-kit",
            "version": "0.10.1",
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
            lambda value: value.update(version="0.10.0"),
        ):
            bad = copy.deepcopy(authorization)
            mutate(bad)
            self.assertTrue(self.m.validate_profile_authorization(bad, intent, profile=profile))

    def test_schema_5_rejects_a_wrong_identity_asset_or_operation(self):
        profile = self.profile()
        intent = profile_test_intent(self.m, 5)
        mutations = (
            lambda value: value.update(version="0.10.0"),
            lambda value: value.update(profile="vibe-kit-v0.10.0-prerelease"),
            lambda value: value["tag"].update(name="v0.10.0"),
            lambda value: value["release"].update(title="Vibe Kit v0.10.0"),
            lambda value: value["release"].update(body_source_path="docs/releases/0.10.0.md"),
            lambda value: value["assets"][2].update(name="vibe-kit-0.10.0.zip"),
            lambda value: value["assets"].pop(),
            lambda value: value["operations"][1].update(natural_key="mintgao/vibe-kit:tag:v0.10.0"),
            lambda value: value["operations"].pop(),
            lambda value: value.update(
                issue_closeout_policy={
                    "mode": "after-public-verification",
                    "issues": [8],
                    "allowed_operations": ["close-issue"],
                }
            ),
        )
        for mutate in mutations:
            bad = copy.deepcopy(intent)
            mutate(bad)
            self.assertTrue(
                self.m.validate_profile_intent(bad, profile=profile),
                f"a mutated v0.10.1 intent must be rejected: {bad.get('version')}",
            )

    def test_historical_profiles_reject_a_v0101_candidate(self):
        intent = profile_test_intent(self.m, 5)
        for schema in (2, 3, 4):
            self.assertTrue(
                self.m.validate_profile_intent(intent, profile=self.m.PUBLICATION_PROFILES[schema]),
                f"a v0.10.1 candidate must not pass the schema-{schema} profile",
            )
        schema_4_intent = profile_test_intent(self.m, 4)
        self.assertTrue(
            self.m.validate_publication_receipt_shape(
                profile_test_receipt(self.m, schema_4_intent, 4), intent
            ),
            "a v0.10.0 receipt must not validate a v0.10.1 intent",
        )
        self.assertTrue(
            self.m.validate_publication_receipt_shape(
                profile_test_receipt(self.m, intent, 5), schema_4_intent
            ),
            "a v0.10.1 receipt must not validate a v0.10.0 intent",
        )
        self.assertEqual(
            self.m.validate_publication_intent(dict(intent, schema_version=6)),
            ["publication intent schema/profile is unsupported"],
        )
        self.assertEqual(
            self.m.validate_publication_receipt_shape(dict(profile_test_receipt(self.m, intent, 5), schema_version=6), intent),
            ["publication receipt schema/profile is unsupported"],
        )
        # the historical entry points keep their own acceptance
        for schema in (2, 3, 4):
            self.assertEqual(
                self.m.validate_profile_intent(
                    profile_test_intent(self.m, schema), profile=self.m.PUBLICATION_PROFILES[schema]
                ),
                [],
            )

    def test_identity_mirrors_publish_schema_5_and_the_verified_label(self):
        profile = self.profile()
        contract = json.loads((ROOT / "agent-install.json").read_text())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text())
        self.assertEqual(
            (self.m.PUBLICATION_INTENT_SCHEMA, self.m.PUBLICATION_RECEIPT_SCHEMA, self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA),
            (5, 5, 3),
        )
        self.assertEqual(
            (
                contract["publication"]["intent_schema"],
                contract["publication"]["receipt_schema"],
                contract["publication"]["issue_closeout_intent_schema"],
            ),
            (5, 5, 3),
        )
        self.assertEqual(
            (
                protocol["publication_intent_schema"],
                protocol["publication_receipt_schema"],
                protocol["issue_closeout_intent_schema"],
            ),
            (5, 5, 3),
        )
        self.assertEqual(contract["kit_version"], "0.10.1")
        for host in ("codex", "hermes"):
            self.assertEqual(contract["hosts"][host]["conformance"]["label"], "verified")
        self.assertEqual(
            contract["hosts"]["hermes"]["conformance"]["evidence"],
            ["docs/work-items/20260921-host-adapters/conformance.md"],
        )
        self.assertTrue((ROOT / profile["body_path"]).is_file())
        guide = (ROOT / "AGENT_INSTALL.md").read_text()
        match = re.search(
            r"presents the closed v(?P<version>\d+\.\d+\.\d+) schema-(?P<schema>\d+) Pre-release",
            guide,
        )
        if match is None:
            self.fail("the managed guide no longer carries its publication boundary")
        self.assertEqual(match.group("version"), self.m.framework_version(ROOT))
        self.assertEqual(match.group("schema"), str(self.m.PUBLICATION_INTENT_SCHEMA))

    def test_release_note_claims_only_the_label_and_the_version_identity(self):
        profile = self.profile()
        body = (ROOT / profile["body_path"]).read_text()
        self.assertIn("Vibe Kit v0.10.1", body)
        self.assertIn("`verified`", body)
        self.assertIn("no product change beyond the host label and the version identity", body)
        for issue in ("#14", "#15"):
            self.assertIn(issue, body)
        for asset in (
            "SHA256SUMS",
            "release-manifest.json",
            profile["direct"],
            profile["distribution"],
            profile["plugin"],
        ):
            self.assertIn(asset, body)
        self.assertIn(
            "Codex five-stage refresh under the schema-4 contract remains a tracked follow-up",
            body,
        )
        changelog = (ROOT / "CHANGELOG.md").read_text()
        self.assertIn("## 0.10.1", changelog)
        self.assertIn("Raised the Hermes host label to `verified`", changelog)

    def test_no_schema_5_closeout_exists(self):
        profile = self.profile()
        self.assertEqual(profile["issue_policy"]["mode"], "none")
        self.assertEqual(self.m.ISSUE_CLOSEOUT_INTENT_SCHEMA, 3)
        self.assertFalse(hasattr(self.m, "build_v101_closeout_intent"))
        self.assertFalse(
            any(5 == value.get("schema") for value in self.m.PUBLICATION_PROFILES.values() if value["issue_policy"]["issues"])
        )
        names = {
            "request": "request.json",
            "parent_intent": "parent.json",
            "publication_receipt": "receipt.json",
            "publication_authorization": "authorization.json",
            "acceptance_receipt": "acceptance.json",
            "validation_result": "validation.json",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / names["parent_intent"]).write_text(json.dumps(profile_test_intent(self.m, 5)))
            for key, name in names.items():
                if key != "parent_intent":
                    (root / name).write_text("{}")
            (root / "packet.json").write_text(json.dumps(names))
            with self.assertRaises(self.m.VibeError) as raised:
                self.m.issue_closeout_command(
                    argparse.Namespace(packet=str(root / "packet.json"), format="json")
                )
            self.assertIn(
                "issue closeout requires a schema-3 (v0.9.0) or schema-4 (v0.10.0) parent publication intent",
                str(raised.exception),
            )


class V011MigrationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.m = load_cli_module()

    def test_the_migration_target_and_the_bridge_bound_agree_with_the_version(self):
        contract = json.loads((ROOT / "agent-install.json").read_text())
        protocol = json.loads((ROOT / ".vibe/core/protocol.json").read_text())
        version = self.m.framework_version(ROOT)
        self.assertEqual(version, "0.10.1")
        self.assertEqual((ROOT / ".vibe/version").read_text().strip(), version)
        self.assertEqual(contract["kit_version"], version)
        bridge = contract["maintenance_bridge"]
        self.assertEqual(bridge["maximum_installed_kit_version_exclusive"], version)
        self.assertEqual(bridge["minimum_installed_kit_version"], "0.2.0")
        self.assertEqual(bridge["supported_installed_agent_protocols"], [0, 1, 2, 3])
        self.assertEqual(bridge["target_agent_install_schema"], 4)
        self.assertEqual(bridge["target_agent_install_protocol"], 4)
        entry = self.m.PREDECESSOR_MIGRATION_REGISTRY["entries"][3]
        self.assertEqual(entry["migration_id"], "v0.5.0-unmanaged-agent-contracts-v1")
        self.assertEqual(entry["target"]["framework_version"], version)
        self.assertEqual(entry["predecessor"]["framework_version"], "0.5.0")
        self.assertEqual(entry["predecessor"]["install_identity_sha256"][:8], "70dd0eac")
        self.assertEqual(
            self.m.PREDECESSOR_MIGRATION_REGISTRY_SHA256,
            self.m.EXPECTED_PREDECESSOR_MIGRATION_REGISTRY_SHA256,
        )
        self.assertEqual(
            bridge["predecessor_migrations"]["registry_sha256"],
            self.m.PREDECESSOR_MIGRATION_REGISTRY_SHA256,
        )
        self.assertEqual(protocol["predecessor_migrations"], bridge["predecessor_migrations"])

    def test_the_target_cli_refuses_a_different_migration_target(self):
        self.assertEqual(self.m.framework_version(ROOT), "0.10.1")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".vibe/core").mkdir(parents=True)
            (root / ".vibe/core/version").write_text("0.10.0\n")
            with self.assertRaises(self.m.VibeError) as raised:
                self.m.validate_target_predecessor_migration_contract(root)
            self.assertIn("supported only by target 0.10.1", str(raised.exception))


if __name__ == "__main__":
    unittest.main()