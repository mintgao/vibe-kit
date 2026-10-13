# Verification: Verification observability and feedback closure

Independent final-candidate QA passed on commit `f138e7df4daed1097ca6ac5d6ccb59125fb19a07`, tree `622512c15d7939b328fa650b21a18993eafbf265`. The final writer stopped before a distinct reviewer approved the exact candidate; the workflow orchestrator froze it before independent QA. This is source development, with no installed downstream project changed.

## Acceptance evidence

| Criterion | Result | Evidence |
|---|---|---|
| AC-1 / #14 | Pass | Valid, invalid and malformed publication inputs remain byte-identical; distinct create-only results reject aliases, candidate descendants and unsafe parents; historical profiles retain their verdicts. The later actual publication validation also preserved all three input byte hashes. |
| AC-2 / #15 | Pass | Equality-aware upgrade expectations, mode drift, two committed same-version upgrades, race/recovery protections; later public repeat smoke passed. |
| AC-3–AC-4 / #16 | Pass | Complete sanitized success output beyond 16 KiB, bounded default results, private modes, deterministic log identity, concurrent reuse and honest optional-storage/resource failures. |
| AC-5–AC-6 / #17 | Pass | Actual silent/output slow checks, durable before-check metadata, locator ordering, concurrent runs, handled signals, SIGKILL, startup failures, terminal transition and stdout backpressure; no incomplete run becomes Pass. |
| AC-7–AC-8 / #18 | Pass | Static source/distribution contracts and prospective outcome scenarios retain scope, state, next action, role owner, waiting conditions, S simplicity and existing readiness/QA authority. No live-model compliance or measured token reduction is claimed. |
| AC-9 | Pass | Actual CPython 3.9 compatibility, standard-library/offline operation, historical profiles and closed tamper/unknown-field cases. |
| AC-10.1 | Pass | Distinct approved implementation review, frozen final-candidate QA, bilingual homepage review and two independent clean deterministic builds. |
| AC-10.2 | Pass | Separate [public acceptance](postpublication.md), including fresh downloads and eleven actual public smokes. |
| AC-10.3 | Pass | Separate [five-issue closeout](closeout.md), individually read back and independently verified. |

## Executed gates

| Gate | Actual interpreter | Result |
|---|---|---|
| One canonical `./bin/vibe verify . --format json` | CPython 3.14.6 | 165/165 unittest cases; zero failures/skips |
| Distinct required complete Python 3.9/release compatibility gate | CPython 3.9.25 | 165/165 unittest cases; zero failures/skips |
| Publication/observability focused compatibility lane | CPython 3.9.25 | 37/37 cases |
| Clean build A plus explicit `validate-release` | CPython 3.9.25 | Passed |
| Separate clean build B plus explicit `validate-release` | CPython 3.9.25 | Passed; all five assets byte-identical to A |

Only `test` is configured. `lint`, `typecheck` and `build` are not configured and were not executed as configured checks. The second complete run was required by the distinct Python/release gate on the unchanged final candidate; no passing normal full matrix was repeated. Later public and documentation gates reuse these results rather than replaying them.

Canonical release-gate evidence SHA-256: `a17fb7af0cc1cfb7ca7369148aca5e637c9c6a382c80d92542f348d8c2d9ca72`. Final QA child receipt: `950453d5180fcd1b07f2529ce3df891a422a8c1bf6e98b757081953e3064018a`. Independent implementation review 3 file SHA-256: `9ae2f1094c47189b9302807ab3ba2f117771fdac0cd6ac8f106bff712f63f0d2`. Final QA report file SHA-256: `4139cf546b79a34365fe81ac9ac7c9e38d0931b7466e30b49da76bff20f23f7a`.

## Limits

Source progress was honestly unavailable for unsafe historical local diagnostic state; it was not rewritten or moved to a fallback. Complete independent receipts passed, and disposable available/unavailable progress scenarios were exercised. Progress is diagnostic, not proof of liveness or acceptance. Complete capture uses memory; selected logs use disk; sanitization detects known patterns, and descendant cancellation remains unproven. Original private raw evidence is retained outside source; this record contains only allowlisted facts and hashes.

The source checkout's ignored 0.10.1 installation state remained unchanged. Fixture doctor results establish installation health; no host activation or project readiness is inferred. The released source/tag/assets remain frozen; later evidence documentation is a separate commit.
