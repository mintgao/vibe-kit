---
name: vibe-feature-flow
description: Deliver a new feature or end-to-end behavior change from problem framing through design, implementation, and independent verification.
---

# Feature flow

Use `.vibe/core/operating-model.md` to classify the work and apply
`.vibe/core/technical-decision-readiness.md` before implementation.

- For S work, confirm the behavior and scan for readiness triggers. Implement directly only when it remains clear, local, reversible, and low risk; otherwise reclassify it before editing.
- For M/L work, create a work item with `./bin/vibe work-item <slug> --size <M|L>` if one does not exist.
- Delegate to `vibe_pm` to establish goal, scope, non-goals, and testable acceptance criteria when shaping is needed.
- Delegate to `vibe_ux` when user flow or interface behavior changes and independent design judgment is useful.
- Treat product-shaped and implementation-ready as separate states. After shaping, scan size, risks, open decisions, relevant architecture, and governing decisions; record the required readiness outcome for M/L work.
- When a decision or review is required, route a read-only `vibe_tech_lead` author pass, persist its exact proposal, and use a different Tech Lead instance for required native review. Follow the core sequential-perspective fallback when independent subagents are unavailable.
- The orchestrator confirms `implementation-ready` only when the core release conditions are complete. While blocked, do not edit application/shared code; return the single next decision or review handoff and ask the user only for material product choices.
- Record only decisions that affect implementation or acceptance; do not create empty phase documents or ceremonial ADRs.
- Use one `vibe_rd` writer to implement the accepted scope, governing decision boundary, and appropriate tests only after the gate is ready.
- If implementation discovers a new durable/high-risk choice, stop the affected edit, reopen readiness, and complete the decision/review path before resuming.
- After implementation, delegate an independent pass to `vibe_qa` for M/L work and update the work item's `verification.md` with criterion-to-evidence results.

Delegate PM, UX, exploration, or QA work when independent analysis materially improves an M/L task. Parallelize read-heavy work only when the parts are genuinely independent, wait for requested results, and synthesize them before implementation. Ask the user only for decisions that would materially change the result.

Close with changed behavior, evidence, skipped checks, risks, and follow-ups. Update durable context only if the project truth changed.
