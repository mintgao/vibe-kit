# Verification: Self-hosting pilot

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Self-adoption created `.vibe/manifest.json` with 17 matching managed-file hashes and a matching AGENTS block hash; `.vibe/version` and core version are `0.1.0`. Existing context remained in place. External-target adoption tests and an independent temporary scenario preserved business and project-owned files. | Pass |
| AC-2 | `./bin/vibe doctor .` exited 0 with `0 warning(s)` after adoption, onboarding updates, and a no-op self-upgrade. | Pass |
| AC-3 | `./bin/vibe verify .` passed all 6 scenario tests. The same suite and a direct syntax compile also passed under `/usr/bin/python3` 3.9.6. | Pass |
| AC-4 | Independent comparison of `docs/context/` against `bin/vibe`, repository structure, and tests found the documented v0.1 capabilities and limits supported by evidence. The ownership model was clarified to include tool-maintained installation state. | Pass |
| AC-5 | A separate read-only QA agent mapped AC-1 through AC-5 to evidence and identified residual coverage and diagnostic gaps. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `./bin/vibe doctor .` | Pass | 0 errors, 0 warnings |
| `./bin/vibe verify .` | Pass | 6 tests passed |
| Python 3.9 compile and test run | Pass | 6 tests passed with `/usr/bin/python3 -B` |
| Manifest integrity | Pass | 17 managed files, AGENTS block, and versions matched |
| `./bin/vibe upgrade .` | Pass | Same-version no-op; 0 managed files updated, doctor remained clean |

## Manual scenarios

- Independent QA repeated adoption against a temporary external project containing pre-existing project configuration, rules, context, work items, decisions, business code, and custom AGENTS content; those project-owned inputs were preserved.
- Repository context was compared with the CLI entry point and scenario tests to distinguish implemented behavior from plans.

## Limitations and follow-ups

- The repository has no initial commit or pre-adoption snapshot, so preservation in the actual self-adopt cannot be proven with a historical diff.
- Self-adoption uses identical source and target paths, so `atomic_copy` skips cross-directory copying. External-target scenario tests remain necessary evidence for copy and permission behavior.
- The automated adoption test asserts business-code and AGENTS preservation but does not yet pin preservation of pre-existing `.vibe/project.yaml`, `.vibe/project-rules.md`, and `docs/context/`; add those assertions in a later change.
- `doctor` does not currently fail or warn when `.vibe/version` is missing or inconsistent with the manifest and core version. Add version-state diagnostics and regression tests in v0.2.
