---
name: vibe-maintain
description: Diagnose or upgrade an existing repository-pinned Vibe Kit from the Plugin's bundled offline payload, with a read-only plan before writes. Use for Vibe Kit doctor checks, controlled upgrades, or local release-candidate validation.
---

# Vibe Kit maintenance

Keep the repository-pinned installation as the runtime source of truth. This Plugin is only a versioned maintenance channel.

- Diagnose with `<target>/bin/vibe doctor <target>` when the installed CLI is runnable.
- A request to “check the latest version” is read-only and does not authorize network access or upgrade. Report the installed project version and this Plugin's bundled version separately. Call `0.4.0` the bundled version, not the latest. A public latest-release lookup is a separate, explicitly authorized trusted-channel operation; this Skill does not perform it automatically.
- Before upgrading, resolve this Skill's directory and run `python3 scripts/vibe_from_plugin.py plan upgrade <target>`. Show the current/target versions, updates, preserved local files, stale paths, and conflicts.
- Run `python3 scripts/vibe_from_plugin.py upgrade <target>` only after the user requested that scoped upgrade and the plan has no conflicts. Then run the installed `<target>/bin/vibe doctor <target>` and the repository's configured verification when relevant.
- To validate a transferred release candidate, run `python3 scripts/vibe_from_plugin.py validate-release <release-directory>` before using any contained payload.

Upgrade never replaces `.vibe/project.yaml`, `.vibe/project-rules.md`, or `docs/`; the Plugin must not regenerate project facts. Do not auto-update, fetch from the network, erase local modifications, resolve a three-way conflict silently, or edit version files to bypass diagnostics. If the bundled payload is older than the project, stop and obtain an explicitly selected trusted release.
