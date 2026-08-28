# 0009: Make post-upgrade takeover host-orchestrated and evidence-gated

- Status: Accepted
- Date: 2026-08-28
- Decision owner: Tech Lead perspective
- Prior decision history: Accepted on 2026-08-28 after independent review; amended and re-accepted after QA-triggered installed-contract and executable-conformance repairs; reopened again after real-project acceptance proved that the official v0.5.0 source state cannot enter the newly managed 0.6.0 contract boundary
- Review: Authenticated-predecessor compatibility amendment approved by the distinct independent Tech Lead instance on 2026-08-28 after digest verification and corrections for symlink-free path authentication, predecessor-source exclusion, exact cross-channel mirror shapes and the normative maintenance-bridge object.

## Context

Vibe Kit 0.5.0 can safely plan and materialize a trusted payload, report truthful
write state, diagnose installed version integrity and expose onboarding readiness.
It cannot prove that a running task loaded newly installed repository instructions,
transfer an unfinished goal to another task, or derive that the project is ready
for continued development.

The accepted product behavior requires one continuous Agent-owned experience after
one exact-version confirmation:

1. resolve and verify the exact target payload;
2. run a read-only plan and safely apply it;
3. prove installed target-version health;
4. activate the target-version repository runtime;
5. adapt project-owned context when evidence requires it;
6. run required installed and project verification;
7. re-evaluate the unfinished goal under the target rules; and
8. resume it or report the exact blocker.

This changes the shared Agent-install lifecycle, result compatibility,
host/Agent ownership, privacy boundary and release conformance. ADR 0007 does not
fully govern those changes. Published Vibe Kit 0.5.0 is immutable and must not be
rewritten.

## Decision

Post-upgrade takeover is a **host-orchestrated, evidence-gated lifecycle**.

The offline CLI remains responsible for trusted-payload materialization, project
diagnostics and configured project-check execution. It can prove filesystem and
process facts. It must never claim runtime activation, goal custody, adaptation,
target-rule re-evaluation or overall readiness.

The host-side Agent adapter owns:

- the takeover evidence object;
- runtime capability negotiation;
- activation-path selection;
- original-goal custody;
- onboarding/adaptation routing;
- final verification aggregation;
- target-rule re-evaluation;
- readiness derivation; and
- the final user-facing completion message.

The selected target payload's verified maintenance bridge governs plan/apply
before project writes. Reading that target maintenance contract is not runtime
activation; installed project rules remain at the source-task generation until
positive activation evidence exists.

ADR 0005 remains unchanged: the Plugin stays bootstrap/maintain-only and gains no
MCP server, hook, app, background updater or implicit network authority. ADR 0007
continues to govern trust, repository pinning and Agent-first installation. ADR
0008 governs target-rule technical-decision readiness. The separate
permission-safe atomic-upgrade work exclusively owns multi-file transaction and
rollback mechanics.

## Installed takeover contract ownership

`AGENT_INSTALL.md` and `agent-install.json` are no longer release-only discovery
documents. In 0.6.0 they are both:

- framework-managed installed files;
- normative inputs to the manual successor;
- recorded members of `.vibe/manifest.json.managed_files`;
- activation-critical files;
- covered by normal install/adopt collision preflight;
- covered by three-way upgrade conflict and local-modification handling; and
- required by installed doctor.

They remain release payload files as well. Release packaging deduplicates paths so
the direct Release, Plugin payload and marketplace contain one byte-identical copy
of each.

`managed_source_files()` includes both root-relative paths:

- `AGENT_INSTALL.md`
- `agent-install.json`

A 0.2.x–0.5.x upgrade creates them when absent. The general rule remains that an
existing untracked path which differs from the incoming contract is a managed
collision or conflict and is never silently overwritten. A path already
byte-identical to the target may still be adopted under the existing rule.

The only differing-content exception is the closed authenticated predecessor
migration below. It applies solely to the exact official v0.5.0 two-file contract
set during an exact 0.5.0-to-0.6.0 upgrade. It does not infer ownership from a
filename, one matching file, a version string, Git ancestry, source-channel text or
user intent.

After installation, local edits receive the same three-way protection as other
managed files. A hash mismatch is blocking for activation and readiness.

The installed activation set includes both files. Its runtime discovery roots
therefore also include `AGENT_INSTALL.md` and `agent-install.json`. If a future
target release removes either file, existing copies are preserved under the
established no-automatic-stale-deletion policy, but they are classified as
`stale-runtime-path-preserved` and block activation until explicitly reviewed.
They are never silently reclassified as project-owned.

Installed doctor must:

1. require both files;
2. verify their manifest hashes;
3. validate `agent-install.json` against the installed schema/protocol registry;
4. verify its kit, core, adapter and activation identities against the installed
   manifest and `.vibe/core/protocol.json`;
5. validate the minimum `AGENT_INSTALL.md` header, canonical source reference and
   machine-contract reference; and
6. return `broken` when any check fails.

Add the blocking doctor error codes `agent-install-guide-invalid` and
`agent-install-contract-invalid`. A missing file may additionally produce the
existing `managed-file-missing` diagnostic; duplicate diagnostics must still refer
to distinct failed checks.

This changes no project-owned boundary. `.vibe/project.yaml`,
`.vibe/project-rules.md`, `.vibe/onboarding.json` and `docs/` remain project-owned
and upgrade-preserved.

## Authenticated v0.5.0 predecessor-contract migration

### Supported boundary and authority

The target 0.6.0 CLI contains one closed predecessor-migration registry. The
authoritative registry is compiled into the selected target `bin/vibe`; editable
installed project state cannot add, remove or weaken an entry.

The registry is exactly:

```json
{
  "entries": [
    {
      "migration_id": "v0.5.0-unmanaged-agent-contracts-v1",
      "mode": "replace-and-adopt-complete-set",
      "paths": {
        "AGENT_INSTALL.md": "321a2e1017a09405b1d44570f21f59e0b135c127abd81f9d8258c89b3f95a304",
        "agent-install.json": "3ac9c51a83f1487fb298c0fd919bca99252c8972b138ae4925d44ee1544ffb4f"
      },
      "predecessor": {
        "adapter_name": "codex",
        "adapter_protocol": 3,
        "agent_install_protocol": 1,
        "agent_install_schema": 1,
        "core_protocol": 3,
        "framework_version": "0.5.0",
        "install_identity_sha256": "70dd0eac0f54d328a803bc71ef409f66c0a6d8dc8016ce27bb80b2fa4b410fb5",
        "manifest_schema": 1
      },
      "target": {
        "framework_version": "0.6.0",
        "source_types": [
          "github-release",
          "plugin-bundled",
          "offline-bundle",
          "local-payload"
        ]
      }
    }
  ],
  "schema_version": 1
}
```

Canonical JSON means UTF-8 output from the equivalent of Python
`json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`.
Array order is significant. The canonical registry SHA-256 is:

```text
6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d
```

The same exact closed mirror object is required at all three JSON pointers:

- `agent-install.json#/maintenance_bridge/predecessor_migrations`
- `.vibe/core/protocol.json#/predecessor_migrations`
- `release-manifest.json#/predecessor_migrations`

Each pointer's value is exactly:

```json
{
  "schema_version": 1,
  "registry_sha256": "6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d",
  "authority": "target-cli-compiled",
  "modes": ["replace-and-adopt-complete-set"]
}
```

All four members are required and no additional member is allowed.
`schema_version` is a JSON integer exactly `1`, not a boolean or numeric string.
`registry_sha256` is a lowercase 64-hex JSON string equal to the target CLI's
independent canonical recomputation. `authority` is the exact JSON string
`target-cli-compiled`. `modes` is an array containing exactly the one shown string
in the shown order.

The target CLI recomputes the canonical digest from its compiled authoritative
registry and compares it with the exact constant
`6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d`;
it does not trust a mirror-provided digest. Before a migration plan can be safe,
the target payload's Agent-install and core-protocol mirror objects must both be
present, closed, valid and deeply equal to the exact object above. Installed doctor
applies the same two checks after upgrade. Release validation additionally requires
the release-manifest mirror and exact deep equality among all three mirrors and the
compiled registry.

The registry digest covers only the canonical authoritative registry object:

```json
{"entries":[...],"schema_version":1}
```

It excludes all three mirror objects. This avoids registry/mirror self-reference.
The exclusions do not remove the mirrors from normal artifact identity:

- the compiled registry is part of raw `bin/vibe`;
- the Agent-install mirror is part of raw `agent-install.json`;
- the core mirror is part of raw `.vibe/core/protocol.json`;
- all three files participate in `payload_tree_sha256`, installed managed-file
  hashing and activation-v2 identity;
- activation-v2 normalization zeros only
  `agent-install.json#/activation/activation_set_sha256`; it does not remove or
  zero the predecessor-migration mirror;
- the release-manifest mirror is outside the payload and activation set, but the
  release manifest is covered by its exact `SHA256SUMS` entry and semantic release
  validation; and
- direct Release, Plugin payload and marketplace payload must contain byte-identical
  `bin/vibe`, `agent-install.json` and `.vibe/core/protocol.json`.

A missing mirror; a null, scalar or array in place of the object; a missing or extra
member; a boolean/string schema version; uppercase, malformed or incorrect digest;
wrong authority; non-array, empty, duplicated or extended modes; mirror divergence;
or a registry/mirror digest mismatch fails closed before migration writes.
Refreshing payload hashes, activation hashes, release checksums or manifest hashes
after such a semantic mutation does not make the package valid.

