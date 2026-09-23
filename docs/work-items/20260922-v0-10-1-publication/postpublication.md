# Post-publication: Publish Vibe Kit v0.10.1

Executed under the owner authorization bound to the frozen intent digest
`0ed6d34facecb5f35b432c8d08cbf250950c86673941205ad149fe8ecde89d16` (owner reply
`批准发布` to the presented digest; authorization and bound time recorded in
`publication-authorization.json`). Six operations, no destructive operation, no
force, no delete, no replace, no Issue mutation.

## Result

| Fact | Value |
|---|---|
| Main | fast-forwarded under an expected-old-OID lease `dc88d3fdccdfbd781298ab0e22718a0fdb6f0e7d → 409d67a6bb6f25a45d54b432d3fab2a9e42f852e` |
| Annotated tag | `v0.10.1` = tag object `2fd9de205bf05dea6ab6dbf66a24e15b38fe605b`, peeled commit `409d67a6bb6f25a45d54b432d3fab2a9e42f852e`, tagger `mintgao`, message `Vibe Kit v0.10.1` (`9fd35300…`) |
| Release | id `394214638`, `https://github.com/mintgao/vibe-kit/releases/tag/v0.10.1`, non-draft Pre-release, title `Vibe Kit v0.10.1`, body sha256 `a0d919e72539aab34698e57783fb243f571f5888b3f27fa7687c68e5de33120c` (byte-equal to the frozen note), `immutable=false` reported from the live API |
| Assets | `SHA256SUMS` id 582601276 `64d9104b…`; `release-manifest.json` id 582601279 `f95f6063…`; `vibe-kit-0.10.1.zip` id 582601280 `ece6fbcc…`; `vibe-kit-distribution-0.10.1.zip` id 582601281 `9f034a69…`; `vibe-kit-plugin-0.10.1.zip` id 582601277 `60cb9910…` |
| Write state | `remote_write_state: confirmed-complete`, `verification_state: passed`; `validate-publication` `status: valid`, zero errors, executed on CPython 3.9.6; `host_evidence_authenticated: false` (the CLI cannot authenticate GitHub — live public evidence is retained instead) |

## Operations

| Seq | Kind | Outcome | Read-back |
|---|---|---|---|
| 0 | `fast-forward-main` | `updated` | remote `main` = `409d67a…` |
| 1 | `create-or-confirm-annotated-tag` | `created` | ref = `2fd9de20…`, peeled `409d67a…` |
| 2 | `create-or-confirm-prerelease` | `created` | id `394214638`, non-draft Pre-release |
| 3 | `upload-or-confirm-five-assets` | `uploaded` | five asset child ledgers, each `uploaded` with a matching read-back |
| 4 | `read-back-publication` | `verified` | main, tag and Release re-read; five assets present |
| 5 | `download-and-verify-public-assets` | `verified` | five public downloads, all five digests matched |

Each write records a pre-write observation and a read-back observation; the
ledger keeps both.

## Transport incident and resume

The first attempt's `create-or-confirm-prerelease` failed with a proxyconnect
error against the local proxy (`127.0.0.1:7897` GraphQL refused) *after* main and
tag had been written and read back. The same intent was resumed: main and tag
were confirmed by read-back and never rewritten, the Release was created
directly and read back, then the five assets. Both attempts are in the ledger;
the retry followed a positively observed absence, which the intent's recovery
policy permits.

## Public verification

- Nine public smokes, exactly the schema-5 profile set and order, all `passed`
  from public artifacts only: `public-direct-init-doctor` (`80adba93…`),
  `public-plugin-bundled-plan-init-doctor` (`294282c1…`), `public-upgrade-v0.3-to-v0.10.1`
  (`f0ed966b…`), `v0.5` (`67991d5b…`), `v0.6` (`316bfa98…`), `v0.7` (`c7e08787…`),
  `v0.8` (`1a262e34…`), `v0.9` (`3597140243…`), `public-upgrade-v0.10.0-to-v0.10.1`
  (`e65ddae3…`). Each install/upgrade ends doctor-healthy with the recorded
  framework version `0.10.1`.
- All five public downloads match the frozen asset digests.
- `validate-publication` on the frozen candidate: `valid`, zero errors, CPython 3.9.6.

## Claims and non-claims

- Now supported: “v0.10.1 published and verified” — the remote write state is
  `confirmed-complete`, public verification passed, and the receipt validates
  against the frozen intent under the separate authorization.
- Still not claimed: platform immutability (`false` from the live API), publisher
  signing, provenance, host activation on any host, measured token reduction, and
  the deferred #14/#15 fixes.

## Evidence (host-side, gitignored)

| Artifact | sha256 |
|---|---|
| `publication-ledger.json` | `43e8c4b3…` |
| `publication-request.json` / frozen intent | `f90152eb…` / `b2914cff…` |
| `release-gate-bundle.json` (canonical digest `985a3d4c…`) | `62ab6599…` |
| `publication-receipt.json` (pristine copy kept aside) | `beeb94e9…` |
| `publication-authorization.json` | `b38b4b84…` |
| `validate-publication-result.json` | `faf36fbd…` |
| `smokes/smokes-summary.json` | `45925eff…` |
| publish / resume / receipt-builder / plan-inputs / smokes-runner scripts | `f82babcc…` / `e26899c4…` / `6a4c0d03…` / `5e70fd7c…` / `23f32387…` |

`validate-publication` overwrites the receipt path it is given (the CLI's global
`--receipt` wiring writes the result envelope at print time), so the pristine
receipt is kept under a separate name and the validation run is given a
throwaway copy; the pristine receipt was restored and hash-verified afterwards.

## Follow-ups

- This evidence commit is local and unpushed: pushing it is outside the
  publication operation set and needs its own authorization (`evidence_pushed=false`).
- Feedback `fb-20260921t171134z-3d4dc8cc` was dismissed locally (`handled-local`,
  reason recorded) by owner decision; no Issue was opened.
- Issues #14 and #15 stay open for the next iteration; the Codex five-stage
  refresh remains a delivered handoff on its older evidence.
- A later version boundary must open its own publication profile; the schema-5
  profile stays closed and bound to `v0.10.1`.
