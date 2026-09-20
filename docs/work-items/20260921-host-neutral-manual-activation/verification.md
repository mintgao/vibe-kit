# Verification: host-neutral manual new-task activation and consistent release identity

- Status: verified with one pending surface; AC-1 and AC-2 are unmet on the managed `AGENTS.md` block only
- Date: 2026-09-21 (Asia/Shanghai)
- Independent QA: bounded Hermes QA subagent, separate from the implementation writer; it edited no file and wrote its outputs under `/tmp`
- Candidate: parent commit `87225de33bdea321257f4723aa60e1f506f2e167`, working tree digest `262fd6421a341dda816c76ff397ea4a8b17aab005c3b9626fe60aa8b6f39a97a` (this record is written after that freeze and is therefore outside the verified digest)
- Gate: ADR 0015 Accepted; independent Tech Lead review approved on revision 2

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | `AGENT_INSTALL.md` no longer hard-codes a schema number and `README.md` states schema 2, but the managed `AGENTS.md` block still reads "takeover schema 1" while the installed contract declares `takeover.schema_version: 2`. QA verified the block by its own read; the block's regression check self-skips with the pending-surface reason. | Fail (partial) |
| AC-2 | QA grep confirmed host-neutral wording on six surfaces (`AGENT_INSTALL.md`, both homepages, `bin/vibe`, both Plugin Skills), but the managed `AGENTS.md` block still reads "create a new Codex task in the same project"; its regression check self-skips for the same recorded reason. | Fail (partial) |
| AC-3 | `AGENT_INSTALL.md` states the manual path is host-neutral, that any host which can start a new task in the same project may own the successor task, that `adapter` metadata and the activation fingerprint describe the installing host, that receipt requirements are unchanged, and that a host which cannot recompute the installed identities must take the degraded stop. `tests/test_release_identity.py::test_installed_contract_states_the_host_neutral_manual_path` passes. | Pass |
| AC-4 | No schema, protocol, enum, validator, receipt or CLI-result code was touched: takeover schema 2, agent-install schema/protocol 3/3 and core/adapter protocol 7 are unchanged, the closed 18-key contract field set and the adapter capability claims are unchanged, `bin/vibe`'s diff is two prose strings, and `validate-takeover` still rejects a malformed object. | Pass |
| AC-5 | `./bin/vibe package --output /tmp/vk-qa-release` exits 0 with 36 payload files; `validate-release` returns `valid` with `payload_tree_sha256=96ad3f14…f1ae` and `activation_set_sha256=5993719c…b9b0`; QA's own recomputation matches the Plugin manifest and both `.vibe/manifest.json` mirrors; the three identity regression tests pass. | Pass |
| AC-6 | `CHANGELOG.md` contains the `## 0.9.0 — 2026-09-07` section with the release entries. | Pass |
| AC-7 | Default lane `OK (skipped=2)` on CPython 3.13.9 and 3.9.6 (86 tests each); `doctor` `healthy` with activation `match` and no diagnostics; `validate-readiness` `valid` with no findings. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `./bin/vibe verify . --format json` | passed | The one canonical default run, executed once by QA on the frozen candidate: `failed=0`, `passed=1` (test lane, 86 tests, `OK (skipped=2)`), `unconfigured=3` (lint, typecheck, build). |
| `python3 -m unittest discover -s tests` (3.13.9) | passed | 86 tests, `OK (skipped=2)`. |
| `/usr/bin/python3 -m unittest discover -s tests` (3.9.6) | passed | 86 tests, `OK (skipped=2)`, no failures or errors. |
| `./bin/vibe package` + `validate-release` | passed | Candidate built; nested validation `valid`. |
| `./bin/vibe doctor . --format json` | healthy | Activation match `5993719c…b9b0`, no diagnostics or warnings. |
| `./bin/vibe inspect-managed-agents . --format json` | valid | Managed span 0–6913 authenticated against the manifest block hash. |
| `./bin/vibe validate-readiness …/brief.md --format json` | valid | No findings. |
| `git diff --check` | clean | No whitespace errors. |

## Manual scenarios

- None recorded beyond the automated checks above; no live host activation was performed.

## Pending surface

The managed `AGENTS.md` block is unchanged. The host refused the write and reported that the user had not consented, forbidding a retry through another path, so AC-1 and AC-2 remain unmet for that single surface. The exact replacement paragraph is recorded in `implementation.md` and in the brief's design notes. After an approved write, the activation identity and the payload digest must be regenerated again (both change with the block), `tests/test_release_identity.py`'s two self-skipping subtests will run instead of skipping, and this record's AC-1/AC-2 rows must be re-verified.

## Limitations and follow-ups

- No live host activation and no non-Codex host were exercised. The host-neutral permission is contract prose, not live conformance evidence; a receipt still requires the host to recompute the installed identities, and `validate-takeover` acceptance remains structural only.
- AC-4 rests on the changed-file scope, unchanged declared schema/protocol numbers and the suite results, not on an A/B byte comparison against the parent commit.
- The full valid takeover-object set was not reconstructed; coverage is the repository suite plus one malformed-object rejection probe.
- Follow-up: the managed block write (AC-1/AC-2), then identity regeneration and re-verification in the same change.
