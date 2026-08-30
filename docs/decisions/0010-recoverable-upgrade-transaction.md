# 0010: Make upgrades recoverable transactions with a create-only onboarding bridge

- Status: Accepted
- Date: 2026-08-31
- Decision owner: read-only Tech Lead author
- Review: base decision approved by a distinct read-only Tech Lead on 2026-08-31 after three changes-required passes; the lossless final-leaf amendment was independently approved after one closure pass; the prepared absent-parent directory amendment was independently approved after two closure passes resolved control-object modes, canonical ordering, parent reauthentication and cleanup-state separation

## Context

Vibe Kit 0.6.0 atomically replaces individual files, but one `upgrade` is not a
cross-file transaction. A permission or write failure can leave
`unknown-partial`, and recovery depends on manual inspection. Official v0.3.0 and
v0.4.0 predecessors also predate persisted onboarding: current upgrade can write
the complete target managed state and then have the first target doctor block on
`onboarding-state-missing`.

v0.7.0 must join managed files, the merged `AGENTS.md`, manifest/version and the
one create-only compatibility file into a recoverable operation. It must not
claim whole-repository, instant multi-path filesystem atomicity, cryptographic
authentication of state controlled by the same OS principal, or ownership of
existing project context.

## Decision

### Transaction scope and ownership

One upgrade transaction covers only:

- changed framework-managed files;
- the complete `AGENTS.md` file when its managed block is merged;
- `.vibe/manifest.json` and `.vibe/version`;
- `.vibe/onboarding.json` only when the compatibility bridge creates a previously
  absent file; and
- conflict/transaction control state created by that upgrade.

It does not cover `init`, `adopt`, existing onboarding contents, other project- or
application-owned files, stale-preserved files, the entire Git worktree, ACLs,
owners or extended attributes. `.vibe/onboarding.json` remains project-owned; the
CLI owns only the create-only transition inside the active transaction and gives
up ownership immediately after commit.

The authoritative journal and recovery metadata live at:

```text
.vibe/local/upgrade-transactions/active/
```

`active/` and every journal subdirectory are mode `0700`; regular journal
members are mode `0600`. The only transaction-control objects outside `active/`
are intent-bound same-parent leaf temporaries, capability probes and directory
staging roots required by the accepted atomic filesystem protocols. Leaf
temporaries use their declared postimage mode. Directory-probe directories use
mode `0700`; regular leaf-probe files and directory-probe marker files use mode
`0600`. Directory-stage directories and files
must have their declared target modes before prepared state; they are hidden
control objects until publication and are excluded from manifests and packages.
These adjacent mode exceptions do not apply to journal metadata or preimage
bytes. Metadata contains only relative paths, hashes,
phases, errno/error class and bounded detail. It excludes credentials,
environment, goal/conversation text and raw unbounded output. Preimage bytes are
removed after verified commit or rollback.

### Supported predecessor and onboarding eligibility

The maintenance bridge continues direct support for authenticated declared
predecessors from v0.2.x through v0.6.x, but SemVer range self-declaration is never
onboarding migration authority. Compatibility registry schema 2 grants the
create-only exception to exactly three compiled identities:

| Family | Authority | Manifest | Core/Codex | Agent-install | Raw manifest SHA-256 | Canonical install identity |
|---|---|---:|---|---:|---|---|
| controlled v0.2.0 fixture | official v0.3.0 release-root fixture; only `.vibe/core/version` becomes `0.2.0\n` | 1 | 1/1 | 0 | `dc250b0e2538f7964421709565615dd20bb594b331f62ce9683ac8d22d5b63ae` | `e4478dd69110743d4872f7e98c8f5cbb02b3bfb766a3e82bfe9e756aea604fc3` |
| official v0.3.0 | tag commit `4f8a2fa8f8de9b947bbf6ea5e6e34ff1b3f0b35b` | 1 | 1/1 | 0 | `46ca3dc91b2f4cd5b763f146b4dcca94f925e97ac405c543a362caa4c9c75f9c` | `1cdef039f939519dc91125ce284ea7ac3572c845e2814b6e0fbfaec87978c71f` |
| official v0.4.0 | tag commit `69ae813098335c4865cf2b6b7b36f66d52097167` | 1 | 2/2 | 0 | `dff3a996cf150883b87a46ead1f698bbe3be3165432e26b2e3521608fe22d936` | `321fd63de3c42d2e7c702d32dd83c1501d3efd1438835c8b49802b483ebc8423` |

Canonical install identity is SHA-256 of canonical JSON containing exactly
`schema_version`, `framework_version`, the complete `managed_files` map and
`agents_block_hash`. The compiled authority also fixes:

```text
managed file count: 21
managed path-set SHA-256:
  0c56aa953b46ece6725f2b0cc36203e7104b89d9702e424899ed827919a89179

managed-map SHA-256:
  controlled v0.2.0: 7ade6fd2bed67dd1e3e4ddd0981bd84781072669d48d6f68804ab4309a09e8dd
  official v0.3.0:   030927ae791596371193aad5af0385f8cc4cbfaec26da0638b51bf04b05864d7
  official v0.4.0:   5e7cd946eec9762e6df625253674e19a3c2bb0b8aea6a47c7a6d4ed7533cde91

AGENTS block SHA-256:
  controlled v0.2.0 and official v0.3.0:
    cb49adced3fc7c77e0e20df98d06db5c8857463d62f629b26047c8ee6a091d2d
  official v0.4.0:
    537d07126e6e8f6704b432bc58af52653b8573b517f74716724fdf769b6317c7

controlled v0.2.0 .vibe/core/version SHA-256:
  1f930dd1f133c1f97a94fe3acb8db34372cf4c01ffdb2b3ff4ca72f9494121e9
```

The registry stores every literal path/hash pair, not only these summaries. The
v0.2 map equals official v0.3.0 path-for-path except for the fixed core-version
hash. Its generation authority is the official v0.3.0 historical
`tests/test_cli.py` fixture, never a current template.

Before the first transaction/control/project write, runtime eligibility compares
exact version, schema/protocol, full managed path/hash map, `AGENTS.md` managed
block and canonical identity, then repeats safe-path/absence checks under the
writer lock. A manifest's self-reported version or digest alone is insufficient.
Unknown v0.2/v0.3/v0.4 identities block before writes.

All three compiled contracts lack `AGENT_INSTALL.md`, `agent-install.json` and
`.vibe/onboarding.json`; the onboarding leaf must still be absent. The only created
value is canonical schema-1 `pending`. Missing onboarding in v0.5.x/v0.6.x is
project-state loss and blocks before any write. For every family, malformed,
unreadable, wrong-type, symlinked or race-changed onboarding blocks. Existing
valid onboarding is byte-preserved. The bridge never writes `complete`, `evidence`
or `updated_at`.

