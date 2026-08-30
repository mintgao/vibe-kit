# Design: Vibe Kit v0.7.0 resilient upgrade and publication flows

## Design principles

- Prove local preconditions before project writes, and prove remote preconditions before GitHub writes.
- Report local installation writes, remote publication writes, and verification as separate states.
- Use one explicit next action for blocked or uncertain outcomes; never rely on color, cursor position, table alignment, or a Python traceback.
- Keep commands non-interactive and JSON closed/stable. The Agent presents plans and binds consent; local package/install/upgrade remain offline.

## Legacy onboarding bridge

For an authenticated audited v0.2-v0.4 predecessor from before persisted onboarding, `plan upgrade`
shows one explicit create-only entry:

```text
CREATE   .vibe/onboarding.json — legacy compatibility bridge; pending only, no context inferred
```

The JSON plan/apply receipt exposes an `onboarding_bridge` object with closed
`planned`, `applied`, `preserved`, `not-needed`, or `blocked` state, predecessor
eligibility, path, from/to state and content digest. The only created content is:

```json
{"schema_version": 1, "status": "pending"}
```

The bridge never invents `complete`, evidence or `updated_at`. Existing valid
onboarding is byte-preserved. Missing onboarding in v0.5/v0.6, or malformed,
wrong-type, symlinked, unreadable or raced state in any family, blocks before any
transaction/control/project write. A successful first target doctor reports persisted
`pending` without a blocking missing-state diagnostic; adaptation still waits for
positive target activation.

## Upgrade transaction and recovery

The CLI transaction model distinguishes invocation writes from installation state:

| Outcome | Write state | Installation meaning |
|---|---|---|
| Failure before any invocation write | `none` | predecessor unchanged |
| Active/stage/preimage control state created and cleaned before installation mutation | `transaction-control-written` | predecessor unchanged |
| Failure followed by verified rollback | `rolled-back` | predecessor restored after attempted writes |
| Successful commit and target verification | `project-files-written` | target installed |
| Integrity-valid unfinished transaction | `recovery-required` | explicit `recover-upgrade`; activation forbidden |
| Tampered or unclassifiable state | `unknown-partial` | inspection required; no automatic recovery |

JSON results include bounded transaction state, from/target versions, failure
phase, a project-relative failed path when known, installation-state conclusion,
and exactly one `next_action` for non-success. JSON mode emits one object on stdout
and no traceback/stderr; text mode emits a concise error on stderr.

Transaction members are integrity-checked but untrusted; a same-OS-principal
malicious writer is outside the threat model. All mutations and recovery are rooted
at a pinned project descriptor with `dir_fd`/`O_NOFOLLOW` traversal, file and
directory fsync, compare-and-swap validation, and an independently atomic
`commit.json`. Unsupported filesystem/platform primitives block before mutation.

`doctor`, `plan upgrade` and `upgrade` detect incomplete transaction evidence and
fail closed. Recovery has its own explicit entry point; blindly rerunning upgrade
is not recovery. Recovery validates the journal, project root, allowed relative
paths, preimage/target hashes, path types and external divergence before restoring
or completing any state. A third-party value is never overwritten silently.

Recommended summaries:

- unchanged: `Upgrade failed before installation files changed.`
- rolled back: `Upgrade failed, and the previous installation was restored and verified.`
- recovery required: `Installation state cannot yet be proven as either predecessor or target. Do not retry or activate the new rules.`

## Exact source trust language

Current contracts use this meaning:

> An exact canonical tag or Release URL selects a specific published version,
> including a pre-release. It does not by itself prove that the tag or Release is
> platform-immutable. Trust the downloaded artifact only after its SHA-256 and
> nested release validation pass.

Machine and human reports keep repository identity, exact version ref, artifact
digest, payload-tree identity and observed platform immutability separate. Moving
refs remain blocked. GitHub's `immutable` field is observed and recorded for the
public release but is not a v0.7.0 Pre-release gate.

## Dry-run-first publication workflow

The product has one Agent-facing release workflow with four conceptual phases:

1. **Plan** — validate the exact clean candidate and remote observation, then
   freeze a canonical intent binding expected-old/target commits, annotated tag
   object, exact Release body/state and the final sorted five-asset set; perform no
   remote writes.
2. **Apply** — after two-layer authorization binds scope, intent digest and host
   operation ID, fast-forward `main` under lease and create or verify the exact
   annotated tag, non-draft Pre-release and asset set. Every uncertain response is
   read back (and assets downloaded/hashed) before retry; identical state is
   idempotent success and divergence or an extra asset is a conflict.
3. **Inspect/verify** — read back main/ref/Release/asset metadata, record observed
   platform immutability, download from the canonical Release URL, rerun checks and
   smoke tests, and persist sanitized work-item evidence.
4. **Issue closeout** — only after confirmed publication and passed public
   verification, freeze an intent for exactly #1-#5; read all pre-states first,
   post marker-bound exact evidence comments, close only after comment confirmation,
   and read back every uncertain write. Never edit/delete/reopen an issue object.

The canonical plan includes repository, version/tag, expected-old and target
commits, exact annotated-tag object identity, Pre-release state, release title/body
hash, exact sorted asset names/sizes/SHA-256 and asset-set hash, local gates,
remote preconditions, ordered read/write steps, authorization boundary and
recovery policy. A changed commit, body, asset or remote precondition invalidates
the plan digest.

The release manifest declares names/roles but never hashes itself, the outer
distribution archive or `SHA256SUMS`; the publication intent is the sole outer
closure binding all five final files.

Remote outcomes are separately reported as `none`, `confirmed-partial`,
`confirmed-complete`, or `uncertain`; verification is `not-run`, `passed`,
`failed`, or `uncertain`. A remotely complete Release with failed public-download
checks is `published-unverified`, not silently deleted and not announced as
verified. Delete, force-move, replacement or remote rollback requires separate
destructive authorization.

The current canonical repository already exists. Repository creation, Stable
promotion, public Plugin Directory publication and automatic updates are outside
this flow.

## Accessibility and automation

- Text output uses explicit `Status`, `Reason`, `Write state`, and `Next action`
  labels, one item per line, with full SHA/URL on their own lines when needed.
- Non-TTY and JSON modes emit no ANSI styling. State is never color-only.
- Success has `next_action: null`; blocked/uncertain has exactly one next action.
- Expected exit behavior remains: `0` safe/success/verified-existing, `1` an
  executed diagnostic or post-publication verification failure, `2` usage,
  preflight, conflict, permission or uncertain outcome.
- Receipts, journals, release plans and public evidence exclude credentials,
  environment values, raw unbounded host output and goal/conversation content.

## Scenario matrix

- Exact historical v0.3.0 and v0.4.0 missing-onboarding plans/applies, v0.5.0
  contract migration, ordinary v0.6.0 upgrade, every valid onboarding state,
  malformed/type/symlink/race cases.
- Permission failure at staging, each commit mutation and finalization; rollback
  success/failure; crash at each persisted phase; tampered journal/backups;
  external divergence; retry after successful recovery.
- Exact tag/Release URL/commit acceptance, moving-ref/version/digest rejection,
  terminology scan and live public `immutable` metadata consistency.
- Publication dry-run no-write proof, stale approval, new and already-identical
  publication, tag/Release/asset conflicts, timeout/read-back match/absent/unknown,
  auth/permission errors, public download tamper, validate/install/Plugin/upgrade
  smoke failures, stdout/stderr/schema and secret-redaction checks.
