---
name: vibe-bootstrap
description: Plan and install the bundled, version-pinned Vibe Kit into a new or existing repository without using the network. Use when a user wants to initialize Vibe Kit, adopt it in an in-progress project, or understand the installation impact.
---

# Vibe Kit bootstrap

Use the Plugin-bundled payload; do not download from `main`, run `curl | sh`, or silently choose another version.

1. Use `init` for a newly created project, including a non-empty framework-generated scaffold. Use `adopt` for a project with established development history. Directory emptiness is only a safety guard: do not use `adopt` on an empty directory.
2. Resolve this Skill's directory and run `python3 scripts/vibe_from_plugin.py plan <init|adopt> <target>`. The wrapper locates the payload inside this Plugin.
3. Show the complete plan and any collisions. Planning is read-only. Stop on malformed `AGENTS.md`, an existing Vibe installation, or a managed-path collision.
4. When the user has requested that scoped installation and the plan is safe, run `python3 scripts/vibe_from_plugin.py <init|adopt> <target>`.
5. Run `<target>/bin/vibe doctor <target>`. For an existing project, ask Codex to run `$vibe-project-onboarding` in a new task so the repository instructions and Skills are loaded from the beginning.

Do not edit project-owned context to generic guesses after installation. `adopt` creates missing context conservatively; onboarding is where the repository is understood and refreshed.
