---
name: vibe-bootstrap
description: Let Codex plan and install the bundled, version-pinned Vibe Kit into a new or existing repository without exposing internal CLI operations to the user.
---

# Vibe Kit bootstrap

Use the Plugin-bundled payload; do not download from `main`, run `curl | sh`, or silently choose another version.

1. Use `init` for a newly created project, including a non-empty framework-generated scaffold. Use `adopt` for a project with established development history. Directory emptiness is only a safety guard: do not use `adopt` on an empty directory.
2. Resolve this Skill's directory and run `python3 scripts/vibe_from_plugin.py plan <init|adopt> <target> --format json --source-type plugin-bundled --source-ref 0.5.0`. The wrapper locates the payload inside this Plugin. Keep this command and its archive details internal unless they explain a blocker or permission prompt.
3. Planning is read-only. Stop on malformed `AGENTS.md`, an existing Vibe installation, or a managed-path collision. Report only the concrete blocking paths and one recovery action.
4. When the user has already requested that exact scoped installation and the plan status is `safe`, run `python3 scripts/vibe_from_plugin.py <init|adopt> <target> --format json --source-type plugin-bundled --source-ref 0.5.0` without asking for redundant confirmation.
5. Run `<target>/bin/vibe doctor <target> --format json`. Installation is not complete if doctor status is `broken`; onboarding readiness is a separate result.
6. Repository instructions reliably activate in a new task. If this host cannot reload them, ask the user only to open a new Codex task in this project and state the development goal normally. Onboarding then runs automatically and resumes that goal; never require the user to name `$vibe-project-onboarding` or another internal Skill.

Do not edit project-owned context to generic guesses after installation. `adopt` creates missing context conservatively; onboarding is where the repository is understood and refreshed. Do not stream CLI commands or raw JSON during a healthy flow.
