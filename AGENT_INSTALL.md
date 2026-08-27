# Agent installation contract

This document is the Codex-facing adoption entry point for Vibe Kit. The human supplies the canonical repository link, a scoped target or new-project intent, and a development goal. Keep local CLI details internal unless troubleshooting requires them. The machine-readable source of truth is `agent-install.json`.

## Trust and source selection

- Recognize `https://github.com/mintgao/vibe-kit` as the only canonical repository by default. A fork or redirect requires a new explicit source decision.
- An exact canonical tag or Release URL selects that immutable version, including a pre-release. For the bare repository URL, select the latest stable Release only. If no stable Release exists, present the highest eligible pre-release once and wait for approval.
- Never follow `main`, execute `curl | sh`, silently select another repository, or use an archive whose published digest was not verified.
- Resolve/download remotely in the Agent or host permission boundary. `bin/vibe` is an offline local materializer and receives the selected source type, immutable ref, and artifact SHA-256 as provenance.

## Adoption state machine

1. Resolve and verify the exact source artifact against its Release metadata.
2. Resolve the target. Use `init` after a framework generator for new application intent; use `adopt` for a repository with established development history.
3. Run the corresponding plan with `--format json` and provenance arguments. Planning must be read-only.
4. If the user already requested this exact scoped install and the plan status is `safe`, apply it without a redundant confirmation. Stop on a collision, malformed managed boundary, existing different installation, or expanded permission/source scope.
5. Run the installed CLI's doctor with `--format json`. Installation succeeds only when doctor is not `broken`; report onboarding readiness separately.
6. Repository instructions normally activate at a new-task boundary. If the host cannot reload them, ask the user only to open a new Codex task in the project and state the development goal normally. Do not require a CLI command or Skill name.
7. When onboarding is pending, missing, stale, or contradicted by repository evidence, run the repository onboarding Skill internally, update evidence-backed context, mark readiness complete, and resume the original development request through normal routing.

## Blocking and recovery

On a blocked result, say that installation is incomplete, whether writes occurred, the concrete blocking paths/state, and one recovery action or material decision. Do not resolve managed conflicts, upgrade/downgrade an existing installation, replace project-owned context, or broaden host permissions silently.

The supported source states, closed command statuses, write states, persisted and derived onboarding states, result schema, protocol versions, and lifecycle states are versioned in `agent-install.json` and validated identically in the direct Release, Plugin payload, and expanded marketplace. Unknown schemas, protocols, or enum states fail closed. After a structured `unknown-partial` result, inspect the target, run its doctor when runnable, and recover with Git or the same trusted payload instead of blindly retrying.