`agent-install.json`, `.vibe/core/protocol.json` and the release manifest declare
predecessor-migration schema 1, this digest, authority
`target-cli-compiled`, and mode `replace-and-adopt-complete-set`. These are
cross-channel mirrors, not independent authorization. `bin/vibe` rejects a mirror
mismatch before project writes. The migration registry itself excludes these
mirrors from its digest and therefore introduces no digest self-reference.

The selected target payload must first satisfy the existing channel-specific trust
and payload-tree requirements. The verified target payload binds the compiled
registry to the selected CLI. `github-release` and `offline-bundle` additionally
require their existing artifact SHA-256 evidence; `plugin-bundled` requires the
Plugin payload-tree match; `local-payload` remains an explicitly selected local
payload and must not claim publisher authentication. Marketplace distribution uses
the same `plugin-bundled` bytes and is not a fifth source type.

The predecessor manifest's top-level `source` member is excluded entirely from
migration eligibility. After the manifest has been parsed as one duplicate-key-free
JSON object, the migration predicate does not require, access, type-check or
normalize `source`. It may be absent or contain any JSON value without changing an
otherwise identical eligibility result.

The official v0.5.0 source checkout value:

```json
{"type":"local-payload","ref":null,"artifact_sha256":null}
```

is retained as positive fixture evidence, not as a credential. This amendment does
not invent a closed historical v0.5.0 channel schema. There are consequently no
“invalid predecessor source” eligibility cases: malformed whole-manifest JSON and
duplicate JSON keys remain invalid manifests, while a well-formed `source` value
cannot either authenticate or disqualify the predecessor.

Target-payload provenance remains independently mandatory under the existing
0.6.0 channel-specific source contract. An official-looking predecessor `source`
value cannot compensate for a wrong version, hash, path type, installation identity
or incomplete contract set.

Hard-coded v0.5.0 hashes are acceptable because 0.5.0 is an immutable published
release and this is a closed compatibility exception. The v0.5.0 tag, release
commit and Git blob identifiers are audit evidence only; runtime does not require
Git or network access and does not infer identity from repository ancestry.

### Predecessor authentication

Before recognizing the migration, the target CLI must establish all of the
following using only Python 3.9-compatible standard-library operations:

1. the target CLI and selected payload version are exactly `0.6.0`;
2. the installed manifest is schema 1, is a regular non-symlink file, and declares
   framework version exactly `0.5.0`;
3. `.vibe/version` and `.vibe/core/version` are regular non-symlink files and both
   declare exactly `0.5.0`;
4. the installed core protocol is the manifest-recorded official v0.5.0 file and
   declares core protocol 3, Agent-install protocol 1 and Codex adapter protocol 3;
5. both migration paths are absent from the predecessor manifest's
   `managed_files`;
6. the normalized predecessor installation identity equals the registered digest;
7. every predecessor `managed_files` path has a symlink-free path chain below the
   canonical project root, ends in a regular non-symlink file, and has raw SHA-256
   equal to its recorded hash;
8. `AGENTS.md` has a symlink-free path chain below the canonical project root,
   exists as a regular non-symlink file, and its current managed block equals the
   predecessor manifest's `agents_block_hash`; project instructions outside that
   block are ignored; and
9. both migration paths have symlink-free path chains below the canonical project
   root, exist as regular non-symlink files, and their raw SHA-256 values equal the
   registry as one complete set.

A symlink-free path chain is checked component-by-component with `lstat`. Every
existing intermediate component below the canonical project root must be an actual
directory and must not be a symlink; the leaf must have the type required above.
No intermediate-directory symlink is permitted, even if it resolves inside the
project or to official bytes. A missing intermediate component, non-directory
intermediate component, symlink, broken symlink, unreadable component or type race
fails authentication.

The CLI's existing resolution of the user-supplied project argument defines the
canonical project root. This amendment does not change project-root selection, but
no relative migration or predecessor-identity path may traverse a symlink below
that resolved root.

Failure of item 7 or 8 invalidates the predecessor installation as a whole.
Therefore a missing, wrong-type, symlinked, broken-symlinked, unreadable or
hash-mismatched `AGENTS.md`, managed predecessor leaf, or intermediate directory
makes both `AGENT_INSTALL.md` and `agent-install.json` migration paths conflicts.
It must not fall back to independent per-file update or creation.

The normalized predecessor installation identity is the canonical SHA-256 of:

```json
{
  "agents_block_hash": "<manifest agents_block_hash>",
  "framework_version": "<manifest framework_version>",
  "managed_files": {"<path>": "<sha256>"},
  "schema_version": "<manifest schema_version>"
}
```

For the official v0.5.0 manifest it is:

```text
70dd0eac0f54d328a803bc71ef409f66c0a6d8dc8016ce27bb80b2fa4b410fb5
```

The canonical SHA-256 of the registry's two-path hash map is:

```text
5ae7da78e4799f23056afc16b8b1511384b12db50dfb5209a64e5b465a71b15d
```

No partial authentication is permitted.

- Both registered predecessor files plus every predecessor check above matching:
  eligible migration.
- Both paths absent: ordinary target-file creation, not a migration.
- Existing paths which are target-byte-identical, or a target-identical/absent
  combination with no predecessor member present: ordinary no-op/create/adoption,
  not a migration.
- One predecessor member missing, modified, target-identical, the wrong filesystem
  type or a symlink: the predecessor set is incomplete and both migration paths are
  conflicts.
- One predecessor member combined with any other bytes is a conflict for both
  migration paths.
- Both official predecessor bytes under an unknown version, malformed manifest,
  mismatched normalized installation identity or unhealthy predecessor managed set
  are conflicts for both migration paths.
- Arbitrary differing bytes which do not authenticate as this complete set remain
  ordinary untracked managed conflicts.

A symlink or broken symlink at a migration leaf, predecessor-identity leaf,
`AGENTS.md`, or any intermediate component is present for collision purposes and
is never treated as an absent path. All path-chain decisions use component-wise
`lstat`; raw hashing occurs only after the chain and regular-file type have been
accepted. `Path.exists()` and symlink-following `is_file()` are insufficient for
migration authentication.

This exception is path-exact. It grants no ownership to any other untracked path
and does not change the project-owned boundary. Project-owned files and arbitrary
unknown paths remain byte-preserved.

### Plan and result evidence

An authenticated plan uses the existing action `update` for both paths. It does
not add an `adopt`, `migrate` or other action enum.

The exact plan entries are:

```json
{"action":"update","path":"AGENT_INSTALL.md","note":"authenticated predecessor migration v0.5.0-unmanaged-agent-contracts-v1; complete set"}
{"action":"update","path":"agent-install.json","note":"authenticated predecessor migration v0.5.0-unmanaged-agent-contracts-v1; complete set"}
```

The two entries contribute to the existing `update` count. Overall plan status is
`safe` only when no other conflict exists, and planning remains read-only.

Plan and upgrade JSON may add the optional top-level field
`compatibility_migrations`. Each member has exactly:

```json
{
  "schema_version": 1,
  "migration_id": "v0.5.0-unmanaged-agent-contracts-v1",
  "phase": "planned",
  "authentication": "target-cli-compiled-registry",
  "from_version": "0.5.0",
  "to_version": "0.6.0",
  "paths": ["AGENT_INSTALL.md", "agent-install.json"],
  "predecessor_install_identity_sha256": "70dd0eac0f54d328a803bc71ef409f66c0a6d8dc8016ce27bb80b2fa4b410fb5",
  "predecessor_contract_set_sha256": "5ae7da78e4799f23056afc16b8b1511384b12db50dfb5209a64e5b465a71b15d",
  "registry_sha256": "6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d"
}
```

`phase` is `planned` in plan output, `applied` only in a successful upgrade
receipt, and `unknown-partial` when an accepted migration entered mutation but the
overall upgrade became `unknown-partial`. An upgrade which writes no migration
member omits this field.

This is an ignorable additive schema-1 field. Existing command names, statuses,
actions, counts, write states, `writes_performed` rules and recovery meanings do
not change. Unknown or malformed migration evidence is never interpreted as
successful authentication.

An incomplete or unauthenticated predecessor set uses the existing conflict action
and note:

```text
untracked managed path differs; predecessor migration not authenticated
```

When one registered predecessor member is present but the set is incomplete, both
registered paths appear in the conflict and recovery path lists.

### Apply, TOCTOU and installed ownership

Apply never trusts a prior plan receipt. It independently repeats target-source,
compiled-registry, predecessor-installation and complete-set authentication.

It performs these checks:

1. once during ordinary apply preflight;
2. again for the complete two-file set immediately before the first project-file
   mutation; and
3. with `lstat` and raw SHA-256 immediately before replacing each migration member.

A mismatch before any project-file mutation stops normal apply, reports both
migration members as conflicts, and may write only the established incoming
conflict candidates with `write_state=conflict-evidence-written`.

A mismatch or filesystem failure after any project-file mutation stops immediately
with the existing `write_state=unknown-partial`. It cannot activate, adapt, verify
or claim ready. No retry, snapshot, transaction or rollback behavior is added.

