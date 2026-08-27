# Implementation: bilingual Agent-first project homepage and brand

## Delivered changes

- Replaced the default Chinese-only `README.md` with a complete English GitHub homepage.
- Added `README.zh-CN.md` as a complete Chinese counterpart with the same hierarchy, promises, prompts, appendix, links, and limitations.
- Added the user-selected third logo direction as `docs/assets/vibe-kit-logo.png`. The selected mark was conservatively cropped to reduce excess transparent whitespace and normalized to a 1024 by 1024 RGBA PNG without redrawing the design.
- Used the logo at a fixed 136 px Hero width with meaningful alternative text in each language.
- Made the exact v0.5.0 Release URL the default copyable Agent entry point for existing and new projects.
- Moved CLI, protocol, ownership, upgrade, verification, feedback, privacy, and limitation material into the final professional appendix.
- Updated the README-facing workflow-contract test to require equivalent English and Chinese static-behavior disclosures after the default-language change.

## Implementation boundary

- No CLI, Agent contract, protocol, Skill, managed workflow, release artifact, tag, or compatibility behavior changed.
- The public homepage no longer calls the selected GitHub Release immutable. It accurately says that the exact URL selects a specific published version and that Release metadata and SHA-256 are checked before installation.
- The existing `AGENT_INSTALL.md` and ADR 0007 immutable-source wording remains outside this homepage-only change and is a separate feedback candidate.
- Existing user-owned changes in `docs/work-items/index.md` and `docs/work-items/20260827-permission-safe-atomic-upgrade/` were preserved and excluded from this implementation.

## Verification adjustments

The first test pass revealed that `tests/test_workflow_contract.py` expected a Chinese disclosure in the former Chinese default README. The test now verifies equivalent English text in `README.md` and the existing Chinese boundary in `README.zh-CN.md`.

Independent QA also found and prompted correction of a nonexistent feedback-policy link and an overstated immutable-Release claim. Both pages were rechecked after those corrections.
