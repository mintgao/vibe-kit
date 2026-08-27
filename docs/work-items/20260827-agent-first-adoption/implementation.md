# Implementation plan: Agent-first adoption

## Planned changes

1. Add root `AGENT_INSTALL.md` and `agent-install.json`, include both in release payloads, and validate their schema/protocol/channel consistency.
2. Add additive JSON rendering for plan, install/adopt, upgrade, doctor, and release validation, including structured errors and provenance inputs.
3. Add project-owned `.vibe/onboarding.json`, doctor readiness reporting, AGENTS first-run routing, and onboarding completion instructions.
4. Update bootstrap/maintenance Skills so Agents use structured internal operations and expose only material user decisions.
5. Reorder README around natural-language Agent usage and move manual commands under maintenance/troubleshooting.
6. Bump the development kit/core/Codex adapter contract to `0.5.0` / protocol 3, document the unpublished candidate, and refresh durable product/architecture context.
7. Add focused scenario, packaging, preservation, error, and compatibility tests; self-upgrade the canonical manifest only after implementation is accepted.

The 0.5.0 release candidate also integrates the separately accepted Technical Decision Readiness Gate. Its managed workflow contract, Tech Lead role, ADR 0008, work item, and workflow-contract tests remain independently owned; Agent-first structured results and release validation distribute them without redefining that decision. The separate permission-safe atomic upgrade work item is not implemented by this release.

## Verification strategy

- Unit/scenario tests for JSON safe, blocked, success, warning, broken, and structured exception paths.
- Fresh init/adopt with pending onboarding and source provenance; preservation of a pre-existing onboarding state.
- Release build and validation proving `AGENT_INSTALL.md` and `agent-install.json` are identical across release, Plugin, and marketplace payloads.
- Installed AGENTS/Skill inspection proving first-run onboarding and natural-language routing are present without requiring a user-visible Skill invocation.
- Full configured suite, `doctor`, bytecode compilation, unpublished package validation, and an independent criterion-to-evidence QA pass.

## Rollback

Git revert restores the prior managed instructions, CLI, templates, protocol, and documentation. Installed projects can use a trusted older payload through the existing controlled upgrade path; project-owned onboarding state is preserved and may be ignored by older versions. Do not edit manifest/version fields manually.
