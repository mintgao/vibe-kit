# Verification: Vibe Kit v0.2 — Installation state trust

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Root `./bin/vibe doctor .` returned 0 with `Version integrity: OK (0.2.0)`, 0 warnings, and empty stderr; all three stored versions are `0.2.0`. | Pass |
| AC-2 | Automated and independent temporary scenarios removed or emptied `.vibe/version`; both returned 1, listed installed/manifest/core states plus trusted-checkout upgrade and rerun commands, and left the file snapshot unchanged. | Pass |
| AC-3 | Independent QA ran 11 negative states: installed missing/empty/mismatch; manifest missing/file damaged/field missing/empty/mismatch; core missing/empty/mismatch. Every scenario returned 1 rather than 2, showed one aggregate three-source diagnostic, raised no traceback, and was read-only. | Pass |
| AC-4 | `test_adopt_preserves_existing_project_and_detects_stack` asserts byte-for-byte preservation of project config, rules, three context files, work/decision indexes, business code, and existing AGENTS content while installing managed assets. | Pass |
| AC-5 | `test_upgrade_updates_managed_files_and_preserves_project_files` constructs a 0.1 installation, upgrades from a 0.2 source, preserves rules/context, updates managed content, aligns all three versions at `0.2.0`, and passes the installed target's doctor. | Pass |
| AC-6 | Warning regression remains exit 0/stdout-only; managed conflict regression remains exit 2 with no partial update and conflict candidates; failed doctor scenarios passed before/after byte snapshots. | Pass |
| AC-7 | Root doctor and verify passed. Nine scenario tests and `py_compile` passed with macOS `/usr/bin/python3` 3.9.6 after directing bytecode cache to `/private/tmp`; independent QA also passed 9/9 on Python 3.11.15 and 3.14.6 plus Python 3.9 grammar parsing. | Pass |
| AC-8 | README and product/architecture context describe only delivered v0.2 behavior and retain offline limits. Independent search found no network fetch, Plugin, package, `adopt --plan`, provenance, or adapter implementation; distribution artifacts explicitly start at v0.3+. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `./bin/vibe upgrade .` | Pass | Self-upgrade aligned manifest, installed version, core version, and managed hashes at `0.2.0`. |
| `./bin/vibe doctor .` | Pass | Version integrity OK; 0 warnings. |
| `./bin/vibe verify .` | Pass | Configured test command passed 9/9 scenarios. |
| `/usr/bin/python3 -m py_compile bin/vibe tests/test_cli.py` with `PYTHONPYCACHEPREFIX=/private/tmp/vibe-kit-pycache` | Pass | Actual Python 3.9.6 syntax/bytecode check. |
| `/usr/bin/python3 -m unittest discover -s tests -v` with the same cache prefix | Pass | Actual Python 3.9.6 passed 9/9 tests. |
| Independent Python 3.11.15 and 3.14.6 runs | Pass | 9/9 tests on both; QA did not modify files. |
| Independent 11-state doctor matrix | Pass | All exit 1, aggregate status, repair guidance, and read-only snapshots. |

## Independent QA conclusion

- No functional or release-blocking defect found.
- Distribution brief/design/ADR are internally consistent with the repo-scoped Skills, installable Plugin, and AGENTS discovery boundaries reviewed from official OpenAI documentation.
- No distribution implementation was included in the v0.2 managed payload.

## Limitations and residual risk

- The first Python 3.9 `py_compile` attempt could not write macOS's default user cache because of the sandbox. It was rerun successfully with a task-specific cache under `/private/tmp`; this was an environment retry, not a skipped check.
- The 0.1→0.2 regression fixture constructs a 0.1 state by changing the copied core version, rather than unpacking an immutable historical 0.1 release artifact. A real historical-payload fixture belongs in the v0.3 release pipeline.
- Only macOS was executed. Linux and Windows distribution matrices are not v0.2 commitments; v0.3 proposes macOS/Linux release coverage and requires an explicit Windows decision.
- No GitHub Release, checksum, Plugin, marketplace, remote update, rollback, or non-Codex adapter was built or tested in v0.2.
