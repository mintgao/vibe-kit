# 0026: Publish exact v0.13.0 from a newly accepted public candidate

- Status: Accepted
- Date: 2026-10-29
- Decision owner: vibe_tech_lead decision author
- Work item: docs/work-items/20261029-v0-13-publication/brief.md
- Exact proposed profile: docs/work-items/20261029-v0-13-publication/feature-contract.md
- Execution sequence: docs/work-items/20261029-v0-13-publication/implementation-plan.md
- Review: approved by the distinct independent Tech Lead in docs/work-items/20261029-v0-13-publication/technical-review.md#final-review; source preparation release belongs to the orchestrator readiness gate

## Context and scope

The accepted local 0.13 feature work contains four bounded modules: runnable Python/Node extension-contract templates, optional read-only payload-identity compatibility checks, controlled upgrade-maintenance guidance and evidence views, and bounded maintenance readback/recovery. The original N01–N36 acceptance matrix remains mandatory. Publication is a newly authorized subsequent stage; earlier local-only records remain truthful historical scope.

ADR0024 governs the historical exact 0.12 publication and separate closeout. ADR0025 governs the accepted 0.13 feature semantics and Agent-install protocol 5, but explicitly did not define a 0.13 publication profile. This decision adds that exact profile and its release gates without broadening feature behavior, host authority or issue scope.

The publication source starts from observed public main. At authoring, the orchestrator reports official GitHub reads of public main at e676446c661e717578b4dd114548cdfecb2b2437, a non-draft 0.12.0 Pre-release published on 2026-10-28, and absence of the v0.13.0 tag. Those observations establish existence and metadata only; no new download hashing, public QA, current protection assessment or 0.13 completion is inferred. Re-read current state at each relevant gate.

The fresh source checkout currently contains the public 0.12 baseline plus this proposed decision packet. It does not yet contain the accepted 0.13 implementation or completed 0.13 acceptance. The accepted feature-governance dependencies are now materialized as public projections: docs/decisions/0025-upgrade-compatibility-and-maintenance-continuation.md and docs/work-items/20261029-v0-13-local-delivery/{scope.md,brief.md,technical-review.md,acceptance-matrix.md}. Scope preserves the original product body; the matrix retains its original bytes. The historical brief/review retain the original local-only boundary and approval history, while omitting private preparation/execution reports. ADR0025 clarifies its historical Accepted status and the durable host-evidence requirement. Their new exact bytes require the current distinct reviewer to finish R1/R2 review before implementation release; materialization is not approval, current activation or product acceptance.

## Decision: one closed publication profile

Add exclusive publication intent/receipt schema 8 for vibe-kit-v0.13.0-prerelease, using the existing offline profile machinery and the exact constants, acceptance mapping and twenty public smokes in feature-contract.md. Keep issue_closeout null and issue policy none. Keep closeout schema 5 current and exclusively bound to the historical schema-7 parent. Publication schemas 1–7 and closeout schemas 1–5 retain their exact identities, behavior and verdicts.

Preserve six ordered publication operations, five sorted assets, natural keys, snapshot-bound preconditions, child attempt ledgers, read-back-before-retry and create-only optional validation output. No generic version substitution, new network client, generalized publication framework, new receipt fields, credentials or CLI network authority are introduced.

Current publication mirrors become 8/8/5. Preserve the accepted 0.13 kit/Plugin version, Agent-install schema/protocol 4/5, core/Codex 7/7, Hermes 1, takeover 2, release manifest 2 and all other existing schemas. A publication profile addition does not authorize protocol rollback to the historical 0.12 values.

## New candidate and activation sequencing

The profile and its managed documentation change bin/vibe and activation-critical inputs. The earlier frozen feature candidate, its source QA and stopped fixtures remain historical evidence for their actual identities. Preserve their source files, installation state, transaction evidence and receipts. Never relabel their hashes, host activation or QA as belonging to the new publication candidate.

Complete the accepted feature projection, publication implementation and public document projection in a distinct source candidate before freezing its final payload and activation identity. Regenerate identity mirrors only after the last relevant edit. README and current release notes also participate in payload identity; their prepublication edits must precede the final freeze.

Use new independent Python and Node fixture roots for the final candidate. The host must establish each actual target, source-task stop and genuine successor activation against that fixture's installed manifest and actual activation set. A collaboration child sharing a different root, an offline valid object, doctor health or an Agent claim is insufficient. Unknown older task outcomes are reconciled through their existing ownership path; new fixtures do not declare those operations completed or absent.

Only an actually activated task with known installation and no active transaction may perform the already authorized bounded compatibility maintenance, subject to its own applicable readiness, independent review, one writer and preserved guards. Known pre-default blockers use the accepted maintenance-required path; do not manufacture an initial full-QA failure. An independently run final fixture default plus doctor may satisfy both maintenance and takeover when all applicable conditions hold.

Do not run another full QA on the old frozen candidate merely to finish a candidate that publication edits supersede. Record genuine existing evidence without rewriting it. Reusing an old fixture instead of the recommended new roots requires its lawful active owner and an official upgrade, doctor and fresh activation boundary; the old source task cannot cross STOP to re-upgrade it.

## Public source and H, M, E

