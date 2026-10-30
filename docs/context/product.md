# Product context

## Product purpose

Provide a project-pinned development system that lets coding Agents carry trusted adoption, evidence-backed project understanding, workflow routing, technical-decision readiness, implementation, and verification with the repository.

## Primary users

- Developers using Codex to create or continue software projects.
- Vibe Kit maintainers validating its CLI, repository contracts, packaged releases, and bootstrap Plugin.

## Current capabilities

- Project-level PM, UX, read-only Tech Lead, RD, QA, and Investigator roles.
- Repository-scoped onboarding, feature, design, implementation, verification, and debugging workflows.
- Size-aware technical-decision readiness before implementation: M trigger scans, explicit L outcomes, Accepted decision/review evidence for durable or high-risk choices, and sequential-perspective fallback disclosure when identity-isolated review is unavailable.
- Risk-adaptive execution: file count alone does not force M, cross-system and
  high-risk work remains L, specialist handoffs are artifact-first and bounded,
  RD owns focused development checks, and independent QA owns one complete
  default verification of an unchanged normal M/L final candidate.
- `init` for new projects and conservative `adopt` for existing projects.
- Read-only `plan init|adopt|upgrade` before project writes.
- Hash-checked, recoverable `upgrade` with conflict candidates, durable transaction
  evidence, lossless final-entry publication, exact rollback when provable, and
  explicit `recover-upgrade` for interrupted state.
- `doctor` with three-source installed/manifest/core version integrity, configurable `verify`, and work-item generation commands.
- Mode-aware `vibe-feedback-flow` plus `feedback mode/close/draft/list/review/revise/check/submit/dismiss` for evidence-backed framework improvement. `ask` proactively presents new/material candidates once, while every GitHub submission to `mintgao/vibe-kit` remains exact-payload consent-bound and deduplicated.
- Deterministic local release/Plugin packaging, SHA-256 manifest validation, expanded marketplace output, and artifact-based offline install checks.
- Agent-first adoption from the canonical GitHub link through packaged human/machine contracts, structured install-critical CLI results, source provenance, and automatic onboarding readiness routing.
- Post-upgrade takeover with one exact-version confirmation, separately evidenced upgraded/activated/adapted/verified/ready states, content-bound activation identity, original-goal custody, target-rule re-evaluation, and a one-action manual new-task fallback.
- Structured doctor diagnostics with fixed readiness effects and full-matrix JSON verification receipts with bounded redacted output.
- Framework-managed installed Agent-install contracts plus privacy-safe `validate-takeover` structural checking authenticated against the installed manifest, normalized activation identity and compiled registry.
- A fail-closed compatibility path from the exact healthy official v0.5.0
  source-checkout contract pair into current managed ownership, without broadening
  adoption for arbitrary untracked files.
- A narrow create-only onboarding bridge for the audited v0.2 fixture and exact
  official v0.3/v0.4 identities; missing v0.5/v0.6/v0.7 onboarding is state loss and
  blocks before writes.
- A first-class `vibe-release` workflow with offline publication/closeout intents,
  host-owned GitHub operations, public five-asset verification, and separate
  evidence-bound issue closure.
- Shallow stack and command detection for common Node.js, Python, Rust, Go, and Swift projects.

## Non-goals and boundaries

