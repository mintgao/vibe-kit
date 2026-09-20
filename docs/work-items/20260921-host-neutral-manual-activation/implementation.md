# Implementation report

- Work item: `20260921-host-neutral-manual-activation`
- Role: one RD writer (Hermes orchestrator acting as RD for this repository, no recursive delegation).
- Gate: `implementation-ready` (ADR 0015 Accepted; independent Tech Lead review approved on revision 2).
- Governing boundary: ADR 0015, `docs/work-items/20260921-host-neutral-manual-activation/brief.md` AC-1..AC-7.

## Implemented changes

### Managed contract surfaces (payload files)

- `AGENT_INSTALL.md` — "Codex-facing" became "Agent-host-facing"; the heading "Activation and current Codex capability" became "Activation and current adapter capability"; a new paragraph after the three activation paths states the host-neutral scope of the manual path, that `adapter` metadata and the activation fingerprint describe the host that installed or adopted the version, and that a host which cannot recompute the installed identities must take the degraded stop rather than supply a receipt; "Do not infer them from the current Codex tool surface" gained "or from any other host's tool surface"; the degraded action and its quoted Chinese message became host-neutral.
- `bin/vibe` — the two printed fallback instructions lost the host name.
- `distribution/plugin-src/vibe-kit/skills/vibe-bootstrap/SKILL.md` and `.../vibe-maintain/SKILL.md` — the manual-fallback action lost the host name and now states the host-neutral manual path; "supplies neither same-task reload nor automatic successor", "do not say ready" and "currently claim only the manual fallback" are preserved.
- `README.md` and `README.zh-CN.md` — the fallback sentence names the host-neutral action; the Codex verified-integration claim is unchanged; the documentation facts required by `tests/test_readiness_doc_gates.py` are preserved.
- `CHANGELOG.md` — the published 0.9.0 section is recorded.

### Release identity

- Regenerated `agent-install.json#activation.activation_set_sha256` from `source_activation_identity(ROOT)`: `5993719ca50d11c75c7850e4d5680615052a84c3a9efb15c451340d4d502b9b0` (was `ba3491c1…081a`).
- Regenerated `.vibe/manifest.json` and `.vibe/version` through a production `init --source-type local-payload --source-ref 0.9.0` install in a disposable directory, then copied them into the source checkout.
- Regenerated the Plugin payload identity in `distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json`: `96ad3f1425def11bff6b0a6268252ee99a5e9f1158ccbe91997225acf80af1ae` (was `0251f492…f5f3`), equal to `payload_tree_sha256(ROOT)` and to the manifest's `source.payload_tree_sha256`.
- No schema, protocol, enum, validator, receipt, custody or CLI-result change; `agent-install.json` keeps its closed top-level field set and adapter capability claims. No version or protocol bump.

### Regression tests (not payload)

New `tests/test_release_identity.py` (6 tests): payload-digest mirror agreement with a failure message naming the regeneration procedure; `./bin/vibe package` buildability on the current tree; activation-mirror agreement with the recomputed identity; takeover-schema agreement with the installed contract; host-neutral manual-fallback wording across the surfaces; and the host-neutral manual-path statement in `AGENT_INSTALL.md`. The two checks that include the managed `AGENTS.md` block skip themselves while that block still carries the pre-approval text, naming the pending surface below as the reason.

## Pending surface (not implemented)

The managed `AGENTS.md` block is unchanged. Its write is blocked by the host's protected-file approval prompt, which timed out without a user response; the host reported "the user has NOT consented to this write" and forbids retrying the same edit through another path. AC-1 and AC-2 therefore remain unmet for that one surface: the block still says "takeover schema 1" and "create a new Codex task in the same project". The exact replacement text is recorded in `implementation-plan` item 1 of this report's revision history and in the work-item brief's design notes; applying it requires an approved write, after which the activation identity and payload digest must be regenerated again and the two self-skipping checks will run.

## Focused verification (RD)

| Check | Command | Result |
|---|---|---|
| Default lane, CPython 3.13.9 | `python3 -m unittest discover -s tests` | Ran 86 tests, OK (skipped=2) |
| Default lane, CPython 3.9.6 | `/usr/bin/python3 -m unittest discover -s tests` | Ran 86 tests, OK (skipped=2) |
| Installation health | `./bin/vibe doctor . --format json` | `healthy`, activation match `5993719c…b9b0`, no diagnostics or warnings |
| Managed region | `./bin/vibe inspect-managed-agents . --format json` | `valid`, span 0–6913 |
| Readiness record | `./bin/vibe validate-readiness . --brief …/brief.md --format json` | `valid`, no findings |
| Release candidate | `./bin/vibe package --output <scratch>` then `validate-release` | built; `valid`, 36 payload files, digest `96ad3f14…f1ae` |
| Whitespace | `git diff --check` | clean |

Independent QA owns the complete default `./bin/vibe verify . --format json` run on the frozen candidate; RD did not run that matrix.