On success, both predecessor files are replaced by the selected target 0.6.0
bytes. The final manifest records their target raw hashes as ordinary
`managed_files`; activation paths and `path_hashes` use only target 0.6.0 identity.
Installed doctor then validates them under the existing activation-critical
contract. Predecessor hashes or migration history are not persisted in the project
manifest, onboarding state or any project-owned file.

A manifest-write failure remains `unknown-partial`. Only a completed manifest and
healthy target doctor can satisfy `upgraded`.

### Packaging and conformance

The same compiled registry and mirror digest must be present in direct Release,
Plugin payload, marketplace payload and offline/local package builds. Release
validation fails on:

- compiled/mirrored registry digest drift;
- missing or duplicate migration identifiers;
- wildcard or non-exact source/target versions;
- unknown modes;
- unsafe, duplicate or non-managed migration paths;
- non-lowercase or non-64-hex hashes;
- a migration member outside the exact two-path set;
- a registry target which differs from the packaged kit version;
- direct/Plugin/marketplace byte drift; or
- any attempt to use manifest or channel text as the sole predecessor credential.

Executable conformance must add an intact official v0.5.0 source-project fixture;
it must not delete or omit `AGENT_INSTALL.md` or `agent-install.json`. It must prove:

1. clean plan is read-only, safe, contains the two `update` entries and exact
   migration evidence;
2. apply succeeds without force, deletion, bypass, network or extra confirmation;
3. the two files enter the target manifest and activation set with target hashes;
4. installed target doctor is healthy and the existing manual-fallback activation
   boundary remains truthful;
5. project-owned and arbitrary untracked path snapshots are unchanged;
6. the ordinary v0.5.0 installed fixture where both files are absent still follows
   the create path;
7. each migration file missing, modified, directory-valued, symlinked or
   broken-symlinked is rejected for both migration paths;
8. missing, modified, directory-valued, symlinked and broken-symlinked
   `AGENTS.md` each reject both migration paths;
9. a symlink or broken symlink at every representative intermediate chain
   (`.vibe`, `.vibe/core`, `.agents`, `.agents/skills` and `.codex`) rejects both
   migration paths, including links whose targets remain inside the project;
10. the official v0.5.0 local-payload `source` object, an absent `source`, `null`,
    and a different well-formed JSON value produce the same positive eligibility
    result when every authenticated field and byte is unchanged;
11. an official-looking local-payload or GitHub-like predecessor `source` value
    cannot make a wrong version, altered install identity, unhealthy managed set or
    incomplete contract pair eligible;
12. missing, null, wrong-type, extra-field, wrong-digest, uppercase-digest,
    wrong-authority, wrong-mode and divergent predecessor-migration mirrors fail
    release validation, and Agent-install/core mirror mutations fail target
    planning before project writes even when surrounding hashes are refreshed;
13. predecessor/target mixed pairs, one-member pairs, wrong versions, malformed
   manifests, altered normalized install identities and unhealthy predecessor
   managed sets are rejected;
14. unrelated untracked managed collisions retain their existing conflict behavior;
15. a pre-mutation injected race causes conflict evidence only, while a race after
    mutation begins produces `unknown-partial`;
16. direct, Plugin-bundled, offline-bundle and local-payload executions have the
    same migration decision after satisfying their existing channel-specific
    digest requirements; and
17. schema-1 consumers which ignore `compatibility_migrations` retain all existing
    status, action, count and write-state behavior.

The source suite must run under the existing dependency-free Python standard
library boundary and parse under Python 3.9. Release confidence additionally
requires an actual Python 3.9 runtime execution in local or supported CI evidence;
an unavailable local interpreter must be recorded as skipped and does not itself
authorize a release claim.

### Alternatives and trade-offs

Inferring ownership from framework version, filenames, one matching file, manifest
source text or Git ancestry is rejected because each permits false-positive
ownership transfer.

Storing the only allowlist in editable `agent-install.json`, the project manifest
or a release document is rejected because local state could weaken the migration
predicate. The compiled registry is authoritative; machine contracts expose only
integrity-checked mirrors.

Network lookup of the historical tag or release is rejected because plan and apply
must remain offline and channel-parity must not depend on network availability.

User deletion, force overwrite, broad `adopt`, or a special acceptance bypass is
rejected because it weakens the existing collision boundary and would not be an
upgrade path users can trust.

Independent per-file adoption is rejected. Requiring the complete pair and a
healthy official predecessor installation can reject locally modified predecessor
installations, but this false-negative bias is intentional: it preserves arbitrary
project-owned content instead of guessing ownership.

A generic historical-file or three-way migration engine is rejected as unnecessary
scope. Future published predecessors receive separate exact reviewed entries.
Adding an entry with the same schema requires a new immutable kit release and new
registry digest. A new mode, eligibility meaning or evidence shape requires the
normal maintenance-bridge or Agent-install protocol review/bump. Published payloads
are never retroactively changed.

Adding transactions, backups or rollback is rejected here because the separate
permission-safe atomic-upgrade work owns those semantics.

### Recovery

An authentication failure before project mutation follows the existing conflict
candidate and review flow. It never silently changes either contract.

An accepted migration which becomes `unknown-partial` follows ADR 0009's existing
scoped inspection, installed-doctor and trusted-payload recovery. It does not claim
automatic rollback and must not proceed to activation.

Before publication, implementation rollback is Git revert of the compatibility
repair. After publication, semantic downgrade continues to require an explicitly
selected trusted older payload; this amendment adds no special downgrade path.

## Normative takeover result

The host-side result is `takeover_schema_version: 1`. It is host/task state under
the host's existing user-account retention boundary. It is not written to the
repository, Vibe Kit manifest, onboarding state, conflict directory, Plugin
payload, release artifact or feedback state.

A conforming result has exactly this shape:

```json
{
  "takeover_schema_version": 1,
  "takeover_id": "opaque-host-id",
  "evidence_origin": "runtime",
  "completion_owner_task_id": null,
  "project_root": "/canonical/absolute/project/path",
  "source": {
    "type": "github-release",
    "ref": "v0.6.0",
    "artifact_sha256": "64-hex-or-null",
    "payload_tree_sha256": "64-hex"
  },
  "versions": {
    "from": "strict-semver",
    "target": "strict-semver"
  },
  "target_fingerprint": {
    "kit_version": "strict-semver",
    "core_protocol": 4,
    "agent_install_schema": 2,
    "agent_install_protocol": 2,
    "adapter_name": "codex",
    "adapter_protocol": 4,
    "manifest_sha256": "64-hex-or-null",
    "activation_set_sha256": "64-hex-or-null"
  },
  "overall_status": "in-progress",
  "last_completed_stage": null,
  "write_state": "none",
  "activation": {
    "path": "none",
    "receipt_kind": null,
    "receipt_id": null,
    "source_task_id": "opaque-host-task-id",
    "active_task_id": "opaque-host-task-id-or-null",
    "handoff_idempotency_key": null,
    "observed_manifest_sha256": null,
    "observed_activation_set_sha256": null
  },
  "goal": {
    "kind": "maintenance-only",
    "custody": "none",
    "continuation": "not-applicable",
    "transfer_id": null,
    "owner_task_id": null,
    "custody_history": []
  },
  "stages": {
    "source-resolved": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "planned": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "applied": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "upgraded": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "activated": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "adapted": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "verified": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "re-evaluated": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []},
    "ready": {"state": "not-started", "outcome": null, "reason_code": null, "evidence": []}
  },
  "next_action": null
}
```

`source.type` is exactly one of `github-release`, `plugin-bundled`,
`offline-bundle`, or `local-payload`.

`overall_status` is exactly one of `in-progress`, `ready`, `degraded`, or
`blocked`.

Every stage `state` is exactly one of `not-started`, `satisfied`, `blocked`, or
`not-applicable`.

An evidence entry has exactly:

```json
{
  "kind": "closed-evidence-kind",
  "ref": "opaque-receipt-id-or-relative-path",
  "sha256": "64-hex-or-null",
  "task_id": "opaque-host-task-id-or-null",
  "sequence": 0
}
```

`kind` is exactly one of:

- `source-attestation`
- `plan-receipt`
- `apply-receipt`
- `doctor-receipt`
- `activation-receipt`
- `manual-task-start`
- `handoff-claim`
- `onboarding-state`
- `adaptation-review`
- `verify-receipt`
- `routing-record`

Evidence contains no original-goal text, raw subprocess output, credentials,
environment values or unrelated project content.

`evidence_origin` is exactly `runtime` or `controlled-fixture`.
`completion_owner_task_id` is null until `ready`; at ready it is the only task
authorized to issue the completion message and equals `activation.active_task_id`.

A custody-history entry has exactly `state`, `task_id`, and `sequence` fields.
Within one takeover object, evidence and custody-history sequences are non-negative
integers; evidence sequences are unique. An activation receipt has a greater
sequence than the apply receipt it follows.

### Stage dependencies

The normative order is:

```text
source-resolved
  -> planned
  -> applied
  -> upgraded
  -> activated
  -> adapted
  -> verified
  -> re-evaluated
  -> ready
```

A stage may become `satisfied` only after every mandatory predecessor is
`satisfied`. `ready` has one permitted exception:
`re-evaluated=not-applicable` with `outcome=maintenance-only`.

`not-applicable` is permitted only for `re-evaluated`, and only when
`goal.kind=maintenance-only` and evidence confirms there was no unfinished
application goal. All other stages are mandatory.

