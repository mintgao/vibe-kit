# Installation and maintenance guide

[English introduction](../README.md) · [简体中文](maintainers-guide.zh-CN.md)

Technical details for Agents and maintainers. Commands below are run from the relevant project or trusted Kit root, as indicated. Version selection and actual installed evidence remain authoritative.

## Release assets

Use the exact [v0.11.0 Pre-release](https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0). The Agent/host checks published hashes and nested release consistency before using downloaded bytes.

| Asset | Purpose |
|---|---|
| [`vibe-kit-0.11.0.zip`](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/vibe-kit-0.11.0.zip) | Direct Kit payload with CLI and project instructions. |
| [`vibe-kit-plugin-0.11.0.zip`](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/vibe-kit-plugin-0.11.0.zip) | Codex bootstrap Plugin with a bundled, version-matched offline payload. |
| [`vibe-kit-distribution-0.11.0.zip`](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/vibe-kit-distribution-0.11.0.zip) | Full direct, Plugin, and expanded marketplace distribution for maintainers. |

The same Release includes [`SHA256SUMS`](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/SHA256SUMS) and [`release-manifest.json`](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/release-manifest.json). An exact canonical Release URL selects that Pre-release; a bare repository URL requires a decision when no stable Release exists.

## Architecture and ownership boundaries

Vibe Kit combines a dependency-free Python CLI with repository-scoped instructions, specialist Agents, workflow Skills, and project-owned Markdown context. Release archives and the bootstrap Plugin are acquisition channels. The installed repository remains the runtime source of truth.

- **Framework-managed:** `AGENT_INSTALL.md`, `agent-install.json`, the marked Vibe block in `AGENTS.md`, `bin/vibe`, `.vibe/core/`, `.codex/agents/vibe-*`, and `.agents/skills/vibe-*`.
- **Tool-maintained:** `.vibe/manifest.json`, `.vibe/version`, and generated `.vibe/conflicts/` candidates.
- **Project-owned:** `.vibe/project.yaml`, `.vibe/project-rules.md`, `.vibe/onboarding.json`, and `docs/`. Upgrades do not overwrite these files.

See the [architecture context](context/architecture.md) for the complete component and ownership model.

## CLI and health checks

These commands are Agent, maintainer, and troubleshooting interfaces. Ordinary users do not need them for daily work.

```bash
./bin/vibe doctor .
./bin/vibe verify .
./bin/vibe work-item settings-page --size M --title "Settings Page"
```

`doctor --format json` reports installation health separately from project-understanding readiness and classifies every warning/error with a closed readiness effect. `verify --format json` emits one canonical result for lint, typecheck, test, and build; it distinguishes passed, failed, unconfigured, and skipped checks. `verify` runs only commands explicitly configured in `.vibe/project.yaml`; review those commands as you would any project script.

## Local verification observability (0.11.0)

Old configurations keep `log_policy: "failures"` and `progress: true` defaults.
Set `checks.log_policy: "all-configured"` (or `verify --log-policy all-configured`)
for complete sanitized successful output beyond the 16 KiB tails. Failed and
environment-limited complete logs remain selected by default. The exact labeled
stdout/stderr layout has a content-addressed private path and SHA-256; successful
output is not automatically written under the default policy.

`checks.progress` accepts strict `true`/`false`; `--progress`/`--no-progress`
overrides only progress. Metadata-only snapshots record the current check and
start time before execution. The startup stderr notice identifies the caller's
run; `latest.json` identifies the last successfully published locator, without
claiming liveness or acceptance. Completed JSON delivery contains one final result.
A handled signal during terminal delivery returns nonzero and can leave an
unusable JSON prefix; no replacement document is appended. A writable explicit
receipt records blocked/error evidence. Interruption never proves all descendants
stopped. Missing progress does not invalidate a complete independent receipt.

Private evidence uses 0700 directories and 0600 files, with nested Git ignores.
Optional storage failures report unavailable and preserve check outcomes. Explicit
`--receipt` requests the bounded final body and fails nonzero if it cannot be
written. No automatic result copy, cleanup or expiry exists; complete capture
uses memory and opt-in logs can consume substantial disk. Known-pattern
sanitization is not universal secret detection. Keep logs private. See the
[settings and safe reader](verification-observability.md).

