# Verification: Agent-first Vibe Kit adoption

- Verified: 2026-08-27
- QA perspective: independent `vibe_qa`
- Evaluated state: integrated 0.5.0 candidate including the completed Technical Decision Readiness Gate
- Conclusion: **Pass with explicit live-host limitations.** No code or release-contract defect remains. AC-7 and AC-8 retain Partial evidence because a fresh real Codex task and live Plugin host were not exercised in this final pass.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | README first screen uses only natural-language existing/new-project examples, then ordinary development requests; CLI details are secondary maintainer material. | Pass |
| AC-2 | Packaged human/machine contracts define the Codex-scoped source, target, plan, apply, doctor, handoff, onboarding, success and blocking state machine, including stable-only bare repository policy and one explicit pre-release decision. | Pass |
| AC-3 | Source, release ZIP, Plugin payload and expanded marketplace copies of both Agent contracts have identical SHA-256 values; missing, malformed, version-drifted, enum-drifted and channel-drifted contracts fail validation. | Pass |
| AC-4 | Safe/blocked/error plans, install success/error, upgrade success/blocked/error, doctor healthy/warning/broken/error and release valid/invalid/error are closed structured states. Default text output and established exit semantics retain regression coverage. | Pass |
| AC-5 | Valid source type/ref/digest is recorded in receipt and manifest. Invalid moving refs/digests fail with `write_state=none` before target creation. Local development remains `local-payload`. | Pass |
| AC-6 | Fresh init/adopt creates pending onboarding; a legal pre-existing complete file is preserved byte-for-byte and both receipt/doctor report complete. Invalid or incomplete complete state is broken/invalid. | Pass |
| AC-7 | Installed AGENTS/onboarding Skill statically require automatic evidence-backed onboarding and resumption of the original request without user-visible Skill vocabulary. A fresh live Codex task was not run. | Partial |
| AC-8 | Artifact and Plugin wrapper structured plan/init/doctor paths passed; bootstrap/maintain remain the only Plugin capabilities. Redundant-confirmation and new-task fallback behavior were not exercised in a live Plugin/Codex session. | Partial |
| AC-9 | Business/project-owned files, repository-specific AGENTS content, offline installation, conflict evidence, version integrity, release/Plugin tamper rejection, and readiness workflow distribution all pass regression coverage. | Pass |
| AC-10 | 0.5.0/version/protocol/Plugin/changelog/release/context are synchronized; full tests, verify, bytecode compilation, release validation, independent QA and controlled self-upgrade/root doctor pass. Linux, Python 3.9 and live hosts are reported as skipped rather than inferred. | Pass |

## Automated and artifact checks

| Check | Result | Evidence |
|---|---|---|
| Focused Agent-first and repair scenarios | Pass | 12/12. |
| Full unittest suite | Pass | 31/31. |
| `./bin/vibe verify .` | Pass | Configured suite 31/31. |
| Python bytecode compilation | Pass | `bin/vibe`, `tests/test_cli.py`, and `tests/test_workflow_contract.py`. |
| Patch hygiene | Pass | `git diff --check` produced no output. |
| Unpublished 0.5.0 candidate | Pass | `validate-release --format json`: valid, 35 payload files, `network_used=false`. |
| Release/Plugin install smoke | Pass | Artifact init+doctor healthy; adopt preserved legal complete state; Plugin plan/init/doctor healthy. |
| Cross-channel identity | Pass | Two Agent contracts match across source, release ZIP, Plugin payload and marketplace; 35 manifest payload entries have zero mismatch. |
| Fail-closed contract | Pass | Unknown command/write/onboarding enums, invalid complete requirements and unsafe schema evolution are rejected. |
| Write truth | Pass | Conflict reports `conflict-evidence-written`; preflight ref error reports `none`; injected post-mutation filesystem failure reports `unknown-partial`, no traceback and explicit inspection recovery. |
| Controlled self-upgrade | Pass | Safe plan contained 24 no-op managed entries and two installation-state updates; upgrade succeeded without managed content changes; root doctor is healthy at 0.5.0 with complete onboarding. |

## Process evidence

- Implementation began before the Technical Decision Readiness Gate landed concurrently. The work item truthfully records late adoption and does not claim pre-implementation compliance.
- After QA exposed the timing gap, shared-code repair paused. ADR 0007 was amended, independently approved, Accepted, and confirmed `implementation-ready` before repair resumed.
- The separately completed readiness-gate iteration is integrated through the same 0.5.0/core protocol 3 candidate and retains its own Accepted ADR 0008 and independent verification.

## Limitations and follow-ups

- Real Linux and Python 3.9 were not run in this final environment; release status remains Pre-release.
- No fresh real Codex task, live Plugin installation, non-Codex adapter, or sequential-only host was exercised. Static/distribution evidence is not presented as live-host proof.
- Init/adopt/upgrade are not whole-directory transactions. Post-mutation failures report conservative `unknown-partial` recovery. The separate permission-safe atomic-upgrade work item remains shaped and unimplemented.
- SHA-256 proves artifact/content consistency but is not an external publisher signature or independent provenance attestation.
