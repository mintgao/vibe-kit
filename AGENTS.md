<!-- vibe-kit:managed:start -->
# Vibe Development System

This repository uses Vibe Kit. Before substantive work:

1. Read `.vibe/project.yaml`, `.vibe/project-rules.md`, and `.vibe/core/operating-model.md`.
2. Read only the product, architecture, design, and work-item documents relevant to the task.
3. Check `.vibe/onboarding.json` and the durable context against repository evidence before substantive work.
4. Route the request to the matching `vibe-*` skill under `.agents/skills/`.
5. Before the first application or shared implementation code edit, apply `.vibe/core/technical-decision-readiness.md`. Product-shaped does not imply implementation-ready.

## Automatic readiness

Users work in ordinary development language and are not required to name a Vibe Skill or CLI command. If onboarding is `pending`, `refresh-needed`, missing, or contradicted by scaffold placeholders/current repository evidence, run `vibe-project-onboarding` internally before the routed workflow. Preserve the user's original request, complete only evidence-backed context updates, then resume that request in the same task. Treat malformed state as a diagnosable blocking project issue; do not silently replace project-owned state.

## Post-upgrade takeover

An upgrade request confirms one exact project/version once. After a safe read-only plan, apply without another conversational confirmation, then run the installed target doctor. Apply and doctor prove only upgraded files/health; never infer that this task loaded new rules.

Follow the installed, framework-managed `AGENT_INSTALL.md` and `agent-install.json` for takeover schema 1. Before trusting a takeover object, pass it to installed `bin/vibe validate-takeover --format json`; structural validity does not authenticate host evidence or prove ready. Activation requires a positive host reload/successor receipt bound to the actual target activation set, or a valid manual new-task receipt. The repository Codex adapter and bootstrap Plugin currently claim only the manual fallback unless the running host independently supplies conforming live evidence. Without it, stop after the consistent upgrade and give exactly one action: create a new Codex task in the same project. Do not say the project is ready.

Only the activated task may inspect/refresh onboarding, run final default verification, re-evaluate an unfinished original request under target rules, and resume it. Keep transfer state in the host task boundary; never persist goal text or takeover state in the repository. Reserve “upgraded”, “activated”, and “ready” for their versioned evidence, and let only the active successor provide the final completion message.

## Work routing

- New behavior or an end-to-end product change: use `vibe-feature-flow`.
- Design-only or interaction work: use `vibe-design-flow`.
- Implementation from an existing brief or plan: use `vibe-implementation-flow`.
- Testing, acceptance, or release confidence: use `vibe-verification-flow`.
- Bug investigation, incidents, or unexplained behavior: use `vibe-debug-flow`.
- Initial or refreshed repository understanding: use `vibe-project-onboarding`.
- Evidence-backed Vibe Kit process or tooling improvement: use `vibe-feedback-flow` after the primary task is complete.

## Technical decision readiness

Users do not need to ask for an ADR or identify an architecture phase. For feature, debug-to-fix, and direct implementation work, the Agent detects the size and risk triggers defined in `.vibe/core/technical-decision-readiness.md`. Unresolved applicable work is blocked before code editing and handed to the read-only `vibe_tech_lead` perspective for decision evidence and required review. The workflow orchestrator confirms the gate; one `vibe_rd` writer implements only after it is `implementation-ready`. Ask the user only for a material product choice, not an internal technical preference.

## Continuous improvement

At Close for M/L work, resolve the project-owned feedback mode through `vibe-feedback-flow`. In `ask` or `local`, silently check whether the task exposed a reproducible Vibe Kit gap; in `off`, skip classification. No qualifying signal stays silent. A new or materially changed candidate follows the mode-aware local Close flow only after the primary result and verification are complete. `ask` presents one exact, local-only decision block; `local` stores without asking; no mode authorizes network access. Submit only after the user's adjacent, unambiguous approval of the exact outbound payload.

Classify work as S, M, or L using `.vibe/core/operating-model.md`. Keep S work lightweight. For M/L work, use the relevant `vibe_pm`, `vibe_ux`, `vibe_tech_lead`, `vibe_rd`, `vibe_qa`, or `vibe_investigator` custom agents when their independent judgment materially improves the result. Prefer parallel agents for read-heavy analysis; keep one active writer for application code and shared artifacts. For required technical review, use a different Tech Lead instance from the decision author when native subagents are available; otherwise record the sequential-perspective limitation required by the core readiness contract.

Do not claim completion without relevant verification evidence. Record skipped checks and the reason. Preserve existing project conventions unless the task explicitly changes them.
<!-- vibe-kit:managed:end -->

<!-- Add repository-specific Codex instructions below this line. Vibe Kit upgrades preserve them. -->
