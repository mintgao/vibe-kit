# Verification: Raise the Hermes host label to verified and refresh the Codex conformance record under the schema-4 contract

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Registry `HOST_REGISTRY.hermes.conformance` reads `verified` with the conformance-record evidence reference; `agent-install.json#hosts.hermes.conformance` mirrors it (equality asserted by `test_registry_mirrors_stay_coherent`); `AGENT_INSTALL.md` row reads ``| `hermes` | 1 | none | verified |`` (asserted by `test_guide_publishes_host_registry`); `README.md` and `docs/context/product.md` updated; the guide's general rule sentence for hosts without a complete record is unchanged. | Pass |
| AC-2 | The label gates no operation (its only readers are the contract-shape mirror check and the tests); the unknown-host and incoherent-selection fail-closed tests are unchanged and green (`test_validator_rejects_unknown_host_and_selection`, `test_install_selection_matrix_and_fail_closed`); test edits are limited to the pinned values plus the new assertions. | Pass |
| AC-3 | The mirror rebuild procedure ran after the content edits (63 checks, none failed); new payload identity `b112db18ad4010dd3f525ac54e07d712775b2476b532bd34e30e59ae910d6df6`, activation set `34f1cd873aef5c9f5c314a4d4fe94ec4a67d4bcf1c600c539bcd11b56f8b7ca6`; `package` built and `validate-release` returned `valid`; the repository's own `doctor` reads `healthy`. | Pass |
| AC-4 | `test_workflow_contract` asserts the new label and the evidence reference; `test_registry_mirrors_stay_coherent` now compares the `conformance` entry; the new `test_hermes_conformance_label_follows_its_record` pins the label, the evidence list and the referenced file's existence. | Pass |
| AC-5 | `codex-refresh-runbook.md` and `codex-refresh-driver.py` live under this work item; the driver was smoke-tested end-to-end in a disposable copy with synthetic ids (`validate-takeover` `valid`, `errors: []`); the runbook records that the real Codex run is a handoff and claims no Codex execution. | Pass |
| AC-6 | `python3 -m unittest discover -s tests`: 118 tests OK (CPython 3.13.9); `/usr/bin/python3 -m unittest discover -s tests`: 118 tests OK (CPython 3.9.6); `doctor` `healthy`; `validate-readiness` `valid` for the brief. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| Project verification (default lane, both interpreters) | Passed | 118 tests on CPython 3.13.9 and 3.9.6. |
| `doctor . --format json` | Healthy | The installed contract authenticates after the mirror regeneration. |
| `package --output <scratch>` | Built | Distribution bundle SHA-256 `b59af40885e478e4a9c958e6a11943f23fd10ba4c6e9d00a9c1a2d6722868699`; publication status `release-candidate-unpublished` (this work item makes no release). |
| `validate-release <scratch>` | Valid | No errors. |
| `validate-readiness --brief docs/work-items/20260922-host-label-raise/brief.md` | Valid | No findings. |

## Manual scenarios

- Codex refresh rehearsal: the driver ran end-to-end in a disposable copy of this
  repository with synthetic task ids; plan `safe`, doctor `healthy`, verify
  `passed`, historical 0.9.0 → 0.10.0 upgrade `success` / transaction
  `committed`, `validate-takeover` `status: valid`, `errors: []`,
  `manual_transfer_status: valid`.
- Regeneration note: the driver's reform-generation check reports the installed
  manifest as byte-unequal to fresh output because the stored file's key order
  differs (the parsed data is equal) — the same serializer-order note recorded
  in the Hermes conformance record.

## Independent QA (delegated run-shaped packet)

The frozen candidate (`3828071`) was verified independently by a delegated QA
packet that ran the complete default lane once and `doctor` once, and reported
the raw output verbatim: `verify` `status: passed` (118 tests OK; summary
`passed: 1, failed: 0, skipped: 0, unconfigured: 3`), `doctor` `status: healthy`
(activation `match`, zero warnings, zero errors, no writes performed), and a
change-surface check confirming exactly the intended 14 files. Raw outputs and
digests are host-side under `.vibe/local/host-label-raise-qa/` (`verify.json`
`f6e3d34074d26dab16ec97dcccf15cafe76ef3f0479b2c0f5b1c0fe93701c75f`,
`doctor.json` `2e026af519f88d3406cf24adcc7b16252c007c91500655373cf9e5ab006dd02d`).

## Limitations and follow-ups

- The real Codex five-stage run is a handoff to the Codex environment (no Codex
  host exists in this environment); the runbook and the driver are the
  deliverable here.
- The release that carries the label change is a separate release-preparation
  decision and stays out of scope.