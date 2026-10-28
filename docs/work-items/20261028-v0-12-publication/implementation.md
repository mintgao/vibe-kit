# Implementation: v0.12.0 public source candidate

The public source candidate implements the accepted F1–F3 scope and
[ADR0024](../../decisions/0024-v0-12-publication-and-separate-closeout.md)'s exact
publication/closeout contracts. Independent source QA, exact-head review,
merged-source release QA and live publication/closeout are pending. This report
is focused development evidence, not product or publication acceptance.

## Implemented scope

- F1/#20 keeps one onboarding predicate: only exact integer schema 1 is supported.
  Real doctor and read-only upgrade-plan paths preserve invalid state bytes and
  do not echo the state body.
- F2/#22 adds applicable bounded entry evidence guidance, its managed Python/Node
  reference and a verification template slice. Direct helpers, live default
  entries, actual loaded origin/arguments and unchanged historical callers are
  tested separately; independent QA still owns complete default verification.
- F3/#23 adds bounded read-only historical inspection with independent metadata,
  receipt validity, binding, coverage, selected artifacts and historical verdicts.
  Explicit receipt precedence, original-slot non-read, pinned no-follow reads,
  interruption, genuinely different wrong-run evidence and resource/privacy
  limits retain the accepted feature contract. Producer defaults are unchanged.
- Current intent/receipt/closeout mirrors are 7/7/5. Exclusive schema 7 selects
  v0.12.0, six operations, five assets, seventeen ordered public smokes, exact
  acceptance phases and existing-authorization source/time binding. Separate
  schema 5 selects only ordered [20,22,23], exact markers and parent schema 7.
  Closeout evidence mapping is a host-checked semantic record; a digest alone
  does not prove it. Publication acceptance excludes AC-11/12.
- Historical publication 1–6 and closeout 1–4 keep their identities and verdicts.
  Dispatch, authorization, asset uniqueness, natural keys and exact-integer guards
  include the new profile; unknown-schema negative sentinels remain unknown.
  Schema 6 remains exclusively v0.11.0. #21/#26 are assessment-only; #24/#25 deferred.

The accepted allowlist was verified byte-for-byte before projection; unrelated
history, installation state, private evidence and the unshipped source work item
were excluded. Both original install-state files and original feature bytes were
preserved. The Accepted decisions, exact review and readiness gate were checked
before implementation; validate-readiness returned valid.

## Focused development evidence

Commands below use portable Python spelling. Private execution records retain
actual argv, runtime identity, result and full output without publishing raw logs.
The existing runtime was CPython 3.9.6; Node 24.22.1 executed the real package
script with `--run`. No package installation or global configuration change was
needed. No required local Node scenario was skipped.

| Command / bounded scope | Observed result |
|---|---|
| `./bin/vibe validate-readiness . --brief docs/work-items/20261028-v0-12-publication/brief.md --format json` | valid before code edits |
| `python3 -m unittest tests.test_next_iteration tests.test_release_identity tests.test_workflow_contract -v` | 45 passed |
| `python3 -m unittest discover -s tests -p test_next_iteration.py -v` | 19 passed after final managed documentation changes; actual configured discovery, Python/Node entry and interruption cases ran |
| `python3 -m unittest tests.test_v120_publication tests.test_v110_publication tests.test_v010_publication tests.test_v011_publication tests.test_release_identity -v` | 42 executed; historical and identity cases passed; one new shape-only negative assertion required the correction described below |
| `python3 -m unittest tests.test_v120_publication tests.test_verification_observability.PublicationInputOwnershipTests -v` | final 17 passed, including actual outer-validator wrong-main rejection for schemas 6 and 7 |
| Affected integration subset: publication input ownership, equal-image/repeat upgrade, host adapters, readiness/doc gates, selected v0.7/v0.8 publication/closeout/gate and predecessor-migration scenarios | 42 passed; exact selection retained in private execution evidence |

