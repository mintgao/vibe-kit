# Architecture context

## System summary

Vibe Kit is a dependency-free Python CLI plus distributable Codex instructions, custom agents, workflow skills, and Markdown templates.

## Components

- `bin/vibe`: command dispatcher, stack detection, read-only install/upgrade planning, safe file installation, manifest hashing and source provenance, versioned Agent JSON results, upgrades, readiness/version diagnostics, verification, feedback controls, deterministic packaging, and release validation.
- `AGENT_INSTALL.md` and `agent-install.json`: release-packaged Codex discovery and machine contracts for trusted source selection, lifecycle states, structured results, and handoff.
- `AGENTS.md`: a marked managed block that checks onboarding and technical-decision readiness and routes ordinary Codex requests while preserving repository-specific instructions outside the block.
- `.codex/agents/vibe-*.toml`: six project-scoped specialist definitions, including a read-only Tech Lead used for separate decision-author and technical-review passes.
- `.agents/skills/vibe-*/SKILL.md`: seven task-scoped workflows discovered from the repository, including the local-first feedback close loop.
- `.vibe/core/`: versioned operating model, technical-decision readiness contract, quality gates, protocol metadata, feedback policy, and work-item templates.
- `distribution/plugin-src/vibe-kit/`: bootstrap-only Plugin source; packaging adds the canonical payload instead of maintaining a second runtime copy.
- `.vibe/project.yaml`, `.vibe/project-rules.md`, `.vibe/onboarding.json`, and `docs/`: project-owned state that upgrades do not overwrite.

## Runtime

- Python 3.9 or later.
- Standard library only.
- The invoking checkout is the source of managed framework files.
- Commands are non-interactive and operate on an explicit target directory, defaulting to the current directory.

## Installation model

- `init` installs into a new or newly generated project.
- `adopt` installs conservatively into an existing project.
- `upgrade` compares recorded hashes before replacing managed files.

The install path validates caller-supplied source provenance before project writes, discovers managed source files, preflights collisions, copies managed files atomically, merges only the marked `AGENTS.md` block, creates missing project-owned context/readiness, and finally records `.vibe/manifest.json` plus `.vibe/version`.

The upgrade path compares the recorded, local, and incoming hashes before writing. If both local and incoming content changed, it writes incoming candidates under `.vibe/conflicts/<timestamp>/` and returns without changing managed files.

## Managed boundaries

- Framework-managed: the marked block in `AGENTS.md`, `bin/vibe`, `.vibe/core/`, `.codex/agents/vibe-*`, and `.agents/skills/vibe-*`. These may be replaced by a safe upgrade.
- Tool-maintained installation state: `.vibe/manifest.json`, `.vibe/version`, and generated `.vibe/conflicts/` candidates. The CLI owns these, but they are not incoming framework payloads.
- Project-owned: `.vibe/project.yaml`, `.vibe/project-rules.md`, `.vibe/onboarding.json`, and `docs/` content. Upgrades do not overwrite them.

## Verification

- The configured project check is `python3 -m unittest discover -s tests -v`.
- Scenario tests exercise initialization, adoption, source provenance, onboarding preservation/readiness, structured install results, planning read-onlyness, collision preflight, successful/conflicting upgrade, configured verification, feedback modes/attention/privacy/idempotency, deterministic packaging, release/Plugin installation, and artifact/contract tamper or drift rejection in temporary directories.
- `doctor` checks installed/manifest/core version consistency, required files, recorded hashes, the managed AGENTS block, Skill metadata, custom Agent required fields, and project-owned onboarding readiness. It separates installation health from readiness; malformed state and version failures are read-only diagnostics with exit code 1.

## Technical decision readiness

`.vibe/core/technical-decision-readiness.md` is the single normative workflow contract. Feature, debug-to-fix, and direct implementation Skills reference it before the first application/shared code edit. M work receives a trigger scan; L work always records an explicit outcome. New or changed durable decisions require an Accepted ADR and approved review, while applicable Accepted decisions and reviewed no-new-decision rationales avoid ceremonial ADRs.

Readiness state is project-owned Markdown in the work-item brief. The orchestrator persists read-only Tech Lead output and confirms the gate; a separate Tech Lead instance reviews L/triggered-M evidence on native-subagent hosts, with an explicitly disclosed sequential-perspective fallback on degraded hosts. One RD writer implements only after release and reopens the gate when implementation reveals a new durable/high-risk boundary. The CLI distributes and hash-checks these managed contracts but does not parse readiness state or enforce a file-write lock.

## Constraints and risks

- Upgrades require a trusted local checkout, validated GitHub release payload, or bundled Plugin payload; there is no remote updater or Plugin Directory publication.
- Purpose-built parsers read only generated `commands` and strict top-level `feedback.mode` shapes, not arbitrary YAML. Missing feedback mode defaults to `ask`; invalid or ambiguous values fail closed.
- `verify` executes project-owned shell commands and therefore assumes those commands have been reviewed.
- Removed managed files are retained for manual review rather than deleted automatically.

## Feedback state

- `.vibe/core/feedback.json` is managed policy and the canonical GitHub destination; the distributed default is `mintgao/vibe-kit`.
- `.vibe/local/feedback/` is tool-maintained local state with a nested ignore rule. It is outside the managed payload and upgrade replacement set.
- Each candidate separates sanitized report content from mutable occurrence, attention revision, dismissal, remote-check, and submission state. `revise` replaces sanitized content explicitly and invalidates prior review hashes.
- Fingerprints omit project identity and timestamps. Attention state, rather than occurrence-driven preview hash changes, decides whether a candidate is presented again. GitHub submission binds repository, title, body and labels into a review hash and checks the remote fingerprint immediately before create.
- Security-sensitive candidates can persist locally but cannot produce a public review hash or reach remote check/submit. Legacy state is normalized lazily without prompting an upgrade backlog.

## Distribution

`package` builds a normalized release ZIP and a Codex Plugin ZIP from the same allowlisted payload. Fixed timestamps, paths and modes make repeated local builds reproducible. `release-manifest.json` declares kit/schema/core/Agent-install/adapter compatibility, source state and per-file/channel hashes; `SHA256SUMS` covers transferred files. `validate-release` rejects unsafe archive paths, checksum/version/Agent-contract/channel drift, forbidden Plugin capabilities, and differences among the release ZIP, Plugin payload and expanded marketplace.

The Plugin exposes only `vibe-bootstrap` and `vibe-maintain`; project runtime Skills appear only after installation. The installed repository remains the runtime source of truth. v0.5.0 is the latest GitHub Pre-release. See ADRs 0002, 0004, 0005, 0006, 0007 and 0008.