Create the public branch from the observed public baseline and project an explicit accepted file allowlist. Do not merge private development history. Exclude installation state, fixtures, raw logs, private execution identifiers, machine paths, credentials, environment values, host goal text, transfer/custody and unshipped references. Public summaries contain only allowed facts, public URLs and hashes whose applicability has been checked.

H is the final local public-candidate commit that will be the PR head. Source privacy review, all required local product acceptance and independent source QA must pass before its first public push. A candidate commit is not publication or proof of acceptance. Keep subsequent runtime evidence outside the tracked source so recording a result does not silently change H. Required public truth changes before push create a new H and invalidate affected evidence.

Create a normal draft PR, obtain independent exact-head review and satisfy the actual checks/protections. Re-read head, rules, checks and mergeability before marking ready or merging with the expected head. Do not self-approve where a separate approval is required, bypass protections, use admin override or push source directly to main. Missing protection rules are absent, not passed.

M is the actual server-produced merge commit and tree. Earlier source receipts retain H or their actual earlier identity even when trees match. Confirm M's tree, payload, activation and approved scope. Unexplained divergence blocks release. Exact equality may establish continued applicability of earlier product/host evidence through an explicit human review under the existing evidence rules; it never changes the receipt identity, authenticates a new host, or activates a different installed target. Changed relevant target bytes require affected acceptance and fresh real activation.

E is a later commit recording observed publication facts and homepage updates. It must not move the tag, rewrite the frozen Release body/assets or become the release source.

## Verification ownership and release gates

Independent QA owns one complete default run for unchanged H. Earlier feature-candidate QA remains historical. Independent QA additionally owns exactly one complete default run of unchanged M as the distinct postmerge release gate; record the new source identity and specialized gate reason before running it.

Use actual CPython 3.9 for the canonical M command, exactly ./bin/vibe verify . --format json. That one real run may truthfully support the independent-QA, configured-check and Python evidence views. Do not execute the full matrix again merely to populate another receipt. All configured checks must pass without skips or environment limitations. RD performs focused checks only.

Require focused feature/publication regression evidence and two clean prerelease builds from distinct clean M checkouts and output locations. Both identify M/tree, use actual CPython 3.9, produce the identical five-asset set, and pass target validate-release. Freeze release-note bytes and annotated-tag identity. Keep gate evidence outside the tracked source.

The ten publication ACs do not replace the 36 product ACs. AC-1 requires the final-target product matrix including real Python/Node host scenarios. A blocked live condition is not a passed static condition. AC-9/10 require publication to exist and remain explicitly not runnable before publication.

## Remote ownership, recovery and authorization

The CLI stays offline. The host reads the complete current main/tag/Release and paginated asset state, hashes every existing asset and rejects extra, duplicate, divergent, incomplete or unhashable state. Construct the existing closed intent only after its actual gate bundle, source, notes, assets and remote snapshot are fixed.

Bind the existing publication authorization with authorization_source_ref and bound_at to the exact intent and host operation. The binding timestamp is not invented later consent. PR lifecycle authorization is recorded separately from the six-operation publication intent. Do not embed conversation text or private host identity in public artifacts.

After PR merge main should already equal M: publish-0 is read-matched with zero writes. Main drift blocks; never move main backward or substitute a different candidate. Before each natural-key write, re-read the actual precondition. After every response, including timeout, read back exact state before proceeding or retrying. A second write is allowed only after positive proof that the first eligible write is absent and its original precondition still holds. Denial, definite execution failure, conflict, divergence or still-unknown state gets no retry. Preserve ledgers for same-intent resume; no third write.

Never force, delete, replace, move a tag, rewrite an existing divergent Release or promote stable. Publication failure preserves observed remote state and reports the exact incomplete operation rather than claiming rollback or completion.

## Public verification and completion

Freshly download all five canonical public assets; compare their sizes/hashes to the intent, validate nested checksums and distribution closure, run downloaded-target validate-release and all twenty ordered smokes. Supported predecessor fixtures use authenticated official public assets, including the existing 0.12 release. Missing or divergent predecessor evidence blocks the relevant test; it does not authorize publishing or altering an older release.

Run final validate-publication on actual CPython 3.9 with read-only receipt input and only an optional distinct create-only result. Independent postpublication acceptance binds the actual validation result and requires all ten publication ACs passed. Remote publication alone is incomplete. Record platform immutability as observed true, false or unknown; no signature, provenance, live compliance or efficiency claim follows from metadata or hashes.

After completion, update both homepages and necessary context in E with observed facts and read back the governed PR/merge result. No issue comment/closure, development-project upgrade or unrelated service operation is part of this stage.

## Alternatives and review focus

Rejected: mutate schema 7 to accept 0.13; import private history; introduce a general release engine; complete old-candidate full QA before changing its target; reuse old activation for changed bytes; bypass a required GitHub approval; close issues as an implicit release side effect.

The distinct reviewer must examine exact profile/dispatch preservation, source privacy and H/M/E separation, the candidate-change and activation boundary, the new-fixture plan, non-circular evidence dependencies, retry/read-back rules, public smoke completeness, unchanged issue scope and verification reuse. A successful review is necessary but not sufficient: only the orchestrator may confirm the implementation gate after Accepted decisions and an actual successful validate-readiness. This Proposed artifact grants no implementation or publication release.
