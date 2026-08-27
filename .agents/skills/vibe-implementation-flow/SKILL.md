---
name: vibe-implementation-flow
description: Implement an already specified requirement, design, or technical plan with focused tests and traceable evidence.
---

# Implementation flow

1. Read the governing brief, acceptance criteria, design notes, project rules, relevant architecture, and `.vibe/core/technical-decision-readiness.md`.
2. Resolve contradictions before editing. Make reasonable local assumptions when they do not alter product scope, and record them.
3. Before the first application/shared code edit—even when the user asks directly for implementation—preflight size, risks, open decisions, relevant architecture, readiness outcome, governing decision status, review evidence, blockers, and gate confirmation.
4. If the core contract applies and evidence is missing or invalid, stop implementation. Record the blocking reason and next handoff; route read-only `vibe_tech_lead` decision/review passes as required. Do not turn an unresolved technical trade-off into a local assumption.
5. Use one writer for shared application code only when the gate is `implementation-ready` (or the work is a qualifying S task). Delegate to `vibe_rd` when a bounded implementation worker is useful; exploration or specialist reviews may run independently.
6. Implement the smallest coherent change inside the accepted decision boundary, including error paths, compatibility, and documentation affected by the behavior. If a new durable/high-risk choice appears, stop the affected edit and reopen readiness before continuing.
7. Run focused checks during development, then the relevant configured project checks with `./bin/vibe verify` when available.
8. Hand the completed change to `vibe_qa` for an independent pass on M/L work or elevated risk.

Report files changed, important decisions, verification evidence, checks not run, and remaining risks. Do not broaden the feature to satisfy unrelated cleanup preferences.
