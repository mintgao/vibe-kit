---
name: vibe-verification-flow
description: Independently test a change, acceptance criteria, or release candidate and produce criterion-to-evidence results without silently fixing failures.
---

# Verification flow

1. For every M/L implementation, use an independent `vibe_qa` perspective. Its
   bounded packet names the role, verification objective, work item, accepted
   criteria, governing technical boundary, readiness/review evidence,
   implementation report, current diff/baseline, configured checks, expected
   criterion-to-evidence output, blockers, and capability limitations. Exclude
   the implementation author's full conversation/reasoning and unrelated files.
   Missing evidence is reported or requested, never reconstructed from guesswork.
   Apply the readiness and review boundary in
   `.vibe/core/technical-decision-readiness.md`; QA does not replace that gate.
2. Build a risk-based verification set covering the main path plus important negative, boundary, state, permission, accessibility, and regression cases that apply. Verify that implementation stayed inside the accepted technical boundary; do not use post-implementation QA as a substitute for missing readiness evidence.
3. Inspect prior verification evidence and candidate identity first. For one
   unchanged normal M/L final candidate, run default
   `./bin/vibe verify . --format json` exactly once as the canonical full matrix,
   plus applicable task-specific scenarios. Run it again only when the prior
   evidence failed, was blocked, malformed, partial, stale or otherwise invalid;
   shared candidate-defining state changed; or a post-upgrade, release, or other
   specialized gate independently requires a complete run. Record the reason and
   candidate state. A partial `--only` receipt cannot close post-upgrade takeover.
4. Treat configured failed/skipped checks as blocking, report unconfigured checks
   explicitly, and do not claim a check ran when the environment prevented it.
   For each acceptance criterion, record evidence and exactly one of: `Pass`,
   `Fail`, `Blocked`, or `Not applicable`. For readiness behavior, distinguish
   deterministic artifact/distribution checks from live Agent or host scenarios;
   static string assertions are not evidence that an Agent actually stopped or
   routed correctly and do not prove measured token reduction.
5. Report defects with reproduction steps, expected versus actual behavior, severity, evidence, and relevant file references.
6. Update the work item's `verification.md` when one exists. Do not edit application code during the independent evaluation unless the user explicitly changes the task to fixing defects.

The final conclusion must distinguish verified behavior from inference and list skipped checks and residual risk.

Use the smallest viable/no-history fork when supported. If transport bounding is
absent or uncertain, preserve QA independence and record
`transport context bounding unavailable`; do not claim prompt isolation or token
reduction.

For newly adopted applicable M/L work, the orchestrator runs `./bin/vibe validate-readiness . --brief docs/work-items/<id>/brief.md --format json` before implementation release and after referenced evidence changes. Nonzero blocks release. QA verifies the persisted release evidence; a passed structural check does not establish human applicability, independence or product acceptance. Implemented notes do not replace Accepted ADRs.

Execution schema 1 under `.vibe/local/verify/runs/` is private diagnostic metadata.
Use `inspect-run <target> --run-id <startup-id> [--final-receipt <path>] --format json`
for safe public consumption. Keep the explicit private receipt, when requested,
and select `--log-policy all-configured` only when complete successful logs are
needed. `inspected` reports an inspection, not passing current-source acceptance.
Metadata state, complete receipt status, binding, coverage, artifact scope and
historical receipt/run verdicts remain separate. The selected explicit receipt
wins; its original metadata receipt slot is not reopened or attested. A valid
receipt owns the sole selected log set, even if metadata disagrees; otherwise
valid metadata owns it. No fallback or union is performed.

Running is a last observation, never liveness; finished is not Pass. Missing,
disabled or invalid progress cannot erase a complete independent receipt, and
progress never promotes partial/interrupted evidence. Inspection performs no
checks, probes, writes, process control or automatic reruns. Applicability is
always unproven and origin not attested. Prepare any private receipt parent via
the project's normal setup: neither verify nor inspection creates receipt parents.
Independent acceptance retains QA's four states and default coverage requirement.


## Applicable affected-entry evidence

For a changed shared helper or adapter, supply a bounded impact slice and explain
why its affected entries are sufficient. Use the configured command's actual
default discovery or package script for focused execution, observe the loaded
origin and arguments, and preserve intentionally historical callers. Static
search locates callers; it does not prove that they ran. A direct helper test
alone does not establish live default wiring. Projects own probes and assertions;
no call-graph builder or additional executor is required.

| Configured check | Actual default entry | Affected live caller/helper | Observed origin/arguments | Focused command/result | Preserved historical caller |
|---|---|---|---|---|---|
| test | project discovery/script | bounded project path/name | runtime observation | project command and evidence | path/assertion, or none |

Mark this inapplicable when no shared entry changes; S work gains no mandatory
table or ceremony. RD runs focused checks; independent QA still owns one complete
default verification per unchanged final candidate. See the
[Python and Node example](../vibe-implementation-flow/references/affected-entry-evidence.md) in the installed workflow.
