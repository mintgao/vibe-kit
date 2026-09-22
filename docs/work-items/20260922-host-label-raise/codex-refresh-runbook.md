# Codex refresh runbook: the schema-4 five-stage record for the Codex host

Status: prepared and smoke-tested in the Hermes environment; the real run is a
handoff to the Codex environment, and no Codex execution is claimed here.

## What the refresh produces

A schema-2 takeover object (receipt kind `existing-install-admission`) for this
repository's existing installation, built by a genuinely new Codex task over the
manual-new-task path (ADR 0018) and validated by `bin/vibe validate-takeover`
together with a minimal manual-transfer payload. The admission claims no upgrade
transaction and writes no project files. All evidence stays host-side under the
conformance directory; only the summary of what ran is later recorded in
`docs/work-items/20260921-host-adapters/conformance.md` (Codex section), whose
label wording changes only after the record does.

## Two-task shape

The admission contract requires the admitting task to differ from the source
task:

1. A preparing Codex task (its id becomes `--source-task-id`) authors two files
   in the conformance directory (default `.vibe/local/codex-conformance/`):
   `handoff-context.json` and `manual-transfer.json` — shapes below. The
   transfer payload's `./`-prefixed evidence references must resolve under the
   project root and match their digests; the validator checks this.
2. A NEW Codex task started in this repository (its id becomes `--task-id`) runs
   the driver once from the repository root and reports its stdout.

## Steps (run by the new Codex task)

1. Download the public v0.9.0 predecessor asset — the driver re-enacts the
   historical 0.9.0 → 0.10.0 upgrade as the applied-stage evidence:
   `https://github.com/mintgao/vibe-kit/releases/download/v0.9.0/vibe-kit-0.9.0.zip`
2. Run:
   `python3 docs/work-items/20260922-host-label-raise/codex-refresh-driver.py --task-id <this task's id> --source-task-id <preparing task's id> --predecessor-zip <downloaded zip>`
3. Report the full stdout including the SUMMARY block. Expect every step rc 0,
   `validate-takeover` `status: valid` with `errors: []`, and
   `manual_transfer_status: valid`.

## Input shapes (authored by the preparing task)

`handoff-context.json`:

```json
{
  "schema_version": 1,
  "purpose": "<one line>",
  "source_task_id": "<preparing task id>",
  "transfer_id": "<opaque id, e.g. vk-0.10.0-codex-conformance-<date>>",
  "manual_transfer_payload": ".vibe/local/codex-conformance/manual-transfer.json",
  "versions": {"from": "0.9.0", "target": "0.10.0"},
  "recorded_at": "<ISO-8601>"
}
```

`manual-transfer.json`:

```json
{
  "transfer_schema_version": 1,
  "transfer_id": "<same id>",
  "goal": "<what the successor continues, <=4096 characters>",
  "decisions": ["<bounded entries, <=16>"],
  "unfinished": ["<bounded entries, <=16>"],
  "evidence": [
    {"ref": "./docs/decisions/0019-host-adapters.md", "sha256": "<digest of that file>"}
  ]
}
```

## Smoke result recorded here

The driver was smoke-tested in the Hermes environment against a disposable copy
of this repository with synthetic task ids (`codex-smoke-source` /
`codex-smoke-active`) and the same predecessor asset: every step returned rc 0 —
plan `safe`, doctor `healthy`, verify `passed`, historical upgrade `success` /
transaction `committed` — and `validate-takeover` returned `status: valid`,
`errors: []`, `manual_transfer_status: valid`. The regeneration check reports
byte equality of the installed manifest as `false` because the stored file's key
order differs from fresh output (the parsed data is equal); this is the same
serializer-order note recorded in the Hermes conformance record.

## Record update after the run

Append to the Codex section of
`docs/work-items/20260921-host-adapters/conformance.md`: what ran, where, the
command results and the artifact digests — with the capability limitations
recorded rather than hidden, the same discipline as the Hermes section. Evidence
stays host-side; only the record returns to the repository.