The closed `onboarding_bridge` state is `planned`, `applied`, `preserved`,
`not-needed`, or `blocked`; it records compiled family identity, eligibility,
path, from/to state and created-content SHA-256. `planned`/`applied` are exclusive
to these three identities. Registry schema 2 separately retains the exact official
v0.5 unmanaged Agent-contract complete-set migration into v0.7. The registry
digest is mirrored exactly in target CLI, Agent-install, core protocol and release
manifest.

### Integrity boundary and durable representation

Transaction evidence is **integrity-checked but untrusted**. Same-OS-principal
malicious modification is outside the threat model. Recovery treats every member
as untrusted input and blocks on any inconsistency; hashes and file modes do not
make same-principal state authenticated.

```text
active/
  owner.json
  intent.json
  stage/
  preimage/
  events.jsonl
  capabilities.json
  prepared.json
  commit.json
  directory-cleanup/
```

`commit.json` is absent until target postimages and installation identity validate.
Its schema is closed:

```text
schema_version = 1
transaction_id
intent_sha256
postimage_set_sha256
directory_postimage_set_sha256
committed_at = ISO-8601 timestamp
```

`intent.json` binds canonical project identity, from/target versions, exact allowed
relative paths, expected preimage state/hash/type/mode, staged postimage hash/mode,
absent markers, manifest/AGENTS/onboarding identities and transaction schema.
`events.jsonl` is bounded, append-only, hash-chained and fsynced.

`owner.json` closes over `schema_version=1`, `transaction_id`,
`project_identity_sha256` and `created_at`. `prepared.json` closes over
`schema_version=1`, `transaction_id`, `intent_sha256`, `stage_set_sha256`,
`preimage_set_sha256` and `prepared_at`. The first installation-path mutation is
forbidden until a valid, directory-fsynced `prepared.json` exists. It is a journal-
schema-1 member and does not introduce another top-level protocol.

Every intent, stage and preimage member is written to a temporary member, file-
fsynced, atomically renamed and followed by parent-directory fsync. Member and
directory creation/deletion also fsyncs its parent. Each event append is fsynced.
Final installation leaves use only the lossless protocol below; ordinary
rename/replace is limited to private journal members. `commit.json` is written to
a temporary member, file-fsynced, renamed fd-relatively and followed by active-
directory fsync. An invalid marker never finalizes a transaction.

All path operations start from a pinned canonical project-root file descriptor.
Every directory component is opened and verified with `O_DIRECTORY`, `O_NOFOLLOW`
and `fstat`; leaves use `O_NOFOLLOW`. Replace, rename and unlink operations use
`dir_fd` variants. No security decision depends on a later `Path.resolve()` or
`exists()` after compare-and-swap validation. If the host lacks required
`dir_fd`, `O_NOFOLLOW`, regular-file or directory-fsync semantics, upgrade blocks
before mutation as unsupported.

### Lossless final-leaf mutation

The threat model includes a non-cooperating process creating, replacing, removing
or writing any in-scope installation leaf at any point, including after the final
read and during the kernel mutation. Discovery or modification by a malicious
same-OS-principal process of random, intent-bound journal, probe or temporary
names remains outside the threat model. "Never overwritten" means that an object
observed at the final leaf remains reachable either at that leaf or at an
intent-bound same-parent temporary leaf until it has been proved to be the
expected transaction object. An exchange window can be observed, but a divergent
displaced object is never unlinked.

The dependency-free Python `>=3.9` adapter uses only `os` and standard-library
`ctypes.CDLL(None, use_errno=True)`. It exposes these fd-relative primitives:

- on macOS, `renameatx_np` with `RENAME_SWAP=0x00000002` and
  `RENAME_EXCL=0x00000004`;
- on Linux, `renameat2` with `RENAME_EXCHANGE=0x00000002` and
  `RENAME_NOREPLACE=0x00000001`; and
- on both platforms, `os.link` with `dir_fd` support and
  `follow_symlinks=false`.

Every call uses pinned parent file descriptors and basenames only. Absolute
paths, `Path.resolve()`, shell commands, subprocesses, native extensions and
external packages are forbidden. An unknown platform, absent symbol,
`ENOSYS`, `ENOTSUP`, `EOPNOTSUPP`, `EINVAL` for a required flag, `EXDEV`, or a
same-filesystem capability-probe failure makes the leaf protocol unsupported;
ordinary rename/replace is never a fallback. Plan is read-only: it checks the
API and symbol surface and reports that an apply-time filesystem probe is still
required.

After the active owner is durable and before any installation mutation, apply
performs a journal-bound round-trip probe in every changed parent directory.
Each probe uses two random intent-bound `O_CREAT|O_EXCL|O_NOFOLLOW` regular
members and proves:

1. exchange moves the two recorded device/inode identities and can exchange them
   back;
2. hard-link publication succeeds only to an absent destination and returns
   `EEXIST` without mutation for an existing destination; and
3. no-replace rename succeeds only to an absent destination and returns `EEXIST`
   without mutation for an existing destination.

Probe files and their parents are fsynced. Cleanup removes only members whose
identities still match the probe. A permission failure uses the existing host-
permission result. An unsupported primitive uses the new unsupported result
below. An uncertain probe cleanup returns recovery-required or unknown.

Journal schema 1 gains `capabilities.json`, same-parent leaf temporaries and
closed additions. `intent.json` contains an exact sorted
`leaf_capability_probes` array. Every item contains exactly `parent_path`,
`probe_a_path`, `probe_b_path`, `requires_hard_link`, `requires_no_replace` and
`requires_exchange`. Every `changes` item additionally contains exactly
`slot`, `path`, `leaf_protocol`, `temporary_path`, `preimage`, `postimage` and
`preimage_object`. `leaf_protocol` is `link-no-clobber-v1` for an absent
preimage and `exchange-preserve-v1` for a regular preimage. The same-parent
hidden temporary name is derived from the transaction ID and slot and must be
absent. `preimage_object` is null exactly for an absent preimage; otherwise it is
an object containing exactly non-negative integer `device` and `inode` values,
with booleans forbidden.

A regular preimage is accepted only when the first `O_NOFOLLOW` read and a
second `fstat` agree on device, inode, type, size and mode. The recorded bytes and
mode remain authoritative; identity additionally rejects byte-identical
replacement. `capabilities.json` contains exactly `schema_version=1`,
`transaction_id`, `intent_sha256`, `probe_set_sha256` and `verified_at`.

