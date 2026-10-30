# N13 and N28 acceptance execution plan

- Work item: 20261029-v0-13-publication
- Author: `vibe_tech_lead`
- Status: Approved technical design; case execution requires final target and harness gates
- Date: 2026-10-29
- Scope: complete the existing N13 and N28 evidence requirements without changing their acceptance strength
- Execution authority: none granted by this document
- Current criterion status: N13 Blocked; N28 Blocked

## Governing evidence and candidate boundary

The original [acceptance matrix](../20261029-v0-13-local-delivery/acceptance-matrix.md), especially N13 and N28, and [ADR0025](../../decisions/0025-upgrade-compatibility-and-maintenance-continuation.md), especially its controlled-maintenance, recovery and evidence sections, remain authoritative. This plan supplements the [publication brief](brief.md); it neither replaces the 36 criteria nor approves its own implementation or execution. The publication decision, independent review, orchestrator gate and actual readiness checks remain prerequisites.

Use `T_H` for the final publication target bound to the future frozen candidate H. H and its payload, CLI, activation and installed identities have not yet been generated. Do not fill these fields with an older candidate's hashes. Bind the exact approved A predecessor, project template, language entry, target source, toolchain and case harness before execution. Historical stopped projects and their original receipts remain untouched.

The current public checkout still declares the predecessor source version. The accepted feature implementation and its applicable tests must be projected and reviewed before final binding. In particular, `tests/test_upgrade_maintenance.py` is a planned dependency of that projection, not a file or executed result asserted by this proposal.

This plan adds no production recovery framework, host authentication protocol, automatic retry mechanism or new product scope. It records finite controlled cases and observations. A controlled CLI test does not establish actual successor activation, live host isolation, or dual-project raw intermediate-state evidence.

## Roles, review and execution gates

Review and release are staged as specified under Orchestrator approval points below. Independent approval of the case design and source technical readiness allow the orchestrator to release one RD to prepare source and the private harness. Review of the prepared harness's exact bytes is a later case-execution gate, not a prerequisite for preparing it. Independent QA evaluates actual observations and actual maintenance-Agent decisions; the writer must not approve its own result.

N13 may run during authorized source-side diagnosis after the new main project's real A baseline is available and before target apply. It performs no adaptation, candidate hooks or project writes. Alternatively it may run after genuine target activation; in that case A availability is explicitly historical, never a claim that A remains installed.

N28 executes only after the corresponding new main Python or Node project has genuine T_H activation, known installation state with no active transaction, applicable independent technical review and an actual maintenance gate covering these shadow cases. Missing activation or readiness keeps N28 blocked. Transaction shadows never supply main-project activation or verification evidence.

The main-project verification budget is unchanged: one reviewed negative candidate default and one final golden candidate default, each on its own exact candidate. There is no preliminary golden default, no shadow-project default and no replay of an old source full run. Independent source QA retains its canonical one complete run for each applicable unchanged candidate or separately justified gate.

## N13: two controlled incomplete-evidence cases

These cases complete only N13's third, insufficient-information group. They do not replace the original identity-only and demonstrated consumption-contract-change groups. Those groups still require their own applicable final-target evidence.

Build each input packet in memory from original permitted records. Label it as a controlled incomplete evidence set. State which observations are not supplied without claiming that the source is absent, a permission was denied, a command failed, or a target contract changed. Do not modify the original evidence or create a fictitious receipt.

| Case | Facts supplied to the maintenance Agent | Evidence deliberately not supplied |
| --- | --- | --- |
| N13-Python | The new Python main project's real A original-entry baseline, exact A and T_H identities, actual read-only compatibility result and upgrade plan, with original references and hashes | The mapping of fields or arguments actually consumed by this Python project, its call observation, and a distinguishing focused result |
| N13-Node | The new Node main project's real A original-entry baseline, actual consumed-interface description, exact A and T_H identities, and original references and hashes | Actual T_H loader origin, argument/result observation, and a distinguishing focused execution result; a shared signature alone is not such an observation |

