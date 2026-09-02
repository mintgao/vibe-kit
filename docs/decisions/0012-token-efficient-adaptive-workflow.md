# 0012: Make workflow execution risk-adaptive, artifact-first, and capability-honest

- Status: Accepted
- Date: 2026-09-02
- Decision owner: Read-only Tech Lead `/root/token_tl_author`
- Review: Approved by distinct read-only Tech Lead `/root/token_tl_review` on
  2026-09-02 after two changes-required passes closed classification,
  exactly-once verification, platform-evidence, and rollback boundaries.

## Context

Vibe Kit already classifies work as S/M/L, gates durable and high-risk
technical decisions under ADR 0008, uses one RD writer, and requires independent
QA for M/L work. Its current contracts can nevertheless amplify context and
work beyond the risk of the change:

- touching more than one closely related file can move otherwise local,
  reversible work into M;
- native subagents can inherit the complete conversation even when a role needs
  only accepted artifacts and a narrow code surface;
- RD and QA can both run the complete configured verification matrix for the
  same unchanged candidate; and
- host support for bounded forks and token telemetry varies, while static
  contract text cannot prove either capability or actual token savings.

The first iteration must reduce avoidable context replication and duplicate
verification without weakening readiness, review, recovery, compatibility,
security, privacy, or independent acceptance safeguards.

Vibe Kit does not collect telemetry. This decision introduces neither token
collection nor a numeric savings target, and it does not treat prompt-level
controls as proof of a measured reduction.

## Decision

### Safety precedence

Adaptive execution is subordinate to the existing safety and quality contracts.
Token budget, context size, latency, or host capability must never:

- downgrade an actual M/L task to S;
- suppress a technical-decision trigger;
- bypass an Accepted ADR, required technical review, or gate confirmation;
- combine required Tech Lead author and reviewer ownership;
- remove the single-writer boundary;
- replace M/L acceptance mapping or final configured verification; or
- turn missing evidence into an assumption.

If efficiency and an applicable safeguard conflict, the safeguard wins and the
extra cost or host limitation is disclosed.

### Risk-first execution

Use the existing S/M/L classification and ADR-0008 trigger scan. Do not add a
second effort score or token-budget state machine.

- **S:** A clear, local, low-risk, reversible change with no readiness trigger
  may touch multiple tightly coupled implementation, test, or documentation
  files and remain S. Default to one implementation perspective and focused
  verification. Delegate only for a concrete risk, and reclassify if a durable
  or high-risk trigger appears.
- **Untriggered M:** Shape only unresolved product or UX questions, record the
  required trigger scan, use one RD writer, then one independent QA pass. Other
  specialists are used only for an identified ownership question.
- **Triggered M:** Preserve Tech Lead decision authorship, review by a different
  Tech Lead instance when available, orchestrator gate confirmation, one RD
  writer, and independent QA. Efficiency comes from narrow handoffs, not role
  removal.
- **L:** Preserve every existing explicit plan, decision/review, specialist,
  recovery, compatibility, security/privacy, and QA requirement. Context may be
  bounded, but required judgment and evidence may not be reduced.

User-flow, shared contract/API, and unresolved acceptance changes remain M
triggers. Cross-system work and the high-risk boundaries in the readiness
contract require L classification. An M item may still become a triggered M
for a durable/shared decision that is not itself cross-system or high-risk.
File count alone is never a size trigger.

The orchestrator owns classification and delegation. A specialist does not
self-expand its assignment or recursively delegate unless the handoff identifies
a genuinely independent bounded subproblem.

### Artifact-first bounded handoffs

Before implementation delegation, accepted scope, criterion identifiers,
material product choices, readiness state, and governing decisions must exist in
project-owned artifacts. Conversational memory is not authoritative evidence.

Every specialist handoff supplies a role-specific packet containing only:

- work-item identifier and assigned role or mode;
- exact objective and expected output;
- authoritative file references, preferably path plus heading;
- applicable acceptance-criterion identifiers;
- accepted technical constraints and governing ADR/readiness references;
- ownership boundary, relevant files, and baseline/change set when applicable;
- evidence the role must return; and
- known blockers and host capability limitations.

