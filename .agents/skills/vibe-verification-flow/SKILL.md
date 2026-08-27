---
name: vibe-verification-flow
description: Independently test a change, acceptance criteria, or release candidate and produce criterion-to-evidence results without silently fixing failures.
---

# Verification flow

1. When independent verification benefits from delegation, use `vibe_qa`. Read the acceptance criteria, changed behavior, relevant project context, diff, and the work item's technical-decision readiness evidence under `.vibe/core/technical-decision-readiness.md` when applicable.
2. Build a risk-based verification set covering the main path plus important negative, boundary, state, permission, accessibility, and regression cases that apply. Verify that implementation stayed inside the accepted technical boundary; do not use post-implementation QA as a substitute for missing readiness evidence.
3. Run focused tests and `./bin/vibe verify` when configured. Do not claim a check was run if the environment prevented it.
4. For each acceptance criterion, record evidence and one of: Pass, Fail, Blocked, or Not applicable. For readiness behavior, distinguish deterministic artifact/distribution checks from live Agent or host scenarios; static string assertions are not evidence that an Agent actually stopped or routed correctly.
5. Report defects with reproduction steps, expected versus actual behavior, severity, evidence, and relevant file references.
6. Update the work item's `verification.md` when one exists. Do not edit application code during the independent evaluation unless the user explicitly changes the task to fixing defects.

The final conclusion must distinguish verified behavior from inference and list skipped checks and residual risk.