`last_completed_stage` is the last ordered stage whose state is `satisfied`. A
`not-applicable` stage is never counted as completed. For maintenance-only work,
while `re-evaluated=not-applicable/maintenance-only` and `ready` has not yet been
satisfied, `last_completed_stage` remains `verified`. Once ready is satisfied,
`last_completed_stage` is `ready`.

At most one stage is `blocked`. All later stages remain `not-started`.

`ready.state=satisfied` is valid only when:

- all preceding mandatory stages are `satisfied`;
- `re-evaluated` is `satisfied` or validly `not-applicable`;
- no blocking diagnostic or verification outcome exists;
- for maintenance-only work, goal custody is `none` and continuation is
  `not-applicable`;
- for unfinished work, custody matches the activation path, the owner matches the
  active task, and continuation is `ready-to-resume` or `resumed`;
- `completion_owner_task_id` is non-null and equals
  `activation.active_task_id`;
- exactly one custody state is current and `goal.custody` equals the final
  custody-history state;
- an unfinished goal's owner equals the completion owner;
- the source task is not completion owner after automatic or manual successor
  ownership;
- `controlled-fixture` evidence proves contract behavior only and is not live host
  capability evidence;
- `overall_status=ready`;
- `reason_code` is null; and
- `next_action` is null.

`overall_status=degraded` is permitted only when `upgraded=satisfied`,
`activated=blocked`, the reason is `manual-new-task-required`, write consistency
is known, and the sole action is `create-new-project-task`.

### Stage outcome contract

`outcome` is null for every stage except `adapted` and `re-evaluated`.

For `adapted`:

| State | Required outcome |
|---|---|
| `not-started` | null |
| `satisfied` | `unchanged-complete` or `refreshed` |
| `blocked` | `blocked` |
| `not-applicable` | invalid |

For `re-evaluated`:

| State | Required outcome |
|---|---|
| `not-started` | null |
| `satisfied` | `routable` |
| `blocked` | `blocked-by-target-rules` |
| `not-applicable` | `maintenance-only` |

`adapted.state=blocked` requires an applicable adaptation reason such as
`onboarding-invalid`, `onboarding-contradicted` or
`adaptation-write-incomplete`.

`re-evaluated.state=blocked` requires `outcome=blocked-by-target-rules` and reason
`target-rule-blocker` or `material-user-decision`.

Unknown, missing or inconsistent stage outcomes fail closed.

### Closed reason codes

A blocked/degraded result uses exactly one of:

- `source-untrusted`
- `source-digest-mismatch`
- `unsupported-source-channel`
- `unsupported-predecessor`
- `unknown-contract`
- `maintenance-bridge-unsupported`
- `plan-blocked`
- `managed-conflict`
- `apply-failed-no-write`
- `conflict-evidence-written`
- `unknown-partial`
- `doctor-broken`
- `diagnostic-blocking`
- `activation-receipt-unavailable`
- `activation-receipt-invalid`
- `automatic-handoff-unavailable`
- `handoff-ambiguous`
- `handoff-failed`
- `manual-new-task-required`
- `onboarding-invalid`
- `onboarding-contradicted`
- `adaptation-write-incomplete`
- `verification-failed`
- `verification-skipped`
- `verification-error`
- `target-rule-blocker`
- `material-user-decision`
- `host-permission-required`
- `internal-error`

A satisfied/not-started/not-applicable stage has `reason_code: null`.

### Closed next actions

`next_action` is null for `in-progress` and `ready`. A degraded/blocked result has
exactly:

```json
{"code": "closed-action-code", "detail": "one-sanitized-sentence"}
```

`code` is exactly one of:

- `select-trusted-source`
- `use-conformant-maintenance-entry`
- `choose-supported-target`
- `review-conflict-candidates`
- `inspect-and-recover-installation`
- `approve-required-host-permission`
- `inspect-existing-handoff`
- `create-new-project-task`
- `resolve-project-context`
- `inspect-adaptation-changes`
- `fix-configured-check`
- `resolve-target-rule-blocker`
- `answer-material-decision`
- `report-internal-failure`

The required reason/action mapping is:

| Reason | Action |
|---|---|
| `source-untrusted`, `source-digest-mismatch`, `unsupported-source-channel` | `select-trusted-source` |
| `unknown-contract`, `maintenance-bridge-unsupported` | `use-conformant-maintenance-entry` |
| `unsupported-predecessor` | `choose-supported-target` |
| `plan-blocked`, `managed-conflict`, `conflict-evidence-written` | `review-conflict-candidates` |
| `unknown-partial`, `doctor-broken`, `diagnostic-blocking` | `inspect-and-recover-installation` |
| `host-permission-required` | `approve-required-host-permission` |
| `handoff-ambiguous` | `inspect-existing-handoff` |
| `activation-receipt-unavailable`, `automatic-handoff-unavailable`, `manual-new-task-required` | `create-new-project-task` |
| `onboarding-invalid`, `onboarding-contradicted` | `resolve-project-context` |
| `adaptation-write-incomplete` | `inspect-adaptation-changes` |
| `verification-failed`, `verification-skipped`, `verification-error` | `fix-configured-check` |
| `target-rule-blocker` | `resolve-target-rule-blocker` |
| `material-user-decision` | `answer-material-decision` |
| `apply-failed-no-write`, `activation-receipt-invalid`, `handoff-failed`, `internal-error` | `report-internal-failure` |

Unknown fields, missing required fields, unknown enums or invalid combinations fail
closed.

## Executable takeover contract and validator

Agent-install schema 2 is the declarative source of truth for takeover structure
and invariants. The `takeover` object in `agent-install.json` adds:

```json
{
  "validator": {
    "command": "validate-takeover",
    "input": "stdin-json",
    "result_schema_version": 1,
    "statuses": ["valid", "invalid", "error"],
    "persistence": "none",
    "authority": "structural-consistency-only"
  },
  "result_shape": {
    "additional_properties": false,
    "required_top_level": [
      "takeover_schema_version", "takeover_id", "evidence_origin",
      "completion_owner_task_id", "project_root", "source", "versions",
      "target_fingerprint", "overall_status", "last_completed_stage",
      "write_state", "activation", "goal", "stages", "next_action"
    ],
    "required_stage_keys": [
      "source-resolved", "planned", "applied", "upgraded", "activated",
      "adapted", "verified", "re-evaluated", "ready"
    ],
    "required_stage_fields": ["state", "outcome", "reason_code", "evidence"],
    "required_evidence_fields": ["kind", "ref", "sha256", "task_id", "sequence"],
    "required_activation_fields": [
      "path", "receipt_kind", "receipt_id", "source_task_id",
      "active_task_id", "handoff_idempotency_key", "observed_manifest_sha256",
      "observed_activation_set_sha256"
    ],
    "required_goal_fields": [
      "kind", "custody", "continuation", "transfer_id", "owner_task_id",
      "custody_history"
    ],
    "required_custody_history_fields": ["state", "task_id", "sequence"],
    "required_next_action_fields": ["code", "detail"]
  },
  "stage_order": [
    "source-resolved", "planned", "applied", "upgraded", "activated",
    "adapted", "verified", "re-evaluated", "ready"
  ],
  "stage_dependencies": {
    "source-resolved": [],
    "planned": ["source-resolved"],
    "applied": ["planned"],
    "upgraded": ["applied"],
    "activated": ["upgraded"],
    "adapted": ["activated"],
    "verified": ["adapted"],
    "re-evaluated": ["verified"],
    "ready": [
      "source-resolved", "planned", "applied", "upgraded", "activated",
      "adapted", "verified"
    ]
  },
  "not_applicable_rules": [
    {
      "stage": "re-evaluated",
      "required_goal_kind": "maintenance-only",
      "required_outcome": "maintenance-only"
    }
  ],
  "stage_outcome_rules": {
    "adapted": {
      "satisfied": ["unchanged-complete", "refreshed"],
      "blocked": ["blocked"],
      "not-applicable": []
    },
    "re-evaluated": {
      "satisfied": ["routable"],
      "blocked": ["blocked-by-target-rules"],
      "not-applicable": ["maintenance-only"]
    }
  },
  "activation_receipt_bindings": {
    "host-reload": {
      "path": "same-task-reload",
      "active_task_relation": "equals-source-task",
      "handoff_idempotency_key": "must-be-null",
      "required_evidence": ["activation-receipt"],
      "required_custody_at_ready": "source-owned"
    },
    "host-successor-start": {
      "path": "automatic-successor-handoff",
      "active_task_relation": "differs-from-source-task",
      "handoff_idempotency_key": "required",
      "required_evidence": ["activation-receipt", "handoff-claim"],
      "required_custody_at_ready": "automatic-successor-owned"
    },
    "manual-task-start": {
      "path": "manual-new-task",
      "active_task_relation": "differs-from-source-task",
      "handoff_idempotency_key": "must-be-null",
      "required_evidence": ["manual-task-start"],
      "required_custody_at_ready": "manual-successor-owned"
    }
  },
  "custody_transitions": {
    "none": [],
    "source-owned": ["automatic-transfer-pending", "manual-transfer-required"],
    "automatic-transfer-pending": ["automatic-successor-owned"],
    "automatic-successor-owned": [],
    "manual-transfer-required": ["manual-transfer-pending"],
    "manual-transfer-pending": ["manual-successor-owned"],
    "manual-successor-owned": []
  },
  "ready_invariants": [
    "exact-result-shape", "stage-dependencies-satisfied",
    "only-maintenance-re-evaluation-not-applicable",
    "stage-outcomes-consistent", "last-completed-is-last-satisfied-stage",
    "write-state-project-files-written", "reason-action-consistent",
    "activation-receipt-bound", "activation-after-apply",
    "activation-identities-match-target", "default-verification-passed",
    "no-blocking-diagnostic", "custody-history-valid",
    "single-active-custodian", "completion-owner-is-active-task",
    "unfinished-goal-owner-is-completion-owner",
    "ready-has-no-reason-or-next-action",
    "overall-ready-iff-ready-stage-satisfied"
  ]
}
```

