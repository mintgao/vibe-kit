# 0017: Verification contract closure — declared check order, diagnostic receipts, an environment-limited verdict, and a sanctioned path for hosts whose subagent budget is smaller than the lane

- Status: Accepted
- Date: 2026-09-21
- Decision owner: read-only Tech Lead author `vibe_tech_lead`
- Work item: `docs/work-items/20260921-verify-contract-closure/brief.md`
- Evidence: feedback issues #9 and #13 (findings F6, F10, F11), the DSH Desktop Mint migration of 2026-09-18, and the verify surface in bin/vibe

## Context and applicable decisions

The verify surface closes four gaps that the recorded evidence names explicitly.

#9 is order. The lane runs `lint → typecheck → test → build` as a fixed sequence, and any repository whose `test` consumes build artifacts therefore runs its tests against a tree the build step has not yet populated. On a clean tree that is a false negative that reads as a real failure, and no declaration can correct it: the order lives in the tool, not in the repository it judges.

F6 is diagnosis. Each check's output is retained as a 16 KB tail plus the flag that marks truncation. A failure whose cause sits earlier in the output is unrecoverable from the receipt, so an operator re-runs the check by hand to learn what the receipt already saw.

F11 is environment limits. A verdict that turns on the host environment — a toolchain version the host does not carry, a capability the host cannot provide — has no state of its own. It is forced into `passed`, where it overstates coverage, or into `failed`, where it misnames the cause and invites a spurious repair task.

F10 is the host-budget gap, recorded during the DSH Desktop Mint migration of 2026-09-18: a host whose subagent budget exists but cannot cover the full verification lane has no compliant record. The operating model requires an independent re-run, the existing fallback covers only hosts without subagents, so an orchestrator on a small-budget host either exceeds its budget or quietly drops the independent evidence.

ADR 0008 governs readiness authority, ADR 0012 governs capability honesty in the operating model, and ADRs 0002 and 0011 pin the offline trust model. This record closes the verify contract under those decisions and changes none of them.

## Decision: check order becomes declared, not hardcoded

`.vibe/project.yaml` may declare check dependencies or an order. The effective order is derived deterministically from that declaration, and the verify receipt keeps describing the effective order, so a reader never has to infer it from the check list.

The declaration is validated fail-closed. An unknown check name, an unknown key, or a dependency cycle fails with an actionable message that names the offending entry. A repository that declares nothing keeps today's `lint → typecheck → test → build` behaviour unchanged, so the default is not a special case of the new path but the degenerate form of it.

## Decision: receipts preserve the output needed to diagnose a failure

Per-check output preservation becomes configurable. The default does not downgrade below today's behaviour — the 16 KB tail and its truncation flag remain the floor, never less.

A failed check's per-file verdicts must be recoverable from the receipt itself or from a referenced full-output artifact on disk, addressed by path plus digest. A reader given only the receipt can therefore arrive at the same per-file verdicts the check reached, without re-running the check and without trusting a mutable file: the digest is what binds the referenced artifact.

## Decision: a verdict that depends on the host environment gets a recordable state

Environment-limited coverage is a distinct outcome, separate from passed, failed, unconfigured, and skipped. It requires a reason and the toolchain versions that produced the verdict — for example node, pnpm, and python as they existed on that host at that moment.

Publication and closeout treat environment-limited coverage as not passing. The state is a diagnostic honesty, not an escape hatch: it cannot be used to avoid a real failure, because anything a check actually failed stays failed.

## Decision: a sanctioned path when the host's subagent budget is smaller than the lane

The operating model gains a compliant procedure for a host whose subagent budget cannot cover the verification lane. The orchestrator runs the complete default verification. An independent bounded subagent re-runs a focused subset, chosen in advance, of that same lane. The work item records the capability limitation in a machine-checkable form.

The existing fallback covers only hosts without subagents; a host whose subagents exist but cannot finish the lane had no compliant record at all, and this decision supplies it. Independence is preserved where the budget allows it: the focused subset is re-run by a subagent that did not produce the orchestrator's result.

## Alternatives weighed

- Hardcoding `build` before `test`. Rejected: correct for one stack and arbitrary for every other, and it would silently reorder lanes for repositories whose checks have no such dependency.
- Inferring order from file names or from check outputs. Rejected: the inferred order cannot be audited, so a misreport on a clean tree could not be attributed to the inference rather than to the code under test.
- Reusing `skipped` for environment limits. Rejected: `skipped` means no verdict was reached, and an environment-limited check is a verdict that was reached and found not applicable on this host. Collapsing the two hides which one happened.
- Giving the orchestrator the whole lane with no independent re-run. Rejected: it removes the independent evidence the operating model requires, and the limitation would be invisible rather than recorded.

## Consequences and boundaries

The change is additive to the verify receipt and to `.vibe/project.yaml`. No version bump is made here; the release work item owns version and profile bumps.

Historical 0.7–0.9 receipts keep their recorded semantics and are never rewritten. A receipt produced under the earlier contract still means what it said when it was written, including its 16 KB tails and its absence of the environment-limited state.

The closed verify declaration in `agent-install.json` must match the new semantics: it keeps rejecting unknown statuses, unknown outcomes, and unknown skipped reasons, and it now admits the environment-limited state under the same closed discipline.

The repo-pinned offline trust model of ADRs 0002 and 0011 is untouched: no network access, no remote attestation, and no change to how a pinned installation resolves its source. The change is revertible with no data migration — remove the declaration and restore the defaults, and the lane returns to the previous contract.

## Verification

The claim of this record is checked in both directions. A repository that declares nothing must produce byte-for-byte the previous default order and receipt shape, proving the default path was not disturbed. A repository whose `test` consumes build artifacts must, with the declaration present, run in the declared order and record that effective order in its receipt. A failed check with a truncating output must have its per-file verdicts recoverable from the receipt or from the referenced artifact, and the referenced digest must match the bytes on disk. An environment-limited verdict must require a reason and toolchain versions, and must be treated as not passing by publication and closeout.

Negative cases must keep failing: an unknown check name, an unknown key, a dependency cycle, an unknown status, an unknown outcome, and an unknown skipped reason each fail closed with an actionable message.

## Follow-ups out of scope

- Version and profile bumps, which belong to the release work item.
- Any rewrite, migration, or reinterpretation of historical receipts.
- Any change to the repo-pinned offline trust model or to how a pinned installation resolves its source.
- Any relaxation of the closed verify declaration in `agent-install.json` beyond admitting the environment-limited state.