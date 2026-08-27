# Architecture context

## System summary

Vibe Kit is a dependency-free Python CLI plus distributable Codex instructions, custom agents, workflow skills, and Markdown templates.

## Components

- `bin/vibe`: command dispatcher, stack detection, read-only install/upgrade planning, safe file installation, manifest hashing, upgrades, version diagnostics, verification, feedback controls, deterministic packaging, and release validation.
- `AGENTS.md`: a marked managed block that routes Codex work while preserving repository-specific instructions outside the block.
- `.codex/agents/vibe-*.toml`: five project-scoped specialist definitions.
- `.agents/skills/vibe-*/SKILL.md`: seven task-scoped workflows discovered from the repository, including the local-first feedback close loop.
- `.vibe/core/`: versioned operating model, quality gates, protocol metadata, feedback policy, and work-item templates.
- `distribution/plugin-src/vibe-kit/`: bootstrap-only Plugin source; packaging adds the canonical payload instead of maintaining a second runtime copy.
- `.vibe/project.yaml`, `.vibe/project-rules.md`, and `docs/`: project-owned state that upgrades do not overwrite.

## Runtime

- Python 3.9 or later.
- Standard library only.
- The invoking checkout is the source of managed framework files.
- Commands are non-interactive and operate on an explicit target directory, defaulting to the current directory.

## Installation model

- `init` installs into a new or newly generated project.
- `adopt` installs conservatively into an existing project.
- `upgrade` compares recorded hashes before replacing managed files.

The install path discovers managed source files, preflights collisions, copies managed files atomically, merges only the marked `AGENTS.md` block, creates missing project-owned context, and finally records `.vibe/manifest.json` plus `.vibe/version`.

The upgrade path compares the recorded, local, and incoming hashes before writing. If both local and incoming content changed, it writes incoming candidates under `.vibe/conflicts/<timestamp>/` and returns without changing managed files.

## Managed boundaries

- Framework-managed: the marked block in `AGENTS.md`, `bin/vibe`, `.vibe/core/`, `.codex/agents/vibe-*`, and `.agents/skills/vibe-*`. These may be replaced by a safe upgrade.
- Tool-maintained installation state: `.vibe/manifest.json`, `.vibe/version`, and generated `.vibe/conflicts/` candidates. The CLI owns these, but they are not incoming framework payloads.
- Project-owned: `.vibe/project.yaml`, `.vibe/project-rules.md`, and `docs/` content. Upgrades do not overwrite them.

## Verification

- The configured project check is `python3 -m unittest discover -s tests -v`.
- Scenario tests exercise initialization, adoption, planning read-onlyness, collision preflight, successful/conflicting upgrade, configured verification, feedback modes/attention/privacy/idempotency, deterministic packaging, release/Plugin installation, and artifact tamper/drift rejection in temporary directories.
- `doctor` checks installed/manifest/core version consistency, required files, recorded hashes, the managed AGENTS block, Skill metadata, and custom Agent required fields. Version failures are aggregated, read-only diagnostics with exit code 1.

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

`package` builds a normalized release ZIP and a Codex Plugin ZIP from the same allowlisted payload. Fixed timestamps, paths and modes make repeated local builds reproducible. `release-manifest.json` declares kit/schema/core/adapter compatibility, source state and per-file/channel hashes; `SHA256SUMS` covers transferred files. `validate-release` rejects unsafe archive paths, checksum/version drift, forbidden Plugin capabilities, and differences among the release ZIP, Plugin payload and expanded marketplace.

The Plugin exposes only `vibe-bootstrap` and `vibe-maintain`; project runtime Skills appear only after installation. The installed repository remains the runtime source of truth. v0.4.0 is the latest GitHub Pre-release. See ADRs 0002, 0004, 0005 and 0006.