The contract also contains the exact reason/action map already defined by this
ADR. All result and nested objects are closed; unknown properties fail validation.
String, nullable, strict-SemVer, SHA-256, non-negative-sequence and exact-enum
types are enforced by the validator.

`bin/vibe validate-takeover --format json` reads exactly one JSON object from
stdin. It performs no project write or network access, does not persist or echo the
input, loads the installed `agent-install.json`, and executes every declared shape,
dependency, mapping, receipt, custody and ready invariant. It reports rule IDs and
JSON paths only, never values that may contain host identifiers.

CLI result schema remains 1. Status is exactly `valid`, `invalid`, or `error`, with
exit codes 0, 1 and 2 respectively. A valid result contains:

```json
{
  "schema_version": 1,
  "command": "validate-takeover",
  "status": "valid",
  "structural_only": true,
  "host_evidence_authenticated": false,
  "ready_claim": false,
  "errors": []
}
```

Structural validity never authenticates a host receipt or proves that a live task
is activated or ready. `validate-release` verifies synchronization between these
declarative rules and CLI constants, and runs canonical valid/invalid objects
through the production validator. Doctor never reads or persists a host takeover
object.

### Installed-contract authentication before takeover validation

`validate-takeover` must not trust installed `agent-install.json` merely because it
parses or declares schema 2. Before using any on-disk takeover rule, the running
CLI authenticates it against installation identity and its compiled contract
registry.

The 0.6.0 CLI contains the complete nested result schema, enums, dependencies,
outcome rules, reason/action mapping, activation receipt bindings, custody
transitions and ready invariants. `TAKEOVER_CONTRACT_REGISTRY_SHA256` is the
canonical JSON SHA-256 of that compiled registry.

The same registry is stored at
`agent-install.json.takeover.contract_registry`; its digest is stored at
`agent-install.json.takeover.contract_registry_sha256` and in
`.vibe/core/protocol.json`. The registry digest covers only
`takeover.contract_registry`, so it is not self-referential.

Before reading the candidate takeover object, the validator:

1. resolves the project root from the installed `bin/vibe`;
2. validates installed/core/manifest version integrity;
3. requires installed `AGENT_INSTALL.md` and `agent-install.json`;
4. verifies the raw Agent-install hash against manifest `managed_files`;
5. checks Agent-install schema 2/protocol 2, kit 0.6.0, core 4 and Codex adapter 4
   against compiled constants and `.vibe/core/protocol.json`;
6. independently recomputes the normalized activation set from installed bytes;
7. parses the on-disk registry as a closed object;
8. compares its full canonical value with the compiled registry;
9. recomputes the registry digest and matches compiled, Agent-install and core
   declarations; and
10. only then validates stdin.

Any authentication failure returns `error`, exit code 2,
`structural_only=true`, `host_evidence_authenticated=false`, and
`ready_claim=false`. It never falls back to locally weakened rules.

Authentication error codes are exactly:

- `installed-version-integrity-failed`
- `installed-agent-contract-missing`
- `installed-agent-contract-hash-mismatch`
- `installed-agent-contract-schema-mismatch`
- `installed-core-contract-mismatch`
- `installed-activation-identity-mismatch`
- `compiled-contract-registry-mismatch`

Errors expose only code and JSON/relative path, never contract content, takeover
values or host identifiers. Authentication proves correspondence with the
canonical validator; it does not authenticate the truth of host receipts.

### Complete compiled nested shape

Every result and nested object has `additional_properties=false`. Scalar types are:

- `opaque-id`: 1–256 UTF-8 characters without NUL/control characters;
- `relative-ref`: 1–4096 UTF-8 characters without NUL;
- `canonical-project-root`: canonical absolute path, 1–4096 characters, no NUL;
- `sha256`: exactly 64 lowercase hexadecimal characters;
- `strict-semver`: `^[0-9]+\.[0-9]+\.[0-9]+$`;
- `sequence`: integer greater than or equal to zero;
- `sanitized-detail`: 1–512 UTF-8 characters without CR/LF/NUL/control chars.

The top-level fields have these exact types:

| Field | Type |
|---|---|
| `takeover_schema_version` | integer exactly 1 |
| `takeover_id` | `opaque-id` |
| `evidence_origin` | `runtime` or `controlled-fixture` |
| `completion_owner_task_id` | null or `opaque-id` |
| `project_root` | `canonical-project-root` |
| `source` | closed source object |
| `versions` | closed versions object |
| `target_fingerprint` | closed fingerprint object |
| `overall_status` | closed overall-status enum |
| `last_completed_stage` | null or stage name |
| `write_state` | closed write-state enum |
| `activation` | closed activation object |
| `goal` | closed goal object |
| `stages` | exact nine-stage object |
| `next_action` | null or closed next-action object |

`source` contains exactly `type`, `ref`, `artifact_sha256`, and
`payload_tree_sha256`. Types and channel-specific nullability follow the normative
source table. `versions` contains strict-SemVer `from` and `target`, with target
equal to fingerprint kit version.

`target_fingerprint` contains exactly `kit_version`, `core_protocol`,
`agent_install_schema`, `agent_install_protocol`, `adapter_name`,
`adapter_protocol`, `manifest_sha256`, and `activation_set_sha256`. Protocol/schema
values equal compiled values; adapter is exactly `codex`; hashes are nullable only
at the lifecycle stages declared by this ADR.

`activation` contains exactly the eight fields declared by `result_shape`.
Receipt/path/task/idempotency/hash constraints are enforced by compiled bindings.

`goal` contains exactly the six fields declared by `result_shape`.
`custody_history` contains 0–4 closed entries of `state`, `task_id`, and
`sequence`.

`stages` contains exactly nine declared keys. Every stage contains exactly
`state`, `outcome`, `reason_code`, and `evidence`; evidence contains 0–32 closed
entries of `kind`, `ref`, `sha256`, `task_id`, and `sequence`. Evidence kind,
placement and hash/task bindings are validated, not merely typed.

Non-null `next_action` contains exactly enum `code` and `sanitized-detail`.

The declarative registry additionally stores:

```json
{
  "scalar_types": {
    "opaque_id_max_chars": 256,
    "path_or_ref_max_chars": 4096,
    "detail_max_chars": 512,
    "sha256_pattern": "^[0-9a-f]{64}$",
    "strict_semver_pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
    "sequence_minimum": 0
  },
  "array_limits": {"evidence_per_stage": 32, "custody_history": 4}
}
```

The complete registry, including scalar types, limits and invariants but excluding
the sibling `contract_registry_sha256`, is hashed canonically. That digest is stored
only in the sibling field and core protocol declaration. A local contract cannot
add fields, relax a type, widen an enum, remove a required field or replace an
invariant; compiled registry wins.

## Source identity and pre-execution maintenance bridge

Every channel computes the same payload-tree identity:

```text
payload_tree_sha256 =
  SHA256(concatenation of
    "<relative-posix-path>\0<file-sha256>\n"
    for every allowlisted payload file,
    sorted by relative path)
```

The digest covers `AGENT_INSTALL.md`, `agent-install.json`, `AGENTS.md`,
`bin/vibe`, `.vibe/core/`, `.agents/skills/vibe-*`,
`.codex/agents/vibe-*` and every other release allowlist entry.

Channel requirements are:

| Channel | Required trust/digest evidence |
|---|---|
| `github-release` | Exact canonical tag/Release URL; downloaded asset SHA-256 must match published `SHA256SUMS`; nested release validation must pass; both `artifact_sha256` and `payload_tree_sha256` are required. |
| `offline-bundle` | Caller-selected local artifact; caller-supplied artifact SHA-256 must match; nested checksums and release validation must pass; both digests are required. |
| `plugin-bundled` | Installed Plugin version must equal target version; the Plugin manifest declares `payload_tree_sha256`; runtime recomputation must match it; `artifact_sha256` is null because no separate transferred release asset is used. |
| `local-payload` | User/host explicitly selected the exact local path; runtime computes `payload_tree_sha256`; clean commit ref is recorded when available; `artifact_sha256` is null and the receipt must not claim publisher authentication. |

A bare repository, moving ref, silent pre-release selection or unverified archive
cannot enter `source-resolved=satisfied`.

The 0.6.0 payload contains a **maintenance bridge schema 1** in both
`AGENT_INSTALL.md` and `agent-install.json`:

```json
{
  "maintenance_bridge": {
    "schema_version": 1,
    "supported_installed_manifest_schemas": [1],
    "supported_installed_agent_protocols": [0, 1],
    "minimum_installed_kit_version": "0.2.0",
    "maximum_installed_kit_version_exclusive": "0.6.0",
    "target_agent_install_schema": 2,
    "target_agent_install_protocol": 2,
    "target_cli_result_schema": 1,
    "predecessor_migrations": {
      "schema_version": 1,
      "registry_sha256": "6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d",
      "authority": "target-cli-compiled",
      "modes": ["replace-and-adopt-complete-set"]
    },
    "operations": ["plan-upgrade", "upgrade", "doctor"]
  }
}
```