Before `prepared.json`, apply creates every existing-parent leaf's same-parent temporary with
`O_CREAT|O_EXCL|O_NOFOLLOW`, writes the postimage, applies its mode, fsyncs the
file and parent, and records its identity. `prepared.json` additionally contains
`capabilities_sha256`, `leaf_temporaries` and
`leaf_temporary_set_sha256`. Each exact `leaf_temporaries` item contains
`slot`, `path`, `temporary_path`, `leaf_protocol`, `postimage` and
`postimage_object`. The extended prepared state is durable before any
installation mutation; the journal schema version remains 1.

`postimage_object` contains exactly non-negative integer `device` and `inode`
values; booleans are forbidden. `probe_set_sha256` is SHA-256 of canonical JSON
of the exact `leaf_capability_probes` array sorted by `parent_path`.
`leaf_temporary_set_sha256` is SHA-256 of canonical JSON of the exact
`leaf_temporaries` array sorted by `slot`. `capabilities_sha256` is SHA-256 of
canonical JSON of the complete exact `capabilities.json` object. Duplicate
`parent_path` or `slot` values are invalid. `capabilities.json` MUST NOT be
written unless every declared probe completed successfully and its exact probe
members were cleaned; uncertain cleanup retains the active transaction and uses
the closed recovery-required/unknown result.

Forward mutation is closed:

- For an absent preimage, fd-relative hard-link publication links the prepared
  temporary to the final name. `EEXIST` is a race. Success requires the final
  leaf to have the exact postimage and the same inode as the retained temporary,
  followed by parent fsync. A later replacement of the final leaf is never
  removed automatically.
- For a regular preimage, one atomic exchange swaps the prepared temporary and
  final leaf. Apply immediately verifies that the final leaf is the exact staged
  postimage with the prepared inode, and the temporary is the exact preimage with
  the recorded preimage inode. The displaced preimage remains at the temporary.
- If the displaced temporary is not the expected preimage, it is third-party
  state. Apply may attempt at most one compensating exchange, and only while the
  final leaf is still the Vibe postimage. It then verifies the third-party object
  is back at the final leaf and the Vibe object is at the temporary. Only after
  that exact proof may it remove the Vibe temporary and record the race. If the
  names changed, compensation fails, or the result is uncertain, it performs no
  further exchange or unlink and preserves both names as active evidence.
- A symlink, directory, byte-identical different inode, in-place divergence,
  missing leaf or unknown type is race divergence. All affected objects and the
  parent plus the journal event are fsynced. Journal events are evidence only;
  recovery derives truth from current entry identities.

Rollback is equally lossless. A regular preimage is restored with one atomic
exchange only when the final leaf is the postimage and the temporary is the
preimage. Rollback verifies the inverse pair before unlinking only the exact
prepared temporary. Third-party state at the boundary is preserved at the
temporary and permits at most one compensating exchange; ambiguity preserves
both names and returns unknown.

Rollback for an absent preimage never directly unlinks the final name. It first
removes only an exact private temporary alias, then atomically moves the final
leaf to the now-absent temporary name using no-replace/exclusive rename. If the
moved object is the exact prepared inode and postimage, absence is restored and
the exact temporary may be unlinked. If it is divergent, rollback restores it
with a no-clobber hard link from temporary to final, verifies that pair, then
unlinks only the alias. Concurrent recreation of final returns `EEXIST`,
preserves both names and returns unknown. No branch uses check-then-unlink.

For an absent preimage, the pre-marker pair `final=exact prepared
inode/postimage` and `temporary=absent` is a recoverable applied substate created
after private-alias removal. Recovery MUST resume the same fd-relative
no-replace/exclusive move from final to temporary, verify the moved identity and
bytes, and unlink only the exact transaction object. It MUST NOT classify this
pair as unknown solely because the private alias is absent. Any divergence or
`EEXIST` preserves both names and returns unknown.

Per-leaf states are closed:

```text
planned -> temporary-ready -> link-published-verified | exchanged-unverified
        -> exchanged-verified -> commit-retained -> cleanup-complete
rollback -> predecessor-restored
divergence -> race-preserved -> unknown
```

Recovery classifies exact pairs rather than trusting events:

| Preimage | Final leaf | Temporary leaf | Classification |
|---|---|---|---|
| absent | absent | exact prepared | not applied |
| absent | exact prepared | same prepared inode | applied |
| absent | exact prepared inode and postimage, without a valid marker | absent | applied with rollback alias removed; resume the absent-preimage no-replace rollback |
| regular | exact preimage inode | exact prepared | not applied |
| regular | exact prepared inode | exact preimage inode | applied |
| either | exact target | expected or clean, with valid marker | committed cleanup |
| any | any other pair | preserve both and return unknown |

Before a valid commit marker, applied pairs roll back; after it, exact committed
pairs finalize. Commit is forbidden until every final leaf is exact, every
retained temporary is in the required identity state, every affected parent is
fsynced and the complete postimage installation validates. Cleanup revalidates
each temporary, so a crash at any point remains recoverable. Even a fully
compensated external race leaves the transaction active as `unknown-partial`,
because the installation is no longer the transaction's recorded predecessor.

### Prepared absent-parent directory units

The lossless-leaf phrase "every changed parent directory" applies only when that
parent already exists. A changed file whose parent chain is partly absent uses
the directory-unit protocol below. It is never blocked merely because a
framework-managed target parent is absent, and apply never calls `mkdir` on a
declared final installation directory before durable prepared state.

During read-only plan, each changed path is walked fd-relatively without
following links. If a parent component is absent, the first absent component
below the deepest existing directory becomes a `final_root`. Every target
framework-managed file below that root is grouped into one directory unit.

Directory units are pairwise disjoint and neither equal nor contain another unit
root. The existing parent is a no-follow directory with recorded device/inode;
`final_root` and every declared descendant directory are absent; every member is
framework-managed, has an absent preimage and belongs to the target managed-file
complete set. No unit contains `AGENTS.md`, onboarding, manifest, version,
another project-owned path, a stale-preserved path or an existing object. All
members are contiguous in transaction slot order. For predecessors where it is
absent, `.agents/skills/vibe-release/` is one directory unit. A non-directory or
symlink before the first absent component is a pre-write conflict. An object
appearing at `final_root` after plan is a no-clobber race and is never
overwritten.

#### Closed directory intent schema

`intent.json` adds exactly `directory_units`,
`directory_capability_probes` and `directory_postimage_set_sha256`. Each
`directory_units` item contains exactly:

```text
unit_id sequence parent_path parent_object final_root staging_root protocol
preimage_state directories members tree_sha256
```