A fresh bounded maintenance-Agent instance evaluates each packet independently. Give it a neutral task: identify supported conclusions, missing evidence, the next owner and one next action. Do not supply the expected classification, an answer JSON, or the QA rubric below. Restrict the evaluation to the supplied evidence set; this is an explicitly incomplete-information scenario, not a claim about everything available elsewhere. Use no-history transport where supported. Otherwise record `transport context bounding unavailable`, disclose possible context contamination and have QA assess whether the actual observation still satisfies the intended independence; do not claim isolation.

Independent QA then compares the actual response with the actual input and the following rubric:

- The Agent distinguishes any established identity/admission finding from an unestablished semantic compatibility conclusion.
- Python's missing consumption mapping cannot be replaced by a hash difference. Node's matching signature cannot replace distinguishing runtime evidence.
- Semantic compatibility remains `not-evaluated / Blocked`; the response neither invents an incompatibility nor asserts compatibility.
- A availability cites the same main project's actual pre-apply baseline and its time/candidate applicability.
- The next owner is `project-maintainer`. Python's single next action is to obtain the missing consumption relationship evidence; Node's is to obtain the missing distinguishing focused evidence for its actual consumer.
- `source_authentication=not-attested` is not used as the semantic information gap. That property is common to the CLI's authority boundary.
- The Agent makes the decision after reading the packet. The harness does not print or fill the decision.

Preserve the actual packet identity, supplied original references, actual Agent response and independent QA judgment. Keep host identity and any host-only context outside repository evidence. If the A baseline or a required binding is missing, record the gap. A separately approved A focused baseline may supply it; do not invent it or borrow another project's Pass. No complete default is added by N13.

## N28: six independent shadows per language, seven states

Create six new owned transaction-shadow projects per language: P, R, I, U, K and D. K supplies two sequential observations: committed with cleanup pending, then no active transaction after cleanup. All shadows receive real A installations; each has its own root identity and actual transaction provenance.

Seed only the approved language project's source/template and configuration. Do not copy a main installation's manifest, transaction directory, Git metadata, activation/takeover records, or host instructions as evidence. Let the real installer create each shadow's managed installation. The shadows are controlled test targets, not new host tasks or replacements for the main fixtures.

Use a private case harness under the publication checkout:

- `.vibe/local/v013/acceptance/harness/n28_transactions.py`
- `.vibe/local/v013/acceptance/n28/<language>/<case>/project/`
- `.vibe/local/v013/acceptance/n28/<language>/<case>/evidence/`

These are proposed ownership boundaries, not created resources. Bind the harness's exact reviewed hash and T_H's actual CLI hash before running it. All runtime, cache, bytecode, receipts and logs remain within the reviewed project-local boundary. Never conduct the faults in main fixtures, historical fixtures or user projects.

### Existing production boundaries to reuse

The following existing functions in `tests/test_cli.py` provide the bounded injection patterns:

- `test_v070_upgrade_write_failure_rolls_back_and_committed_cleanup_recovers`: a forward-mutation failure followed by production rollback; a committed cleanup failure followed by existing recovery.
- `test_v070_interrupted_prepare_recovers_and_tampered_stage_stays_fail_closed`: production-created interrupted preparation and refusal after genuine stage/predecessor divergence.
- `test_v070_commit_marker_is_irreversible_and_target_cas_rechecks_leaf`: a durable real commit preceding cleanup failure, and preservation of divergent project bytes.
- After the accepted feature projection, `UpgradeMaintenanceTests.test_recover_without_active_transaction_is_blocked_not_downgrade` supplies the existing no-active rejection assertion.

Reuse the real production implementation and retain all original assertions. Load the exact frozen CLI and use its actual `main()` dispatcher for case operations. The harness may wrap the approved functions in memory solely for a finite fault or observation; it must not modify the production CLI, fabricate its result, or implement a second recovery algorithm. Normal recovery and negative guard probes use an unpatched CLI. If final T_H changes a relied-on boundary, stop and obtain an updated review before executing the affected case.

### Exact case sequence and observations

