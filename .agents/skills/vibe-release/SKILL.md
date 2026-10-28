---
name: vibe-release
description: Plan, authorize, publish, and verify exact versioned Vibe Kit GitHub Pre-releases through offline intents and host-owned remote operations.
---

# Vibe Kit release

Use this Skill only for the Vibe Kit repository release lifecycle. The CLI stays
offline; GitHub authentication, network reads and writes belong to the Agent/host.

## Homepage review for every release

Before final release QA, review `README.md` and `README.zh-CN.md` together:

- Compare the proposed release's actual capabilities with the user-facing introduction. Lead with what users can do, short examples, quick start, and supported scope; link deep contracts and implementation details to maintained guides.
- Keep both languages aligned on capabilities, defaults, limitations, exact version, Pre-release/stable status, install/upgrade entry points, and published asset names. Review section length, order, and duplication rather than only replacing the version badge. Record changed facts and reasons for unchanged sections in the existing implementation or verification record.
- Describe workflow guidance as guidance. Preserve evidence boundaries; do not invent model outcomes, efficiency savings, screenshots, or endorsements.
- Keep latest-published claims tied to observed publication. After confirmed release completion, update and read back both homepages in the later evidence commit. Never rewrite an older tag, Release body, or asset to refresh the introduction.

## Historical v0.7 profile

1. Confirm the accepted version, release kind and scope. For v0.7.0 the exact
   scope is repository `mintgao/vibe-kit`, annotated tag `v0.7.0`, one non-draft
   Pre-release, the exact five assets, public verification, then issues #1–#5.
2. Require an accepted clean commit, independent QA, all configured checks,
   Python 3.9 evidence, two byte-identical prerelease builds and successful
   `validate-release`. Freeze the release-note bytes and annotated-tag identity.
3. Read remote `main`, tag, Release and the complete asset list. Build the closed
   request and run `bin/vibe publication-plan --phase publish --request <json>
   --candidate <release-dir> --format json`. This command performs no network or
   writes. Present the exact intent digest and bind authorization to repository,
   version, operation set, intent digest and one host operation ID.
4. Under that authorization only, fast-forward `main` with the expected-old OID
   lease; create or confirm the exact annotated tag and Pre-release; then upload
   or confirm exactly `SHA256SUMS`, `release-manifest.json`, the direct ZIP,
   distribution ZIP and Plugin ZIP. Extra, duplicate or divergent state blocks.
   Never force, delete, replace or rewrite.
5. After every write, read back exact identity. A timeout or transport-unknown
   response is followed by read-back before retry. Retry only a positively absent
   natural-key object, at most once. Download and hash all five public assets.
6. Produce the closed sanitized receipt and run `bin/vibe validate-publication
   --intent <json> --receipt <json> --candidate <release-dir> --format json`.
   Structural validity does not authenticate GitHub; retain live public evidence.
7. Only after confirmed-complete publication and passed public verification,
   build the #1–#5 request and run `publication-plan --phase issue-closeout`.
   The request carries the exact five-item remote snapshot, ten ordered
   comment/close operations with their canonical snapshot preconditions, and the
   declarative non-destructive scope. Bind a separate executable closeout
   authorization to the exact intent digest, repository, issue set and two-operation
   allowlist before any write.
8. Before every closeout operation, reread issue state and all exact-marker
   comments. Reuse `open-exact`/`closed-exact`; never close before the exact comment
   is read back. After a definite or uncertain response, read back before retry.
   Retry only a positively absent natural key after attempt one, at most once, and
   read back again after attempt two. Conflict, permission denial or still-unknown
   state gets no retry and stops the current and all later operations. Resume the
   same intent from the first non-terminal operation without duplicating comments
   or closes.

## V0.8 profile

V0.8.0 is the separate closed schema-2 profile
`vibe-kit-v0.8.0-prerelease`; it must never enter the schema-1 Issue-closeout
branch. Require the accepted clean source commit, fresh independent
prepublication QA, canonical configured checks, actual CPython 3.9 evidence,
and two independent clean byte-identical prerelease builds from the same commit
and tree. Keep the complete release-gate evidence outside the source checkout.

Read complete paginated main/tag/Release/assets state and publicly hash every
existing asset. Extra, duplicate, divergent, incomplete or unhashable state
blocks before an intent digest exists. Run:

```text
bin/vibe publication-plan --phase publish --request <json> \
  --candidate <candidate-a> --comparison-candidate <candidate-b> \
  --release-gate-evidence <json> --format json
```