Installed Agent protocol `0` means the installed version predates
`agent-install.json`.

After source identity is verified and before any project write, the acquisition
Agent reads and validates the target bridge. Target `bin/vibe`, not the installed
older CLI, performs plan and upgrade. This supports declared 0.2.x–0.5.x manifest
schema 1 installations, including the accepted 0.4.x/0.5.x upgrade cases, without
pretending their old runtime rules understand protocol 2.

An acquisition Agent that cannot interpret bridge schema 1 or target Agent-install
schema/protocol 2 stops before apply. It must not coerce protocol 2 into protocol 1.

## Applied and upgraded evidence

`applied` requires a target-CLI upgrade result bound to the planned project,
source, target version and payload tree digest, with a complete successful mutation
outcome.

`write_state` remains exactly one of the ADR 0007 values: `none`,
`project-files-written`, `conflict-evidence-written`, or `unknown-partial`.

Only `project-files-written` can satisfy `applied`.

`upgraded` additionally requires the installed target CLI's JSON doctor result,
with exact target version integrity, manifest framework version equal to target,
no `broken` or `error` status, known onboarding state and complete structured
diagnostic classification.

Apply success alone cannot produce `upgraded`, `activated` or `ready`.

## Activation content identity

The target release and installed project declare the same exact sorted
`activation_paths` list. It consists of:

- `AGENT_INSTALL.md`;
- `agent-install.json`;
- `bin/vibe`;
- every target-release file under `.vibe/core/`;
- every target-release file under `.agents/skills/vibe-*/`;
- every target-release file under `.codex/agents/vibe-*/`; and
- `AGENTS.md#managed-block`.

The first two entries are activation-critical because the only currently supported
manual successor must discover and validate the takeover lifecycle from its
installed project. Project-owned files are excluded. Stale files absent from the
target release are not included in the expected target set.

### Activation-set normalization and independent recomputation

`agent-install.json` is activation-critical and also declares the expected digest.
Hashing its raw bytes into that same digest would be self-referential and is
forbidden.

The activation algorithm is
`sha256-canonical-json-fingerprint-and-normalized-path-hashes-v2`.

Ordinary activation paths use their raw-byte SHA-256.
`AGENTS.md#managed-block` uses the SHA-256 of the exact extracted block.
For `agent-install.json`, the algorithm parses the complete JSON with duplicate-key
and UTF-8 validation, deep-copies it, replaces only
`/activation/activation_set_sha256` with 64 ASCII zeroes, serializes canonical
UTF-8 JSON with sorted keys/no insignificant whitespace/`ensure_ascii=false`/
separators `,` and `:`, then hashes those bytes. No other field is ignored.

The release and installation manifest publish:

```text
activation_set_sha256 =
  SHA256(canonical JSON of {
    "fingerprint": target fingerprint without manifest_sha256 or
                   activation_set_sha256,
    "path_hashes": sorted activation path -> algorithm-defined path hash
  })
```

The digest is stored in Agent-install `/activation/activation_set_sha256`, the
release manifest, installed manifest activation identity, and installed target
fingerprint. Raw managed-file integrity remains separate: manifest `managed_files`
stores the final unnormalized Agent-install raw-byte hash.

Packaging uses two passes: compute normalized identity with the zero sentinel,
write that digest into the final contract, then compute payload/managed hashes from
final bytes. No fixed-point iteration is used.

Installed doctor and every activation receipt bind the raw installed manifest
SHA-256, actual installed activation-set SHA-256, target expected activation-set
SHA-256, exact target fingerprint, and stale runtime-discoverable paths.

The actual and expected activation-set digests must match. Presence, version text
or manifest declaration without matching installed bytes is insufficient.

Release validation and doctor independently recompute from actual bytes and do not
trust any declared digest, per-path hash, manifest identity or receipt. Tests use a
separate reference implementation and reject mutation of every covered contract
field. Algorithm v1 is invalid for canonical unpublished 0.6.0 artifacts.

Runtime discovery roots are exactly `AGENT_INSTALL.md`, `agent-install.json`,
`bin/vibe`, `.vibe/core/`, `.agents/skills/`, `.codex/agents/`, and
`AGENTS.md#managed-block`. A preserved stale path under any root is
`stale-runtime-path-preserved` and blocks activation. A stale path outside all
runtime roots is `stale-nonruntime-path-preserved` and is the sole initial
non-blocking stale diagnostic.

## Adapter capability matrix

| Adapter/runtime | Same-task reload | Automatic successor handoff | Manual new-task activation |
|---|---|---|---|
| Repository Codex adapter protocol 4 | Contract defined; not currently claimed | Contract defined; not currently claimed | Supported |
| Bootstrap-only Plugin maintain path | Not provided by the Plugin | Not provided by the Plugin | Supported |
| Future Codex host integration with live conformance receipts | Conditional | Conditional | Supported |
| Non-Codex adapter | Unverified | Unverified | Unverified until adapter-specific evidence exists |

Therefore the current repository implementation and packaged Plugin are
**manual-fallback-only** unless the running host independently supplies a
conforming live receipt.

Adding or changing Codex product APIs, task-creation APIs, reload APIs or host
integration code is outside this repository work item. This repository defines the
negotiation/evidence contract and controlled fixtures only. Static prompts,
native-subagent availability, thread-tool presence or simulated receipts do not
upgrade the current capability claim.

A future host integration may enable the conditional paths without changing the
core lifecycle only after live conformance evidence is recorded and the adapter
capability declaration is updated through its normal reviewed release process.

## Activation paths

`activation.path` is exactly one of `none`, `same-task-reload`,
`automatic-successor-handoff`, or `manual-new-task`.

`receipt_kind` is exactly one of `host-reload`, `host-successor-start`,
`manual-task-start`, or null when `path=none`.

### Same-task reload

This path requires a host `host-reload` receipt binding the same task identity,
canonical project root, completion after the apply receipt, raw installed manifest
SHA-256, actual activation-set SHA-256 and target fingerprint.

Capability declaration or Agent self-report without that host event is invalid.

### Automatic successor handoff

This path requires an idempotent host create/handoff operation, a distinct
successor task identity, a `host-successor-start` receipt after apply and an
acknowledged single-owner handoff claim.

An ambiguous creation result is inspected by idempotency key before retry. If the
host cannot determine whether a task exists, no second task is created.

The source task stops all adaptation, verification, re-evaluation and original-goal
work after the successor claim. The successor owns the final completion response.

### Manual new-task activation

When no conforming live receipt exists, the source ends with:

- `overall_status=degraded`;
- `activated.state=blocked`;
- `reason_code=manual-new-task-required`;
- `next_action.code=create-new-project-task`; and
- goal custody `manual-transfer-required` when an unfinished goal exists.

The user performs one action: create a new task in the same project, using a
host-prefilled continuation when available or the one copyable continuation
sentence supplied by the source.

The new task produces a `manual-task-start` receipt by establishing a distinct
task identity, loading the project through the normal new-task instruction
boundary, recomputing installed manifest/activation-set identities, acknowledging
the target fingerprint, and validating the transfer identifier when an unfinished
goal exists.

Only then may the manual successor set `activated=satisfied` and continue
adaptation. Merely opening another chat outside the project, quoting the target
version or reading target files from the old task is insufficient.

## Goal custody and privacy

`goal.kind` is exactly one of `maintenance-only` or `unfinished`.

`goal.custody` is exactly one of:

- `none`
- `source-owned`
- `automatic-transfer-pending`
- `automatic-successor-owned`
- `manual-transfer-required`
- `manual-transfer-pending`
- `manual-successor-owned`

`goal.continuation` is exactly one of:

- `not-applicable`
- `paused`
- `ready-to-resume`
- `resumed`
- `blocked`

Takeover completion and original-goal completion are different facts.
`overall_status=ready` means takeover is complete; it does not mean the user's
original development goal is complete.

For maintenance-only work, custody is `none`, continuation is `not-applicable`,
and `owner_task_id` is null.

For an unfinished goal, the active custodian at ready is:

| Activation path | Required custody | Required owner |
|---|---|---|
| `same-task-reload` | `source-owned` | source task |
| `automatic-successor-handoff` | `automatic-successor-owned` | activated successor task |
| `manual-new-task` | `manual-successor-owned` | activated manual successor task |

At ready, `goal.owner_task_id` must equal `activation.active_task_id`, and
`goal.continuation` must be `ready-to-resume` or `resumed`.

A target-rule blocker does not erase custody. Custody remains with the active
source/successor task while `goal.continuation=blocked`.

Automatic custody transitions are:

```text
source-owned
  -> automatic-transfer-pending
  -> automatic-successor-owned
```

Manual custody transitions are:

```text
source-owned
  -> manual-transfer-required
  -> manual-transfer-pending
  -> manual-successor-owned
```

At `manual-transfer-required`, the source task becomes terminal for the original
goal and performs no more project work. Custody is temporarily user-mediated and
`owner_task_id` is null. Ownership becomes `manual-successor-owned` only after the
new task's valid manual activation receipt and transfer-id validation.