The initial publication run found a synthetic already-target-main fixture whose
final before-image still contained the old OID. Fixture repair round 1 corrected
that value. Its retest passed the positive and exposed a distinct assertion that
asked shape-only receipt validation to own the full final-main comparison. That
negative moved to the real outer publication validator; the final 17-test run
passed. Neither correction changed production semantics. No persistent production
acceptance failure was concealed or repaired through relaxed assertions.

### Affected default-entry slice

| Configured check | Actual entry | Affected live helper/caller | Observed origin/arguments | Focused evidence | Preserved historical caller |
|---|---|---|---|---|---|
| `python3 -m unittest discover -s tests -v` | Same discovery machinery, bounded to `test_next_iteration.py` | Real doctor/upgrade-plan and inspect-run CLI paths plus entry-evidence fixtures | Python live observer loads new.py with test/focused; stale import and wrong argument both fail | 19-test bounded discovery passed, including direct/new/live/historical cases | old.py with legacy remains byte-identical |
| Fixture package.json test script | Actual Node `--run test -- --focused` dispatcher | Live adapter.cjs to new.cjs | Runtime resolved helper origin and exact --focused argv; old origin and WRONG argv both fail | Direct helper, corrected package script and historical assertion pass | old.cjs legacy assertion remains byte-identical |

This finite slice covers the changed consumers and both documented dispatch
patterns. It is not a general dependency graph or a claim of live host isolation.
Synthetic release receipts test contracts only; they are not actual release gates.

## Homepages and release documentation

README.md and README.zh-CN.md were reviewed together. Both now identify the
unpublished 0.12.0 candidate and exact onboarding validation, read-only inspection
and actual-entry evidence, while latest-published links and installation examples
remain the observed v0.11.0 Pre-release. The introduction, goal examples, quick
start, host support, defaults and limitations remain because their underlying
behavior is unchanged. Deep field/resource contracts remain in maintained guides.
Both languages preserve privacy, offline/Python requirements and conditional
activation wording without claiming measured efficiency or live-model compliance.

The guide and release Skill describe schema 7 / closeout 5. Frozen managed/Plugin
wording reports a bundled version or required evidence, so it remains true after
publication. Release notes describe intended Pre-release scope, all five asset
names and truthful limits without predicting successful publication or closure.
Decision/work-item indexes point to actual public records.

Later E may update observed homepage/context facts without changing M, its tag,
notes or assets. Existing packaging includes README.md and CHANGELOG.md in the
payload, so an E change to those files requires the existing production metadata
refresh: load bin/vibe and set
`distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json#payload_tree_sha256`
to `payload_tree_sha256(ROOT)`. This bootstrap-source mirror is outside the managed
activation set. E's refreshed digest is distinct from the published M digest;
managed M bytes stay fixed. Run targeted documentation/identity checks for E.

## Identities, ownership and remaining stages

After the last managed edit, activation v2 was regenerated through
`activation_paths(ROOT)` and `source_activation_identity(ROOT)` with the existing
normalized Agent-install calculation. Plugin payload identity was regenerated by
`payload_tree_sha256(ROOT)`. Activation is
`a70e287709814e5b1feabfc4b79a7715fbfe2f257514d101c8bf1b2bf4137471`;
payload is `678af8bd10feb544d4a6ebe4cb1cfd6f8e880b2a904090d2d6c1ec134a2d8ffe`.
The compiled predecessor registry is
`2bd4f69282952136004fbe5a66a7efe785ae407d55f36ed3b6b9f08bedb669d0`.
These are content identities, not evidence of live activation. Disposable installs
and packaging passed the focused identity tests. No source-checkout installation
manifest/version was rewritten to manufacture health.

RD did not run complete unittest discovery or complete default verify, build
clean merged-source release candidates, mutate remote state, commit or tag.
Independent QA owns the complete unchanged H candidate run; M receives its own
distinct postmerge release gate/two builds. Live protections/checks, public
seventeen-smoke acceptance, separate closeout, E and official project upgrade
remain orchestrator-owned later stages. Current source implementation does not
claim publication, closure, upgraded development-project health or readiness.


