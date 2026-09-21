# Implementation plan: verification contract closure

- Work item: `docs/work-items/20260921-verify-contract-closure/brief.md`
- Governing decision: `docs/decisions/0017-verification-contract-closure.md`
- Writer: one writer (orchestrator, RD perspective) after the readiness gate is confirmed; review notes 2 and 3 of `technical-review.md#Pass 1` are resolved here.

## 1. Declared check order (AC-1, issue #9)

Concrete surface, since the decision allows dependencies or an order: a `checks` block in `.vibe/project.yaml`.

```yaml
checks:
  requires:
    test: ["build"]
```

- Semantics: `requires` maps a configured check to the checks it depends on. The effective order is a deterministic topological sort of the four configured checks, stably seeded by today's `lint → typecheck → test → build`, so a repository that declares nothing runs in exactly the previous order.
- Fail-closed validation (rule `verify.check-declaration`): `checks` must be a mapping whose only keys are `requires` and `output_limit_bytes`; every entry and dependency must be one of `lint`, `typecheck`, `test`, `build`; no dependency cycles; every failure message names the offending entry and the accepted values.
- The receipt's `default_order` field records the effective order actually executed, so a reader never has to infer it.

## 2. Output preservation (AC-2, F6)

- New optional `checks.output_limit_bytes`: absent keeps today's bound (the existing 16 KB tail plus truncation flags), and a value below the existing floor is rejected with rule `verify.output-limit` — the default can never downgrade.
- Every failed check additionally writes its complete captured stdout and stderr to a project-local artifact under `.vibe/local/verify/`, and the receipt references it as `output.full` with `path` and `sha256`. The digest binds the artifact, so a reader given only the receipt can reach the same per-file verdicts without re-running the check.
- Passing checks keep the current tail-only behaviour unless a bound is declared.

## 3. Environment-limited verdict (AC-4, F11)

- Classification trigger, defined here: the project may declare a `toolchain` block (for example `toolchain: {node: "24", python: ">=3.9"}`). Before running the checks, verify observes the actual versions of the declared tools and compares them with the declared expectations.
- A check that **fails** while a declared toolchain expectation is unmet is recorded with outcome `environment-limited` and `reason_code: toolchain-mismatch`, carrying the expected and observed versions; its raw exit code is preserved. A check that passes is never reclassified, and a failing check with no unmet declaration stays `failed`, so the state cannot launder a real failure.
- The receipt gains a top-level `toolchain` record of the observed versions (`python`, `node`, `pnpm`; `null` when the tool is absent).
- Summary and status: `environment-limited` counts with `skipped` toward the `blocked` status and exit code 2, and publication/closeout consume the receipt as not passing.

## 4. Closed contract updates (AC-5)

- `agent-install.json`'s verify declaration admits the `environment-limited` outcome (and its reason code) while continuing to reject unknown statuses, unknown outcomes and unknown skipped reasons; validation compares the declaration exactly, so the change lands in the same commit.
- Historical 0.7–0.9 receipts keep their recorded semantics; nothing rewrites them and no schema version moves here (the release work item owns version bumps).

## 5. Constrained-QA record form (AC-3, F10)

- The operating model gains the sanctioned path: on a host whose subagent budget is smaller than the lane, the orchestrator runs the complete default verification, an independent bounded subagent re-runs a pre-chosen focused subset of the same candidate, and the work item records the limitation.
- Machine-checkable form: the work item's `verification.md` must carry a `## Host capability limitation` section with exactly these labelled lines — `- limitation:`, `- complete run:`, `- independent focused re-run:` — and a regression test asserts the operating model states the path and that the form's labels are the required ones.
- This repository demonstrates the path on its own lane (about 40 seconds) rather than only documenting it.

## 6. Compatibility, recovery and rollback (AC-6)

- Additive only: new optional configuration, new receipt fields, one new outcome. An undeclared repository keeps the previous order, bounds and outcomes.
- Rollback: revert the change; no data migration, no rewriting of receipts, no profile boundary moves. The release-identity mirrors are regenerated in the same change (procedure recorded in `docs/work-items/20260921-readiness-naming-grammar/verification.md`).

## 7. Test plan (AC-7)

- `tests/test_cli.py`: declaration validation (unknown key, unknown check name, cycle, sub-floor bound), effective-order derivation and receipt recording, the untouched default order, output artifact plus digest for a failed check, toolchain observation, and the environment-limited path via a stub tool (a declared expectation the host deliberately violates).
- A docs-binding regression test for the operating-model path and the record labels.
- The full default lane stays green, `doctor` stays healthy, and `validate-readiness` stays valid for this brief.

## 8. Step order

1. Configuration parsing, order derivation and validation; receipt `default_order`.
2. Toolchain observation, the `environment-limited` outcome and the summary/status rules.
3. Output bound and the referenced full-output artifact with its digest.
4. `agent-install.json`'s verify declaration update.
5. Operating-model prose plus the docs-binding test.
6. Regression tests, release-identity regeneration, lane, `doctor`, then independent QA on the frozen candidate.