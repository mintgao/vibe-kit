# Implementation report

- Work item: `20260921-host-neutral-manual-activation`
- Role: one RD writer (Hermes orchestrator acting as RD for this repository, no recursive delegation).
- Gate: `implementation-ready` (ADR 0015 Accepted; independent Tech Lead review approved on revision 2).
- Governing boundary: ADR 0015, `docs/work-items/20260921-host-neutral-manual-activation/brief.md` AC-1..AC-7.

## Implemented changes

### Managed contract surfaces (payload files)

- `AGENTS.md` managed block — one prose paragraph, single physical line: it now follows "the takeover schema they declare" instead of a hard-coded number, states that the manual path is host-neutral and that any host which can start a new task in the same project may own the successor task, and ends the degraded path with "create a new task in the same project". The block was written only after the host's protected-file approval was granted; the first attempt was refused pending consent, and the identity regeneration was repeated for the written block.
- `AGENT_INSTALL.md` — "Codex-facing" became "Agent-host-facing"; the heading "Activation and current Codex capability" became "Activation and current adapter capability"; a new paragraph after the three activation paths states the host-neutral scope of the manual path, that `adapter` metadata and the activation fingerprint describe the host that installed or adopted the version, and that a host which cannot recompute the installed identities must take the degraded stop rather than supply a receipt; "Do not infer them from the current Codex tool surface" gained "or from any other host's tool surface"; the degraded action and its quoted Chinese message became host-neutral.
- `bin/vibe` — the two printed fallback instructions lost the host name.
- `distribution/plugin-src/vibe-kit/skills/vibe-bootstrap/SKILL.md` and `.../vibe-maintain/SKILL.md` — the manual-fallback action lost the host name and now states the host-neutral manual path; "supplies neither same-task reload nor automatic successor", "do not say ready" and "currently claim only the manual fallback" are preserved.
- `README.md` and `README.zh-CN.md` — the fallback sentence names the host-neutral action; the Codex verified-integration claim is unchanged; the documentation facts required by `tests/test_readiness_doc_gates.py` are preserved.
- `CHANGELOG.md` — the published 0.9.0 section is recorded.

### Release identity

- Regenerated `agent-install.json#activation.activation_set_sha256` from `source_activation_identity(ROOT)`: `db8c95b7bfab0003247b5068d92daad45d98c73d4a2b186d427579910553fc30`. The contract-text edits moved it from `ba3491c1…081a` to `5993719c…b9b0`, and the managed-block write moved it again to this value; the last regeneration ran after every payload edit.
- Regenerated `.vibe/manifest.json` and `.vibe/version` through a production `init --source-type local-payload --source-ref 0.9.0` install in a disposable directory, then copied them into the source checkout; `agents_block_hash` is `05b27773496d4259063fd1eef987f3ccd5624b9fa7b3ad983f5ac339fa12bfef`.
- Regenerated the Plugin payload identity in `distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json`: `6d6c8e275d6f47cc653d5465384c07aab83e0882656dd58b7a77acf9e43b1e76`, equal to `payload_tree_sha256(ROOT)` and to the manifest's `source.payload_tree_sha256`.
- No schema, protocol, enum, validator, receipt, custody or CLI-result change; `agent-install.json` keeps its closed top-level field set and adapter capability claims. No version or protocol bump.

### Regression tests (not payload)

New `tests/test_release_identity.py` (6 tests): payload-digest mirror agreement with a failure message naming the regeneration procedure; `./bin/vibe package` buildability on the current tree; activation-mirror agreement with the recomputed identity; takeover-schema agreement with the installed contract; host-neutral manual-fallback wording across the surfaces; and the host-neutral manual-path statement in `AGENT_INSTALL.md`. With the managed block written, the two subtests that previously self-skipped for `AGENTS.md` now execute and pass.

The first QA pass found that the pre-approval skip guard failed open: reintroducing the old wording in `AGENTS.md` made the check skip instead of failing. The guard is removed and the checks were hardened with positive assertions (the host-neutral sentence and `host-neutral` must be present in both `AGENT_INSTALL.md` and `AGENTS.md`). Five mutations were then verified to fail the suite: `AGENTS.md` regaining "new Codex task", `AGENTS.md` hard-coding `takeover schema 1`, the host-neutral clause removed from `AGENTS.md`, `bin/vibe` printing "Codex task", and the bootstrap Skill regaining "Codex task".

## Focused verification (RD)

| Check | Command | Result |
|---|---|---|
| Default lane, CPython 3.13.9 | `python3 -m unittest discover -s tests` | Ran 86 tests, OK, no skips |
| Default lane, CPython 3.9.6 | `/usr/bin/python3 -m unittest discover -s tests` | Ran 86 tests, OK, no skips |
| Installation health | `./bin/vibe doctor . --format json` | `healthy`, activation match `db8c95b7…fc30`, no diagnostics or warnings |
| Managed region | `./bin/vibe inspect-managed-agents . --format json` | `valid`, span 0–7123 |
| Readiness record | `./bin/vibe validate-readiness . --brief …/brief.md --format json` | `valid`, no findings |
| Release candidate | `./bin/vibe package --output <scratch>` then `validate-release` | built; `valid`, 36 payload files, digest `6d6c8e27…1e76` |
| Whitespace | `git diff --check` | clean |

Independent QA owns the complete default `./bin/vibe verify . --format json` run on the frozen candidate; RD did not run that matrix. The first QA run covered the candidate before the managed-block write, so a second complete run is required by the changed shared candidate state and is recorded in `verification.md`.
