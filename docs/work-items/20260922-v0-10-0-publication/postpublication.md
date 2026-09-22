# Postpublication record — Vibe Kit v0.10.0

- Date: 2026-09-22 (Asia/Shanghai)
- Executor: Hermes orchestrator, under the product owner's single authorization of
  2026-09-22 covering the archived operation plan (push, tag, non-draft Pre-release,
  five assets, postpublication acceptance, closeout of #8–#13).
- Published source: `96285138a620c4c9a076c64b16efef61c775fbb0` (local `main`, previously
  unpushed by design). Frozen publication intent digest:
  `3092fa1d1c2b0582b6478e404f9f1d441f952dd3b1d7a2976c8f4ef4f7efb842`.

## Publication operations (all read back)

| Operation | Result |
|---|---|
| Fast-forward `main` | `54451c310d078c43db29f681323c5a7cef4b319f` → `96285138a620c4c9a076c64b16efef61c775fbb0`, CAS-checked; read-back equals target |
| Annotated tag `v0.10.0` | tag object `ea86da049f3aa6c579016bd7cf9309e592128a7c`, peeled `9628513…`, message sha256 `20d416e9…`; all equal to the intent |
| GitHub Pre-release | id `393445539`, <https://github.com/mintgao/vibe-kit/releases/tag/v0.10.0>; title `Vibe Kit v0.10.0`; non-draft, prerelease; body bytes equal `docs/releases/0.10.0.md` (sha256 `2515964b…`) and the intent |
| Five assets | SHA256SUMS `7d3dbb57…`, release-manifest.json `950828da…`, vibe-kit-0.10.0.zip `2fd82577…`, vibe-kit-distribution-0.10.0.zip `f3675cfe…`, vibe-kit-plugin-0.10.0.zip `4105177f…`; API sizes and digests equal the frozen intent |

Publication receipt canonical digest:
`138b7b9fc024e58e823a7a99e5118a59bbbbede9b4f284a253896582d6fea455`
(`remote_write_state: confirmed-complete`, `verification_state: passed`; offline
validation envelope `ef6026f0…`, `status: valid`, executed on CPython 3.9 as required).

## Postpublication acceptance (independent)

- Executed by an independent QA subagent (separate session) running a pre-written
  run-shaped harness exactly once; exit 0; verdict PASS.
- Acceptance receipt: execution `postpub-qa-1790052060`, 2026-09-22T04:40:50Z–04:41:00Z;
  canonical digest `c7b746cc3f638ae11ba984eaeae98ede9bdecea80cf33dd5774d930bfdbc767d`;
  `status: passed`; AC-1…AC-7 with evidence references.
- Fresh evidence gathered in that run: five unauthenticated public downloads
  (5/5 byte-matched), canonical reconstruction passing `validate-release`, eight public
  smokes passing from the published assets, and live read-backs bound to the frozen
  intent (main, tag object+message, Release identity and body hash, five asset
  identities).

## Closeout of #8–#13

- Plan validated offline (six-reference `issue-closeout` packet): closeout intent
  digest `a8f81224525bc1f36a0ee854c2ead5c43134522b99debebadd8773a626fef389`;
  closeout id `27e450dd1568e58ac87c74d65a2ed776daeead5f5b0029b9272c9cca3da08214`.
- Separate closeout authorization bound at 2026-09-22T04:45:08Z.
- Twelve operations executed 2026-09-22T04:45:08Z–04:45:44Z; every operation read back
  (exact comment present, issue closed):
  - #8 → comment `5771333408`
  - #9 → comment `5771334092`
  - #10 → comment `5771334775`
  - #11 → comment `5771335449`
  - #12 → comment `5771336108`
  - #13 → comment `5771336941`
- Closeout receipt canonical digest
  `86eef5fafc0c8108942dfc6eaa51a707da72f4db1daf36d19d836c545cc84e1a`,
  `overall_state: confirmed-complete`.
- Final validation (eight-reference packet, offline): `status: valid`, `errors: []`;
  all six issues read back as closed/completed with exactly one evidence comment each.

## Execution anomaly and remediation (kept for the trail)

- Offline validation via `validate-publication --receipt <path>` first *read* the receipt
  (the `valid` verdict and its receipt-derived fields stand), but the CLI's global
  `--receipt` wiring (bin/vibe:13671–13678 → `print_json` → `write_receipt_artifact`,
  bin/vibe:954–958) then *overwrote that same path* with the validate-publication result
  envelope. The result envelope therefore also appeared at the receipt path; the
  canonical result was preserved on stdout and is the artifact referenced above.
- The publication receipt was restored deterministically (regenerated from the frozen
  observation record and public-verification outputs; restored canonical digest
  `138b7b9f…` byte-equal to the build-time value).
- The postpublication acceptance was re-run end-to-end against the restored inputs
  (superseded v1 acceptance `43c11bbc…` is archived with an anomaly note); the v2 record
  above is the binding one.
- Follow-up candidate for the next feedback loop: the read/write dual meaning of
  `--receipt` on `validate-publication` silently replaces its input artifact.

## State

- The release points at `9628513…`; this record is the causally later evidence commit
  with no tag movement. The main-branch evidence push (if performed) must be a separate,
  explicitly authorized CAS push.
- No other GitHub write occurred under the 2026-09-22 authorization beyond the six
  publication operations and the twelve closeout operations above.
- The Hermes host keeps its supported-unverified conformance label (ADR 0019); this
  release claims no host activation and no measured token reduction.