### Custody-history ordering and current ownership

Custody history shares one monotonic event domain with takeover evidence:

1. every evidence and custody sequence is globally unique;
2. custody sequences strictly increase in array order;
3. maintenance-only has empty history, custody `none`, null transfer/owner and
   continuation `not-applicable`;
4. unfinished work starts with `source-owned`, the source task ID, and a
   non-negative sequence;
5. later entries are one direct compiled transition—no skip, reverse or repeat;
6. the final history state equals current custody;
7. no transition follows automatic/manual successor ownership;
8. current owner is derived from custody/history rather than trusted separately;
9. automatic-transfer-pending retains source ownership and requires an idempotency
   key;
10. automatic successor ownership requires a distinct active task, matching
    successor-start receipt and later handoff claim;
11. manual-transfer-required clears owner and makes source terminal;
12. manual-transfer-pending identifies one distinct candidate while owner is null;
13. manual successor ownership uses that same candidate and a later manual-start
    receipt;
14. same-task activation retains a one-entry source-owned history;
15. at ready, derived owner equals active task and completion owner;
16. source cannot regain ownership after successor transfer; and
17. a target-rule blocker changes continuation only, not custody.

Derived ownership is:

| Custody | History task | `goal.owner_task_id` |
|---|---|---|
| `none` | no history | null |
| `source-owned` | source | source |
| `automatic-transfer-pending` | source | source |
| `automatic-successor-owned` | active successor | active successor |
| `manual-transfer-required` | null | null |
| `manual-transfer-pending` | candidate successor | null |
| `manual-successor-owned` | active manual successor | active manual successor |

Duplicate/non-monotonic sequence, invalid first state/transition, history/current
mismatch or inconsistent supplied owner invalidates the result.

The registry includes the additional invariants
`custody-sequences-globally-unique`,
`custody-history-strictly-increasing`, `custody-first-state-valid`,
`custody-transitions-direct`, `custody-final-equals-current`,
`custody-owner-derived`, and `successor-custody-terminal`.

The transfer contains only opaque takeover/transfer identifiers, canonical project
identity, exact target version/fingerprint, the active objective when safe,
accepted material decisions, minimal unfinished status and references to durable
repository evidence.

It never contains hidden reasoning, unrelated conversation, raw terminal/tool
output, environment variables, credentials, tokens or duplicated repository
content. Secrets are not copied; existing scoped host authorization is reused or
the normal permission/authentication action is requested.

The transfer is not persisted in the repository or CLI results. The opaque
transfer identifier is single-use within the host task boundary. A manual
successor must inspect current repository/work-item state before writes because the
portable fallback cannot provide a repository lock.

There is no custody value meaning “original goal completed.” Completion of the
original development goal belongs to its routed workflow, outside the takeover
result.

## Adaptation, verification and re-evaluation order

The selected order is:

```text
activation
  -> evidence-backed adaptation
  -> final installed/project verification
  -> target-rule re-evaluation
  -> resume or maintenance completion
```

This matches the persisted design. Verification may execute configured project
commands, but it does not authorize Agent-authored application/shared edits.
Target-rule re-evaluation still occurs before any such edit.

Only an activated task may adapt project-owned context.

Adaptation satisfies the stage as either
`state=satisfied, outcome=unchanged-complete` or
`state=satisfied, outcome=refreshed`. An invalid, contradicted or incomplete
adaptation is `state=blocked, outcome=blocked`. `unchanged-complete` requires valid
complete onboarding and evidence that no stale or contradictory context remains.
`refreshed` records only evidence-backed changes. Template regeneration,
uncertain-fact replacement and silent conflict resolution remain forbidden.

A partial adaptation write failure records touched relative paths, sets
`adaptation-write-incomplete` and stops. It does not silently revert potentially
concurrent project-owned changes.

After adaptation, final doctor and project verification run. Only after
`verified=satisfied` does the Agent classify and route the original goal under the
target rules.

For an unfinished goal, re-evaluation is
`state=satisfied, outcome=routable` or
`state=blocked, outcome=blocked-by-target-rules`. For maintenance-only work it is
`state=not-applicable, outcome=maintenance-only`.

`blocked-by-target-rules` may coexist with a healthy Kit, but it blocks overall
ready and unconditional “可以继续开发” language.

## Doctor structured diagnostics

Doctor keeps CLI result schema 1 and existing command statuses `healthy`,
`warning`, `broken`, and `error`. Exit codes remain `0` for `healthy` or `warning`,
`1` for `broken`, and `2` for `error`.

With `--format json`, stdout contains exactly one JSON envelope and expected
diagnostic results write nothing to stderr.

The compatibility `warnings` and `errors` string arrays remain. Agent-install
protocol 2 additionally requires one authoritative `diagnostics` entry for every
warning/error:

```json
{
  "code": "closed-code",
  "level": "warning",
  "readiness_effect": "blocking",
  "path": "relative-posix-path-or-null",
  "detail": "sanitized-bounded-detail"
}
```

Initial warning codes and fixed effects are:

| Code | Effect |
|---|---|
| `managed-file-hash-mismatch` | `blocking` |
| `agents-block-hash-mismatch` | `blocking` |
| `onboarding-state-missing` | `blocking` |
| `stale-runtime-path-preserved` | `blocking` |
| `stale-nonruntime-path-preserved` | `non-blocking` |

Initial error codes, all blocking, are:

- `version-integrity-failed`
- `manifest-missing-or-invalid`
- `managed-file-missing`
- `agents-file-missing`
- `agents-block-missing`
- `required-project-file-missing`
- `project-config-invalid`
- `onboarding-state-invalid`
- `skill-contract-invalid`
- `agent-contract-invalid`
- `diagnostic-internal-error`

The initial doctor non-blocking allowlist is exactly
`stale-nonruntime-path-preserved`. No other warning can be inferred non-blocking
from prose or severity.

Persisted onboarding `pending` and `refresh-needed` remain structured onboarding
states rather than doctor warnings. They require adaptation before ready.
`invalid` is blocking.

Unknown code, missing diagnostic, duplicate coverage or an effect differing from
the registry blocks readiness.

## Structured verify contract

`verify --format json` is added additively under CLI result schema 1.

Aggregate status is exactly one of `passed`, `failed`, `blocked`, or `error`.
CLI exit codes are `0` for `passed`, `1` for `failed`, and `2` for `blocked` or
`error`.

JSON mode emits exactly one envelope to stdout. Expected command failures,
captured subprocess output and structured errors do not write additional stdout or
stderr text.

The envelope contains:

```json
{
  "schema_version": 1,
  "command": "verify",
  "status": "passed",
  "target": "/canonical/project/path",
  "selection": {"mode": "default", "requested": [], "coverage": "all-configured"},
  "producer": "cli",
  "cli_invoked": true,
  "checks": [
    {
      "name": "lint",
      "configured": false,
      "applicability": "not-applicable",
      "required": false,
      "outcome": "unconfigured",
      "exit_code": null,
      "reason_code": "not-configured",
      "provenance": {"kind": "cli", "task_id": null, "operation_id": null},
      "output": {
        "stdout_tail": "",
        "stderr_tail": "",
        "stdout_truncated": false,
        "stderr_truncated": false
      }
    }
  ],
  "summary": {"passed": 0, "failed": 0, "unconfigured": 4, "skipped": 0}
}
```

The verify envelope makes no `network_used` claim. `bin/vibe verify` performs no
independent resolver or updater network operation, but configured project commands
are arbitrary project-owned child processes and may access the network. The CLI
does not observe or attest to their network behavior.

A host may separately block or permission-gate a configured command because of
network or side-effect policy. That produces a provenance-bound `skipped` outcome;
it must not be represented as `network_used=false`.

Default selection emits exactly one entry, in order, for `lint`, `typecheck`,
`test`, and `build`.

A non-empty configured command is always `applicable` and `required` for takeover.
An empty or missing command is `not-applicable`, not required and `unconfigured`.
No deeper applicability inference is made.

Default mode continues later independent checks after a failure when the process
can still be started.

`--only` may be repeated and retains its maintainer behavior. It emits unique
selected checks in canonical order. Its `selection.mode` is `only` and coverage is
`partial`. Takeover always uses default mode; an `--only` receipt cannot satisfy
`verified`.

Check outcomes are exactly `passed`, `failed`, `unconfigured`, or `skipped`:

- `passed`: configured, applicable, required, exit code `0`, reason null;
- `failed`: configured, applicable, required, executed nonzero exit code, reason
  null;
- `unconfigured`: not configured, not applicable, not required, null exit code,
  reason `not-configured`;
- `skipped`: configured, applicable, required, null exit code and a closed skipped
  reason.

Skipped reasons are exactly:

- `host-permission-denied`
- `host-capability-unavailable`
- `side-effect-not-authorized`
- `execution-interrupted`
- `process-start-failed`

Shell exit values such as 126 or 127 are executed nonzero results and therefore
`failed`, not silently reclassified as skipped.

If the CLI cannot start a configured subprocess, it records
`process-start-failed`, continues other safe checks and returns aggregate
`blocked`.

If the host prevents the CLI from being invoked, the host produces the same check
matrix with `producer=host`, `cli_invoked=false`, `status=blocked`, `outcome=skipped`
for each configured check, one allowed host skipped reason,
`provenance.kind=host`, and non-null task and host operation/permission receipt
identifiers. Unconfigured entries remain unchanged. Missing provenance is invalid.

