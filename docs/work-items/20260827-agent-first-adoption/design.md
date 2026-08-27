# Design: Agent-first adoption

## Experience principle

The human interaction has two moments:

1. Give Codex the canonical Vibe Kit link plus the existing-project or new-project intent.
2. After handoff, describe the development goal in ordinary language.

Every named CLI command, archive, manifest, lifecycle operation, doctor check, onboarding Skill, task-size classification, and specialist flow is internal Agent vocabulary unless troubleshooting requires disclosure.

## State machine

```text
source resolution
  -> target and lifecycle resolution
  -> read-only preflight
  -> materialize repository-pinned files
  -> installed doctor
  -> task handoff
  -> first-run onboarding when pending
  -> resume original goal through normal workflow routing
```

An operation is complete only when the installed CLI passes doctor. Runtime readiness is separate: `pending` onboarding means the installation is healthy but the next Codex task must establish project context before substantive work.

## Source states

- Exact canonical tag or Release URL: use that immutable version. An explicit pre-release link is already a version decision.
- Bare canonical repository URL: select the latest stable Release. If none exists, present the highest eligible pre-release once and wait for approval.
- Plugin or offline bundle: use only the bundled, version-matched payload and report it as bundled/selected, never as latest.
- Fork, redirect to another repository, moving branch, missing digest, incompatible adapter, or unverified archive: stop and request a source decision. Never fall back to `main`.

## Target states

- New application intent, including a non-empty framework-generated scaffold: use `init` after the framework generator finishes.
- Established development history: use `adopt`.
- Existing healthy installation at the selected version: no-op and continue to onboarding/readiness.
- Existing different version: an install request does not silently authorize upgrade or downgrade; present installed and selected versions once.
- Managed collision or malformed `AGENTS.md`: stop before writes and show only the paths and a recommended inspection action.

## Interaction states

### Progress

Use goal language: “Checking the selected version and its impact on this project.” Do not stream archive names or commands unless they explain a delay or permission prompt.

### Success

Report, in order:

1. selected version/source and whether the operation was new-project or existing-project adoption;
2. doctor health and onboarding readiness;
3. one next action: continue automatically in a new task when the host supports it, otherwise open a task in this project and state the development goal normally.

### Blocked

Report, in order:

1. the operation is not complete;
2. whether project writes occurred;
3. the concrete blocking state;
4. one recommended recovery or the one decision that changes the outcome.

### Permissions and network

A request to adopt a precise source into a precise target supplies product-level intent for necessary reads and scoped project writes. Host permission prompts remain authoritative and should name the source, version, target, and operation. Credentials, a different host/repository, destructive conflict resolution, or extra system access require a new scoped decision.

## First run and daily routing

`.vibe/onboarding.json` is project-owned and tracked. `pending`, `complete`, and `refresh-needed` are the supported states; a missing file is compatible with an older install and treated as requiring evidence review. Upgrade never overwrites this file.

At the beginning of substantive work, the managed `AGENTS.md` checks readiness. If onboarding is not complete or durable context still contains scaffold placeholders/contradicts the repository, Codex runs the onboarding Skill internally, updates only evidence-backed context, marks the state complete, and resumes the original goal. Ordinary feature, design, implementation, debug, and verification requests are then routed without requiring a Skill name.

## Compatibility and fallback

- Default text CLI output and exit codes remain compatible.
- JSON is an additive, versioned Agent interface.
- The Plugin remains bootstrap/maintain-only.
- Core installation stays offline-capable and never resolves GitHub itself.
- Hosts that cannot reload newly installed repo instructions use a one-step new-task handoff; no CLI or Skill name is exposed to the user.