| Case | Real state producer and finite operation | Required raw evidence and maintenance-Agent decision |
| --- | --- | --- |
| P: before apply | Install A and run the actual read-only T_H upgrade plan. Do not call upgrade. | Retain A's exact observed installation/project state, plan, no-active observation and zero upgrade calls. The Agent preserves A and identifies the actual remaining plan/admission condition and its owner. It must not call this a successful rollback. |
| R: rolled-back | Start one actual upgrade. Wrap `mutate_leaf_forward` to fail once on its second call after a real earlier mutation. Let production rollback complete. | Capture the real fault, transaction material before automatic cleanup, original rolled-back result, A preimage restoration and absence of active state. The Agent verifies A and recommends a new read-only plan if appropriate; it does not replay upgrade. |
| I: recovery-required | In a separate actual upgrade, inject one `KeyboardInterrupt` at the next forward mutation after preparation and an actual first leaf change. The outer harness records the interruption, not a fabricated CLI result. | Preserve production intent/prepared/events, absent commit, actual project changes and the production reader's state classification. The Agent blocks ordinary maintenance and, under the reviewed original authority, chooses one existing recovery. Retain that actual recovery result and exact A restoration evidence. |
| U: unknown-partial | In a separate project, create the same real interrupted transaction, then deliberately change one verified ordinary stage file's bytes. Do not edit journal fields. Run one approved unpatched recovery negative probe. | Preserve stage bytes before/after, genuine journal, production classification and actual blocked/unknown result. Show no overwrite of the divergent evidence. The Agent stops automatic repair, names the exact private-state gap, assigns the transaction-evidence maintainer and requests inspection of that member. |
| K: committed cleanup pending | In one actual upgrade, fail `append_transaction_event` once at `commit-complete`, after production has durably written the real commit marker. Pause before recovery. | Preserve the real commit, intent, prepared state, events and T_H postimages. The actual result must establish committed target plus unfinished cleanup. The Agent permits only the existing cleanup recovery and explicitly rejects interpreting cleanup as downgrade. |
| K continued: no active | Run the one authorized unpatched cleanup recovery. After its real terminal result and readback, invoke recovery once more as a separately approved no-active negative probe. | Retain both original results, target continuity and active-state disappearance. The second call must be blocked and leave the installation unchanged. The Agent identifies the absence of an active transaction and rejects use of recovery as an arbitrary undo API. |
| D: project drift | In a separate project, create a real interrupted transaction and write one transaction-covered target file to explicitly labelled third-state bytes matching neither recorded preimage nor postimage. Run one approved unpatched recovery negative probe. | Preserve all three byte/hash identities, exact divergent path, journal and original result. The Agent keeps unknown/Blocked, preserves the third state, assigns the project maintainer and asks for the path's change ownership to be resolved before any overwrite. |

For R/I/U/D, a missed injection point or lack of the required earlier real mutation is a failed or blocked case, not permission to silently choose another point. I's particular second-forward-mutation interruption combines existing bounded fault patterns and requires explicit harness review.

U/D recovery invocations are pre-approved controlled guard probes used to obtain real refusal evidence. They are not actions selected by the maintenance Agent in response to unknown state. Present the actual probe evidence to that Agent without preprinting its conclusion. Unexpected mutation by a negative probe is a test failure confined to its shadow; preserve it and stop, rather than trying another probe.

The injected interruption is a controlled Python exception. A synthetic `PermissionError` is a controlled failure. Neither is evidence of a real host disconnection, operating-system crash, permission denial or interrupted remote service. No unknown process is killed.

## Capture raw state before cleanup

The observer must retain actual raw production evidence while it still exists. A previous test's name, source assertion or aggregate Pass log is insufficient.

For each operation retain the exact invocation, source/harness binding, observed start/terminal or interruption facts, original stdout/stderr, return code when one exists, and typed snapshots of the affected project and transaction members. Preserve owner, intent, prepared, events, commit, preimage and stage bytes that production actually generated; record genuinely absent members as absent.

Capture real state at the selected fault point and immediately before automatic removal. For automatic rollback, a reviewed observer around `remove_transaction_control_project` captures the actual rollback-complete material and then calls the original function. For K, capture the durable commit before cleanup. Do not make a missing journal from a receipt or edit a journal to manufacture a state.

Store raw copies in the separate evidence directory, without hard links back to mutable originals. Observe types and symlinks without following them. Preserve bytes, modes, membership and chronological operation correlation. Runtime records may retain scoped private filesystem facts, but actual host task IDs, original goals and custody remain solely in the host boundary.

Set reviewed evidence-size/member limits from the bounded fixture and transaction inputs before execution. If capture is incomplete, interrupted, exceeds its bound or fails before deletion, retain the exact gap and stop. Do not silently truncate raw evidence into a passing case.

