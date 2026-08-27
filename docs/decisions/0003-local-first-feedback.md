# 0003: Keep Vibe Kit feedback local-first and consent-bound

- Status: Accepted
- Date: 2026-08-27

## Decision

Vibe Kit feedback uses three boundaries:

1. Agent workflows may proactively identify a high-confidence, reusable Vibe Kit gap after the primary task is complete.
2. The CLI stores only sanitized structured candidates under `.vibe/local/feedback/`. A nested `.gitignore` excludes this local state by default; upgrades do not manage or overwrite it.
3. Any GitHub operation is explicit. Remote duplicate checking requires an explicit command. Issue creation requires a review hash over the exact repository, title, body and labels that the user just reviewed.

Candidates separate observation, expected behavior, impact, hypothesis and confidence. Fingerprints exclude project identity, timestamps and Vibe version, so repeated instances of the same generalized framework gap update one local candidate. Dismissed candidates stay suppressed unless severity or evidence materially changes.

Ordinary public feedback excludes raw code, logs, prompts, conversations, environment values and business identifiers. Obvious secret or security-sensitive patterns block the public submission flow rather than offering a force bypass.

## Rationale

- Real project work provides the best evidence for framework improvement, but silent collection would break user trust.
- Exact-payload confirmation prevents a stale approval from authorizing changed content or a different repository.
- Local-first behavior keeps offline and restricted projects useful and prevents GitHub availability from blocking product delivery.
- Stable fingerprints reduce repeated drafts and retry-created duplicate Issues.

## Consequences

- Installing Vibe Kit or authenticating `gh` never authorizes a report submission.
- Users must explicitly choose a central repository before real reporting can begin.
- Local redaction remains a safety aid, not a guarantee; users see the complete outbound payload before approval.
- Feedback failures never change `doctor`, `verify`, or the primary work item's result.
- Cross-project aggregation, automatic telemetry and security disclosure need separate designs.

## Recovery

- A draft can be dismissed or removed locally without affecting Vibe Kit installation state.
- Failed or uncertain submission remains locally recoverable. A retry searches by fingerprint before attempting create.
- Changing repository, title, body or labels invalidates the previous review hash.
