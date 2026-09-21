# Verification: Takeover admission: the public takeover object, CLI receipts and the minimal manual-transfer payload

Frozen candidate: `bc7ac542e00fa830928882997f02fa1c80ae4e2c`, working tree clean (re-checked by the independent run and again after it).
Verifier: independent QA subagent (Hermes, dispatched 2026-09-21, completed in 304 s with a full report), read-only in the repository, throwaway installs under the host temporary directory; plus the orchestrator's complete default runs under the operating-model constrained path.

## Host capability limitation

- `- limitation:` this host's subagent sessions are capped at a 600 s budget, and analysis-shaped packets have timed out repeatedly this iteration; the pre-chosen focused subset was therefore expressed as a run-shaped harness (`~/.hermes/cache/scratch/vibe-qa-item3.py`) that the independent subagent executed exactly once against the frozen candidate (as a tracked background process, since the harness exceeds the foreground cap). Raw output: `~/.hermes/cache/scratch/vibe-qa-item3.out` (re-read by the orchestrator); transcript: `~/.hermes/cache/delegation/live/deleg_bbdab281/task-0.log`.
- `- complete run:` orchestrator, on the frozen candidate: `python3 -m unittest discover -s tests` => `Ran 98 tests in 42.192s`, `OK`; `/usr/bin/python3 -W ignore::DeprecationWarning -m unittest discover -s tests` => `Ran 98 tests in 41.109s`, `OK` (CPython 3.13.9 and 3.9.6; 96 before this change); `python3 bin/vibe doctor . --format json` => `status: healthy`; `python3 bin/vibe validate-readiness . --brief docs/work-items/20260921-takeover-admission/brief.md --format json` => `status: valid`.
- `- independent focused re-run:` independent QA subagent, pre-chosen subset = the harness's 24 checks (both full lanes, doctor, readiness, two targeted regressions, admission accept/reject probes, receipt byte-stability probes, manual-transfer probes, clean-tree checks) => `VERDICT: 24/24 checks passed`; the frozen hash was verified as HEAD and the repository stayed clean before and after.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Independent probe `1.1`: a healthy throwaway install is admitted through an `existing-install-admission` receipt (exit 0, `status: valid`); the admission binds the current host task, the canonical `project_root` and the recomputed identity (enforced by `2.3`), cites the historical upgrade as an `apply-receipt`/`doctor-receipt` reference with digest (enforced by `2.2`), and claims no transaction in this directory (enforced by `2.1`). Regression `test_existing_install_admission_receipts_and_manual_transfer` green. | Pass |
| AC-2 | Independent probes: a claimed committed transaction is rejected (`2.1`); a missing historical source is rejected (`2.2`); a forged observed fingerprint is rejected (`2.3`); target-content mismatch and any beyond-evidence `upgraded`/`activated`/`ready` claim stay rejected by the pre-existing contract tests, all green on the frozen candidate. | Pass |
| AC-3 | `## Takeover object contract` published in `AGENT_INSTALL.md` (92 lines generated from the compiled registry: per-layer closed field sets, every vocabulary, evidence kinds by stage, required evidence and dependencies per stage, the activation-bindings table, admission rules, custody transitions, the receipt artifact and the transfer payload); `test_agent_install_guide_publishes_the_takeover_contract` asserts every vocabulary value and fails on drift. | Pass |
| AC-4 | Independent probes `4.1`–`4.6`: `--receipt` artifacts written; identical bytes for two runs on the same tree and for two fresh installs under different parent directories; the artifact is root-relative (`target` `"."`) and self-describing (`status` `healthy`); the regression test proves the artifact and the digest a host cites. | Pass |
| AC-5 | Independent probes `5.1`/`5.2`: the conforming minimal payload is accepted (`manual_transfer_status` `valid`, exit 0) and a forged digest is rejected (`invalid`, exit 1); the payload shape, validation rules and disk boundary (custody stays in host task state; the framework never writes goal text) are published in the contract section. | Pass |
| AC-6 | Additive only: no schema or protocol bump; the historical path's tests are unchanged and green; revert is a single commit revert with no data migration; release-identity mirrors regenerated in the same change — 62 recorded checks equal a fresh recomputation (contract activation `3b6864a6…`, payload `f980b5cc…`), including a disposable `init` cross-check. | Pass |
| AC-7 | Frozen candidate: dual lane green (98 tests on CPython 3.13.9 and 3.9.6), `doctor` healthy, `validate-readiness` valid for this brief; both added regression methods cover the admission flows, the receipt artifacts, the transfer payload and the contract drift. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `python3 -m unittest discover -s tests` | Pass | `Ran 98 tests in 42.192s`, `OK` |
| `/usr/bin/python3 -m unittest discover -s tests` | Pass | `Ran 98 tests in 41.109s`, `OK` (CPython 3.9.6) |
| `python3 bin/vibe doctor . --format json` | Pass | `status: healthy` |
| `validate-readiness` for this brief | Pass | `status: valid` |
| Release-identity mirrors | Pass | 62 checks equal a fresh recomputation (contract activation `3b6864a6…`, payload `f980b5cc…`) |
| Focused subset (24 checks, independent) | Pass | `VERDICT: 24/24 checks passed`; raw output re-read by the orchestrator |

## Manual scenarios

- The probes ran as throwaway installs created inside the harness (two fresh `init` projects under different parent directories plus the fixture's controlled objects); the repository stayed clean, and only read-only git commands touched it.

## Limitations and follow-ups

- The QA packet was run-shaped (a pre-chosen harness executed by the subagent); its independence is over execution and reporting on the frozen candidate, not over authoring the checks — the constrained path recorded in `.vibe/core/operating-model.md` and ADR 0017.
- Structural verification only: probes drive the installed CLI against throwaway installs, not downstream repositories; the post-admission continuation (default verification in the admitted directory) is the manual-new-task contract verified by work item `20260921-host-neutral-manual-activation`.
- Receipt byte-stability is proven for healthy receipts across roots; check-output text embedding absolute paths outside the project root is not normalized.
- The dual-lane requirement was exercised here (system CPython 3.9.6); the release work item still owns repeating it against the release candidate.