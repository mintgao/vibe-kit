# Verification: Verification contract closure

Frozen candidate: `d2f079af429825279955c846119fad12f1b4548e`, working tree clean (re-checked after every independent run).
Verifier: independent QA subagent (Hermes, dispatched 2026-09-21; read-only in the repository, throwaway projects under `/tmp`), plus the orchestrator's complete default run under the operating-model constrained path.

## Host capability limitation

- `- limitation:` this host's subagent sessions are capped at a 600 s budget and its lifecycle guard refuses to scan `./bin/vibe` while a subagent runs on the gateway host; the independent QA subagent completed the freeze check, the focused subset and its own acceptance demos, then timed out on the guard while finishing AC-7 and never issued a report. Its evidence is taken from its live transcript and by re-running its own harness (`/tmp/vibe-qa-demo.py`) on the same frozen candidate.
- `- complete run:` orchestrator, on the frozen candidate: `python3 -W ignore::DeprecationWarning -m unittest discover -s tests` => `Ran 96 tests in 40.059s`, `OK` (86 pre-existing plus 7 added here plus the readiness work item's 3); `python3 bin/vibe doctor . --format json` => `status: healthy`, activation `50852b031713…`; `python3 bin/vibe validate-readiness . --brief docs/work-items/20260921-verify-contract-closure/brief.md --format json` => `status: valid`, findings `[]`.
- `- independent focused re-run:` independent QA subagent, pre-chosen subset = the seven new verify-declaration tests plus the whole `test_release_identity` module, run from the repository root where the tests' module imports resolve => `Ran 13 tests in 2.178s`, `OK`; plus its own acceptance demos, re-executed on the same candidate (below).

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Independent demo: with no declaration the receipt records `default_order ["lint","typecheck","test","build"]`; with `checks.requires: {test: ["build"]}` the effective order is `["lint","typecheck","build","test"]` and exit code 0; a dependency cycle fails closed with `checks.requires contains a dependency cycle among: test, build`; an unknown key fails closed with `checks must only declare requires, output_limit_bytes`. `test_verify_declared_check_order_is_derived_and_recorded` and `test_verify_check_declaration_fails_closed` green. | Pass |
| AC-2 | Independent demo: a 17 KB failing output has `stdout_truncated true`, the verdict line present in the referenced `.vibe/local/verify/*.log` and absent from `stdout_tail`, and the recorded `sha256` equals the file's bytes under three independent computations (python hashlib, `shasum`, the receipt). `test_verify_failing_check_keeps_a_recoverable_full_output_artifact` and `test_verify_declared_raise_of_the_output_bound_is_honoured` green. | Pass |
| AC-3 | Operating model section `Constrained runs when the host's subagent budget is smaller than the lane` states the path and the three record labels; `test_operating_model_states_the_constrained_path_and_record_labels` binds the prose; this record itself uses the path and its labels on this work item's own lane. | Pass |
| AC-4 | Independent demo: a declared unmet `toolchain: {python: ">=99.0"}` with a failing check records `environment-limited` + `toolchain-mismatch`, preserves exit code 4, carries expected `>=99.0` / observed `3.13.9`, and yields `status blocked` with exit code 2 and `summary["environment-limited"] == 1`; the passing checks stay `passed`; the receipt records `toolchain {python: 3.13.9, node: v22.22.3, pnpm: 12.5.1}`. `test_verify_environment_limited_outcome_carries_reason_and_toolchain` green. | Pass |
| AC-5 | Independent demo: the repository and a freshly installed `agent-install.json` both list `environment-limited` in `cli.verify.outcomes`; mutated copies with an unknown status, an unknown outcome and an unknown skipped reason each produce exactly one `agent install verify contract is unsupported` error, so the closed discipline still rejects drift. | Pass |
| AC-6 | Independent demo: an undeclared project records `default_order ["lint","typecheck","test","build"]` unchanged; the change is additive and reverts by restoring the previous tree, with no data migration. | Pass |
| AC-7 | Complete default lane `Ran 96 tests in 40.059s`, `OK` on the frozen candidate; `doctor` healthy; `validate-readiness` valid; every behavior change carries a regression test in `tests/` (standard-library `unittest`). | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `python3 -W ignore::DeprecationWarning -m unittest discover -s tests` | Pass | `Ran 96 tests in 40.059s`, `OK` (89 before this change) |
| `python3 bin/vibe doctor . --format json` | Pass | `status: healthy`, activation `50852b031713…` |
| `validate-readiness` for this brief | Pass | `status: valid`, findings `[]` |
| Release-identity mirrors | Pass | payload `abf5e430…`, activation `50852b03…`; 64 recorded mirrors equal a fresh recomputation, including a disposable `init` cross-check and the installed contract admitting `environment-limited` |
| Focused subset (13 tests: 7 new plus `test_release_identity`) | Pass | `Ran 13 tests in 2.178s`, `OK` (independent subagent) |

## Manual scenarios

- The independent demos listed under the acceptance criteria ran as throwaway `/tmp` projects created by the QA subagent's harness (`/tmp/vibe-qa-demo.py`), re-executed by the orchestrator on the same frozen candidate; the repository stayed clean throughout.

## Limitations and follow-ups

- The independent QA subagent delivered no report (600 s budget, then the lifecycle guard); its evidence is salvaged from its live transcript and from re-running its own harness — the host limitation this record already names.
- Structural verification only: the demos drive the installed CLI against throwaway projects, not against downstream repositories.
- The lane ran on CPython 3.13.9; no 3.9 interpreter is installed on this host, so the release work item still owns the CPython 3.9/3.13 dual-lane requirement.
- Date-named decision records still carry no ordering key; that remains the readiness work item's recorded follow-up and is unaffected here.