# Design: bilingual Agent-first project homepage and brand

## Audience and reading goal

The primary reader uses Codex to create or maintain a project and does not want to learn Vibe Kit's internal CLI or role vocabulary. The secondary reader maintains Vibe Kit or needs its technical and trust boundaries.

The main page should let the primary reader stop after installation and use. The appendix preserves professional depth without competing with that path.

## Page hierarchy

1. Hero: selected logo, textual product name, one-sentence value proposition, language switch, and exact current Pre-release link.
2. Purpose: two short paragraphs explaining the repository-pinned Agent workflow and the current Codex compatibility boundary.
3. Main capabilities: four vertical, outcome-oriented items for safe adoption, project understanding, workflow routing, and risk-aware verified delivery.
4. Install and use: three human-visible steps, followed by copyable prompts for existing and new projects and ordinary-language daily examples.
5. Professional appendix: architecture and ownership, maintenance commands, trust and compatibility, upgrades and conflicts, verification and release engineering, feedback and privacy, and current limitations.

## Brand asset

Use the user-selected third direction from the 2026-08-28 visual exploration. The modular mint M represents connected Agent roles and a workflow ending in a verified check node. Preserve that concept and color relationship.

- Display the centered mark at 136 px in both Hero sections.
- Keep the `Vibe Kit` H1 and purpose text independent of the image.
- Use equivalent, descriptive alternative text in each language.
- Preserve transparency and enough safety area for GitHub light and dark themes.
- Do not rely on mint color as the only carrier of state or meaning.

## Content behavior

- `README.md` is the complete English default page; `README.zh-CN.md` is the complete Chinese counterpart.
- Language navigation uses `English · 简体中文` with the current language unlinked.
- Prompts use blockquotes so they wrap cleanly on mobile.
- Main content avoids tables, badges, ASCII diagrams, and internal command names.
- The appendix is visibly secondary but not hidden, so maintenance and trust limitations remain discoverable.
- Current status is written as `v0.5.0 Pre-release`; it is never communicated by color alone.

## Agent-first flow

The visible flow has three steps:

1. Give Codex the exact trusted Release link and a project goal.
2. Codex verifies the source, checks impact, adopts the Kit, checks health, and establishes project context internally.
3. Continue describing feature, debugging, design, implementation, or release goals in ordinary language.

When a host cannot reload newly installed repository instructions, the only general fallback is to open a new task in the project and state the original goal normally. The user is not asked to run a CLI command or name a Skill.

## Factual boundaries

- Codex is the currently verified adapter. The page does not promise universal coding-Agent compatibility.
- v0.5.0 is a Pre-release and the exact Release URL is the recommended shortest path.
- Installation is not described as a whole-directory transaction.
- Technical decision readiness is a repository workflow contract, not a mechanical CLI write lock.
- The separate permission-safe atomic-upgrade work is not part of this change.