Subprocess output handling is:

- capture stdout and stderr separately;
- retain at most the final 16 KiB of sanitized UTF-8 text per stream per check;
- drain excess output and set the corresponding truncated flag;
- replace undecodable bytes;
- strip ANSI sequences and disallowed control characters;
- redact the repository's versioned secret-pattern registry;
- replace the canonical project-root prefix with `.`; and
- never copy captured output into the takeover evidence object.

`passed` includes an all-unconfigured project with zero executed checks. Human
output must say no project checks are configured; it must not say tests ran.

Any failed, skipped, malformed or unknown required outcome blocks `verified`.

## Ready semantics

`ready` is host-derived and never emitted by one CLI receipt.

For maintenance-only work it requires upgraded, activated, adapted, verified,
valid `re-evaluated=not-applicable`, and no blocker.

For an unfinished goal it additionally requires `re-evaluated.state=satisfied`
with `outcome=routable`, correctly established ownership, and original-goal
continuation begun or explicitly ready to begin.

Only then may the Agent say unconditionally that the upgrade is complete and
development may continue.

A target-rule blocker is reported separately:

> Vibe Kit 已升级、激活并完成项目适配；原开发任务因新版规则暂停，需要确认或补齐：……

The source and successor never both announce completion.

## Failure and atomic-upgrade composition

Source, bridge, protocol and safe-plan failures retain `write_state=none`.

Managed conflicts retain `write_state=conflict-evidence-written`; managed and
application state is not described as upgraded.

`unknown-partial` always blocks at `applied`. The Agent inspects scoped Vibe Kit
paths, runs whichever installed doctor is runnable and uses Git or the same trusted
payload for recovery. It never activates, hands off, adapts, verifies or blindly
retries while consistency is unknown.

The separate permission-safe atomic-upgrade work owns transaction phases,
snapshots, backups, rollback records, permission diagnostics and any stronger
mutation outcomes. This ADR adds no rollback claim and no second transaction
writer.

If atomic upgrade lands first, only its proven committed result satisfies
`applied`; `not-applied` and `rolled-back` leave the old installation active, while
`recovery-required` blocks. If it changes a closed result enum or meaning, this
decision is reopened or an additional reviewed compatibility decision is required.

A release containing both work items must expose one merged schema/protocol and
joint failure/recovery conformance evidence.

Activation, adaptation, verification or re-evaluation failure does not
automatically downgrade a consistent installation.

## Version and migration

Published 0.5.0 remains unchanged:

- kit `0.5.0`;
- core protocol `3`;
- Codex adapter `3`;
- Agent-install schema `1`;
- Agent-install protocol `1`;
- CLI result schema `1`.

This decision targets an unpublished 0.6.0 candidate:

- kit `0.6.0`;
- core protocol `4`;
- Codex adapter `4`;
- Agent-install schema `2`;
- Agent-install protocol `2`;
- takeover schema `1`;
- maintenance bridge schema `1`;
- predecessor-migration registry schema `1` with compiled registry digest
  `6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d`;
- CLI result schema `1`.

CLI result schema 1 is retained only because existing command fields and meanings
remain compatible; doctor fields are additive and verify had no prior JSON
contract. Removing, renaming, retyping or changing an existing result
field/status/write-state meaning requires reopening readiness and declaring result
schema 2.

`compatibility_migrations` is an optional additive command field under the existing
schema-1 ignorable-field rule. It does not change an existing status, action,
write-state or recovery meaning. The install manifest remains schema 1 because
successful migration records only ordinary target managed-file hashes.

Install manifest schema 1, onboarding schema 1, release-manifest schema 1 and
feedback protocol 2 remain unchanged.

No part of this decision publishes 0.6.0, promotes stable status, installs a public
Plugin or changes an external host. Those require their normal authorization and
evidence.

## Packaging and executable conformance

The 0.6.0 payload synchronizes installed and release copies of
`AGENT_INSTALL.md` and `agent-install.json`, `.vibe/core/protocol.json`, managed
`AGENTS.md`, workflow Skills and Agent definitions, bootstrap-only Plugin
maintenance instructions, CLI doctor/verify/takeover-validator behavior, Plugin
version and payload-tree identity, release documentation, and direct Release,
Plugin and marketplace payloads.

Release validation rejects drift in kit/schema/protocol values, installed-contract
membership and hashes, lifecycle shape and rule tables, stage dependencies,
not-applicable rules, reason/action mapping, activation receipt bindings, custody
transitions, ready invariants, activation identity, doctor/verify registries,
source-channel requirements, compiled predecessor-migration registry identity, its
Agent-install/core/release mirrors, complete-set semantics and executable intact-
v0.5.0 migration behavior, cross-channel bytes, or forbidden Plugin capabilities.

Static text assertions do not satisfy takeover behavior. A source-only controlled
harness uses a deterministic fake host and the production takeover validator. It
stores synthetic goal text only in fake host memory and never in the takeover
object. It exercises:

1. valid same-task reload plus wrong-task, pre-apply, manifest and activation
   mismatches;
2. idempotent automatic successor creation, lookup-before-retry, unresolved
   ambiguity, single custody claim and terminal source ownership;
3. degraded manual fallback, installed contract presence, distinct manual successor
   identity, transfer validation and replay/wrong-project blocking;
4. unchanged/refreshed/invalid/contradicted/incomplete adaptation with activated
   owner enforcement;
5. default verification, all-unconfigured truth, required failure, host skip,
   partial `--only`, malformed receipt and advancement only from valid evidence;
6. maintenance-only, routable unfinished goal, target-rule blocker and material
   decision routing before application/shared edits;
7. same-task/automatic/manual ready objects, single completion owner and rejection
   of source completion after transfer;
8. a goal/secret sentinel absent from repository, manifests, onboarding, conflicts,
   release/Plugin payloads, feedback, validator output/errors and takeover object;
9. negative objects for every dependency, outcome, reason/action, receipt, custody,
   ready invariant, unknown field/enum and duplicate owner.

The harness invokes the packaged/installed production validator, not a test-only
reimplementation. Tests assert transitions and validator results, not wording.

`validate-release` runs a bounded canonical subset covering one valid maintenance
result and invalid dependency, action, activation, custody and false-ready cases.
The complete controlled matrix remains in the source test suite.

Controlled fixtures use `evidence_origin=controlled-fixture`. They prove contract
and state-machine behavior only, not a live `host-reload`, `host-successor-start`
or Codex product integration claim. Current capability remains
manual-fallback-only until external receipts and adapter evidence exist.

## Alternatives considered

### Treat apply or doctor as activation

Rejected because they cannot observe which instructions govern the running task.

### Put takeover in `bin/vibe`

Rejected because the offline CLI cannot own task identity, host activation or
conversation custody.

### Claim current Codex automatic handoff from tool availability or static prompts

Rejected because no live receipt/conformance evidence exists and the repository
does not implement external host APIs.

### Always stop after apply and require the user to reconstruct the goal

Rejected because the accepted fallback is one new-task action with preserved or
copyable continuation context.

### Copy the whole conversation or persist a repository handoff file

Rejected because it exceeds scope and creates privacy, duplication and ownership
risks.

### Reuse the published 0.5.0 lifecycle/protocol

Rejected because the new required stages, bridge, activation evidence and result
semantics are breaking Agent-contract changes.

### Fold atomic upgrade into takeover

Rejected because transaction/rollback mechanics already belong to a separate L
work item and require their own decision.

## Consequences

- Users confirm an exact scoped upgrade once.
- Current repository/Plugin Codex behavior truthfully guarantees the manual
  new-task fallback; automatic paths remain conditional on future external host
  receipts.
- CLI and host claims are separated.
- Activation is bound to actual target managed content, not version text.
- Goal transfer is minimal, single-owner and absent from repository state.
- Doctor warnings and configured checks have closed machine-readable readiness
  semantics.
- Adaptation, verification and target-rule re-evaluation have one unambiguous
  order.
- 0.6.0 is required; 0.5.0 remains immutable.
- The official healthy v0.5.0 source state has one fail-closed path into the newly
  managed 0.6.0 Agent-install contracts; no arbitrary untracked path gains a broader
  adoption rule.
- Atomic-upgrade ownership remains separate.
- Installed projects contain the two normative Agent-install contracts referenced
  by their managed runtime.
- Host takeover state remains outside the repository; only its closed structural
  validator is distributed in `bin/vibe`.
- Release validation rejects machine-contract drift, and controlled fixtures
  exercise lifecycle behavior without claiming live host support.
- `docs/work-items/index.md` remains project-owned traceability and must link this
  active L work item before Close; it is not managed or activation-critical.

## Rollback

Before publication, exact source rollback is Git revert of reviewed implementation
commits.

After a future publication, installed-project rollback uses an explicitly selected
older trusted payload and is semantic rather than byte-for-byte. Existing stale
managed-path policy applies.

A failed activation or verification does not roll back a consistent target
installation. Recovery follows the one stage-specific action in the takeover
result.

## Open decisions

None.

The user has already fixed the material product behavior: one exact-version
confirmation, automatic healthy-path continuation when the host can prove it,
truthful manual degradation otherwise, evidence-backed adaptation, and ready
language only after activation and verification.

External host integration and public 0.6.0 publication are explicitly outside this
decision and are not silently authorized.