Do not copy entire briefs, ADR collections, repository listings, transcripts,
raw logs, or unrelated agent output when a precise local reference is available.
Do not omit accepted criteria or governing evidence merely to make a packet
smaller.

Role-specific minimum evidence is:

- **PM/UX:** user request, relevant product/design context, and current brief;
- **Tech Lead author:** accepted scope/AC, architecture, readiness contract,
  current readiness record, and only plausibly applicable ADRs;
- **Tech Lead reviewer:** the exact persisted decision, accepted scope,
  readiness record, and referenced governing context;
- **RD:** accepted brief, accepted decision/review/gate evidence, project rules,
  relevant architecture/code, and owned paths; and
- **QA:** accepted AC, governing technical boundary, readiness/review evidence,
  implementation report, current diff/baseline, and configured checks. QA does
  not need the implementation author's complete conversation or reasoning.

If the packet is insufficient, the receiving perspective requests the missing
artifact or reference. It must not reconstruct acceptance evidence from
guesswork.

### Host capability and honesty boundary

Bounded context has two distinct meanings:

1. **Semantic bounding:** the role is assigned only the packet and authoritative
   sources it needs.
2. **Transport bounding:** the host actually omits or limits inherited
   conversation history.

When the host exposes a bounded/no-history fork control, use the smallest viable
history plus a self-contained handoff packet.

When native subagents exist but bounded fork control is absent or uncertain,
preserve every required role using the host's available full-context mechanism.
Record `transport context bounding unavailable`; do not claim prompt isolation
or token reduction.

When native subagents are unavailable, ADR 0008's sequential-perspective
fallback remains authoritative for technical review, including its required
identity-isolation disclosure. This decision neither relabels a sequential pass
as independent nor invents an equivalent QA independence claim.

Unknown capability is unavailable, not inferred from tool presence, static
documentation, or a controlled fixture.

Vibe Kit does not collect or persist prompt/token telemetry. If a host
independently exposes trustworthy aggregate usage, a report may identify its
source and coverage, but workflow completion must not depend on it. Without
such evidence, only the applied efficiency controls may be reported; no
percentage, cost, or token-saving result may be claimed.

### Verification ownership

For M/L work, QA is the canonical owner of the final default configured
verification matrix and criterion-to-evidence result.

- RD runs focused tests during implementation: changed units, affected
  integration surfaces, important error paths, and regressions directly related
  to the change.
- For one unchanged normal M/L final candidate, RD does not run the complete
  default matrix and independent QA runs
  `./bin/vibe verify . --format json` exactly once, plus applicable
  task-specific scenarios.
- A repeated complete default run is justified only when:
  - the prior run failed, was blocked, or produced malformed, partial, stale, or
    otherwise invalid evidence;
  - an applicable post-upgrade takeover, release, or other specialized gate
    independently requires complete verification; or
  - shared implementation, contract, fixture, configuration, or other
    candidate-defining state changed after the prior run.
- The rerun reason and candidate state are recorded. A complete run against a
  different candidate state or for a distinct specialized gate is not classified
  as duplicate verification.
- RD may use focused diagnostic commands after a failure, but it does not repeat
  the unchanged candidate's complete default matrix merely for confidence or
  pre-handoff ceremony.
- Failed, skipped, malformed, partial, or environment-blocked configured checks
  retain their existing blocking and reporting semantics.

S work retains focused verification by the implementer unless its actual risk
or project rules require broader checks.

### Ownership

- **Orchestrator:** size/trigger scan, minimal role routing, packet construction,
  capability disclosure, evidence persistence, and readiness confirmation.
- **PM/UX:** accepted product/interface artifacts only when shaping is needed.
- **Tech Lead:** durable decision author/reviewer duties defined by ADR 0008.
- **RD:** one implementation writer and focused development verification.
- **QA:** independent AC mapping and canonical final full verification for M/L.
- **Host/adapter:** expose capabilities honestly; a missing capability is not an
  authorization to remove safeguards.
