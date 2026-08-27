<!-- vibe-kit:managed:start -->
# Vibe Development System

This repository uses Vibe Kit. Before substantive work:

1. Read `.vibe/project.yaml`, `.vibe/project-rules.md`, and `.vibe/core/operating-model.md`.
2. Read only the product, architecture, design, and work-item documents relevant to the task.
3. Route the request to the matching `vibe-*` skill under `.agents/skills/`.

## Work routing

- New behavior or an end-to-end product change: use `vibe-feature-flow`.
- Design-only or interaction work: use `vibe-design-flow`.
- Implementation from an existing brief or plan: use `vibe-implementation-flow`.
- Testing, acceptance, or release confidence: use `vibe-verification-flow`.
- Bug investigation, incidents, or unexplained behavior: use `vibe-debug-flow`.
- Initial or refreshed repository understanding: use `vibe-project-onboarding`.
- Evidence-backed Vibe Kit process or tooling improvement: use `vibe-feedback-flow` after the primary task is complete.

## Continuous improvement

At Close for M/L work, silently check whether the task exposed a reproducible gap in Vibe Kit itself. Create a local sanitized feedback candidate only when evidence crosses the threshold in `vibe-feedback-flow`; otherwise stay quiet. Feedback must not block the primary task, perform network access automatically, or be submitted without the user's approval of the exact outbound payload.

Classify work as S, M, or L using `.vibe/core/operating-model.md`. Keep S work lightweight. For M/L work, use the relevant `vibe_pm`, `vibe_ux`, `vibe_rd`, `vibe_qa`, or `vibe_investigator` custom agents when their independent judgment materially improves the result. Prefer parallel agents for read-heavy analysis; keep one active writer for application code and shared artifacts.

Do not claim completion without relevant verification evidence. Record skipped checks and the reason. Preserve existing project conventions unless the task explicitly changes them.
<!-- vibe-kit:managed:end -->

<!-- Add repository-specific Codex instructions below this line. Vibe Kit upgrades preserve them. -->
