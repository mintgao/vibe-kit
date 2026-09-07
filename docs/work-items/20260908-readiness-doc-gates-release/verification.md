# Verification and publication evidence

- Status: complete; published-and-verified
- Date: 2026-09-08 (Asia/Shanghai)
- Independent QA: `/root/qa`; implementation writer: `/root/rd`
- Exact release source: `5e0fe0568be595ef8a992ef6f6e612ba2ed57bb3`
- Exact source tree: `c251f7d2afaf006918d099a76f64ffe75c46ed0c`
- Annotated tag object: `206475ce446cdbcc12be86183cb63804fad5789c`
- Public release: https://github.com/mintgao/vibe-kit/releases/tag/v0.9.0

## Acceptance mapping

| Criterion | Result | Evidence |
|---|---|---|
| AC-6.1 | Pass | Real Accepted ADRs pass; implemented notes and spoofed metadata fail. |
| AC-6.2 | Pass | Missing/malformed fields, paths and review evidence fail; independent QA found malformed Size quoting, which was corrected before publication. |
| AC-6.3 | Pass | Accepted/no-new positive routes and independent negative cases passed. |
| AC-7.1 | Pass | Single-line managed paragraphs, authenticated exact span and project-byte preservation passed. |
| AC-7.2 | Pass | The full merged 2858-word file fails its 2800-word ceiling even when the managed region alone fits. |
| AC-7.3 | Pass | No checker/ceiling rewrite; explicit counting policy and actual/threshold output verified. |
| AC-DOC.1 | Pass | Bilingual version, links, installation examples, capabilities and limitations reviewed; published labels synchronized after public acceptance. |
| AC-REL.1 | Pass | Exact schema-3 v0.9 and separate ordered #6/#7 closeout; historical profiles and parent/authorization isolation passed. |
| AC-REL.2 | Pass | 80 default tests; 80 actual Python 3.9 tests; 15 focused tests; 16 independent negatives; two clean byte-identical builds and both validators passed. |
| AC-REL.3 | Pass | Independent live identity, all five unauthenticated downloads, nested distribution validation and seven public smokes passed. |
| AC-CLOSE.1 | Pass | Independent paginated read-back confirmed both closed issues and one exact evidence comment per issue; all parent/receipt validators passed. |

## Candidate verification and invalidation

The first candidate `f6ab7218` was rejected by independent QA because malformed Size quoting was accepted. Its overlapping default-check output is mixed/stale evidence and was not used for release. RD repaired exact enum quoting, added regressions, regenerated identities and froze `5e0fe056`. Independent QA then ran the canonical default matrix once for that unchanged candidate. Actual CPython 3.9 full/focused checks and dual builds were separately identified release gates. No implementation changed after this accepted source was frozen.

The command was introduced by this release; it did not exist in the v0.8 baseline. Initial implementation was released through the then-current manual Accepted-ADR/independent-review gate before RD started. The new command's later successful invocation is not misrepresented as a preimplementation historical machine check.

Lint, typecheck and build are unconfigured; none is described as executed. All configured checks passed. Postpublication testing used downloads and installation/upgrade smokes rather than repeating the unchanged full suite.

## Public verification

Both clean builds produced the same exact five assets. Independent QA re-downloaded all five without authentication, matched every size/hash, reconstructed the nested distribution and passed its target validator on CPython 3.9.25. Live main, annotated tag, Release title/body/state and complete asset inventory matched the frozen intent. The public smoke set passed direct init/doctor, Plugin-bundled plan/init/doctor and healthy v0.3/v0.5/v0.6/v0.7/v0.8 upgrades to v0.9.

Publication executed the exact six-operation graph under existing user authorization bound to its frozen digest. Every write had read-back; no retry, replacement, deletion or tag movement occurred. The main update was ancestry-checked and protected by the exact predecessor lease. Host scripts received distinct technical review, including destination rewriting, full asset conflict preflight and honest failure observations.

`validate-publication` returned valid with empty errors, remote write state confirmed-complete and public verification passed. Later independent postpublication acceptance passed the first ten criteria. Only then did the separately bound closeout execute issue 6 comment/close and issue 7 comment/close. The standalone closeout validator and independent final issue acceptance passed.

## Closed issues

- #6: https://github.com/mintgao/vibe-kit/issues/6#issuecomment-5574037474
- #7: https://github.com/mintgao/vibe-kit/issues/7#issuecomment-5574038838

Both comments link the original problem, fix, regression source and public version, and preserve the limitations of structural validation and project-owned counting policies.

## Homepage and durable context finalization

Both README files change only the release-status label from the prepublication target to Latest published / 最新已发布 after public acceptance. Current product/architecture context and onboarding evidence now reference the published v0.9 result. The existing focused bilingual-homepage/managed-paragraph contract test passed (1 test); documentation whitespace validation also passed.

Distinct Tech Lead `/root/tl_review` confirmed this separate documentation-only finalization is covered by the user's homepage request and ADR0014. Its subsequent main update is bound to the exact documentation commit and expected release-source predecessor; it does not amend the six-operation publication receipt or move the release tag. Machine-readable allowlisted public facts and canonical receipt digests are in `public-evidence.json`; raw local/network execution evidence remains outside the source checkout.

## Limits

GitHub reports platform immutability false. The annotated tag is unsigned. No publisher-signature/provenance, stable/Directory publication, live host activation, filesystem write-lock or arbitrary counting-policy claim is made. Health and structural checks retain their documented scope. All eleven requested acceptance criteria passed within those boundaries.