- **CLI:** distribute and validate managed contracts; it does not schedule
  agents, measure tokens, parse handoff packets, or enforce workflow execution.

### Development candidate identity

This work mechanically advances the repository source tree to an unpublished
Vibe Kit `0.8.0` development candidate with core protocol `6` and Codex adapter
protocol `6`.

`0.8.0` is a normal strict-semver kit version whose only artifact status in this
work is `release-candidate-unpublished`; no development suffix or alternative
version grammar is introduced.

This is an internal compatibility implementation choice, not a publication:

- the accepted scope changes distributed managed workflow contracts;
- the published `0.7.0` identity cannot name different bytes or semantics;
- the next minor candidate is reversible through source rollback;
- no tag, GitHub Release, Plugin publication, network operation, latest-version
  claim, or public compatibility promise is created; and
- any future publication of `0.8.0` remains separately shaped and authorized.

The candidate carries forward existing installation, upgrade transaction,
recovery, and takeover mechanisms without changing their safety semantics,
schemas, result enums, or host-evidence requirements. Mechanical target-version
alignment must not introduce a new migration mode, recovery primitive, trust
exception, or publication path.

## Version, protocol, and compatibility alignment

| Identity | Value |
|---|---|
| Kit/source candidate | `0.8.0` |
| Candidate status | `release-candidate-unpublished` only |
| Core protocol | `6` |
| Codex adapter protocol | `6` |
| Agent-install schema/protocol | unchanged at `3` / `3` |
| CLI result schema | unchanged at `2` |
| Takeover schema | unchanged at `2` |
| Maintenance bridge schema | unchanged at `2` |
| Release-manifest schema | unchanged at `2` |
| Manifest schema | unchanged at `1` |

The implementation synchronizes current-candidate mirrors in the core protocol,
compiled CLI constants and target fingerprints, Agent-install contract, source
and installed versions, installed manifest, Plugin metadata and payload identity,
generated release metadata, tests, and current-source documentation.

Existing compatibility is carried forward, not redesigned. The declared bridge
upper bound moves mechanically to `0.8.0`, and its supported predecessor Agent
protocol list covers the already defined v0.2–v0.7 predecessor family under the
existing schema. The ordinary healthy v0.7-to-v0.8 path receives explicit
offline scenario coverage. Existing special predecessor migrations may be
retargeted only to the new candidate identity; their eligibility sets,
authentication, failure behavior, and recovery guarantees do not change.

If supporting v0.7 requires a new migration exception, schema, recovery
behavior, trust assumption, or irreversible operation, readiness reopens for a
separate compatibility decision.

Exact historical/public v0.7 facts are not mechanically replaced: its tag,
release notes/evidence, historical ADRs/work items, public README links, exact
publication/closeout Skill and validation, public asset names, issue markers,
publication tests, and published Plugin artifact remain v0.7-specific. Current
documentation may distinguish latest published v0.7.0 from the unpublished
v0.8.0 source candidate.

## Alternatives considered

### Run the complete specialist pipeline for every task

Rejected. It ignores risk proportionality and makes S work pay M/L coordination
and context costs without improving confidence.

### Use a token budget to suppress roles or checks

Rejected. Token telemetry is not universally available, and a cost threshold
must not override security, recovery, compatibility, readiness, or acceptance.

### Pass full conversation history to every agent

Rejected as the preferred path. It duplicates unrelated context and increases
confirmation bias. It remains a disclosed fallback when the host cannot bound
transport context.

### Let RD and QA both own the full verification matrix

Rejected because duplicate complete verification of the same unchanged normal
M/L candidate adds cost without distinct evidence. RD remains responsible for
focused development checks and QA remains the canonical final full-verification
owner. Another complete run is justified only by the prior evidence being
failed, blocked, or invalid, by a distinct specialized gate, or by a changed
candidate, exactly as defined under Verification ownership; those exceptions do
not create ordinary RD/QA co-ownership.

### Combine RD and QA to avoid a handoff

Rejected. It removes the independent acceptance perspective and weakens the
existing M/L quality boundary.

