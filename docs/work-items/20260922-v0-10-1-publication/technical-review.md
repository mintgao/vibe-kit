# Technical review: Publish Vibe Kit v0.10.1

## Review pass — approved

- Reviewer perspective: read-only Tech Lead reviewer, recorded as a distinct
  sequential-perspective pass by the Hermes orchestrator (session 2026-09-22),
  separate from the Tech Lead author that wrote the record.
- Reviewed artifact: `docs/decisions/0021-v0-10-1-publication.md`
  (175 lines, `Status: Accepted`), authored on 2026-09-22.
- Work item: `docs/work-items/20260922-v0-10-1-publication/brief.md`.
- Capability limitation: this host has native subagents, but analysis-shaped
  review packets exceed its 600 s session budget (measured 4/4 on 2026-09-21),
  so the review is a sequential-perspective pass rather than an
  identity-isolated independent reviewer. The limitation is recorded here
  rather than hidden, as the core readiness contract requires.

Verdict: the record is complete, internally consistent and true to the
repository at `bd9db6e`. Every claim below was re-checked against the working
tree, not taken from the author's summary.

## Claims verified against the repository

| # | Claim in the record | Verification |
|---|---|---|
| 1 | Source version identity reads `0.10.0` in `.vibe/core/version`, `.vibe/version`, `agent-install.json#kit_version` and the Plugin metadata | All four confirmed byte-equal to `0.10.0` |
| 2 | The maintenance-bridge bound sits at `0.10.0` | `bin/vibe:8278` `maximum_installed_kit_version_exclusive`, mirrored at `agent-install.json#maintenance_bridge` — confirmed |
| 3 | The predecessor-migration target and its compiled digest literal move together | `bin/vibe:268` target `framework_version` plus the checked literal at `:282-283`; both mirrors carry the byte-equal digest `cf0b7a15…` (`.vibe/core/protocol.json#predecessor_migrations.registry_sha256`, `agent-install.json#maintenance_bridge.predecessor_migrations.registry_sha256`) — confirmed |
| 4 | Two plan/upgrade branches and the migration target guard compare the target literally against `0.10.0` | `bin/vibe:1358-1360`, `:5614`, `:6073` — confirmed, exactly three version-literal sites besides the registry target |
| 5 | Moving the publication intent/receipt schema to `5` cannot weaken historical validation | `PUBLICATION_INTENT_SCHEMA`/`PUBLICATION_RECEIPT_SCHEMA` are read only for the current contract mirrors (`bin/vibe:8105-8107`, `:8552-8554`, `:10002-10004`); historical validation runs through `HISTORICAL_PUBLICATION_INTENT_SCHEMA`/`HISTORICAL_PUBLICATION_RECEIPT_SCHEMA` (`:10280`, `:11457`) and per-profile dispatch (`:11292`, `:11842`, `:12073`) — confirmed, and this is the material check the schema decision depends on |
| 6 | No schema-5 closeout is needed and the closeout dispatch stays unchanged | `bin/vibe:13442-13447` selects only schema 3 or 4 and fails closed with a generic message otherwise; `V100_CLOSEOUT_ISSUES` remains the v0.10.0 graph — confirmed |
| 7 | The managed-guide drift check already exists and binds all three literals plus the schema number | `tests/test_v010_publication.py::ManagedGuideDriftTests` (lines 340-375) — confirmed; no second check is needed |
| 8 | The nine-name smoke set follows the published-predecessor convention | The v0.10.0 profile carries 2 base smokes plus the six predecessors 0.3, 0.5–0.9; the record retargets those six and adds the 0.10.0 predecessor — consistent |
| 9 | The AC-1…AC-6 prepublication/postpublication mapping matches the brief | Brief criteria AC-1…AC-6 map one-to-one; AC-6 is the only `live-read-back` criterion and AC-1…AC-5 are `passed` — confirmed |
| 10 | The label claim is backed by the recorded evidence | `HOST_REGISTRY.hermes.conformance` reads `verified` with `docs/work-items/20260921-host-adapters/conformance.md`; `agent-install.json#hosts.hermes.conformance` mirrors it; the Codex refresh stays a delivered handoff — confirmed |

## Findings

1. **Editorial (corrected in place).** The shared-helper paragraph named "the six
   that carry a schema-4 (or schema-2/3/4) condition". The code carries seven
   such sites — `bin/vibe:11087` (authorization field set and its
   source-reference/binding-time validation), `:11221` (exact asset-name
   closure), `:11241` (operation natural-key grammar), `:11292` (intent
   dispatch), `:11343` and `:11355` (publication-plan schema selection and
   profile lookup), `:11842` (receipt dispatch) and `:12073` (validate-publication
   command dispatch) — grouped as the record's six bullets. The count now reads
   "seven sites — six grouped checks", and the bullet list is unchanged.
2. **Non-blocking implementation note.** The record fixes the schema change but
   leaves the module constant names implicit: implementation must move
   `PUBLICATION_INTENT_SCHEMA` and `PUBLICATION_RECEIPT_SCHEMA` to `5` together
   with the contract mirrors, because `validate_agent_install_contract_shape`
   compares `agent-install.json#publication` against those constants and
   `ManagedGuideDriftTests` compares the guide's publication-boundary schema
   number against `PUBLICATION_INTENT_SCHEMA`. `ISSUE_CLOSEOUT_INTENT_SCHEMA`
   stays `3`.
3. **Non-blocking implementation note.** `tests/test_v010_publication.py` mixes
   profile pins with source-version pins: the profile pins (its
   `PUBLICATION_PROFILES[4]` identity block) stay byte-exact, while the
   source-version pins (`self.version`, the contract `kit_version`, the bridge
   bound and the migration target) move with the identity. The schema-5 profile
   gets its own evidence file rather than reusing the schema-4 fixtures.
4. **Non-blocking implementation note.** The publication-plan branch
   (`:11343`) and the validate-publication dispatch (`:12073`) must admit `5`
   while still refusing anything else; both already fail closed with generic
   messages, so no message change is required.

No finding changes the decision. The gate may be confirmed
`implementation-ready` for this work item.