---
name: vibe-debug-flow
description: Investigate a bug, incident, flaky test, performance regression, or unexplained behavior before implementing and verifying a fix.
---

# Debug flow

Follow evidence before edits.

1. Establish expected and observed behavior, impact, environment, frequency, and the smallest reproducible case.
2. Delegate evidence gathering to `vibe_investigator` when an independent read-only investigation is useful. Inspect code, tests, logs, history, and state; separate facts, hypotheses, eliminated causes, and missing evidence.
3. Confirm the likely root cause with a discriminating test or observation when feasible.
4. If the user asked only for diagnosis, stop with the evidence-backed cause and proposed next step.
5. If the user asked for a fix, classify the fix and apply `.vibe/core/technical-decision-readiness.md` before the first code edit. For M/L work, scan whether the fix introduces or changes a durable/high-risk boundary; root-cause confirmation alone does not release implementation.
6. When readiness is blocked, route the required read-only `vibe_tech_lead` decision and review passes and stop before editing application/shared code. Follow the core sequential-perspective fallback when native subagents are unavailable.
7. Only after the orchestrator confirms readiness, hand the confirmed cause and accepted technical boundary to one writer, optionally `vibe_rd`, add regression coverage, and keep the patch narrowly tied to the cause. Reopen the gate if implementation discovers a new durable/high-risk choice.
8. Use `vibe_qa` for an independent pass to rerun the reproduction and relevant regressions when the risk warrants it.

For M/L incidents, create or update a work item. Record root cause, evidence, fix, regression coverage, skipped checks, and follow-ups. Do not present temporal correlation or a plausible code path as proven causation.
