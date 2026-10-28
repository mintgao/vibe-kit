# Verification: {{TITLE}}

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Not run | Pending |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| Project verification | Not run | |

## Manual scenarios

- None recorded.

## Limitations and follow-ups

- None recorded.

## Affected-entry evidence (when applicable)

For shared helper/adapter changes, record only the applicable bounded slice:
configured command → actual default entry → affected live caller/helper → observed
origin and arguments → focused command/result → preserved historical callers.
Explain sufficiency; static search alone and direct helper tests do not prove live
wiring. Mark inapplicable when no shared entry changes. No mandatory S table or
additional full verification run is introduced.
