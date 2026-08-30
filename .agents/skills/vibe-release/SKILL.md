---
name: vibe-release
description: Plan, authorize, publish, verify, and close the exact Vibe Kit v0.7.0 GitHub Pre-release through an offline-intent and host-owned remote workflow.
---

# Vibe Kit release

Use this Skill only for the Vibe Kit repository release lifecycle. The CLI stays
offline; GitHub authentication, network reads and writes belong to the Agent/host.

1. Confirm the accepted version, release kind and scope. For v0.7.0 the exact
   scope is repository `mintgao/vibe-kit`, annotated tag `v0.7.0`, one non-draft
   Pre-release, the exact five assets, public verification, then issues #1–#5.
2. Require an accepted clean commit, independent QA, all configured checks,
   Python 3.9 evidence, two byte-identical prerelease builds and successful
   `validate-release`. Freeze the release-note bytes and annotated-tag identity.
3. Read remote `main`, tag, Release and the complete asset list. Build the closed
   request and run `bin/vibe publication-plan --phase publish --request <json>
   --candidate <release-dir> --format json`. This command performs no network or
   writes. Present the exact intent digest and bind authorization to repository,
   version, operation set, intent digest and one host operation ID.
4. Under that authorization only, fast-forward `main` with the expected-old OID
   lease; create or confirm the exact annotated tag and Pre-release; then upload
   or confirm exactly `SHA256SUMS`, `release-manifest.json`, the direct ZIP,
   distribution ZIP and Plugin ZIP. Extra, duplicate or divergent state blocks.
   Never force, delete, replace or rewrite.
5. After every write, read back exact identity. A timeout or transport-unknown
   response is followed by read-back before retry. Retry only a positively absent
   natural-key object, at most once. Download and hash all five public assets.
6. Produce the closed sanitized receipt and run `bin/vibe validate-publication
   --intent <json> --receipt <json> --candidate <release-dir> --format json`.
   Structural validity does not authenticate GitHub; retain live public evidence.
7. Only after confirmed-complete publication and passed public verification,
   build the #1–#5 request and run `publication-plan --phase issue-closeout`.
   The request carries the exact five-item remote snapshot, ten ordered
   comment/close operations with their canonical snapshot preconditions, and the
   declarative non-destructive scope. Bind a separate executable closeout
   authorization to the exact intent digest, repository, issue set and two-operation
   allowlist before any write.
8. Before every closeout operation, reread issue state and all exact-marker
   comments. Reuse `open-exact`/`closed-exact`; never close before the exact comment
   is read back. After a definite or uncertain response, read back before retry.
   Retry only a positively absent natural key after attempt one, at most once, and
   read back again after attempt two. Conflict, permission denial or still-unknown
   state gets no retry and stops the current and all later operations. Resume the
   same intent from the first non-terminal operation without duplicating comments
   or closes.

Persist only allowlisted public facts and hashes in work-item evidence. Never put
tokens, headers, environment values, raw host output, hidden reasoning, goal text
or conversation content in an intent, receipt, release asset or issue comment.
Do not announce the release or close issues until public verification has passed.