`unit_id` is `d` followed by four decimal digits. `sequence` is the integer value
of the lowest member slot. `protocol` is `directory-no-clobber-v1` and
`preimage_state` is `absent`. `parent_path` is the deepest existing
project-relative parent; `parent_object` contains exactly non-negative integer
`device` and `inode`, with booleans forbidden. `staging_root` is a random,
intent-bound hidden sibling of `final_root` in the same parent, is not a final
installation path and must initially be absent.

`directory_units` is sorted by `(sequence, UTF-8 final_root)`, and `unit_id`
values `d0001`, `d0002`, ... are assigned in that order. `sequence` rejects
booleans. `directories` and `tree_objects` are each sorted by `(depth relative
to final_root, UTF-8 logical path)`; this is the required total
parent-before-child order. `members` remains sorted by slot.

`directories` is the complete parent-before-child array for the unit, including
`final_root`. Each item contains exactly `path` and `mode`. Paths are safe
project-relative directories below or equal to `final_root`; modes are integers
with booleans forbidden. V0.7 managed directory-unit target mode is `0755`
(`493` decimal).

`members` is the complete slot-ordered array of target files below the unit.
Each item contains exactly `slot`, `path` and `postimage`. `slot` is four decimal
digits and `postimage` is the existing exact regular-file identity object.
Member paths and directory paths are unique, and their union is the complete
target tree. `tree_sha256` is SHA-256 of canonical JSON containing exactly
`directories` and `members`. `directory_postimage_set_sha256` is SHA-256 of the
canonical array containing exactly `unit_id`, `final_root` and `tree_sha256` for
every unit, sorted by `unit_id`.

Each transaction `changes` item now contains exactly:

```text
slot path leaf_protocol temporary_path directory_unit
preimage postimage preimage_object
```

For an existing-parent leaf, `directory_unit` is null and the accepted
link/exchange rules apply. For a directory-unit member,
`leaf_protocol=directory-unit-member-v1`, `temporary_path=null`,
`directory_unit` is the owning unit ID, `preimage.state=absent` and
`preimage_object=null`. Every unit member appears once in `changes` and once in
its unit, and the identities agree byte-for-byte.

#### Same-filesystem directory capability probe

A directory unit never probes or creates inside its absent final parent. Its
hidden stage and final root use one pinned fd for the already-existing
`parent_path`, so they are on the same filesystem. Each
`directory_capability_probes` item contains exactly `parent_path`,
`parent_object`, `probe_a_path`, `probe_b_path` and
`requires_directory_no_replace`; the last field is always true. Items are unique
and sorted by UTF-8 `parent_path`; probe paths are random intent-bound hidden
siblings in that parent.

The probe creates two private directories with distinct marker files, fsyncs
files, directories and parent, and proves: no-replace rename A to existing B
returns `EEXIST` without changing either directory; after exact private removal
of B, A to B succeeds and preserves A's directory/marker identities; and B to A
succeeds as a round trip. It uses macOS `renameatx_np(RENAME_EXCL)` or Linux
`renameat2(RENAME_NOREPLACE)` with no ordinary-rename fallback.

`probe_set_sha256` in `capabilities.json` is SHA-256 of canonical JSON containing
exactly `leaf_capability_probes` and `directory_capability_probes`.
`capabilities.json` is forbidden until every required file and directory probe
round-trips and cleans exactly.

#### Prepared directory identity

After `capabilities.json` is durable, apply constructs each unit entirely at its
hidden `staging_root` without touching `final_root`. Construction revalidates the
existing parent identity and final-root absence; creates `staging_root` and all
declared subdirectories with exclusive fd-relative `mkdirat`; opens directories
with `O_DIRECTORY|O_NOFOLLOW`; creates every member with
`O_CREAT|O_EXCL|O_NOFOLLOW`; writes exact staged bytes, applies mode and fsyncs
the file; fsyncs all staged directories bottom-up and the existing parent; then
no-follow walks the tree and rejects missing, extra, duplicate, symlinked,
wrong-type, wrong-mode or wrong-hash entries. No leaf probe or same-parent leaf
temporary exists for a `directory-unit-member-v1` change.

Creation mode is not authoritative because `mkdirat` is affected by `umask`.
Before fsync and prepared verification, apply MUST use the opened no-follow
directory descriptors to apply every declared directory mode explicitly and
then verify it.

`prepared.json` adds exactly `directory_stages`,
`directory_stage_set_sha256` and `directory_postimage_set_sha256`. Each
`directory_stages` item contains exactly:

```text
unit_id final_root staging_root parent_object staging_object tree_sha256
tree_objects verified_at
```

`staging_object` contains exactly non-negative integer `device` and `inode`;
booleans are forbidden.
`tree_objects` is the complete parent-before-child array; each item contains
exactly `path`, `type`, `device`, `inode`, `mode` and `sha256`. `type` is
`directory|regular`; `sha256` is null exactly for a directory and lowercase
64-hex for a regular file. Device, inode and mode are non-negative integers with
booleans forbidden. Logical paths are final project-relative paths even while
objects reside below `staging_root`.

`directory_stages` uses the owning `directory_units` order and no alternative
ordering is valid. `directory_stage_set_sha256` is SHA-256 of exactly that
canonical array. Its `tree_sha256` values equal intent;
`directory_postimage_set_sha256` equals intent. Duplicate units, paths or object
identities are invalid. `commit.json` adds the required exact
`directory_postimage_set_sha256` field equal to intent and prepared state. These
are final refinements of unpublished journal and commit-marker schema 1.

#### Directory publication and mutation ordering

The complete order is:

```text
read-only API/symbol/path/directory-unit preflight
  -> create/fsync active and owner
  -> repeat predecessor, existing-parent and final-root-absence CAS
  -> write/fsync stage and preimage
  -> write/fsync intent including units/probes/staging names
  -> run existing-parent leaf and directory no-replace probes
  -> write/fsync capabilities.json
  -> construct/fsync/verify hidden adjacent directory stages
  -> construct/fsync existing-parent leaf temporaries
  -> repeat parent identity and final-root absence checks
  -> write/fsync extended prepared.json
  -> publish directory units and existing-parent leaves in transaction order
  -> verify every directory tree and final/retained leaf pair
  -> fsync every affected directory and validate complete target installation
  -> write/fsync commit.json
  -> cleanup retained private control objects
```

The hidden adjacent stage is transaction control state. Creating, populating or
cleaning it is `transaction-control-written`, not a final installation mutation.
The first final directory mutation occurs only after valid prepared state.

