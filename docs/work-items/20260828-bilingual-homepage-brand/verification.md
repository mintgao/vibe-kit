# Verification: bilingual Agent-first project homepage and brand

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Both Hero sections contain the selected logo, textual H1, value proposition, reciprocal language navigation, and exact `v0.5.0 Pre-release` link. | Pass |
| AC-2 | Both pages contain the same four H2 sections in the same order, with aligned promises, examples, appendix topics, limitations, and link semantics. | Pass |
| AC-3 | The main path asks for a trusted Release link and goal; it contains no required CLI command, lifecycle command, or Skill name. | Pass |
| AC-4 | Each main capability section has exactly four source-backed items covering safe adoption, project understanding, workflow routing, and risk-aware verified delivery. | Pass |
| AC-5 | Existing-project and new-project prompts in both languages use the exact v0.5.0 Release URL. | Pass |
| AC-6 | Both pages expose a three-step user flow, ordinary-language feature/debug/release examples, and the one-new-task fallback. | Pass |
| AC-7 | The pages limit current compatibility to Codex, describe readiness as a workflow contract rather than a mechanical lock, and avoid claiming GitHub Release immutability. | Pass |
| AC-8 | Each final appendix contains architecture/ownership, CLI/health, trust/compatibility, upgrade/conflict, verification/release, feedback/privacy, and current limitations. | Pass |
| AC-9 | Logo alt text describes the modular M and verified node; the title and purpose remain textual. The 1024 by 1024 RGBA asset is readable at the 136 px Hero size and on a dark background. | Pass |
| AC-10 | All current local links and asset paths exist. GitHub API confirmed that the external v0.5.0 URL is public, non-draft, and a Pre-release. `main` appears only as a rejected moving ref. | Pass |
| AC-11 | The intended boundary is two READMEs, one logo, one README contract-test update, and this work item. The existing atomic-upgrade folder and index edit remained unchanged and unstaged during QA. | Pass |
| AC-12 | An independent read-only `vibe_qa` pass checked every criterion, repository facts, live Release state, static rendering constraints, and change isolation. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `python3 -m unittest discover -s tests -v` | Pass | 31 of 31 tests passed after the bilingual contract-test update. |
| `./bin/vibe verify .` | Pass | Configured project verification passed, 31 of 31 tests. Independent QA reran this after final copy fixes. |
| README local-link and asset-path scan | Pass | 24 references inspected; every local target exists. |
| README main-path structure scan | Pass | Four H2 sections per language, exactly four capability items, exact Release prompts, and no maintainer CLI fence before the appendix. |
| Chinese prose check | Pass with reviewed warnings | No hard violations. Two `范式` occurrences are intentional product terminology; short blockquote examples are intentional copyable prompts. |
| `git diff --check` | Pass | No whitespace errors. |
| Logo file inspection | Pass | 1024 by 1024, 8-bit RGBA PNG with alpha. |
| README workflow-contract test | Pass | 7 of 7 focused workflow contract tests passed in independent QA. |
| GitHub Release API | Pass | `v0.5.0` exists, `prerelease: true`, `draft: false`. API also reported `immutable: false`, which prompted correction of the homepage trust wording. |

## Manual scenarios

- Read the English and Chinese pages from Hero through appendix and compared section order, claims, prompts, examples, limitations, and link destinations.
- Viewed the normalized logo at its 136 px Hero size against a dark background; the modular M and verified check node remain distinguishable.
- Removed the image mentally from the reading order; textual H1, value proposition, and purpose still identify the product.
- Compared the final worktree boundary before and after QA. Existing `docs/work-items/index.md` and `docs/work-items/20260827-permission-safe-atomic-upgrade/` changes remained separate.

## Defects found and resolved

1. The first full test run failed because the former default Chinese README assertion had not moved with the bilingual homepage. The test now checks equivalent English and Chinese disclosures; all tests pass.
2. Both drafts linked to nonexistent `.vibe/core/feedback-policy.md`. They now link to the existing proactive feedback-loop design.
3. Both drafts said an exact tag or Release URL selects an immutable version. Live GitHub evidence showed `immutable: false`; the copy now says it selects a specific published version whose Release metadata and SHA-256 are checked before installation.

## Publication evidence

- Homepage implementation commit: `4e4ccff350c70f931a2fbe28b045e1537448ef82`.
- Remote `main` read-back after push resolved to the same commit.
- GitHub rendered the English default homepage with the selected Logo, centered title, language switch, current Pre-release link, and four-part content hierarchy.
- `https://github.com/mintgao/vibe-kit/blob/main/README.zh-CN.md` rendered the complete Chinese counterpart with the same Logo and content hierarchy.
- GitHub API confirmed `README.md` at 9,916 bytes, `README.zh-CN.md` at 9,199 bytes, and `docs/assets/vibe-kit-logo.png` at 454,680 bytes.

## Limitations and follow-ups

- Real Agent installation, task handoff, and Plugin-host scenarios were not rerun because this change does not modify those behaviors. The homepage explicitly says static string tests cannot replace behavioral evidence.
- GitHub live rendering was inspected after push for both language pages. The main layout remains table-free and mobile-friendly; broader device/browser sampling was not required for this Markdown-only change.
- `AGENT_INSTALL.md` and ADR 0007 still use immutable-source wording that does not match the GitHub API's current Release immutability state. This is outside the homepage scope and should be tracked through the Vibe feedback close flow.
- Final staging and publication excluded the existing atomic-upgrade worktree changes.