The plan and both candidates run on CPython 3.9 and perform no network or writes.
Obtain a later executable authorization bound to the exact six-operation intent
digest and one host operation ID. Apply expected-old-OID main CAS, annotated tag,
non-draft Pre-release and exactly five assets without force, move, delete,
replace, rewrite, promotion or any Issue operation. Read before every natural-key
write and after every response. A second write is permitted only after the first
read-back proves the kind-specific positive-absence state; permission denial,
divergence, failure, execution error or unknown state gets no retry. Preserve
the main/tag/Release and five child asset attempt ledgers for same-intent resume.

After authenticated read-back, canonical public downloads, nested checksum and
distribution validation, target `validate-release`, and all six exact public
smokes, run:

```text
bin/vibe validate-publication --intent <json> --authorization <json> \
  --receipt <json> --candidate <candidate-a> --format json
```

Only a later independent postpublication receipt with AC-1 through AC-12 all
passed permits “v0.8.0 published and verified.” Record platform immutability as
true, false or unknown. The causally later evidence commit is not part of the
publication operation set and `evidence_pushed=false` unless a separate future
task authorizes its exact CAS push.

Persist only allowlisted public facts and hashes in work-item evidence. Never put
tokens, headers, environment values, raw host output, hidden reasoning, goal text
or conversation content in an intent, receipt, release asset or issue comment.
Do not claim platform immutability, publisher signing, provenance, final product
acceptance or measured token reduction without corresponding evidence.


## v0.10.1 exact profile and homepage gate

ADR0021 governs schema-5 `vibe-kit-v0.10.1-prerelease`: six publication operations, five exact assets, issue policy `none` and no closeout — the schema-3 closeout graph stays bound to the historical v0.10.0 parent. `publication-plan` and `validate-publication` select the closed profile from its exact schema; the historical schema-1, schema-2, schema-3 and schema-4 entry points keep their exact semantics, and a v0.10.1 candidate never passes them. Existing authorization is bound to the frozen intent through `authorization_source_ref` and `bound_at`; never invent a later user approval. The read-only `issue-closeout --packet <file> --format json` validates a bounded set of relative evidence-file references, exact comments and separately authorized receipt, dispatching on the parent publication intent's schema. No command performs network writes.

Before final release QA, review both README.md and README.zh-CN.md version, links, installation commands, capabilities and limitations. Synchronize changed facts and record reasons for unchanged sections in the implementation report. Publication completion facts are a later evidence commit without tag movement.

## v0.11.0 exact profile and separate five-issue closeout

ADR0022 governs schema-6 `vibe-kit-v0.11.0-prerelease`: the same six ordered
publication operations, exactly five assets, eleven ordered public smokes,
including two same-version upgrades, and ordered issue policy [14,15,16,17,18].
Historical publication profiles 1–5 and closeout profiles 1–3 stay fixed.
Publication receipt `issue_closeout` is null. Prepublication AC-10.1, publication
AC-10.2 and separate issue closeout AC-10.3 are distinct evidence phases.
Publication acceptance includes AC-1–AC-9, AC-10.1 and AC-10.2; it excludes
AC-10.3, so verified publication does not depend on future closeout.

`validate-publication --receipt` is read-only input. With no output option it
writes no result artifact. Use optional `--result-receipt <new-path>` to create a
distinct result exactly once; aliases, candidate descendants, existing leaves
and unsafe/unavailable parents are refused without overwriting. Nested validators
cannot persist intermediate results. Existing authorization is bound using
`authorization_source_ref` and `bound_at`; do not ask for another approval of
an already-authorized unchanged exact scope.

After validated schema-6 public verification and passing postpublication
acceptance, use `issue-closeout --packet <file> --format json` for the separate
schema-4 profile over ordered [14,15,16,17,18]. Bind separate exact closeout
authorization, verify each issue's evidence, then comment, read back, close and
read back in the ten-operation order. Markers are exactly
`<!-- vibe-kit:v0.11.0:issue-<number>:<closeout-id> -->`.
Issue #14 binds AC-1; #15 binds AC-2 and the published repeat smoke; #16 binds
AC-3/AC-4; #17 binds AC-5/AC-6; #18 binds AC-7/AC-8, with static evidence only
and no live-model compliance claim. A completed pair proves only that issue;
uncertain/unfinished items remain non-passing. Complete AC-10.3 only after all
five exact comment identities and closed-state read-backs pass. Reconcile the
same authorized intent only; no divergence, force, replacement or deletion.

Record public acceptance in `postpublication.md` and issue evidence/comment/
closed-state and bound digests separately in `closeout.md` within work item
`20261010-feedback-closure`. These are audit summaries, not new receipt fields.
For the historical v0.11.0 publication, both homepages retained 0.10.1 as
latest published until observed live 0.11.0 completion. No offline profile definition claims publication
or issue closure. Private logs and host goal/custody payloads never enter public
receipts, comments or summaries.