A directory unit is one mutation at `sequence`; member slots are not separately
mutated. Apply performs one fd-relative no-replace rename from `staging_root` to
`final_root`. Immediately before it, apply reopens `parent_path` from the pinned
root, verifies its recorded identity and proves final absence. The syscall is
authoritative: `EEXIST` means a third-party file, symlink or directory won and
neither object changes; success requires stage absence, final root to have the
prepared root identity, and every tree object/path/hash/mode to equal prepared
state. Parent-path replacement or detachment is divergence, preserving reachable
objects and failing closed. Parent and every published directory are fsynced
before the unit is recorded applied. No apply or rollback branch creates final
parent components individually.

Immediately before every directory probe mutation, publication, rollback
detach, compensating restore or private-tree cleanup, the implementation MUST
reopen `parent_path` from the pinned project root and require exact
`parent_object` device/inode identity. A missing, replaced or detached canonical
parent performs no rename, unlink or recursive cleanup; it preserves evidence
and returns unknown-partial. Possession of an older parent descriptor is not
authority to continue after canonical parent divergence.

#### Lossless directory rollback and cleanup

Rollback never recursively deletes `final_root`. For an applied unit it performs
one no-replace rename from `final_root` to the now-absent `staging_root`,
atomically detaching whatever directory occupies the final namespace without
destroying it.

If root identity and every `tree_object` equal prepared state, final absence is
restored and only that exact private tree may be cleaned. Added, removed,
modified, byte-identical different-inode, symlink/type-changed or root-divergent
content is third-party state. A divergent detached tree is restored with at most
one no-replace rename from stage to final. Successful restore leaves it at final
and the transaction unknown-partial. `EEXIST` on restore preserves both final and
hidden trees as unknown-partial. No divergent tree is recursively deleted,
merged or copied.

Before exact private-tree deletion, apply or recovery writes and fsyncs
`active/directory-cleanup/<unit_id>.json`, containing exactly
`schema_version=1`, `transaction_id`, `unit_id`, `cleanup_kind`, `final_root`,
`staging_root`, `staging_object`, `tree_sha256` and `started_at`.
`cleanup_kind` is `not-applied|rollback`. Recursive private cleanup is post-order
and fd-relative. Crash continuation may delete only a prepared-tree subset when
the root has the prepared identity, every remaining entry is an exact prepared
object, no extra entry exists and the cleanup marker is valid. Missing prepared
entries mean already cleaned only after that marker. Any extra/divergent entry is
preserved unknown-partial. An external object at final during private cleanup is
untouched and keeps the installation unknown with active evidence.

Before a valid `prepared.json`, an intent-bound construction stage may be
recursively removed without a cleanup marker only when canonical
`parent_object` revalidation succeeds, `final_root` remains absent, every
present entry exactly matches the intent-declared path/type/mode/postimage, and
no extra entry exists. Missing declared entries in this branch mean never
created, not already cleaned. Any divergence is preserved as unknown-partial.

After a valid `prepared.json`, no recursive private-tree deletion may begin
until the exact cleanup marker below is durably published. Missing prepared
entries are interpreted as already cleaned only under that valid marker.

A cleanup marker is valid only when its transaction ID, unit ID, paths,
`staging_object` and `tree_sha256` equal the exact intent/prepared unit. It is
written as a mode-`0600` private temporary journal member, file-fsynced,
fd-relatively atomically renamed to `<unit_id>.json`, and followed by
`directory-cleanup/` fsync. No staged entry may be removed before that directory
fsync succeeds. After the exact staged root is absent, marker deletion is also
followed by directory fsync. A partial prepared-tree subset with an absent,
invalid or unbound cleanup marker is preserved as unknown-partial and MUST NOT
be recursively cleaned.

#### Directory crash classification

Recovery derives truth from intent, prepared identities, sibling names and the
exact tree; events are not authority.

| Crash/current pair | Classification and recovery |
|---|---|
| intent exists; final absent; stage absent or exact declared partial subset; no prepared | no final mutation; clean exact control subset, otherwise unknown |
| prepared; final absent; stage exact prepared tree | not applied; mark cleanup and remove exact private tree |
| prepared; final exact prepared tree; stage absent; no marker | applied; detach and roll back |
| rollback detached; final absent; stage exact prepared tree | predecessor absence restored; clean exact private tree |
| rollback detached; final absent; stage divergent | restore once no-replace; preserve/unknown |
| final third-party object; stage exact prepared tree | publication-lost `EEXIST`; never touch final, clean exact private tree, retain unknown evidence |
| final object and divergent stage both exist | preserve both; unknown-partial |
| final absent; stage absent | predecessor-restored unless other evidence is invalid |
| valid marker; final exact committed tree; stage absent | committed; finalize control cleanup |
| valid marker but final tree differs | preserve unknown-partial; never reconstruct over it |
| valid cleanup marker with exact prepared-tree subset | continue idempotent private cleanup |
| unknown, symlinked or unbound control member | preserve unknown-partial |

A construction crash has control writes but no final installation mutation. A
post-publication crash is detectable because the prepared directory inode moves
as a unit from stage to final.

#### Directory result mapping

Directory capability failure reuses `upgrade-leaf-atomicity-unsupported`, where
"leaf" means a final namespace entry and may be a file or directory. Read-only
rejection is blocked/no-write/predecessor/not-applied/absent with action
`use-supported-upgrade-filesystem`. Probe or stage failure with exact cleanup and
untouched final roots is blocked or error by permission versus I/O cause,
`transaction-control-written`, predecessor, not-applied/complete. Exact
pre-publication cleanup is not-applied; exact complete rollback is the existing
rolled-back mapping.

A concurrent final-root/tree race returns error
`upgrade_directory_race_preserved`, reason `upgrade-leaf-race-preserved`,
`unknown-partial`, writes true, unknown installation, an
unknown-partial/invalid transaction with absent marker, the exact final root as
failed path, `failure_kind=external-directory-race-preserved`, and the single
action `inspect-upgrade-transaction`. Incomplete exact cleanup uses the existing
recovery-required mapping; unclassifiable/divergent trees use unknown-partial.
Plan, upgrade, doctor and takeover cannot claim healthy, applied or ready while
any stage, cleanup marker or active transaction remains.

### Transaction state machine

```text
absent
  -> preparing -> prepared -> committing -> commit-complete -> cleaning -> complete

prepared|committing
  -> rolling-back -> rollback-complete -> cleaning -> complete

any non-terminal phase
  -> recovery-required
```

`plan upgrade` completes every read-only source, predecessor, onboarding,
path/type, directory-unit, platform-capability, conflict and space check without
creating a transaction path. The exact combined apply order is:

