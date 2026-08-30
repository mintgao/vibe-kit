---
name: vibe-bootstrap
description: Let Codex plan and install the bundled, version-pinned Vibe Kit into a new or existing repository without exposing internal CLI operations to the user.
---

# Vibe Kit bootstrap

Use the Plugin-bundled payload; do not download from `main`, run `curl | sh`, or silently choose another version.

1. Use `init` for a newly created project, including a non-empty framework-generated scaffold. Use `adopt` for a project with established development history. Directory emptiness is only a safety guard: do not use `adopt` on an empty directory.
2. Resolve this Skill's directory and run `python3 scripts/vibe_from_plugin.py plan <init|adopt> <target> --format json --source-type plugin-bundled --source-ref 0.7.0`. The wrapper verifies the Plugin version and declared payload-tree identity before it runs the bundled target CLI. Keep this command and its archive details internal unless they explain a blocker or permission prompt.
3. Planning is read-only. Stop on malformed `AGENTS.md`, an existing Vibe installation, or a managed-path collision. Report only the concrete blocking paths and one recovery action.
4. When the user has already requested that exact scoped installation and the plan status is `safe`, run `python3 scripts/vibe_from_plugin.py <init|adopt> <target> --format json --source-type plugin-bundled --source-ref 0.7.0` without asking for redundant confirmation.
5. Run `<target>/bin/vibe doctor <target> --format json`. Installation is not complete if doctor status is `broken`; onboarding readiness is a separate result.
6. Apply and doctor do not prove runtime activation. This Plugin provides no reload or task-creation capability and currently supports only the manual new-task path. Unless the running host independently supplies a conforming live receipt, state that the files are installed and healthy but not activated, then give exactly one action: open a new Codex task in this project. Prefill or provide one copyable development-goal sentence; never require the user to name a CLI command or internal Skill.
7. The activated new task authenticates the installed framework-managed Agent-install contracts and passes its closed takeover object to installed `bin/vibe validate-takeover --format json`. A structurally valid result does not authenticate host evidence. It then validates actual manifest/activation-set identity, performs evidence-backed onboarding, runs default structured verification, re-evaluates the original goal under target rules, and resumes it. Only that task may announce readiness.

Do not edit project-owned context to generic guesses after installation. `adopt` creates missing context conservatively; onboarding is where the repository is understood and refreshed. Do not stream CLI commands or raw JSON during a healthy flow.
