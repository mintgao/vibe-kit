# Bilingual Agent-first project homepage and brand

- ID: `20260828-bilingual-homepage-brand`
- Size: `M`
- Status: complete
- Created: 2026-08-28

## Technical decision readiness

- Outcome: `no-new-durable-decision`
- Trigger evidence: The work changes a selected brand asset and two public documentation pages. It does not change a durable/shared contract, component boundary, schema, protocol, compatibility behavior, migration, trust boundary, recovery behavior, or irreversible state.
- Decision owner: Workflow orchestrator
- Governing decision: none
- Review mode: `not-required`
- Review result: `not-required`
- Review evidence: M-sized trigger scan found only local, reversible documentation and asset choices. The Agent-install contract, release channel, protocol versions, compatibility boundary, and CLI behavior remain unchanged.
- Material product decisions: Resolved — the user selected logo direction 3, requested complete English and Chinese pages, identified ordinary Agent users as the primary audience, and supplied the four-part reading flow.
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-08-27T16:49:00Z`
- Confirmation basis: User-approved visual direction and content flow, product and UX shaping, complete acceptance criteria, no-new-durable-decision trigger scan, unchanged v0.5.0 Agent-install and trust contracts, and no open blockers.
- Readiness history: `2026-08-28 — work classified M; PM and UX read-only shaping completed; user-visible scope and selected logo were resolved; trigger scan found no new durable technical decision; workflow orchestrator confirmed implementation-ready before editing shared assets or README files.`

## Goal

Make the GitHub project homepage understandable and usable for ordinary Codex users without requiring them to learn Vibe Kit's CLI, Skill names, lifecycle operations, or internal roles. A visitor should understand the product, see its main outcomes, copy one Agent-first adoption prompt, and continue development in ordinary language. Professional and maintainer details remain available in a clearly secondary appendix.

## Context

- Vibe Kit 0.5.0 is a public GitHub Pre-release with Agent-first adoption and Technical Decision Readiness Gate capabilities.
- The current default README is Chinese and mixes the ordinary user path with long maintainer, distribution, feedback, and limitation material.
- The user selected the third generated logo direction: a modular mint-colored M whose nodes end in a verified check state.
- [Agent-first adoption design](../20260827-agent-first-adoption/design.md) defines the two-moment user experience and keeps CLI details internal.
- [0.5.0 release notes](../../releases/0.5.0.md), [Agent installation contract](../../../AGENT_INSTALL.md), `agent-install.json`, and accepted decisions remain the factual source of truth.

## Scope

- In: make `README.md` the complete English default homepage and add a complete, semantically aligned `README.zh-CN.md`.
- In: add the selected logo as a repository asset and use it in both Hero sections with meaningful alternative text.
- In: organize both pages as purpose, four main capabilities, installation/use, and a professional developer/maintainer appendix.
- In: use the exact v0.5.0 Release URL in copyable existing-project and new-project Agent prompts.
- In: preserve links to detailed release, installation contract, architecture, decisions, upgrade, verification, and feedback material.
- In: update the README-facing workflow contract test so it verifies equivalent English and Chinese disclosures after the default-language change.
- Out: CLI, Agent contract, Skills, managed workflow, protocols, release assets, tag, compatibility behavior, public Plugin Directory, stable promotion, automatic updates, or publisher signing.
- Out: claiming generic coding-Agent support, whole-install transactionality, or completion of the separate permission-safe atomic-upgrade work.
- Out: committing or modifying unrelated user-owned worktree changes.

## Acceptance criteria

- [x] AC-1: Both Hero sections contain the selected logo, a textual `Vibe Kit` title, one-sentence value proposition, exact `v0.5.0 Pre-release` link, and reciprocal language navigation.
- [x] AC-2: English and Chinese pages follow the same four-part order and carry equivalent promises, examples, limitations, and link semantics; neither is a summary of the other.
- [x] AC-3: The ordinary-user path states that a user gives Codex a trusted Release link and project goal, without requiring CLI commands, `init`/`adopt`, or internal Skill names.
- [x] AC-4: The main-capability section contains no more than four outcome-oriented items covering safe adoption, evidence-backed project understanding, workflow routing, and risk-aware verified delivery.
- [x] AC-5: Existing-project and new-project sections each provide a directly copyable natural-language prompt using `https://github.com/mintgao/vibe-kit/releases/tag/v0.5.0`.
- [x] AC-6: Installation/use is explained as three user-visible steps, and the installed-state examples cover feature work, debugging, and release verification in ordinary language.
- [x] AC-7: Main-section claims are supported by current repository evidence, identify Codex as the verified host, and do not describe the readiness workflow as a mechanical CLI file lock.
- [x] AC-8: The final appendix contains architecture/ownership, CLI/health, trust/release/compatibility, upgrade/conflict, verification/release engineering, feedback/privacy, and current limitations.
- [x] AC-9: Logo alternative text is meaningful, the written title and purpose remain understandable without the image, and the Hero remains readable at common GitHub desktop and mobile widths.
- [x] AC-10: All local Markdown links, asset paths, and external Release links are valid; no recommended installation source follows `main`.
- [x] AC-11: The change set contains only the two homepage files, selected logo asset, the README-facing contract-test update, and this work item's artifacts; existing permission-safe atomic-upgrade changes remain untouched and unstaged.
- [x] AC-12: Independent QA maps every criterion to observed evidence and records automated checks, manual limitations, and the exact change boundary.

## Design and technical notes

- Use `README.md` for English and `README.zh-CN.md` for Simplified Chinese. Both pages share the same hierarchy and reciprocal language links.
- Keep one H1 and four user-level H2 sections. The appendix may use H3 subsections. Only the Hero is centered.
- Use the selected RGBA logo as a real asset. Normalize its whitespace for GitHub presentation without redesigning the chosen mark; target a 128–144 px Hero display width and retain enough transparent safety area for light and dark themes.
- Prefer the exact Release URL because the bare repository currently has no stable Release and would require one additional Pre-release decision.
- Keep maintainer commands and protocol details out of the first three sections.
- Detailed UX constraints and content hierarchy are recorded in [design.md](design.md).

## Risks and open decisions

- The generated logo has generous transparent whitespace and slight rendered edge effects. A conservative crop is permitted, but visual redrawing or reinterpretation is not.
- README facts can drift from machine contracts. Keep protocol detail short and link to normative files rather than duplicating every enum or rule.
- v0.5.0 remains a Pre-release. The homepage must not imply stable status or verified non-Codex compatibility.
