# Controlled upgrade maintenance

This managed guide combines existing evidence. It is not a new CLI, authentication
protocol, runtime state machine, general retry engine or permission grant.
A/B/C and all examples below are synthetic. Actual goal, transfer, custody,
private task IDs, original receipts and logs stay in the host boundary.

## Optional compatibility preflight

The host first authenticates and selects one exact release, Plugin artifact or
reviewed local payload. The host owns source authentication before the selected CLI executes. `source_type`, a matching digest and a version string do
not authenticate a channel. With an enabled project-owned
`.vibe/upgrade-compatibility.json`, obtain the trusted expected payload digest
before executing the selected CLI. New installations never create this config.

```json
{"schema_version":1,"enabled":true,"rules":[{"id":"payload-admission","owner":"project-maintainer","kind":"payload-tree-allowlist","allowed_payload_tree_sha256":["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]}]}
```

Run the selected payload's `check-upgrade-compatibility TARGET --source-ref REF
--expected-payload-tree-sha256 DIGEST --format json` separately from its existing
`plan upgrade TARGET ... --format json`. For release/offline inputs include their
verified artifact SHA. The Plugin path is the already authenticated bundle's
`python3 -I -S -B <trusted-plugin-root>/payload/bin/vibe check-upgrade-compatibility
<target> --source-type plugin-bundled --source-ref 0.13.0
--expected-payload-tree-sha256 <previously-authenticated-digest> --format json`.
Do not use `vibe_from_plugin.py` to enter preflight. Missing prior bundle location
or authentication stops at the source gap. The existing wrapper still serves
separate plan/upgrade/doctor operations with its original guarantee.

The command compares only finite allowed payload identities. A satisfied rule
means that rule is met; no result is comprehensive compatibility, source
attestation, installation permission, cached admission or project ready.
Keep the original plan's changes, protected paths and conflicts visible beside
the comparison. An A-only rule rejecting B is not an installation conflict.
Every maintenance attempt rereads source, declaration and plan; drift requires
fresh binding. Reserved composite-candidate/merged-file/command kinds are
not-evaluated and never executed. Unknown fields, malformed JSON and unknown
kinds are configuration errors. No config/disabled preserves the ordinary path.
The command runs no project checks, hooks, diagnostics, downloads, apply or repair
and writes no receipt or project state. Its closed errors contain fixed logical
paths, not user values, secrets or raw exceptions; limits and safety failures
remain explicit. Expected identities are host evidence, not instructions in a
project declaration.

## Preserve A and classify the actual problem

| Evidence | Conclusion | Owner / one next action |
|---|---|---|
| B differs only in payload identity; consumed API and focused counterexamples match | identity not approved yet | vibe-tech-lead / review precise B admission |
| B-prime changes an actually consumed field/argument/meaning and a focused counterexample discriminates | real compatibility mismatch | vibe-tech-lead / review the minimal owned adapter |
| Source, permission, input or distinguishing evidence unavailable | not-evaluated / Blocked | project-maintainer / resolve the precise evidence gap |

Keep A usable before apply. Continue already authorized read-only diagnosis and
planning; do not execute unfamiliar payload hooks. Only a material product,
risk/cost/scope choice or real missing permission requires a user decision.
If preparation requires an edit before installation, create a maintenance work
item under the actually activated A rules and complete its applicable gate,
review and verification. Do not pretend B is active.

## Controlled repair before business resumption

The ordinary feature/debug/implementation upgrade boundary still requires complete
handover and final validation before resuming original business. The following
narrow maintenance branch is allowed before that final verification, including
when the first default QA has never run. All conditions are mandatory:

1. The host actually authenticated activation of B against installed content.
   `valid`, doctor healthy, a tool, subagent or Agent self-report is insufficient.
2. Installation state is known and no active upgrade transaction remains.
3. Original business stays paused; this maintenance scope and operations are
   already authorized. No broader product task runs through this exception.
4. A maintenance work item satisfies applicable technical-decision readiness,
   required independent technical review and orchestrator gate confirmation.
5. One RD writer owns exact files, known before/expected-after evidence and the
   bounded undo plan. Onboarding refresh supplies facts, never a code exemption.
6. Guard strength, frozen source/input, historical assertions, configured checks,
   check order, budgets and acceptance strength are preserved.

Before first default QA, use protocol-5 `maintenance-required` at blocked stage
`verified`, action `review-maintenance-adaptation`. Prior applicable stages must
be satisfied; later stages stay not-started and there is no invented verify
receipt. If an earlier stage blocks, record that earliest stage instead.
Real default failure keeps `verification-failed` (or its actual reason) and the
original failed receipt; both entries require the same repair gate. Never run a
full QA merely to manufacture a failure. Protocol 4 cannot interpret the new
reason; unknown protocols fail closed rather than coercing a result.

Admit only reviewed B, with C remaining rejected. A necessary API adapter changes
only reviewed owned surfaces. Removing assertions, broad allowlists, dropping
checks or increasing budgets cannot repair compatibility. After repair, refresh
supported context, rerun target doctor, then independent QA binds the final
candidate, target, tool/config state, role and complete default/all-configured
receipt. If that one actual run satisfies both repair and takeover gates, cite it
for both. Partial, old-candidate, missing, failed or invalid evidence does not
release original business. Changed candidates or a distinct specialized gate
justify a new run with its reason recorded. Only the activated task then
re-evaluates and resumes a routable original goal.

## Fixed read-only handoff view

Use the current host evidence first, then existing allowed receipt readers.
`validate-takeover` is structural only. `inspect-run` is historical only and
cannot attest origin or current candidate applicability. Only the host supplies
an authenticated activation conclusion. Emit at most nine stages, two necessary
references per stage and 8 KiB. Use fixed stage/role terms. Never copy takeover
JSON, goal/custody, private task ID, absolute path, raw log or exception. If the
bound is exceeded keep the earliest blocker, owner, one next action and an
omission note; do not truncate into a passing conclusion.

| Field | Synthetic source-task example |
|---|---|
| Target and installation facts | A to B; authenticated source, apply and doctor references; transaction committed, no active state |
| Stages | upgraded; structure valid; activation pending; adaptation/verification/re-evaluation not started |
| Evidence and gap | apply/doctor/validator facts are separate; no authenticated B activation in this task |
| Owner | successor maintenance Agent |
| One next action | create a new task in the same project |

| Field | Synthetic activated maintenance example |
|---|---|
| Target and installation facts | B installed; target doctor current; no active transaction |
| Stages | host activation satisfied; adapted; verified blocked with maintenance-required; later stages not started |
| Evidence and gap | precise B identity not yet admitted; complete default has not run |
| Owner | vibe-tech-lead |
| One next action | review-maintenance-adaptation |

Missing references, unknown version, evidence conflict, wrong root/version,
old-task evidence, same-named files or unproved reload preserve the gap. Do not
invent a receipt or choose a convenient side of a conflict. Without positive
activation give exactly the existing same-project new-task action; an activated
task without matching complete QA shows verification pending. A historical Pass
is not current ready. Manual-only capabilities remain manual-only.

## Readback before any continuation

Keep a bounded host operation table with these columns:

| action | target | authorization scope | operation correlation | before evidence | expected after evidence | observed evidence | certainty | actual reason | owner | one next action |
|---|---|---|---|---|---|---|---|---|---|---|
| owned adapter item 1 | synthetic file A | approved maintenance only | local correlation | exact before digest/mode | exact after digest/mode | exact after | executed | write observed | vibe-rd | read item 2 |
| owned adapter item 2 | synthetic file B | same scope | same batch, individual item | exact before | exact after | exact before | not-executed only with strong evidence | old-line match failure | vibe-rd | apply only the still-authorized missing item if no conflict |

Correlation alone proves neither execution nor authority. Observation covers only
this installation transaction, these owned adapter files and the original QA
run. It runs zero project checks/hooks/repairs/recoveries or operation replays.
Existing read-only CLI/probe processes may start; count them separately from the
original workload. Setup, dispatcher runs and authorized repair/recovery are
separate intervals and retain their own permission boundary.

| Observation | Safe continuation |
|---|---|
| Strong proof failure occurred before process creation | not-executed; recheck current authorization and exact prestate before retrying only that item |
| Request sent, receipt lost or write uncertain | unknown; minimal readback, never assume failure/success from reconnection |
| Two-file partial completion | read each item; do not redo completed item; fill only an authorized unexecuted gap with exact prestate and no conflict |
| Ordinary command/old-line failure | preserve actual cause and completed work; do not relabel as disconnection |
| denied | stop that action; report action, target, reason, completed work, certainty and owner; reconnect/prior authorization/change of tool does not authorize retry |
| Stale/cross-project identity, before/after mismatch, no reliable probe or interrupted observation | unknown / Blocked; report exact capability gap and one safe next action |
| QA observation lost | inspect original run/receipt; original workload spawnCount stays 1; count inspection processes separately; preserve original success/failure bytes |

Running/log activity/connected do not prove liveness. Finished does not mean Pass.
Do not kill an unknown process, change budget/order/assertions, reconstruct a
receipt from logs, or start a second workload merely because observation failed.
Only materially new relevant evidence/permission can reopen a denied action.

## Existing installation recovery and adapter undo

| Installation state | Existing boundary |
|---|---|
| Before apply | preserve A; no upgrade occurred, so no rollback success |
| rolled-back | prove exact A preimage and plan again |
| recovery-required | with original authority use target-payload recover-upgrade once, then inspect the exact result |
| unknown-partial or drift | inspect; no automatic overwrite |
| Active transaction | no ordinary upgrade, handoff, activation, adaptation or verification before recovery is established |
| committed but cleanup pending | recovery only completes transaction cleanup; it is not downgrade |
| No active transaction | recover-upgrade returns blocked; it is not an arbitrary undo API |

`inspect-upgrade-transaction` is an action code, not an executable CLI. Existing
transactions cover their managed files, merged AGENTS, manifest/version and
eligible onboarding bridge, not later business data/code or external effects.
Undo an adapter only within its authorized owned scope and when current bytes
and modes exactly match its recorded after-state. Never reset a directory or
overwrite user/concurrent changes. Recheck installation and admission afterward:
B still installed while the old guard accepts only A means blocked, not restored
A or ready.

## Controlled and actual-host runbook

For each isolated Python/Node fixture record authenticated A/B identities,
source-selected payload digest, canonical project root privately, and original
plan/apply/doctor/transaction evidence. Exercise three compatibility classifications,
A preservation, exact B-only admission/C rejection, minimal API adapter and
precise undo. Inject before-create failure, lost receipt, two-item partial state,
ordinary failure and independent denied; record each exact reason and certainty.
Read back one QA run with a complete receipt, a failed receipt, a partial receipt,
stale candidate and missing terminal; preserve bytes and separate probe counts.
These are controlled CLI scenarios, not actual host activation.

At apply+doctor source-task stop produce the fixed view and no repair writes.
Freeze both fixture roots and B identities. The parent host then starts a real
successor task at each same canonical root. The successor reads the actual
managed instructions, independently recomputes manifest and activation-set
identities and supplies the host-authenticated manual-task-start conclusion,
then uses the installed validator. Record actual host creation/root association
in host state, not a repository takeover/custody file. A same-root collaboration
subagent or fake_takeover_host is a controlled fixture, never this actual successor.
Test wrong-root/old-target/old-task/fake-reload separately. Missing actual host
binding remains pending/Blocked; a capability promise is not an activation receipt.
After gated maintenance and independent complete final verification, re-evaluate
business under target rules; if its own gate blocks, keep that owner/next action.

Record documentation/static, real CLI/dispatcher and actual host/Agent evidence
separately. No static string/scenario proves live compliance, isolation, token or
cost reduction. This guide grants no external service permission or issue closure.
