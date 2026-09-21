# Technical review: Host adapters (ADR 0019)

- Work item: `docs/work-items/20260921-host-adapters/brief.md`
- Artifact reviewed: `docs/decisions/0019-host-adapters.md`, revision 1 (104 lines, 2026-09-21)
- Review mode: `sequential-perspective`
- Capability limitation: an identity-isolated independent reviewer is unavailable on this host (analysis-shaped subagent packets time out at the 600 s budget; write-shaped packets complete), so this review ran as a separate sequential pass by the orchestrator against the brief's acceptance criteria and the recorded contract surfaces.
- Verdict: **changes-required** (Pass 1)

## Pass 1 — changes-required

### Blocking findings

1. **Unprovable byte claims (lines 33 and 90).** "The default `codex` preserves today's behavior byte-for-byte" and "a Codex-selected install byte-equivalent to today's install" cannot hold as written: this very change moves the contract (schema 3 → 4, the `hosts` registry, the recorded selection), so no install of the new version is byte-identical to a pre-change install. The provable claim the verification fixtures need: a Codex-selected install carries the same managed file set as today's default install — every pre-change managed path, including `.codex/agents/vibe-*.toml` and the skill-local `agents/openai.yaml` — with content differences limited to the versioned contract change itself.
2. **The release payload cannot filter by the selection (line 35).** "Install, plan, upgrade, doctor and the release payload all filter by the partition" misstates the release payload's role: the source release must carry every declared host's files (the source declares all hosts), or a Hermes-only install could not be produced from the artifact and future host re-selection would break. The partition defines the groups and the completeness the release payload must include; it never shrinks the release.

### Non-blocking notes (carried to `implementation.md`)

- Core protocol staying at 7: re-check during implementation if core-surface documents (`.vibe/core/**`) change materially; if they do, argue the bump rather than assume it.
- "No managed text requires a specific host" (AC-1/AC-4): sweep `AGENT_INSTALL.md` and the distribution copy during implementation; the Codex plugin's existence stays — only requirement-implying copy changes.
- The "Hermes entry" payload is intentionally minimal at the ADR level; implementation defines its exact shape (registry entry plus documentation) and must not grow new managed surfaces beyond the role mapping.

### Facts spot-checked against the repository

- `adapter` block and claims (`agent-install.json` 5–24), activation statics (131–187); `managed_source_files()` Codex path and glob (`bin/vibe` 1074–1076); activation fingerprint fields (1598–1605); validator pins (7933+); the six role agents; the two plugin `openai.yaml` files. All verified as stated; the author's line-range correction (1074–1076) is itself correct.
- Structural conformance: header grammar (`# 0019: ...`, exactly one `- Status: Accepted`), section order and tone mirror 0018; the index line was appended in the existing style; no other files were touched.

## Pass 2 — approved

Revision 2 (2026-09-21) was checked directly against the Pass 1 findings: both blocking fixes landed verbatim (lines 33, 35 and 90) with the line count unchanged at 104 and every other line exactly as reviewed; the non-blocking notes stay carried into `implementation.md`. Approved for implementation gating.
