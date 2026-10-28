<p align="center">
  <img src="docs/assets/vibe-kit-logo.png" width="136" alt="Vibe Kit logo, a modular mint M ending in a verified check node">
</p>

<h1 align="center">Vibe Kit</h1>

<p align="center">Give your coding Agent a way of working that stays with the project.</p>

<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center">Latest published · <a href="https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0"><code>v0.11.0 Pre-release</code></a></p>

This checkout also contains an **unpublished 0.12.0 source candidate**, including exact onboarding-version validation, bounded read-only `inspect-run` and focused entry evidence. See the [local candidate notes](docs/releases/0.12.0.md); the published installation links below remain v0.11.0.

## Turn a goal into work you can follow

Tell your Agent what you want to build or fix. Vibe Kit supplies project instructions, reusable workflows, and local verification tools so the work has a place to start, a way to be checked, and a record of what remains.

The instructions and project context live in your repository. A new task or collaborator can pick up the same pinned version instead of relying only on the previous conversation.

## What can you do with it?

These are example requests and the workflow or tool support Vibe Kit provides.

| When you want to… | Try asking… | What the Kit supports |
|---|---|---|
| Work on an existing project | “Understand this project, then add email sign-in.” | Repository-backed context, a bounded scope, and review before significant technical choices. |
| Fix a problem | “Find why the home page is slow on first load and fix the confirmed cause.” | An investigation workflow that connects a proposed fix to observations and verification. |
| Understand a long check | “Which check is running, and when did it start?” | Available local progress metadata, including silent checks; optional complete logs to inspect afterward. |
| Upgrade the workflow | “Upgrade this project's Vibe Kit and preserve my project files.” | A plan before writes, conflict protection, recovery paths, and a separate check of installed health. |

Delivery guidance asks the Agent to explain what was completed, what was checked, and what still needs an action or permission. It does not turn an unfinished step into a completed result.

## Get started

The current version is **[v0.11.0 Pre-release](https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0)**. Open your project in Codex and send this, replacing the final goal:

> Adopt Vibe Kit from https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0 into this project. Preserve my existing files and documentation, verify the installation and establish project context, then continue with this goal: [what I want to build or fix].

Starting a new app? Include the app idea, preferred stack, and target folder. For example: “Create an expense-tracking app in `./my-app`, then adopt the exact Vibe Kit version above.”

Already using Vibe Kit? Ask: “Upgrade this project to the exact Release above, show the plan, preserve project-owned files, and check the result.” The target version's trusted payload performs the upgrade. The old CLI does not fetch new versions.

When the supported activation path asks for it, **open a new task in the same project**. Installation health and active rules are separate facts; automatic reload or handoff is conditional on host evidence.

For manual acquisition: [direct Kit ZIP](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/vibe-kit-0.11.0.zip) · [Codex bootstrap Plugin ZIP](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/vibe-kit-plugin-0.11.0.zip). The Agent checks published hashes before using downloaded bytes. See the [installation and maintenance guide](docs/maintainers-guide.md) for all assets and technical steps.

## Recent improvements in 0.11.0

- **Inspect more of a check.** Opt into complete sanitized success logs with `all-configured`; use available durable progress to find the current check even when it produces no output.
- **Upgrade to the same version again.** You can repeat the upgrade while keeping the existing conflict protection and recovery paths.
- **Keep unfinished stages visible.** Applicable workflow guidance can record stage coverage, the next action, its owner, and what it is waiting for. A stage marked Unverified remains unfinished.

Progress is diagnostic and can be stale or unavailable. Complete success logs are opt-in and must stay private. The staged-outcome guidance has static contract/scenario evidence; it is not a measurement of live-model compliance or efficiency.

[All 0.11.0 changes](docs/releases/0.11.0.md) · [Published verification evidence](docs/work-items/20261010-feedback-closure/postpublication.md)

## Is it a fit for your project?

- **For repository-based development.** You can adopt it in an existing project or after generating a new app. The CLI needs Python 3.9+ and uses only the standard library; local installation and maintenance can run offline.
- **For supported Agent hosts.** Codex and Hermes have adapter records marked verified. Actual tool access, permissions, and activation still depend on the host. Other hosts need their own adapter and evidence.
- **For checks you configure.** The Kit reports observed outcomes and missing or blocked steps; it does not supply every project's tests or guarantee that an Agent always follows the instructions.
- **For explicit control over sharing.** There is no telemetry or silent public feedback submission. Logs remain private; known-pattern sanitization cannot detect every secret.

This is a Pre-release, with no stable Release or publisher signing. Read the [capabilities and limits](docs/maintainers-guide.md), [verification and log settings](docs/verification-observability.md), or [Agent installation contract](AGENT_INSTALL.md). Earlier release: [v0.10.1](https://github.com/mintgao/vibe-kit/releases/tag/v0.10.1).

## Maintainer checks

The CLI `validate-readiness` validates bounded work-item readiness evidence read-only. `inspect-managed-agents` uses the `unicode-whitespace-v1` word policy when requested; a 2858-word file fails a 2800-word ceiling. These checks preserve project policy. Documentation string tests cannot replace this kind of behavioral evidence; live Agent scenarios remain separate verification. See the [maintainers guide](https://github.com/mintgao/vibe-kit/blob/v0.12.0/docs/maintainers-guide.md) for commands and the earlier v0.10.1 contract history.
