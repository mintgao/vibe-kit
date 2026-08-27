# 0007: Make Agent behavior the primary adoption interface

- Status: Accepted
- Date: 2026-08-27

## Decision

Vibe Kit treats the coding Agent, not the terminal user, as the primary installation and runtime interface. A canonical GitHub link and scoped project intent are sufficient human input. An Agent-discoverable root contract defines immutable source selection, trust checks, lifecycle choice, read-only planning, local materialization, doctor, task handoff, onboarding readiness, and natural-language workflow routing.

The existing dependency-free CLI remains the shared local installer and diagnostic engine. Its human-readable behavior stays compatible, while an additive versioned JSON interface lets Agents consume states and recovery data without parsing prose. The CLI does not resolve or download remote versions; the Agent/host performs network acquisition under its permission model and passes a selected local payload plus provenance into the installer.

Project runtime remains repository-pinned. `AGENTS.md` automatically routes ordinary development intent and performs evidence-backed onboarding when project-owned readiness is pending, missing, or stale. Internal Skills and CLI commands are not required user vocabulary. The bootstrap Plugin remains bootstrap/maintain-only and uses the same release payload and Agent contract as GitHub/offline acquisition.

## Alternatives considered

- **Human-first CLI onboarding:** rejected because it exposes archives, lifecycle verbs, health checks, and internal Skills as product concepts even though the Kit's product is Agent behavior.
- **Plugin-only installation:** rejected because it would make project behavior depend on one host/user installation and would not cover a plain GitHub link, offline bundle, collaborator, or new host.
- **Network resolver inside `bin/vibe`:** rejected because it would expand the offline materializer's authority, mix remote identity/permissions with project writes, and weaken deterministic acquisition/install separation.
- **Agent parses human terminal prose:** rejected because prose wording, warning placement, and recovery explanation are not a stable machine contract. Human-readable output remains for maintainers, while Agents receive a versioned structured interface.
- **Depend on hot reload or automatic task creation:** rejected because those capabilities are not portable across Codex/Agent hosts. A host may automate handoff, but the guaranteed fallback is one new task in the project with the original development goal preserved.
- **Agent/host resolver plus offline local materializer (selected):** keeps network access under the host permission boundary, pins a local payload before writes, and preserves one installer across GitHub, Plugin, and offline channels.
- **Infer onboarding readiness from template prose:** rejected because it is ambiguous across customized projects. A tracked project-owned state is selected, with explicit compatibility behavior when older installations lack it.

## Structured result contract

Agent result schema 1 is additive; default text and established exit codes remain compatible. Every command status list below is a closed enum:

- `plan`: `safe`, `blocked`, or `error`;
- `init`/`adopt`: `success` or `error`;
- `upgrade`: `success`, `blocked`, or `error`;
- `doctor`: `healthy`, `warning`, `broken`, or `error`;
- `validate-release`: `valid`, `invalid`, or `error`.

Every structured result includes `schema_version`, `command`, and `status`. Operations that may write also expose a closed `write_state` enum:

- `none`: the target and conflict-evidence state are unchanged;
- `project-files-written`: the requested project mutation completed;
- `conflict-evidence-written`: managed project files were unchanged, but recovery candidates were created;
- `unknown-partial`: mutation began and failure prevented a reliable complete-path inventory.

`writes_performed` may remain as a compatibility summary, but it must agree with `write_state`; a generic exception handler must not claim `false` after mutation has begun. Preflight/provenance validation failures report `none`. Installation must translate filesystem failures after the mutation boundary into a structured error whose write state is truthful and whose recovery tells the Agent to inspect/doctor the target rather than blindly retry.

Persisted onboarding schema 1 supports exactly `pending`, `complete`, and `refresh-needed`. Doctor may derive `review-required` for a missing legacy state and `invalid` for malformed state; these derived values are part of the Agent contract but are never persisted silently. `complete` is valid only with an ISO-8601 `updated_at` value and a non-empty string list of evidence paths. Install/adopt receipts report the actual preserved or created onboarding state after materialization, never an assumed `pending` value.

An unknown result schema or Agent-install protocol version fails closed. Within result schema 1, adding an optional field is backward-compatible only when consumers can ignore it without changing the meaning of any existing field or enum. Adding a required field, adding/removing/renaming a command status or onboarding/write-state enum value, changing requiredness, or changing any existing meaning requires a new declared result schema and/or Agent-install protocol version plus release cross-channel validation. Consumers must not coerce an unknown enum into a known success state.

## Trust and interaction boundaries

- The first contract recognizes only the canonical `mintgao/vibe-kit` repository by default.
- Exact tag/Release URLs select an immutable version. A bare repository selects stable only; when no stable exists, adopting a pre-release requires one explicit decision.
- No flow follows `main`, executes `curl | sh`, silently changes repositories, resolves conflicts, upgrades/downgrades an installed project, or expands filesystem/network scope.
- A safe plan after an explicit scoped install request does not require a redundant conversational confirmation. Host permission prompts remain authoritative.
- Doctor failure is not completion. Onboarding readiness and runtime activation are reported separately from installation health.
- Recorded provenance is an Agent/host attestation supplied to the local CLI. The CLI validates source-type requirements, immutable-ref shape/version agreement, and SHA-256 syntax; it does not prove that a repository owns the ref or that bytes match the digest. The resolving Agent/host must perform those checks before invoking the materializer, and receipts must not overstate CLI validation as publisher authentication.
- Install and upgrade are not whole-directory transactions. A failure after mutation begins must report `unknown-partial` unless the operation can prove a narrower state. The recovery boundary is inspect the target, run the installed doctor when runnable, and use a selected trusted payload or Git rollback; never claim an untouched target or silently retry.

## Rationale

- The Kit defines how an Agent works; exposing its implementation commands makes the human learn the wrong abstraction.
- Structured, non-interactive state is more reliable for Agents than polished terminal prose.
- Keeping remote resolution outside the installer preserves offline capability, deterministic local writes, and the existing channel-neutral architecture.
- A tracked, project-owned onboarding state lets collaborators and new hosts distinguish installation health from project-understanding readiness without upgrades overwriting project truth.

## Consequences

- README information architecture prioritizes copyable natural-language requests and relegates CLI details to maintenance/troubleshooting.
- Release validation must treat the Agent installation contract as required, versioned channel content.
- Core/Codex protocol versions advance because automatic first-run routing and structured install results are adapter behavior changes.
- Current Codex task-loading limitations still require a new-task handoff when the host cannot reload repository instructions; the fallback is one UI action, not a command or Skill invocation.
- Non-Codex Agents require their own adapter and conformance evidence before receiving the same compatibility claim.
- Release validation checks that the Agent guide, machine contract, protocol metadata, Plugin payload, and expanded marketplace agree on result/onboarding enums, channel policy, and version.
- Project-owned onboarding state is preserved by install/adopt when present and by every upgrade. A malformed state blocks truthful readiness reporting; it is not replaced automatically.

## Recovery

Revert the managed instructions, CLI, protocol metadata, Plugin guidance, and release contract through Git. Installed repositories remain pinned and can use a trusted older payload for a controlled rollback. `.vibe/onboarding.json` is project-owned and is preserved; older Kits safely ignore it.

If installation fails after mutation begins, do not infer atomic rollback. Inspect the structured `write_state`, preserve any conflict candidates, run doctor when possible, and compare/revert only the scoped Vibe Kit paths through Git or a trusted payload. Repairing whole-install permission/crash atomicity remains a separate work item; this decision requires truthful reporting rather than claiming that capability exists.
