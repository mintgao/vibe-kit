---
name: vibe-maintain
description: Let Codex diagnose or safely upgrade a repository-pinned Vibe Kit from the Plugin's bundled offline payload using structured internal operations.
---

# Vibe Kit maintenance

Keep the repository-pinned installation as the runtime source of truth. This Plugin is only a versioned maintenance channel.

- Diagnose with `<target>/bin/vibe doctor <target> --format json` when the installed CLI is runnable. Present health and onboarding readiness in goal language, not raw JSON.
- A request to “check the latest version” is read-only and does not authorize network access or upgrade. Report the installed project version and this Plugin's bundled version separately. Call `0.5.0` the bundled version, not the latest. A public latest-release lookup is a separate, explicitly authorized trusted-channel operation; this Skill does not perform it automatically.
- Before upgrading, resolve this Skill's directory and run `python3 scripts/vibe_from_plugin.py plan upgrade <target> --format json --source-type plugin-bundled --source-ref 0.5.0`. Report current/target versions and material preserved/conflict states only.
- Run `python3 scripts/vibe_from_plugin.py upgrade <target> --format json --source-type plugin-bundled --source-ref 0.5.0` only after the user requested that exact scoped upgrade and the plan status is `safe`; do not ask for redundant confirmation. Then run the installed `<target>/bin/vibe doctor <target> --format json` and the repository's configured verification when relevant.
- To validate a transferred release candidate, run `python3 scripts/vibe_from_plugin.py validate-release <release-directory> --format json` before using any contained payload.

Upgrade never replaces `.vibe/project.yaml`, `.vibe/project-rules.md`, or `docs/`; the Plugin must not regenerate project facts. Do not auto-update, fetch from the network, erase local modifications, resolve a three-way conflict silently, or edit version files to bypass diagnostics. If the bundled payload is older than the project, stop and obtain an explicitly selected trusted release.
