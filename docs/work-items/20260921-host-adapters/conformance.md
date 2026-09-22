# Host conformance evidence: codex and hermes

Work item: `docs/work-items/20260921-host-adapters/`. Host labels live in the
contract's `hosts` registry; this record is their evidence basis, and a label
changes only when this record changes first.

## Hermes — five-stage evidence complete (label: `verified`)

Session: Hermes Agent on this machine; install, upgrade, adaptation and
verification runs on 2026-09-21, the takeover and re-evaluation stages on
2026-09-22 as the manual-new-task admission of this repository's own installed
0.10.0 contract (single writer for this work item).

1. **Upgrade (install and re-upgrade):** `init --host hermes` into a fresh
   target, then `upgrade` on the same target — both exit 0, selection preserved
   across the upgrade, no `.codex` payload appears (stage suite
   `tests/test_host_adapters.py::test_install_selection_matrix_and_fail_closed`).
2. **Adaptation (host payload boundary):** the Hermes-selected install carries
   no `.codex/agents` payload and no skill-local `agents/` configuration; core
   documents, skills and both contracts install normally and the installed copy
   records `selected_hosts: ["hermes"]` with a recomputed activation identity.
3. **Default verification:** `doctor` passes with 0 warnings for the
   Hermes-selected install before and after the upgrade; `validate-readiness`
   for this work item returns `valid`.
4. **Takeover (manual new-task admission):** a genuinely new Hermes task
   (session `20260922_153702_717d1f`) took over the existing installation
   through the manual-new-task path with receipt kind
   `existing-install-admission` — it claims no transaction and writes no project
   file. Its schema-2 takeover object (nine stages satisfied,
   `overall_status: ready`, `last_completed_stage: ready`) passed
   `bin/vibe validate-takeover --format json` with `status: valid` and no
   errors; the minimal manual-transfer payload validated alongside it
   (`manual_transfer_status: valid`).
5. **Target re-evaluation:** under the successor task, `doctor` reported
   `healthy` and the default verification channel `verify` reported `passed`
   (117 tests) after the takeover; the routing record re-evaluates the target as
   `routable` under target rules.

Command results for the admission: `plan upgrade` → `safe` (28 no-op, 1 update,
1 preserve); `doctor` → `healthy`; `verify` → `passed`; historical predecessor
upgrade (v0.9.0 → v0.10.0) → `success`, transaction `committed`;
`validate-takeover` → `valid`.

Evidence artifacts are host-side under `.vibe/local/takeover-conformance/`
(gitignored local state: the takeover contract keeps transfer state in the host
task boundary, so this record cites it instead of committing it):

| artifact | sha256 |
| --- | --- |
| `takeover-object.json` | `eb3b926ecff4b29c13398cc426666598f1e3bbba852d384ac1b066a2ab8ba587` |
| `validation-receipt.json` | `b333bec21b940039274da90cc67a450f5c69b9fcda6bb2a2336f5b490af4a2cb` |
| `manual-transfer.json` | `f64ae3cba0e51f4fffbbe28c25a8302634bf21d52bfad1cbc4deafa8c272a1e8` |
| `historical-upgrade-receipt.json` | `9c2fa6f87fad48018785cc699e58a07bcc970c09cb2151d1b36fc08530d33e00` |
| `doctor-receipt.json` | `2c26077f9040d4f4451c01119a7da7a8e25d1ad8bf91817015a44deb29359884` |
| `verify-receipt.json` | `984f4f69219ba12ba773ea9bcc5d306fdca018abd9d930d30053e84a0f7786e8` |
| `summary.json` | `7d6617f4ea4a04548d32e02f5b39cb434133372c9ed7a3586fb7a30381959319` |

Admission honesty notes: this checkout carries no in-place upgrade transaction —
its installed identity was produced by the documented regeneration procedure (a
disposable production `init` copied into the checkout at the release-prep
commit). The `applied` stage therefore cites the receipt of a real production
0.9.0 → 0.10.0 upgrade run in a disposable predecessor, and a fresh production
`init` with the recorded selection reproduces the installed manifest's data
exactly (the stored file orders the `hosts` key last; fresh output places it
after `source` — a serializer ordering difference, not a content difference).
Known limitation surfaced by this exercise, not a conformance blocker: running
`upgrade` again on an already-current install fails
`target postimage validation failed` and rolls back (reproduces on the 0.9.0 and
0.10.0 CLIs; tracked as a feedback candidate).

The exit criteria for a `verified` label — the full
upgrade → takeover → adaptation → verification → re-evaluation sequence run
under the Hermes host with its takeover object validated by
`bin/vibe validate-takeover`, recorded here with command results — are met by
this record, and the label was raised to `verified` by the owner-approved work
item `docs/work-items/20260922-host-label-raise/` (product-owner confirmation
2026-09-22): the registry, the contract mirror and the guide now read `verified`
for Hermes. Historical records — the v0.10.0 release note and the 0.10.0-era
decisions — keep their point-in-time wording.

## Codex — basis of the current `verified` label

The Codex adapter and its bootstrap Plugin have shipped and been exercised
through the published releases; the registry's evidence references
(`docs/decisions/0005-bootstrap-plugin-capabilities.md`, `docs/releases/0.9.0.md`)
are the recorded basis. Re-running the five-stage sequence under the schema-4
contract during the 0.10.0 release window remains a tracked follow-up; this note
does not downgrade that label, and no other host's label may be raised without an
equivalent record.

## Fail-closed invariants proven by the suites

- An unknown selection (`--host bogus`) is refused before any file is written.
- Installed coherence is bound to the recorded selection and the recomputed
  activation identity; payload that does not match the recorded selection fails
  the identity checks, and upgrades preserve the recorded selection.
- Release payloads always carry every declared host's files — a selection never
  shrinks the release (regression-checked by the release identity suites).