## v0.12.0 exact profile, merged-source gate and separate closeout

[ADR0024](../../../docs/decisions/0024-v0-12-publication-and-separate-closeout.md)
governs exclusive schema-7 `vibe-kit-v0.12.0-prerelease`. It has the six existing
ordered publication operations and exactly five UTF-8-name-sorted assets:
`SHA256SUMS`, `release-manifest.json`, `vibe-kit-0.12.0.zip`,
`vibe-kit-distribution-0.12.0.zip`, `vibe-kit-plugin-0.12.0.zip`. Publication
receipt issue_closeout is null. Historical publication 1–6 and closeout 1–4
retain their exact semantics; schema 6 is exclusively v0.11.0.

Project only accepted sanitized source onto public main; do not copy unrelated
local history, installation state or private evidence. Review both homepages
before final source QA. Until observed v0.12.0 completion, retain v0.11.0 as
latest published and label 0.12.0 a candidate. Record changed facts and
unchanged-section reasons.
Create a normal draft PR, obtain independent exact-head review and satisfy actual
checks/protections before marking ready and merging with expected head. Never
bypass protections or push source directly to main. H is the reviewed PR head;
M is the server-produced merged commit/tree; E is a later publication-fact commit.
Earlier receipts keep their actual source identities even when trees match.

Freeze clean M and notes. Independent QA runs one complete default verification
of unchanged M as a distinct postmerge gate, with its reason recorded. Require
actual CPython 3.9, all configured checks passing, focused feature/publication
scenarios, two builds from distinct clean M checkouts/output locations, identical
five assets and target validate-release for both. One actual canonical
`./bin/vibe verify . --format json` run may support truthful QA/configured/Python
views; do not repeat it to fill another receipt. Keep gate evidence outside the
source checkout. Final managed edits invalidate the affected identities/gates.

Prepublication mapping is exactly AC-1–AC-8 passed, AC-9–AC-12
not-runnable-before-publication. Requirements are none for AC-1–AC-8, then
live-read-back, public-smoke, issue-closeout and project-upgrade. Only this profile
uses project-upgrade. After freezing the exact remote snapshot, construct the
intent and bind existing authorization through authorization_source_ref and
bound_at. An already-target main is read-matched without a write; any main drift
blocks. Reconcile the same natural keys with read-back before retry and at most
two writes; denial, divergence and still-unknown state get no retry.

Freshly download/hash all five public assets, validate nested distribution and
downloaded-target validate-release, then execute all seventeen ordered smokes
from ADR0024. These include every supported predecessor through v0.11.0, two
same-version upgrades, exact onboarding entry points, actual focused Python/Node
entry wiring, and the three inspection separation/interruption/wrong-run cases.
Skipped Node or static inspection cannot pass that execution requirement.
Run final validate-publication on CPython 3.9 with read-only receipt input and an
optional distinct create-only result. Independent postpublication acceptance
must contain exactly AC-1–AC-10 passed. AC-11/12 never gate publication or its
closeout parent. A profile definition alone proves no publication.

Only after that acceptance, use the separate schema-5 `issue-closeout --packet`
path for ordered [20,22,23] and six comment/close operations. Its parent is exact
schema 7. Bind separately authorized existing scope to the exact closeout intent;
authorization_source_ref/bound_at identify the authorization and its binding time. Markers are
exactly `<!-- vibe-kit:v0.12.0:issue-<number>:<closeout-id> -->`.
criterion_evidence_sha256 binds a separate sanitized semantic record:

- #20: AC-1 and public-onboarding-exact-integer-entrypoints.
- #22: AC-2 and public-focused-entry-evidence-python-node, the shipped reference
  and preserved independent QA ownership.
- #23: AC-3 and all three public-inspect-run smokes, with origin, applicability
  and interruption limitations.

The host checks the actual mapped evidence; a digest alone does not prove it.
Read back each exact comment before close, then closed state. A completed pair
proves only that issue; AC-11 passes after all three read-backs. Do not operate on
#21/#26 (assessment only) or #24/#25 (deferred). Keep public bounded summaries in
the current work item; raw logs, paths and host custody remain private.

After confirmed publication, update and read back both homepages/context in E
without moving the tag or rewriting notes/assets. The separately authorized
project upgrade uses real downloaded validated target bytes and official
plan/upgrade/target doctor, preserving unknown-path ownership and local work.
Never hand-edit manifest/version to force health. Upgraded health alone requires
the installed activation boundary; absent positive conforming host evidence,
provide exactly the manual action: create a new task in the same project.