```text
read-only API/symbol/path/directory-unit preflight
  -> atomic mkdir active/              # first control write and writer lock
  -> write/fsync owner.json
  -> repeat predecessor/path/parent/final-root CAS
  -> write/fsync stage and preimage
  -> write/fsync intent.json including units, probes and private names
  -> run existing-parent leaf and directory capability probes
  -> write/fsync capabilities.json
  -> construct/fsync/verify adjacent directory stages
  -> create/fsync existing-parent leaf temporaries
  -> repeat parent identity and final-root absence checks
  -> write/fsync extended prepared.json
  -> publish directory units and lossless existing-parent leaves in order
  -> verify directory trees and all final/retained pairs; fsync parents
  -> write/fsync commit.json
  -> cleanup exact private objects and active state
```

`active/`, owner, stage, preimage, intent, prepared and journal are control writes.
The guarantee is that read-only eligibility completes before the first control
write, and all durable stage/preimage/intent/prepared state completes before the
first installation mutation. An existing active directory blocks a second writer.
Each installation mutation follows the lossless leaf or directory-unit protocol
above; a repeated fd-relative comparison alone is not a sufficient mutation
primitive.
Commit order is managed files, complete `AGENTS.md`, create-only onboarding,
manifest, then `.vibe/version`. Normal divergence and every postimage fail closed.
Rollback runs in reverse transaction order. Existing-parent leaves use the
preserved pair protocol. A directory unit uses only its no-replace
detach/restore protocol; `final_root` is never recursively deleted. Recursive
deletion is permitted only for (a) an exact intent-bound pre-prepared
construction subset under the rule above, or (b) an adjacent prepared private
tree covered by a valid cleanup marker and exact prepared identities. Any other
transaction-created directory may be removed only when exact and empty.

Crash classification is closed:

| Crash point | Installation mutation possible | Recovery |
|---|---:|---|
| after `active/` mkdir, before valid owner | no | if only allowlisted bootstrap temp members exist and predecessor revalidates, delete active |
| after owner, before valid prepared | no | prove no installation mutation, then clean; an unknown member is unknown-partial |
| after valid prepared, before first target write | no | verify all preimages and clean as not-applied |
| during commit, before valid commit marker | yes | reverse rollback from preimages |
| after valid commit marker, during cleanup | target committed | verify all postimages and finalize cleanup |
| during rollback/cleanup | predecessor restored or recovery required | reclassify each path, complete rollback or block |

A third-party value, symlink, unknown type or hash divergence is never overwritten.

External processes may observe the commit window, but Vibe plan, upgrade, doctor,
activation and ready fail closed while active state exists.

### Recovery entry point

Add an explicit offline non-interactive `recover-upgrade` command. Ordinary
upgrade never auto-recovers. Closed branches are:

- valid commit marker plus exact postimages: finalize and return committed target;
- predecessor preimages restorable: roll back, verify and return rolled-back;
- prepared with no mutation: clean up and prove unchanged predecessor;
- integrity-valid unfinished transaction that cannot yet recover: block as
  recovery-required;
- invalid/tampered/unclassifiable evidence: block as unknown-partial and perform no
  automatic recovery; and
- unexpected recovery I/O failure: report the truthful recovery-required or
  unknown-partial class, preserving evidence.

Recovery needs neither Git, network nor the original target payload. Required
preimages and integrity metadata must already be transaction members.

### Closed CLI result schema 2

Every JSON result has `schema_version: 2`, `command` and `status`. Status is closed
per command:

```text
plan                 safe | blocked | error
init                 success | error
adopt                success | error
upgrade              success | blocked | error
recover-upgrade      success | blocked | error
doctor               healthy | warning | broken | error
verify               passed | failed | blocked | error
validate-takeover    valid | invalid | error
validate-release     valid | invalid | error
publication-plan     safe | blocked | error
validate-publication valid | invalid | error
```

Upgrade results always include nullable fields `operation`, `target`,
`from_version`, `target_version`, `source`, `write_state`, `writes_performed`,
`installation_state`, `transaction`, `onboarding_bridge`,
`compatibility_migrations`, `summary`, `error` and `next_action`. Recovery results
always include `target`, `from_version`, `target_version`, `write_state`,
`writes_performed`, `installation_state`, `transaction`, `error` and
`next_action`.

`transaction` has required `schema_version`, `transaction_id`, `outcome`, `phase`,
`commit_marker`, `failed_path` and `failure_kind`. Closed values are:

```text
outcome: not-applied | committed | rolled-back | recovery-required | unknown-partial
phase: absent | preparing | prepared | committing | commit-complete |
       rolling-back | rollback-complete | cleaning | recovery-required | complete | invalid
commit_marker: absent | valid | invalid
write_state: none | transaction-control-written | project-files-written |
             conflict-evidence-written | rolled-back | recovery-required | unknown-partial
installation_state: predecessor | target | recovery-required | unknown
```

`transaction_id` is a nullable string only for a bootstrap-only active directory
created before valid `owner.json`; it must be null in that branch. Every valid
owner, prepared, committing, committed, rolling-back or completed transaction
requires a non-empty ID, and a non-null ID must equal the value in every durable
member. Schema tests include valid null-bootstrap and non-null-owned fixtures plus
negative null-after-owner, empty-ID and member-ID-mismatch cases.

CLI `write_state` and `writes_performed` describe only this invocation's actual
filesystem writes; they are never inferred from a pre-existing installation.
`writes_performed=false` iff `write_state=none`. Creating, cleaning or deleting
transaction state is `transaction-control-written`. `installation_state`
separately classifies the observed project.

Thus plan and doctor observing a pre-existing active transaction report
`write_state=none`, `writes_performed=false`, and installation state
`recovery-required` or `unknown`. Upgrade blocked by that state does the same. A
pre-installation staging failure that cleans its active state reports
`transaction-control-written`, predecessor, not-applied; cleanup failure reports
`recovery-required`, recovery-required. Conflict candidate publication remains
`conflict-evidence-written`.

`recover-upgrade` mapping is exact:

| Observed transaction | Invocation action | Status | Invocation write state | Installation | Outcome |
|---|---|---|---|---|---|
| valid committed target, cleanup pending | delete control state after validation | success | transaction-control-written | target | committed |
| incomplete commit | restore preimages and clean | success | rolled-back | predecessor | rolled-back |
| valid prepared, zero installation mutation | delete control state | success | transaction-control-written | predecessor | not-applied |
| bootstrap-only active | validate predecessor and delete control state | success | transaction-control-written | predecessor | not-applied |
| active state absent | no write | blocked | none | independently observed predecessor/target/unknown | not-applied |
| valid state cannot yet recover | preserve | blocked or error | recovery-required if this invocation wrote, otherwise none | recovery-required | recovery-required |
| state cannot be classified | preserve | blocked or error | unknown-partial if this invocation wrote, otherwise none | unknown | unknown-partial |

