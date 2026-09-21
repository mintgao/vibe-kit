# Implementation plan: takeover admission

- Work item: `docs/work-items/20260921-takeover-admission/brief.md`
- Governing decision: `docs/decisions/0018-takeover-admission.md` (Accepted, revision 2)
- Writer: single writer, Hermes orchestrator session 2026-09-21
- Rollback: revert the change commit; no data migration, no receipt-format migration, no version bump

## Scope (what the seven acceptance criteria require)

1. A new receipt kind `existing-install-admission` in the closed `receipt_kinds` vocabulary, declared in `agent-install.json` and compiled in `bin/vibe`, without touching the takeover schema version or any closed object shape.
2. Admission rules in `validate_takeover_object`: an admitting object must claim no transaction in this directory (`upgrade_transaction.transaction_id` null with a valid null pair), must carry at least one historical source reference as evidence (`apply-receipt` or `doctor-receipt` with a non-null `ref` and a non-null digest), and must present the recomputed target identity (`observed_manifest_sha256` and `observed_activation_set_sha256` non-null and equal to the context recomputed by `installed_takeover_contract_context`, never trusting recorded fingerprints).
3. The published contract: a `## Takeover object contract` section in `AGENT_INSTALL.md` (the host-facing guide, managed as one payload file) stating the closed field sets per layer, the custody transition table, the evidence ordering rules, the per-stage evidence types, the blocked-state contract, the admission kind, the receipt artifact and the minimal manual-transfer payload — bound to the compiled registry by a drift test that regenerates every published list from `TAKEOVER_CONTRACT_REGISTRY` and asserts it appears in the guide.
4. The receipt artifact: `--receipt <path>` on `doctor`, `verify`, `plan` and `upgrade`, plus `validate-takeover`, writing the exact result envelope the command prints, canonicalized for byte-stability: JSON with sorted keys, two-space indent, `ensure_ascii=False`, one trailing newline, and every string that equals the resolved project root (or is rooted at it) rewritten root-relative before serialization. Two runs on the same tree produce identical bytes; two checkouts at different parent directories produce identical bytes. The framework never writes goal text.
5. The manual-transfer payload: a closed host-neutral shape (schema version, opaque transfer identifier, goal text supplied by the host, accepted decisions, unfinished state, evidence references with digests) validated by `validate-takeover --manual-transfer <path>`: shape and limits, digest syntax, and freshness — when a referenced file resolves under the project root, its recomputed sha256 must equal the recorded digest; references that cannot resolve are reported as findings, not accepted silently.

## Steps

1. `agent-install.json`: add `existing-install-admission` to `takeover.enums.receipt_kinds` and to `contract_registry` wherever the receipt kinds are declared; keep every other vocabulary and the schema version untouched.
2. `bin/vibe`: add the same value to the compiled `TAKEOVER_CONTRACT_REGISTRY`; add `TAKEOVER_ADMISSION_RECEIPT_KIND` and the admission cross-rules in `validate_takeover_object` (after the activation block validates); add `receipt_kind`-aware handling so an admission object cannot claim a committed transaction and a non-admission object is unaffected.
3. `bin/vibe`: add `write_receipt_artifact(envelope, path, root)` and wire `--receipt` into the `doctor`, `verify`, `plan` and `upgrade` parsers and command functions; wire it into `validate-takeover` as well (validation results are receipts too).
4. `bin/vibe`: add `validate_manual_transfer_payload(value, root)` and the `validate-takeover --manual-transfer <path>` flag; when the payload is supplied alongside an object, additionally require the object's `goal.transfer_id` to equal the payload's (consistency), and when only the payload is supplied, validate it standalone.
5. Tests (`tests/test_cli.py`, `tests/fake_takeover_host.py`): fixture method `admitted()` building a valid admission object from the same context; regressions for (a) valid admission accepted, (b) admission claiming a transaction rejected, (c) admission without a historical source reference rejected, (d) admission with a forged observed fingerprint rejected, (e) receipt artifact byte-stability (same tree twice, and a second checkout at a different parent), (f) manual-transfer payload accepted with resolvable evidence and rejected on digest mismatch and on shape violations, (g) the drift test over every published list.
6. `AGENT_INSTALL.md`: the new contract section, generated content checked by the drift test.
7. Release identity: recompute `payload_tree_sha256` / `activation_set_sha256` and the three mirrors with `scripts/rebuild-mirrors.py` (from the vibekit-dev skill).
8. Evidence: full default channel on CPython 3.13 and 3.9, `doctor` healthy, `validate-readiness` valid, mirrors green; then the verification record and the commit.

## Review notes carried from `technical-review.md` (Pass 1, notes 2–4)

- Publication location (note 2): fixed as `AGENT_INSTALL.md` § "Takeover object contract"; the drift test binds the section's lists to the compiled registry, so a registry change without a guide change fails the channel.
- Byte-stability (note 3): the root-relative rewrite and the canonical serializer above; step 5(e) proves both directions.
- Re-derivation (note 4): the admission rules compare against the context recomputed at validation time; step 5(d) proves a forged fingerprint is rejected.