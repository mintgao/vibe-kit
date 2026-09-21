# Verification: host-neutral manual new-task activation and consistent release identity

- Status: verified; AC-1..AC-7 pass on the final candidate
- Date: 2026-09-21 (Asia/Shanghai)
- Independent QA: bounded Hermes QA subagents, separate from the implementation writer; they edited no repository file and wrote their outputs under `/tmp`. One earlier QA session ran the full check set on the pre-block candidate and its session ended at the 600 s host budget before it composed a report; its raw transcript is the evidence for that pass. Two further bounded QA sessions completed and are quoted below: one owned the canonical default run, one verified contract text, identity mirrors and regression-test enforcement.
- Candidate: parent commit `87225de33bdea321257f4723aa60e1f506f2e167`; final working tree digest `889fbdcfe312ec3fbebf63757bcf13b531c37a885d41c90ad41df5ad45529170`, unchanged before and after every QA command (this record is written after that freeze and is therefore outside the verified digest).
- Gate: ADR 0015 Accepted; independent Tech Lead review approved on revision 2.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | No managed surface states a conflicting takeover schema number. QA read the managed `AGENTS.md` block: it references "the takeover schema they declare" and contains no hard-coded number; repo-wide `takeover schema <n>` hits are historical changelog entries and decision/work-item records. Mutation: replacing that phrase with `takeover schema 1` fails `test_takeover_schema_references_agree_with_the_installed_contract` (isolated run: `Lists differ: ['1'] != []`). | Pass |
| AC-2 | All seven surfaces (`AGENTS.md`, `AGENT_INSTALL.md`, both homepages, `bin/vibe`, both Plugin Skills) contain zero occurrences of "Codex task" or "Codex 任务"; `AGENTS.md` and `AGENT_INSTALL.md` carry "create a new task in the same project" and "host-neutral". Mutation: restoring "new Codex task" in `AGENTS.md` fails `test_manual_fallback_action_is_host_neutral`; no `skipTest` guard remains in the test module. | Pass |
| AC-3 | `AGENT_INSTALL.md` states the manual path is host-neutral, that any host which can start a new task in the same project may own the successor task, that `adapter` metadata and the activation fingerprint describe the installing or adopting host and never restrict the successor, that receipt requirements are unchanged, and that a host which cannot recompute the installed identities must take the degraded stop. Its regression test passes. | Pass |
| AC-4 | No schema, protocol, enum, validator, receipt, custody or CLI-result change. QA diffed against `HEAD`: `agent-install.json` changes one `activation_set_sha256` value, `AGENTS.md` one prose paragraph, plus tests and work-item docs; `bin/vibe` is byte-identical to `HEAD` for the contract logic. `validate-takeover` still returns `invalid` with `ready_claim: false` for malformed input and for a `schema-99` object, and a fixture-host valid object validates identically under the candidate and the parent CLI. | Pass |
| AC-5 | Three-way agreement, recomputed independently by QA: `payload_tree_sha256(ROOT) = 6d6c8e275d6f47cc653d5465384c07aab83e0882656dd58b7a77acf9e43b1e76` equals the Plugin manifest and `.vibe/manifest.json#source`; `activation_set_sha256 = db8c95b7bfab0003247b5068d92daad45d98c73d4a2b186d427579910553fc30` equals `agent-install.json#activation` and the manifest. `./bin/vibe package` exits 0 with 36 payload files and `validate-release` returns `valid`; the manifest's `agents_block_hash` and `managed_files['agent-install.json']` match the recomputed values. | Pass |
| AC-6 | `CHANGELOG.md` contains `## 0.9.0 — 2026-09-07` with the release entries, and `kit_version` is `0.9.0`. This change's own release note belongs to the next release preparation, as ADR 0015 states. | Pass |
| AC-7 | Default lane `OK` with **no skips** on CPython 3.13.9 and 3.9.6 (86 tests each); `./bin/vibe verify . --format json` `passed`; `doctor` `healthy` with activation `match` and no diagnostics; `validate-readiness` `valid` with no findings. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `./bin/vibe verify . --format json` | passed | The one canonical default run for this candidate, executed by the bounded QA session: `status=passed`, `selection=all-configured/default`, `summary failed=0 passed=1 skipped=0 unconfigured=3`, test check tail `Ran 86 tests in 37.297s` / `OK`. |
| `python3 -m unittest discover -s tests` (3.13.9) | passed | 86 tests, `OK`, no skips. |
| `/usr/bin/python3 -m unittest discover -s tests` (3.9.6) | passed | 86 tests, `OK`, no skips. |
| `./bin/vibe package` + `validate-release` | passed | Built with 36 payload files; nested validation `valid` with digest `6d6c8e27…1e76`. |
| `./bin/vibe doctor . --format json` | healthy | Activation match `db8c95b7…fc30`, `differing_paths: []`, no diagnostics or warnings. |
| `./bin/vibe inspect-managed-agents . --format json` | valid | Managed span 0–7123 authenticated against the manifest block hash. |
| `./bin/vibe validate-readiness …/brief.md --format json` | valid | No findings. |
| `git diff --check` | clean | No whitespace errors. |

## Regression-test enforcement (mutation evidence)

The first QA pass found the pre-approval skip guard failed open. The guard is gone and the checks carry positive assertions. Verified to fail the suite after hardening: `AGENTS.md` regaining "new Codex task"; `AGENTS.md` hard-coding `takeover schema 1`; the host-neutral clause removed from `AGENTS.md`; `bin/vibe` printing "Codex task"; the bootstrap Skill regaining "Codex task". The second QA session reproduced two of these independently on a `/tmp` copy and confirmed the module passes on the restored copy with `AGENTS.md` byte-identical to the repository.

## Manual scenarios

- None recorded beyond the automated checks above; no live host activation was performed.

## Limitations and follow-ups

- No live host activation and no non-Codex host were exercised. The host-neutral permission is contract prose, not live conformance evidence; a receipt still requires the host to recompute the installed identities, and `validate-takeover` acceptance remains structural only.
- AC-4 rests on the changed-file scope, unchanged declared schema/protocol numbers, a `HEAD` diff and the suite results, not on an exhaustive A/B comparison of every command path.
- The full valid takeover-object set was not reconstructed; coverage is the repository suite, a fixture-host valid object differential, and malformed plus `schema-99` rejection probes.
- The verify lane's test step invokes the `PATH` `python3`; the CPython 3.9 evidence therefore rests on direct interpreter runs of the same suite.
- The earlier QA session that exceeded the host's 600 s budget is recorded as such: its checks ran, but the session produced no composed report, and only its raw transcript is available.
- Follow-ups out of scope here: publishing the takeover object schema (F2), a receipt helper (F7), a minimal manual transfer payload (F12), host capability limitation recording for bounded subagents (F10), an environment-limited check state (F11), configured-check ordering (issue #9), and this change's release note in the next release preparation.