Applicable prospective multi-stage M/L briefs can record approved outcome/AC
references, stage coverage, state, evidence, next action, role owner and waiting
condition. Source Pass plus API Blocked plus export Unverified completes only
the source stage. S stays lightweight; technical review and independent QA
remain required, and host goal/custody data stays outside repository documents.

## Trust, releases, and compatibility

The default trust contract recognizes only `https://github.com/mintgao/vibe-kit`. Exact tag and Release URLs select a specific published version, whose Release metadata and SHA-256 are checked before installation. Moving refs such as `main`, unverified archives, silent repository changes, and `curl | sh` flows are rejected.

The normative human and machine contracts are [AGENT_INSTALL.md](../AGENT_INSTALL.md) and [agent-install.json](../agent-install.json). Release 0.11.0 uses core/Codex protocol 7 and Hermes adapter protocol 1, Agent-install schema/protocol 4, takeover schema 2, maintenance bridge schema 2, publication schema 6 with a separate closeout schema 4, CLI result schema 2, independent local execution schema 1, release-manifest schema 2, transaction/commit schemas 1, and feedback protocol 2. Historical releases, including [v0.10.1](https://github.com/mintgao/vibe-kit/releases/tag/v0.10.1), remain unchanged. The CLI requires Python 3.9 or later and uses only the standard library.

In release 0.11.0 both Agent-install contracts are installed framework-managed files, recorded in the project manifest and included in activation identity. `bin/vibe validate-takeover --format json` authenticates the installed contract/registry and checks the complete closed takeover structure from stdin without persisting or echoing it. A valid result is structural evidence only; it never authenticates a host receipt or claims readiness.

`bin/vibe init` and `adopt` take a comma-separated `--host` selection over the declared hosts (default `codex`). `upgrade` preserves the installation's recorded host selection. The installed copy records that selection in the manifest and in the contract's activation identity, and an install carries only the selected hosts' payload; the release payload itself always carries every declared host's files. A recorded selection that no longer matches the installed payload fails closed.

## Upgrades and conflicts

Use a newer trusted checkout, validated Release payload, or bundled Plugin payload to update an installed project. The project-local older CLI does not fetch a new version from the network.

```bash
/path/to/newer-vibe-kit/bin/vibe plan upgrade /path/to/my-app
/path/to/newer-vibe-kit/bin/vibe upgrade /path/to/my-app
```

Upgrade compares recorded, local, and incoming hashes before replacing managed files. When both the project and incoming version changed the same managed file, Vibe Kit stops before changing managed files and writes review candidates under `.vibe/conflicts/<timestamp>/`.

The 0.11.0 release retains one narrow compatibility exception for an exact healthy
official v0.5.0 source checkout: its two previously untracked Agent-install
contracts are authenticated as a complete set and then replaced and adopted as
managed files. Partial, modified, mixed, symlinked, raced, or otherwise unhealthy
sets remain conflicts; arbitrary untracked files receive no new adoption path.

The v0.7 target also recognizes only the audited v0.2 fixture and exact official
v0.3/v0.4 pre-onboarding identities for a create-only persisted `pending` bridge.
Existing valid onboarding is byte-preserved; missing v0.5/v0.6 onboarding is state
loss and blocks before writes. Upgrade is a recoverable transaction. A handled
failure either proves rollback, asks for explicit `recover-upgrade`, or reports
unclassifiable state without overwriting it.

Final installation entries use capability-probed, fd-relative lossless
publication: hard-link no-clobber for absent leaves, atomic exchange for existing
leaves, and an adjacent prepared no-replace directory unit when the first managed
parent is absent. Unsupported primitives block; ordinary rename/replace is not a
fallback for final installation entries.

After a consistent apply, the CLI still does not claim that the running Agent loaded the new rules. A host-provided reload/successor receipt may continue automatically; without one, the current repository and Plugin stop truthfully at the manual new-task fallback. Only the activated task may refresh onboarding, run final default verification, re-evaluate the unfinished goal under target rules, resume shared edits, or say development can continue.

## Verification and release engineering

The configured repository checks are dependency-free and scenario-driven.

```bash
python3 -m unittest discover -s tests -v
./bin/vibe package --status prerelease
./bin/vibe validate-release dist/vibe-kit-0.11.0
```

Maintainers use the repository `vibe-release` Skill plus offline
`publication-plan`/`validate-publication` for the exact five-asset GitHub
Pre-release. GitHub credentials and all remote writes remain in the Agent/host;
exact selection and verified SHA-256 do not claim platform immutability.

Release validation checks archive safety, checksums, versions, Agent-contract/compiled-registry identity, activation v2 independent recomputation, bounded production-validator cases, and drift across the direct Release, Plugin payload, and expanded marketplace. See the [0.11.0 release notes](releases/0.11.0.md), [post-upgrade takeover decision](decisions/0009-post-upgrade-takeover.md), and [reproducible release decision](decisions/0004-reproducible-release-contract.md).

Static contract tests confirm that the distributed instructions contain the required boundaries. Controlled Agent scenarios and independent QA are still required to observe real workflow behavior. Documentation string tests cannot replace this kind of behavioral evidence.

## Feedback and privacy

Vibe Kit does not collect telemetry or silently submit feedback. Evidence-backed Kit gaps can be stored locally and deduplicated. In `ask` mode, an exact sanitized GitHub Issue payload is shown once; submission still requires adjacent, unambiguous approval bound to that report, repository, and current review hash. `local` keeps candidates on disk without asking, while `off` disables proactive classification.

```bash
./bin/vibe feedback mode
./bin/vibe feedback list
./bin/vibe feedback review <report-id>
```

Security-sensitive candidates can remain local but cannot produce a public review hash or reach remote submission. See the [feedback-loop design](work-items/20260827-proactive-feedback-loop/design.md) for the full boundary.

## Current limitations

- `v0.11.0` is published and independently verified as a Pre-release. Five public assets match two clean builds; eleven public installation/upgrade smokes passed; [#14–#18 closeout](work-items/20261010-feedback-closure/closeout.md) is confirmed. See [verification](work-items/20261010-feedback-closure/verification.md) and [public acceptance](work-items/20261010-feedback-closure/postpublication.md). There is no stable Release, public Plugin Directory entry, automatic network updater, or publisher signature and provenance attestation.
- SHA-256 metadata verifies asset and manifest consistency. Publisher identity still depends on the GitHub account, commit, and tag.
- The Codex adapter and the Hermes host are both verified Agent integrations; Hermes's label follows its completed five-stage conformance record, and hosts without a complete record keep the strictest fail-closed rules. The current repository and Plugin are manual-fallback-only for upgrade activation; live same-task reload, automatic successor handoff, real Linux, and live Plugin-host evidence remain unverified.
- Install is not a whole-directory transaction. Upgrade has a scoped recoverable transaction over managed/tool-maintained state and the narrow eligible onboarding bridge; it does not cover business files or the whole Git worktree.
- Technical-decision readiness is a fail-closed repository workflow contract carried by prompts, role separation, and Markdown evidence. The CLI validates bounded work-item readiness evidence read-only and hash-checks distributed contracts; human applicability and gate ownership remain required, and it does not mechanically prevent file writes.
- Adoption performs shallow stack detection. Evidence-backed onboarding performs deeper project understanding after installation.

For deeper implementation details, read the [Agent-first adoption decision](decisions/0007-agent-first-adoption-contract.md), [technical-decision readiness contract](../.vibe/core/technical-decision-readiness.md), and [distribution design](work-items/20260827-distribution-architecture/design.md).

## Readiness evidence and project documentation gates

`./bin/vibe validate-readiness . --brief docs/work-items/<id>/brief.md --format json` checks a newly adopted M/L record and real Accepted ADR/review files before release to implementation. Implemented project notes cannot substitute for Accepted ADRs. The narrow Markdown grammar is documented in the [readiness contract](../.vibe/core/technical-decision-readiness.md). This read-only check leaves applicability, reviewer independence and product decisions with people and Agents; it is not a filesystem lock.

`./bin/vibe inspect-managed-agents . --word-policy unicode-whitespace-v1 --max-words 2800 --format json` authenticates the managed AGENTS region against installed state and reports its exact UTF-8 byte span. The optional counter uses Python `str.split()` over the entire merged file, including markers and project-owned prose. A 2858-word file fails a 2800-word ceiling even if the managed region alone fits. It never changes a ceiling or checker. Other word policies require the actual project checker. Manifest correspondence is not a publisher signature.
