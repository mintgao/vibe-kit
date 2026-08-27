# 0006: Make feedback proactively ask without silent submission

- Status: Accepted
- Date: 2026-08-27

## Decision

Vibe Kit 0.4.0 makes `feedback.mode: ask` the default Close behavior for new installations and projects where the mode is absent.

For an evidence-backed Vibe Kit gap, the Agent may automatically perform local classification, draft, sanitization, deduplication and exact review after the primary task is complete. A new or materially resurfaced candidate is then shown once with its target, privacy state, complete outbound payload and review hash. The user can authorize that exact report with one unambiguous natural-language reply; the Agent passes the bound hash to the existing CLI submission gate.

The MVP supports:

- `ask`: generate locally and proactively present one exact submission decision;
- `local`: generate locally without a proactive submission question;
- `off`: disable proactive Close generation and presentation.

No mode authorizes external writing. Repository configuration, Plugin installation, GitHub authentication, a previous approval or a previously presented hash cannot replace current exact-payload consent.

Silent `auto-submit` is not part of this protocol.

## Rationale

- A local candidate that users never see does not create a useful maintenance loop.
- Requiring users to discover report IDs, hashes and CLI commands makes valid feedback unlikely to reach maintainers.
- Proactive presentation and a one-reply primary action remove that friction without weakening the local-first, consent-bound decision in ADR 0003.
- Treating missing mode as `ask` gives new and historical projects a useful default, while treating invalid mode as an error prevents typos from silently enabling behavior.

## Consequences

- CLI owns deterministic mode parsing, candidate attention state, exact rendering and hash enforcement.
- Managed Agent instructions own evidence qualification and natural-language authorization adjacency.
- Historical candidates without attention metadata are classified as legacy and are not presented as an upgrade backlog.
- “Later” or no response consumes the current prompt opportunity; unchanged evidence does not prompt again.
- `auto-submit` requires a separate trust design bound to local user, GitHub identity, repository, project scope, policy version and expiry.

## Recovery and rollback

- Changing a project-owned mode to `local` stops proactive questions while preserving local candidates.
- Changing it to `off` stops proactive classification without deleting state or disabling explicit feedback commands.
- Rolling back to 0.3 ignores added state fields because existing fields keep their meanings.
- Failed, blocked or uncertain remote operations remain locally recoverable and never alter the primary task result.
