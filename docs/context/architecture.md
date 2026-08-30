# Architecture context

## System summary

Vibe Kit is a dependency-free Python CLI plus distributable Codex instructions, custom agents, workflow skills, and Markdown templates.

## Components

- `bin/vibe`: command dispatcher, stack detection, read-only install/upgrade planning, safe file installation, manifest/payload/activation hashing and source provenance, versioned Agent JSON results, upgrades, structured readiness diagnostics, full-matrix verification, authenticated structural takeover validation, feedback controls, deterministic packaging, and release validation.
- `AGENT_INSTALL.md` and `agent-install.json`: release-packaged and framework-managed installed Codex contracts for trusted source selection, the pre-execution maintenance bridge, takeover stages, host capability negotiation, activation/goal custody, the compiled structural registry, and handoff.
- `AGENTS.md`: a marked managed block that checks onboarding and technical-decision readiness and routes ordinary Codex requests while preserving repository-specific instructions outside the block.
- `.codex/agents/vibe-*.toml`: six project-scoped specialist definitions, including a read-only Tech Lead used for separate decision-author and technical-review passes.
- `.agents/skills/vibe-*/SKILL.md`: eight task-scoped workflows discovered from
  the repository, including the local-first feedback close loop and the exact
  v0.7.0 publication/closeout workflow.
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

The install path validates caller-supplied source provenance and computes the release payload-tree identity before project writes, discovers managed source files, preflights collisions, copies managed files atomically, merges only the marked `AGENTS.md` block, creates missing project-owned context/readiness, and finally records `.vibe/manifest.json` plus `.vibe/version`. The manifest additively carries the target fingerprint, exact activation paths/hashes and target activation-set digest so installed doctor and host receipts can bind activation to actual content.

The upgrade path compares the recorded, local, and incoming hashes before writing. If both local and incoming content changed, it writes incoming candidates under `.vibe/conflicts/<timestamp>/` and returns without changing managed files. For a v0.7 transaction, final existing-parent leaves use capability-probed hard-link no-clobber or atomic exchange through the platform libc adapter; a first missing managed parent is instead published as one prepared adjacent directory unit with no-replace rename. Ordinary rename/replace/unlink is not a fallback for a final installation entry, and recovery retains exact displaced objects or trees until predecessor or target state is proved.

The sole untracked-contract exception is an exact official v0.5.0
authenticated-predecessor migration for the two Agent-install contracts that
exist outside the v0.5.0 managed manifest. A compiled closed registry
authenticates the complete file pair,
normalized predecessor installation, every recorded managed hash and the managed
AGENTS block with component-wise symlink-free path checks. Plan exposes paired
`update` entries; apply independently reauthenticates the full set and each member.
Pre-mutation drift remains a paired conflict and post-mutation drift remains
`unknown-partial`. The predecessor manifest's `source` field is excluded from
eligibility, while selected target-channel provenance remains mandatory.

## Managed boundaries

- Framework-managed: `AGENT_INSTALL.md`, `agent-install.json`, the marked block in `AGENTS.md`, `bin/vibe`, `.vibe/core/`, `.codex/agents/vibe-*`, and `.agents/skills/vibe-*`. These may be replaced by a safe upgrade; the two Agent-install contracts are also activation-critical and receive normal collision/three-way protection.
- Tool-maintained installation state: `.vibe/manifest.json`, `.vibe/version`, and generated `.vibe/conflicts/` candidates. The CLI owns these, but they are not incoming framework payloads.
- Project-owned: `.vibe/project.yaml`, `.vibe/project-rules.md`, `.vibe/onboarding.json`, and `docs/` content. Upgrades do not overwrite them.

## Verification

- The configured project check is `python3 -m unittest discover -s tests -v`.
- Scenario tests exercise initialization, adoption, source provenance, onboarding preservation/readiness, structured install results, planning read-onlyness, collision preflight, successful/conflicting upgrade, configured verification, feedback modes/attention/privacy/idempotency, deterministic packaging, release/Plugin installation, and artifact/contract tamper or drift rejection in temporary directories.
- `doctor` checks installed/manifest/core version consistency, required files, recorded hashes, the managed AGENTS block, Skill metadata, custom Agent required fields, project-owned onboarding readiness, actual activation identity and stale runtime discovery paths. JSON results preserve warning/error strings and add a complete closed diagnostic registry with fixed readiness effects.
- `verify --format json` emits one ordered entry for lint, typecheck, test and build in default mode, captures bounded/redacted output tails, continues independent checks after failures, and treats configured failures or skips as takeover-blocking. Partial `--only` remains a maintainer interface and cannot satisfy takeover.
- `validate-takeover --format json` authenticates the installed raw contract, core/manifest/activation identities and compiled registry digest before validating one stdin object against the complete closed takeover schema. Errors contain rule IDs and paths only; structural validity never authenticates host evidence or emits a ready claim.
- Runtime activation, adaptation, goal custody, target-rule re-evaluation and ready derivation are host/Agent responsibilities. The repository and Plugin currently declare only manual new-task activation unless a live conforming host receipt exists.

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

`package` builds a normalized release ZIP and a Codex Plugin ZIP from the same allowlisted payload. Fixed timestamps, paths and modes make repeated local builds reproducible. `release-manifest.json` declares kit/schema/core/Agent-install/adapter compatibility, payload-tree, normalized activation-set and takeover-registry identities, source state and per-file/channel hashes; `SHA256SUMS` covers transferred files. `validate-release` independently recomputes activation v2, exercises canonical production-validator cases, and fails closed on unsafe archive paths, checksum/version/bridge/lifecycle/diagnostic/verify/activation/registry/Agent-contract drift, forbidden Plugin capabilities, and differences among the release ZIP, Plugin payload and expanded marketplace.

The release manifest also mirrors the compiled predecessor-migration registry
digest, authority and only supported mode. Validation requires exact equality with
the Agent-install/core mirrors and the packaged compiled CLI authority.

The Plugin exposes only `vibe-bootstrap` and `vibe-maintain`; project runtime Skills appear only after installation. Its wrapper verifies the bundled version and payload-tree identity before target-CLI execution, but it provides no reload/task-creation API. The installed repository remains the runtime source of truth. v0.7.0 is the latest GitHub Pre-release. See ADRs 0002, 0004, 0005, 0006, 0007, 0008, 0009, 0010 and 0011.