### Add CLI scheduling, token telemetry, or a handoff JSON state machine

Deferred. The CLI cannot control host prompt inheritance or authenticate token
usage. A new parser/state machine would add schema and migration cost without
proving host behavior.

## Consequences

Positive:

- S work avoids default multi-agent ceremony.
- M/L roles receive narrower, artifact-backed context.
- Full project verification has one canonical owner.
- Missing host capabilities produce honest fallback evidence.
- Existing readiness and QA safeguards remain unchanged.

Costs and risks:

- The orchestrator must construct precise handoffs.
- An over-narrow packet can omit needed context; missing evidence therefore
  fails closed and expands the packet explicitly.
- QA detects some broad regressions later because RD defaults to focused tests.
- Token savings remain an inference unless trustworthy host telemetry exists.
- Hosts without transport bounding retain full-history overhead.

Minimum-context handling also reduces incidental disclosure, but packets and
persisted artifacts must still exclude secrets, credentials, raw private logs,
and unnecessary conversation content.

## Compatibility and adoption

- Existing S/M/L and ADR-0008 readiness records remain valid; no work-item
  migration or new readiness field is required.
- Completed work is not retrofitted. Active unimplemented work adopts the policy
  at its next orchestration handoff.
- Hosts without token telemetry or bounded fork controls remain supported
  through disclosed fallbacks.
- Older Vibe Kit versions ignore the new prompt guidance.
- This work does not modify historical v0.7 source, release artifacts, or
  publication evidence. Platform-enforced immutability may be claimed only from
  contemporaneous platform evidence and is outside this decision.

## Rollback and recovery

Source rollback of the unpublished candidate is a Git revert of the managed
instructions, protocol/version mirrors, regenerated identities, tests, and
documentation. Because this work authorizes no release or remote write, source
rollback creates no public-version recovery obligation.

This source rollback does not establish an installed-project downgrade path.
The current v0.7 contract does not support treating protocol-3/v0.8 as an
eligible predecessor for an ordinary downgrade to v0.7, and this decision does
not authorize invoking the existing upgrade command in that direction.

Disposable development installations may be discarded and recreated from the
selected trusted source. Recovery or downgrade of any durable project already
installed with the v0.8 candidate requires a separate compatibility decision,
an explicit supported predecessor/target contract, and a controlled recovery
plan. It must not be described as supported by the existing upgrade contract.

No token data, handoff state, or new project-owned schema requires data
recovery. If adaptive routing or a context packet is uncertain, restore the
applicable full-safeguard workflow path rather than skipping a role or check.

## Verification

Deterministic contract and distribution tests prove:

- S does not mandate default delegation and file count alone does not force M;
- M/L trigger and readiness behavior from ADR 0008 remains intact;
- triggered M/L keeps distinct Tech Lead author/reviewer, gate, RD, and QA roles;
- role prompts encode the artifact packet and role-specific evidence boundary;
- RD owns focused checks while QA owns final default M/L verification;
- missing bounded-fork or telemetry capability requires limitation language;
- no contract introduces token collection or uses a token budget as a safety
  input;
- an offline unpublished package is internally identified as `0.8.0`;
- source ZIP, installed files, Plugin payload, marketplace expansion, protocol
  metadata, target fingerprint, payload tree, and activation set agree;
- init/adopt and doctor from the candidate succeed;
- an ordinary healthy v0.7 predecessor uses the unchanged upgrade/recovery path;
- no test or documentation claims that v0.7 accepts an installed
  protocol-3/v0.8 candidate as a supported downgrade predecessor;
- protocol-6 mirrors match while all unchanged schemas remain unchanged;
- v0.8 input cannot pass the exact v0.7 publication contract; and
- historical v0.7 publication tests and documentation remain exact.

QA scenarios cover S, untriggered M, triggered M/L, bounded and full-history
fallback handoffs, post-verification change invalidation, and configured-check
failure/skip behavior.

Static tests prove contract distribution, not live Agent behavior, transport
isolation, or measured token savings. Those remain unverified without
corresponding host evidence.

## Open decisions

None.
