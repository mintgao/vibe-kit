# Vibe operating model

## Principles

- Use the lightest process that provides enough confidence for the task.
- Treat roles as independent perspectives, not ceremonial steps.
- Keep product intent, implementation decisions, and verification evidence traceable.
- Prefer executable checks over assurances in prose.
- Ask the user only when a missing choice would materially change scope, behavior, risk, or cost.

## Work sizes

### S — small and explicit

A local, low-risk change with clear expected behavior, such as copy, a small style adjustment, or an obvious defect with a known cause.

- A separate work-item folder is optional.
- One implementation pass and focused verification are normally enough.
- Do not spawn multiple agents unless the task has a specific risk that benefits from independent review.

### M — bounded feature or uncertain change

A change that affects a user flow, component contract, API behavior, or more than one closely related file, or whose acceptance criteria need shaping.

- Create a work item.
- Establish acceptance criteria before implementation.
- Include UX analysis for user-facing behavior.
- Scan for durable or high-risk technical-decision triggers before implementation.
- Use independent QA verification after implementation.

### L — cross-cutting or high risk

A change involving multiple subsystems, migrations, authentication, permissions, payments, sensitive data, irreversible state, or substantial ambiguity.

- Create a work item and explicit plan.
- Record an explicit technical-decision readiness outcome before implementation.
- Record new or changed durable architectural decisions in `docs/decisions/`.
- Include rollback or recovery considerations.
- Use independent specialist reviews and QA evidence.

Apply the size-aware readiness rules in
`.vibe/core/technical-decision-readiness.md`. A shaped requirement is not by
itself implementation-ready.

## Lifecycle

Use the phases that apply; do not manufacture empty artifacts for inapplicable phases.

1. **Shape** — goal, users, scope, non-goals, acceptance criteria, open decisions.
2. **Design** — flow, states, accessibility, responsiveness, and visual constraints when user experience changes.
3. **Technical decision readiness** — before the first code edit, scan size and risk, resolve or cite durable decisions, complete required review, and confirm the gate under `.vibe/core/technical-decision-readiness.md`.
4. **Plan** — affected areas, accepted technical boundaries, risks, migrations, and verification strategy.
5. **Implement** — minimal coherent change with appropriate tests and documentation; reopen readiness if a new durable/high-risk choice appears.
6. **Verify** — map acceptance criteria and accepted technical boundaries to observed evidence and record limitations.
7. **Close** — summarize the result, update durable context only when the project truth changed, list follow-ups, and silently check whether evidence exposed a reusable Vibe Kit gap. Use `vibe-feedback-flow` only when its threshold is met; do not generate ceremonial feedback.

## Role boundaries

- **PM:** owns what, why, users, scope, observable behavior, and acceptance; identifies but does not decide technical questions.
- **UX:** owns user flow and interface behavior; does not silently expand product scope.
- **Tech Lead:** owns durable architecture, alternatives, trade-offs, technical boundaries, migration, recovery, and compatibility; authors or independently reviews decision evidence without editing implementation code.
- **Orchestrator:** owns trigger detection, role handoff, evidence checks, and readiness-gate confirmation; does not invent technical decisions or answer material product choices.
- **RD:** owns local implementation planning and implementation inside accepted technical boundaries; does not waive readiness or self-certify product acceptance.
- **QA:** owns independent verification of acceptance and the accepted decision boundary; does not replace the pre-implementation gate or silently patch failures it is evaluating.
- **Investigator:** owns reproduction and root-cause evidence; separates observation from hypothesis and fix.

The user decides a technical option only when it changes product scope,
observable behavior, risk or cost commitments, irreversible state, or external
compatibility. See `.vibe/core/technical-decision-readiness.md` for detailed
authority, review, and fallback-host rules.

## Evidence contract

Completion reports should state:

- what changed;
- which acceptance criteria were verified and how;
- commands or scenarios run and their results;
- checks not run and why;
- known limitations or follow-ups.