## Managed decision-reference correction after H1 review

Exact-head H1 review found two managed links to ADR0024 whose relative targets
are absent from the released payload. AGENT_INSTALL.md and the release Skill now
qualify the canonical v0.12.0 public source URL as a versioned source decision.
The packaging allowlist, runtime, profiles, tests and accepted contract are unchanged.
This managed-document correction defines a new candidate; H1's independent QA
and package evidence retain H1's identity and are not relabelled as H2 evidence.

The two explicit source-reference checks passed.
`python3 -m unittest tests.test_release_identity tests.test_v010_publication.ManagedGuideDriftTests -v`
passed all 10 focused identity/guide tests. Existing activation-v2 normalization
and production payload calculation regenerated the Agent-install and Plugin
mirrors. Activation is `4966b6962be25b0be8bdb1d3d51a3fff7c2ed32543ceb50a97dbb5b406a39924`;
payload is `afb5d0fc3dbed7c1af16c428b19dc93f8b9eb26a862005d4f85be922aefc986c`.
These supersede the earlier candidate identities above. Original feature and
installation-state bytes remain unchanged. Complete independent QA for this new
candidate and public completion remain pending; no remote operation occurred.


## Packaged-reference closure after intermediate H2 review

The earlier guide/Skill correction passed 10 focused tests. A subsequent repair
converted the release-note and consumption-contract references, passed nine
focused tests and built/validated one offline package. H1's 195-test independent
QA and both prior focused runs retain their original source identities; no H2
complete QA had started. The intermediate package payload was
`476cbae3786a851de422886db3723a631982378b098b5f4f81bc947927610702`.

The intermediate closure claim used target membership and incorrectly classified
a newly added README guide-link occurrence as inherited. Reusing an old target
does not make a new occurrence historical. Its earlier count-based audit had
correctly identified only five unchanged missing occurrences; changing that
classification to six did not close the remaining new occurrence. Private prior
evidence is retained with this scope correction, without claiming a repeated
failure of the same product test.

The final bounded correction changes only the newly added guide-link occurrence
in each homepage to the canonical v0.12.0 English source guide and refreshes the
existing Plugin payload mirror. All five earlier canonical references remain.
The audit compares individual Markdown occurrences with the actual public
baseline `ddeaec74ae6cea03e71f30e8f88d3b235dfce722`. All nine new references in
shipped Markdown resolve in both direct and Plugin payloads or name tracked files
through versioned source URLs. All sixteen new source-only references resolve in
the reviewed source. These counts include seven new canonical source references
across both languages. The direct and Plugin payloads contain the same 37 source
members; the Plugin contains 44 total members. Prospective tag URLs were not
fetched; live availability remains a later publication obligation.

Five unchanged package-relative README references remain recorded limitations:
`docs/maintainers-guide.md` twice, `docs/releases/0.11.0.md`,
`docs/work-items/20261010-feedback-closure/postpublication.md`, and
`docs/verification-observability.md`. Exact unchanged occurrences match the
public baseline. Historical cleanup and distribution expansion remain outside
this correction, so the existing allowlist and these references are preserved.

On the final corrected bytes, six focused release-identity tests and three
managed-guide tests passed on CPython 3.9.6. One retained offline
`release-candidate-unpublished` package and explicit `validate-release` passed;
the occurrence audit has no new-reference failures. No complete default
verification ran. Runtime, profiles, tests and original feature/installation
state remain unchanged. Production calculation preserves activation
`f2bccba7ec741eb9fad904576f5515df556f8593564a67e299e5bfc1a936d6f3`
and refreshes payload to
`d8ce4dc0843902b869d52fff4c9c8d7ded6c16f3bb9f4f292cb74a4eaa1bc598`.
RD writer ownership is released. Final-candidate independent QA and all public
completion stages remain pending; no commit or remote operation occurred.
