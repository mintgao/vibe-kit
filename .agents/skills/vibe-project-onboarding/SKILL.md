---
name: vibe-project-onboarding
description: Build or refresh durable product, architecture, design, and command context when Vibe Kit is first adopted or the repository has materially changed.
---

# Project onboarding

Create an accurate baseline without refactoring the application. This is an internal readiness workflow: users do not need to name it. Preserve the ordinary development request that triggered onboarding and resume that request after readiness is established.

1. Read `.vibe/project.yaml`, `.vibe/project-rules.md`, the README, dependency manifests, build configuration, tests, and entry points.
2. Inspect the repository broadly enough to distinguish observed facts from guesses. For a large repository, delegate bounded read-only exploration by subsystem and synthesize the results.
3. Update only the durable context that can be supported by evidence:
   - `docs/context/product.md` for users, problems, current capabilities, boundaries, and unknowns;
   - `docs/context/architecture.md` for runtime structure, dependencies, data flow, commands, and constraints;
   - `docs/context/design-system.md` when a user interface or established design language exists;
   - `.vibe/project.yaml` for verified project commands and stack facts.
4. Preserve existing documentation and call out contradictions instead of overwriting uncertain information.
5. Report gaps that require product knowledge or credentials. Do not manufacture history or retroactively create work items.
6. Only after the evidence-backed context and verified commands are updated, write `.vibe/onboarding.json` with `schema_version: 1`, `status: "complete"`, an `updated_at` date, and a concise list of evidence paths. Never mark readiness complete while material contradictions or required repository inspection remain unresolved.
7. Resume the user's original request through the appropriate Vibe workflow. Do not ask the user to repeat it or to invoke another Skill.