- Vibe Kit v0.12.0 is the latest observed published non-draft GitHub Pre-release: [official Release](https://github.com/mintgao/vibe-kit/releases/tag/v0.12.0). The current 0.13.0 source is an unpublished candidate. Historical v0.11.0 public acceptance is recorded in `docs/work-items/20261010-feedback-closure/postpublication.md`; the earlier v0.10.1
  public completion and live verification are recorded in
  `docs/work-items/20260922-v0-10-1-publication/postpublication.md`. The historical
  v0.10.0 publication, public verification and issue #8–#13 closeout are recorded in
  `docs/work-items/20260922-v0-10-0-publication/postpublication.md`, and the
  earlier v0.9.0 evidence in
  `docs/work-items/20260908-readiness-doc-gates-release/verification.md`. Both
  homepages reflect the selected Pre-release version. This does not imply stable
  promotion, public Plugin Directory publication, or automatic network updates.
- Current repository/Plugin activation is manual-fallback-only unless a running host supplies positive conformance receipts. Static prompts, controlled fixtures and tool presence do not establish live same-task reload or automatic successor handoff.
- It does not collect telemetry or silently submit feedback. The central feedback repository is configured, but every outbound payload still requires adjacent, unambiguous approval bound to its report, repository and current hash.
- The accepted distribution uses channel-neutral releases, repository-pinned installations, a bootstrap-only Codex Plugin, generated thin adapters, and a validated GitHub Release bundle.
- It does not replace framework-specific project generators.
- It does not infer deep product or architecture truth during CLI installation; the onboarding workflow performs evidence-based enrichment afterward.
- Ordinary users are not expected to learn `init`, `adopt`, `doctor`, or internal Skill names; those remain Agent/maintainer interfaces and may surface for troubleshooting.
- Ordinary users are not expected to request an ADR or recognize an architecture phase. They decide only technical options that materially change product scope, observable behavior, promised risk/cost, irreversible state, or external compatibility.
- Vibe Kit does not collect prompt/token telemetry. Static contract and
  distribution tests can prove the encoded controls, not live host isolation or
  a token, cost, or percentage reduction.

## Product principles

- Lightweight by default, rigorous when risk demands it.
- Existing projects are preserved during adoption.
- Framework-owned and project-owned files remain distinguishable.
- Verification results must distinguish executed evidence from assumptions or skipped checks.
- Upgrade completion language must distinguish installed files, active target rules, adapted context, configured-check coverage, and original-goal routability.

The published v0.9.0 release added bounded preimplementation evidence validation and authenticated AGENTS-region integration without changing project word budgets. The published v0.10.0 release added the widened readiness grammar, the closed verification contract, published takeover admission and the per-host registry with the schema-4 Agent-install contract and the first-class Hermes entry, and its closeout closed issues #8–#13. The published v0.10.1 release publishes the Hermes label raise: the conformance label rose from `supported-unverified` to `verified` on its completed five-stage record, and the version boundary advances with publication schema 5 and no issue closeout. Both release homepages are reviewed and synchronized; independent public acceptance is recorded in the current work item.

The published 0.11.0 source implements the accepted
five feedback targets: safe publication result persistence, repeatable maintenance
transactions, opt-in complete sanitized success logs, private diagnostic progress
and prospective multi-stage outcome coverage. Source implementation alone does not establish QA, public completion or issue closure. Those separate phases are recorded in `docs/work-items/20261010-feedback-closure/verification.md`, `postpublication.md` and `closeout.md`. Default successful output is not written by progress,
optional storage failure preserves observed checks, and interruption remains
incomplete with descendant cancellation unproven.


The published 0.12.0 source added exact onboarding schema-version validation,
applicable real-entry focused evidence and bounded read-only `inspect-run` under
ADR0023. Inspection reports historical evidence with unproven current-candidate
applicability, unattested origin and liveness not assessed. ADR0024 retains its
exclusive schema-7 publication and schema-5 [20,22,23] closeout contract; release,
public acceptance, issue closure and project upgrade are separate evidence
obligations. The current observation of the official Release does not infer
completion of those later stages.

The current source candidate is 0.13.0, unpublished. [ADR0025](../decisions/0025-upgrade-compatibility-and-maintenance-continuation.md)
governs four accepted modules: runnable Python/Node extension-contract templates;
optional read-only payload identity comparison; controlled protocol-5 maintenance;
and bounded evidence/readback/recovery guidance. The identity check does not prove
API compatibility or authenticate origin. Missing or disabled project declarations
add no upgrade requirement. Node is needed for the Node examples, while the Kit
CLI remains Python 3.9+ and standard-library-only.

Maintenance before the first QA and a real failed check remain distinct. Actual
target activation, accepted technical readiness, one maintenance writer,
preserved guards and independent final QA are required before resuming business
work. Guidance and controlled fixtures do not establish live Agent compliance or
measured savings. The root installation state is preserved rather than rewritten
to claim activation.

[ADR0026](../decisions/0026-v0-13-publication.md) adds exclusive publication schema 8:
five assets, six operations, twenty ordered public smokes and issue policy none.
Historical publication 1–7 and closeout 1–5 retain their exact semantics. All
[N01–N36](../work-items/20261029-v0-13-local-delivery/acceptance-matrix.md), actual
final-target host acceptance, privacy review, independent source and merged-source
QA, normal PR approval and public verification remain required. Source
implementation supplies no publication or acceptance claim. The current scope is
[the 0.13 publication brief](../work-items/20261029-v0-13-publication/brief.md).