Exit codes are closed: plan/publication-plan safe `0`, blocked/error `2`; upgrade
and recover success `0`, blocked/error `2`; doctor healthy/warning `0`, broken `1`,
error `2`; validate-publication valid `0`, invalid `1`, error `2`.

Text and JSON contain no traceback. JSON emits exactly one object on stdout and
uses bounded project-relative error detail. Success has `next_action: null`; a
blocked or uncertain result has exactly one next action.

### Active-state diagnostics and takeover schema 2

`plan upgrade` is blocked with `files_changed: false`, `upgrade` never
auto-recovers, and `doctor` is broken while active state exists. Integrity-valid
state emits blocking diagnostic `upgrade-transaction-active` for the active path
and action `recover-upgrade`. Invalid/unclassifiable state emits
`upgrade-transaction-state-invalid` and action `inspect-upgrade-transaction`.
Normal operation resumes only after verified cleanup.

Takeover top-level `write_state` is logical apply state and excludes the CLI-only
`transaction-control-written` value. It remains `none`, `project-files-written`,
`conflict-evidence-written`, `rolled-back`, `recovery-required`, or
`unknown-partial`. Required `upgrade_transaction` contains exactly
`schema_version`, nullable `transaction_id`, `outcome`, `commit_marker`,
`installation_state` and `active_state_present`, with closed values:

```text
outcome: not-started | not-applied | committed | rolled-back |
         recovery-required | unknown-partial
commit_marker: not-applicable | absent | valid | invalid
installation_state: predecessor | target | recovery-required | unknown
```

Before apply it is null-ID/not-started/not-applicable/predecessor/no-active and
top-level none. A preflight failure is null-ID/not-applied/not-applicable/
predecessor/no-active and none. Committed is non-null-ID/committed/valid/target/
no-active and project-files-written. Rolled back is non-null-ID/rolled-back/absent/
predecessor/no-active and rolled-back. Recovery state has non-null ID, except an
unclassifiable active bootstrap may use null; its outcome is recovery-required or
unknown-partial, marker absent or invalid, installation recovery-required or
unknown, active true, and matching top-level state. Null ID is otherwise invalid.

Schema 2 reason codes are the exact union:

```text
source-untrusted source-digest-mismatch unsupported-source-channel
unsupported-predecessor unknown-contract maintenance-bridge-unsupported
plan-blocked managed-conflict apply-failed-no-write conflict-evidence-written
unknown-partial apply-failed-rolled-back upgrade-recovery-required
upgrade-recovery-blocked upgrade-leaf-atomicity-unsupported
upgrade-leaf-race-preserved doctor-broken diagnostic-blocking
activation-receipt-unavailable activation-receipt-invalid
automatic-handoff-unavailable handoff-ambiguous handoff-failed
manual-new-task-required onboarding-invalid onboarding-contradicted
adaptation-write-incomplete verification-failed verification-skipped
verification-error target-rule-blocker material-user-decision
host-permission-required internal-error
```

Next actions are exactly:

```text
select-trusted-source use-conformant-maintenance-entry choose-supported-target
review-conflict-candidates inspect-and-recover-installation rerun-upgrade-plan
recover-upgrade inspect-upgrade-transaction approve-required-host-permission
use-supported-upgrade-filesystem
inspect-existing-handoff create-new-project-task resolve-project-context
inspect-adaptation-changes fix-configured-check resolve-target-rule-blocker
answer-material-decision report-internal-failure
```

The complete reason-to-action mapping is:

```text
source-untrusted, source-digest-mismatch, unsupported-source-channel
  -> select-trusted-source
unsupported-predecessor -> choose-supported-target
unknown-contract, maintenance-bridge-unsupported
  -> use-conformant-maintenance-entry
plan-blocked, managed-conflict, conflict-evidence-written
  -> review-conflict-candidates
apply-failed-no-write, activation-receipt-invalid, handoff-failed, internal-error
  -> report-internal-failure
unknown-partial, doctor-broken, diagnostic-blocking
  -> inspect-and-recover-installation
apply-failed-rolled-back -> rerun-upgrade-plan
upgrade-recovery-required -> recover-upgrade
upgrade-recovery-blocked -> inspect-upgrade-transaction
upgrade-leaf-atomicity-unsupported -> use-supported-upgrade-filesystem
upgrade-leaf-race-preserved -> inspect-upgrade-transaction
host-permission-required -> approve-required-host-permission
handoff-ambiguous -> inspect-existing-handoff
activation-receipt-unavailable, automatic-handoff-unavailable,
manual-new-task-required -> create-new-project-task
onboarding-invalid, onboarding-contradicted -> resolve-project-context
adaptation-write-incomplete -> inspect-adaptation-changes
verification-failed, verification-skipped, verification-error
  -> fix-configured-check
target-rule-blocker -> resolve-target-rule-blocker
material-user-decision -> answer-material-decision
```

Existing reason-to-stage mappings remain exact; the five new reasons all map to
`applied`. Ready adds `upgrade-transaction-outcome-committed`,
`upgrade-commit-marker-valid` and `no-active-upgrade-transaction`. Applied is
satisfied only by logical project-files-written, committed, valid marker, target
installation and no active state. Rolled-back/recovery/unknown block applied and
leave all later stages not-started. A recovery-finalized commit may satisfy this
only after target doctor revalidation; its invocation-local
`transaction-control-written` is never copied into takeover.

Read-only preflight atomicity failure returns `blocked`, no writes, predecessor,
not-applied, absent transaction, error
`upgrade_leaf_atomicity_unsupported`, reason
`upgrade-leaf-atomicity-unsupported` and the single action
`use-supported-upgrade-filesystem`. An apply-time probe that proves unsupported
after clean evidence removal uses the same reason/action with
`transaction-control-written`, predecessor and not-applied/complete. Uncertain
probe cleanup returns the existing recovery-required or unknown mapping.

A final-leaf race uses error `upgrade_leaf_race_preserved` and reason
`upgrade-leaf-race-preserved`. If the exact predecessor was restored, it uses the
existing rolled-back result. If any third-party object remains in the preserved
pair, upgrade returns error, `unknown-partial`, `writes_performed=true`, unknown
installation, an unknown-partial/invalid transaction with absent marker, the
exact failed path, `failure_kind=external-leaf-race-preserved`, and the single
action `inspect-upgrade-transaction`. Takeover uses the existing unknown-partial
mapping and cannot be ready.

### Conflict evidence

Managed conflicts remain outside the installation transaction. All candidates are
completed in one private directory and published by one directory rename. A
permission failure cleans the temporary directory or truthfully reports recovery-
required; half a candidate set is never called complete.

## Alternatives considered

