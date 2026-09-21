# Host conformance evidence: codex and hermes

Work item: `docs/work-items/20260921-host-adapters/`. Host labels live in the
contract's `hosts` registry; this record is their evidence basis, and a label
changes only when this record changes first.

## Hermes — partial evidence (label: `supported-unverified`)

Session: Hermes Agent on this machine, 2026-09-21 (single writer for this work
item). Stages actually exercised, with results:

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
4. **Takeover:** not yet exercised end-to-end on Hermes — no five-stage takeover
   object was produced for a Hermes-owned task in this session.
5. **Target re-evaluation:** not yet exercised on Hermes.

Exit criteria for a `verified` label: the full
upgrade → takeover → adaptation → verification → re-evaluation sequence run under
the Hermes host with its takeover object validated by
`bin/vibe validate-takeover`, recorded here with command results. Until then the
label stays `supported-unverified` and Hermes keeps the strictest fail-closed
rules (decision C of this work item).

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