Compare the scoped installation/project preimage separately from transaction-owned runtime parents. Production cleanup may leave legitimate empty runtime directories; record them explicitly instead of weakening the preserved installation/project comparison or pretending the complete directory tree is identical.

## Actual decisions and safe continuation

At each required intermediate state:

1. The producer stops after retaining actual raw facts.
2. A bounded actual maintenance Agent reads those facts and independently records state, certainty, gap, owner and one next action.
3. Independent QA evaluates that response against the actual evidence and accepted contract.
4. The single writer executes only the next operation already included in this exact reviewed case.

The harness supplies observations, not answer fields. Keep actual Agent decisions and available host tool-call observations distinct from source tests. With active, invalid or unknown transaction state, the Agent must not start ordinary upgrade, handoff, activation, adaptation or verification. The action code `inspect-upgrade-transaction` must not be presented or executed as a CLI command; bounded raw readers and the existing production state reader provide the inspection.

After known recovery, inspect the actual terminal result before proceeding. Committed means cleanup only; a preserved A preimage means predecessor restoration; an unknown state does not permit overwrite. Unknown or drifted shadows remain retained for review. This plan does not authorize a directory reset or arbitrary cleanup to make a case pass.

## Fixed counts and verification ownership

Per language, the finite plan is:

| Operation | Planned maximum |
| --- | --- |
| New A shadow installations | 6 |
| Initial read-only upgrade plans | 6 |
| Target upgrade invocations | 5: R, I, U, K, D, once each |
| Recovery invocations | 5: I once; U and D once each as negative probes; K once for cleanup and once for no-active rejection |
| Complete default QA in shadows | 0 |
| Host successor creation in shadows | 0 |

Count setup writes, fault injection, production mutation entry/success, recovery, read-only probes, evidence capture and main QA workload starts separately. API call counts are not operating-system write-syscall counts. A no-write conclusion requires the actual result, observed production calls and relevant typed before/after evidence; disclose the observation's limits.

The main Python and Node fixtures each retain the established two distinct default candidates: negative once, then final golden once. Do not consume those runs for these transaction shadows. An observation gap requires readback of the original operation, not another workload.

Prefer a private harness without a tracked-code change. If a small tracked test addition is necessary, the RD proposes the exact change and related focused checks before H is frozen. Preserve old assertions, configured checks/order and budgets. After H is frozen, do not change production source or tests to rescue these observations; any such necessity reopens candidate identity and review. A new full QA run needs the existing explicit reason and candidate binding.

## Orchestrator approval points and remaining gaps

Before source and harness preparation, the orchestrator must obtain independent approval of this case design, inputs, injection/capture boundaries, proposed owned paths and operation counts, and confirm applicable source technical readiness. It may then release one named RD to prepare the source and private harness within that approved scope. Ordinary focused development checks may run under their existing approval; they do not count as N28 live acceptance evidence. Final T_H identities, prepared harness bytes and main-fixture activation are outputs of later stages, not prerequisites for this preparation.

Before the actual acceptance cases execute, the orchestrator must:

- Bind the actual final T_H and approved A identities, language baselines, real entrypoints and original receipt references.
- Obtain independent review of the prepared harness's exact bytes and their applicability to the bound final target. This is the case-execution gate, not the harness-preparation gate.
- Confirm the source-stage diagnostic gate for N13; its authorized read-only pre-apply diagnosis does not require target activation.
- For N28, confirm genuine final-target activation and the maintenance gate for each corresponding main fixture before executing its transaction-shadow cases.
- Confirm that local filesystem primitives, bounded raw capture and actual Agent-decision observation are available.
- Release only the named writer's exact case scope and keep the independent QA rubric separate from the decision actor's input.

Unsupported filesystem primitives, unavailable A evidence, a changed production boundary, missing raw originals, incomplete capture or unavailable real Agent observation remain precise blockers. Existing controlled tests may establish that their encoded algorithm assertions ran; they cannot substitute for these dual-project intermediate originals or actual Agent decisions. No criterion is downgraded to fit the available evidence.

No cases have been executed by this document. N13 and N28 remain Blocked until independent QA evaluates their required real evidence. This proposal neither establishes project readiness nor authorizes publication.