- Keep per-file replacement plus `unknown-partial`: rejected because it cannot
  satisfy handled-failure rollback or deterministic recovery.
- Depend on Git reset/revert: rejected because targets may not use Git and
  unrelated user changes are out of scope.
- Copy and swap the whole project root: rejected because cross-device paths, open
  handles and business-file ownership make it unsafe.
- Overwrite malformed or modern missing onboarding: rejected because it violates
  project ownership and masks state loss.
- Automatically roll forward every interrupted commit: rejected; a durable
  commit-marker boundary gives deterministic rollback/finalization semantics.
- Add another stat immediately before ordinary rename: rejected because another
  writer can still act between that stat and the rename.
- Rely only on the active transaction lock: rejected because a non-cooperating
  writer does not honor it.
- Rename the old object away and inspect afterward: rejected because it creates a
  destructive visibility gap and still cannot preserve an interleaving writer.
- Add a native extension or helper daemon: rejected because it breaks the
  dependency-free Python `>=3.9`, offline distribution contract.
- Use no-clobber publication for absent leaves and atomic exchange for existing
  leaves while retaining displaced objects: selected because it provides a
  kernel mutation boundary and lossless recovery without weakening AC-2.
- Block a target file whose parent is absent: rejected because it breaks the
  accepted direct predecessor range, including official v0.6 to v0.7.
- Create final parents before prepared state: rejected because externally visible
  installation mutation would lack durable rollback evidence.
- Build below `.vibe/local` and move to the target parent: rejected because a
  nested mount can make it cross-filesystem and would not prove target-parent
  capability.
- Create the final directory and then publish each leaf: rejected because
  rollback cannot safely remove a directory a third party may have populated.
- Build one exact hidden sibling subtree and publish/detach it with directory
  no-replace rename: selected because preparation uses the target filesystem,
  publication is one non-overwriting mutation, and rollback preserves the whole
  displaced tree.

## Compatibility, versioning and supersession

This decision requires kit `0.7.0`, core protocol `5`, Codex adapter protocol `5`,
Agent-install schema/protocol `3`, CLI result schema `2`, takeover schema `2`,
maintenance bridge schema `2`, compatibility migration registry `2`, transaction
journal `1` and commit marker `1`. Installed manifest and onboarding remain schema
`1`; Python `>=3.9` and offline operation remain.

For targets at or above v0.7, this decision supersedes only:

- ADR 0007's CLI result schema-1/write-state closed set;
- ADR 0007's shared nontransactional install/upgrade statement, for `upgrade`
  only;
- ADR 0007's failed-upgrade manual-only recovery statement; and
- ADR 0009's deferred-atomicity, unknown-partial-only failure mapping, old write-
  state composition and v0.6 protocol/version matrix.

ADR 0007 init/adopt semantics remain. ADR 0009 host activation, custody and
successor-receipt boundaries remain. Historical release contracts are unchanged.

For v0.7+, this decision creates the **sole project-owned absent-path exception**
to ADR 0007 and ADR 0009 upgrade-preservation rules: the target CLI may create
`.vibe/onboarding.json` only for one of the three compiled identities above, only
while the leaf is absent, and only with canonical schema-1 `pending` bytes inside
the upgrade transaction. It grants no ownership over an existing onboarding file
or any other project-owned path. ADR 0007/0009 preservation remains authoritative
in every other case.

## Recovery and rollback

- A caught failure with successful rollback restores the scoped preimage, clears
  active state and returns `rolled-back`.
- A final-leaf race never deletes a third-party object. Exact compensation may
  restore reachability, but the transaction stays active and unknown unless the
  exact predecessor pair is proved and the closed rolled-back result applies.
- Rollback/cleanup failure preserves private evidence and returns the truthful
  recovery-required or unknown-partial state.
- Source implementation rollback is Git revert of reviewed v0.7 commits.
- Published-project downgrade is a separately selected trusted older payload, not
  failed-upgrade recovery.
- No user file, stale path or external GitHub object is deleted automatically.

## Verification

Verification covers exact v0.2 historical fixture and official v0.3–v0.6
families; all onboarding states; unsupported platform/path/race failures; every
intent/stage/preimage/journal/replacement/AGENTS/onboarding/manifest/version/
marker/fsync/cleanup fault point; rollback success/failure; subprocess interruption;
repeat recovery; tamper/symlink/unknown path/divergence/concurrency; byte/existence/
mode snapshots; result/status/exit/takeover matrices; package exclusion; existing
conflict/source/stale regressions; and secret/traceback/stdout behavior.

Lossless-leaf verification injects deterministic races after final
prevalidation; before and after hard link, exchange, displaced-object
verification, compensation, alias removal and no-replace rollback; and at every
fsync/event boundary. It covers absent and existing leaves, byte-identical
different inodes, in-place writes, deletion, symlinks, directories, permissions,
forward and rollback replacement, and a second writer during compensation.
Every third-party byte must remain reachable; ordinary rename/replace or direct
final-leaf unlink is forbidden; no race branch may commit; and the result must be
truthful. Crash tests cover every probe, temporary, prepared, link, exchange,
rollback, commit and cleanup boundary. Real libc integration runs on macOS and
Linux, with mocked missing-symbol and errno branches, Python 3.9, network-disabled
execution and the full regression suite.

Directory-unit verification covers exact official v0.6 to v0.7 and every direct
predecessor lacking `.agents/skills/vibe-release/`; read-only plan snapshots;
one- and multi-level missing chains; multiple members and disjoint units;
rejection of overlap, incompleteness and project-owned members; every unit,
probe, back-reference, object-identity, digest and commit schema negative; and
fault injection at intent, probes, staged mkdir/write/chmod/fsync/walk, prepared,
publication, verification, event/fsync, rollback detach/restore and recursive
private cleanup. Races create files, symlinks or directories at final root,
replace/detach parents, and add/remove/modify/replace members before verification
and rollback. Crash tests cover every directory crash-table row with repeat
recovery. Real macOS/Linux no-replace integration and mocked symbol/errno failures
are required. Tests prove no ordinary final mkdir, replacing rename or recursive
final-tree deletion occurs, and all private stages/probes/markers are excluded
from manifests, packages, Plugin payloads and release assets. Every failure
snapshots predecessor paths, modes, third-party bytes and both sibling identities;
rolled-back requires exact original absence, otherwise unknown-partial.

## Open decisions

None. The lossless leaf protocol preserves the accepted product commitment and
does not require a material user choice. A best-effort fallback or weakened
never-overwrite guarantee would require one and is rejected. Narrowing direct
support, expanding create-only eligibility, weakening
handled-failure rollback, expanding the transaction beyond `upgrade`, or
overwriting project state requires a new material product decision.
