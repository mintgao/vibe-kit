# Quality gates

Apply gates in proportion to the work size and risk.

## Required for every code change

- The changed behavior is understood and described.
- The smallest relevant automated or manual check is run.
- Existing unrelated behavior is not intentionally changed.
- Failures and skipped checks are reported plainly.
- Before the first code edit, apply `.vibe/core/technical-decision-readiness.md`; do not treat product-shaped as implementation-ready when that contract applies.

## Additional for M work

- Acceptance criteria exist before implementation is considered complete.
- User-visible states are covered when relevant: loading, empty, success, error, disabled, and permission states.
- Relevant lint, type, test, and build commands from `.vibe/project.yaml` are run when available.
- QA maps each acceptance criterion to evidence.
- The M work item records its technical-decision trigger scan; triggered M work is blocked until required decision and review evidence is approved.

## Additional for L work

- Risks, migration, compatibility, and rollback are explicit.
- New or changed security and privacy boundaries are reviewed.
- Critical paths have regression coverage or a documented reason why they do not.
- An explicit readiness outcome, required technical review, and gate confirmation exist before implementation.
- A decision record is Accepted before implementation for new or changed durable architectural choices; citing an applicable Accepted decision or a reviewed no-new-decision rationale is allowed.

## Vibe Kit feedback gate

- At M/L Close, resolve `feedback.mode` before classifying observed workflow friction; `off` stops, while `ask` and `local` continue.
- Create local feedback only for evidence-backed framework gaps; an empty retrospective produces no artifact or notification.
- Use the mode-aware `feedback close` contract so new/material candidates prompt once in `ask`, remain local without a question in `local`, and unchanged/legacy candidates do not create noise.
- Feedback remains local and non-blocking unless the user gives adjacent, unambiguous approval for the exact report, destination and review hash.

Use `./bin/vibe verify` to run the configured project checks. The command complements task-specific validation; it does not replace it.

## Post-upgrade takeover gate

- A safe apply plus target doctor proves `upgraded`, never `activated` or `ready`.
- Activation requires a content-bound live host receipt or a valid manual new-task receipt under `AGENT_INSTALL.md`; unknown capability fails closed.
- The installed Agent-install guide/contract raw hashes, compiled registry digest, core declaration and independently recomputed activation v2 identity match before `validate-takeover` trusts structural rules.
- The production takeover validator accepts the exact closed result and rejects invalid dependencies, reason/action pairs, receipt bindings, custody transitions and ready claims without echoing takeover values.
- Only the activated task may adapt project context, run final default verification, re-evaluate target rules, resume the original goal, or announce completion.
- A default structured verify receipt must cover every configured check. Failed, skipped, malformed, unknown, or partial coverage blocks readiness.
- Unconditional “ready to continue development” language requires upgraded, activated, adapted, verified, re-evaluated/no-goal-applicable, and no blocker.
