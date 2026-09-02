# Implementation: Token Efficient Adaptive Workflow

## Readiness used

- Work item: `20260902-token-efficient-adaptive-workflow`
- Gate: `implementation-ready`
- Governing decisions: Accepted ADR 0012 with Accepted ADR 0008 as the safety
  floor
- Review: approved by the distinct read-only Tech Lead reviewer recorded in the
  brief
- Implementation writer: one shared RD writer
- Reopen result: not required; implementation introduced no new migration,
  schema, recovery, compatibility, trust, or irreversible-state choice

## Implemented boundary

- Made classification risk-first across the managed operating/readiness/
  orchestration contracts: multiple tightly coupled files do not force M,
  user-flow/shared-contract/API/unresolved-acceptance work remains at least M,
  and cross-system/high-risk work is L.
- Added artifact-first specialist packets with role/mode, bounded objective,
  authoritative references, applicable criteria, governing readiness evidence,
  ownership, expected output/evidence, blockers, and capability limitations.
  Missing evidence fails closed. Full conversation history and unrelated files
  are excluded by default; unavailable transport bounding is disclosed.
- Preserved triggered-M/L author, distinct reviewer, gate, single RD writer, and
  independent QA separation. RD owns focused checks; QA owns one complete default
  verification of the unchanged normal M/L final candidate, with only the
  accepted invalid-evidence, changed-candidate, or specialized-gate rerun cases.
- Advanced the unpublished source/install/package/Plugin identity to Vibe Kit
  `0.8.0`, core protocol 6, and Codex adapter protocol 6. Agent-install schema and
  protocol remain 3/3; CLI result, takeover, maintenance bridge, release manifest,
  and managed manifest schemas remain unchanged.
- Retargeted the existing compiled special predecessor registry to the new
  candidate and extended the existing maintenance-bridge predecessor protocol
  declaration through the v0.7 family. The eligibility, authentication,
  transaction, recovery, and failure behavior are unchanged.
- Preserved the exact v0.7 publication/closeout Skill, CLI validation, release
  notes, historical ADR/work-item evidence, and public links.

## Focused implementation evidence

- `python3 -m unittest tests.test_workflow_contract -v` — 17 passed on the final
  focused run.
- `python3 -m unittest -v` with the four selected CLI scenarios for init/doctor,
  official v0.5 special migration, reproducible package/install/validation, and
  healthy offline v0.7-to-v0.8 ordinary upgrade — 4 passed.
- Final rerun of the package/distribution and healthy v0.7-to-v0.8 scenarios —
  2 passed.
- Exact historical v0.7 publication behavior plus rejection of an unpublished
  v0.8 candidate by that contract — 2 passed.
- `./bin/vibe doctor . --format json` — healthy, version `0.8.0`, protocol 6
  fingerprint, activation set match, no diagnostics, and no network use.
- `git diff --check` — passed.

## Verification handoff

Independent QA owns the final criterion-to-evidence mapping and the exactly-once
complete default `./bin/vibe verify . --format json` run for the unchanged final
candidate. RD intentionally did not run that default matrix and does not claim
AC-1 through AC-11 as accepted. Static contract/distribution evidence does not
prove live host context isolation or a measured token, cost, or percentage
reduction.
