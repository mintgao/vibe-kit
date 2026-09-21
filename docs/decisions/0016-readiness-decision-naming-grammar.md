# 0016: Readiness accepts both NNNN-slug and YYYYMMDD-slug decision records, and reads a record's heading and status from its own grammar

- Status: Accepted
- Date: 2026-09-21
- Decision owner: read-only Tech Lead author `vibe_tech_lead`
- Work item: `docs/work-items/20260921-readiness-naming-grammar/brief.md`
- Evidence: feedback issues #11 and #13 (finding F4), the DSH Desktop Mint migration of 2026-09-18, and the validator at bin/vibe lines 12463 and 12471

## Context and applicable decisions

The readiness gate reads decision records under a grammar narrower than the repositories it has to judge. At `bin/vibe` line 12463 the validator raises `readiness.adr-reference` for the Governing decision field; the reference pattern accepts only `docs/decisions/NNNN-slug.md`. At line 12471 the heading rule requires exactly one H1 that starts with `"# " + Path(relative).name[:4] + ": "`, so a file name's first four characters decide the heading prefix. The preamble check requires a dash-prefixed `- Status: Accepted` bullet.

That grammar is the kit's own house style and nothing else. DSH Desktop Mint migrated on 2026-09-18 with decision records named `YYYYMMDD-slug.md` and a plain `Status: Accepted` line; its decision `docs/decisions/20260913-desktop-versioned-assembly.md` cannot be cited by the readiness gate. Both checks fail on that record: the four-character heading prefix is `2026`, and a plain status line is not a dash-prefixed bullet.

The failure is silent and it distorts evidence. A repository that in fact produced an Accepted decision record cannot cite it, so the record degrades to `no-new-durable-decision`. That classification understates the evidence the repository actually carries, and it pushes an agent toward inventing an ADR in a foreign naming convention — writing a new `NNNN-slug` record to satisfy the validator instead of citing the decision that exists. ADR 0008 governs readiness authority; this decision corrects the grammar that authority reads, and nothing about the authority itself changes.

## Decision: accept both naming conventions

A citation is valid when it resolves to `docs/decisions/NNNN-slug.md` or `docs/decisions/YYYYMMDD-slug.md`. Both conventions are first-class: four-digit sequence numbers and eight-digit date stamps are equally acceptable identities for an Accepted record, and neither is preferred, aliased, or rewritten. A citation under either convention is the same evidence of a durable decision.

## Decision: read a record's heading and status from its own leading identifier

The heading rule keys on the file name's leading identifier — four or eight digits — followed by `: `, instead of on the first four characters of the name. `# 0001: ...` and `# 20260913: ...` are both correct headings for their files; a five- or six-digit prefix is not an identifier under this grammar and fails closed.

The preamble status check accepts `- Status: Accepted` and `Status: Accepted`, provided exactly one such line appears in the preamble before the first second-level heading. Bullet-prefixed and plain forms are equivalent; the record's status is read the same way under either.

The grammar widens; the gate does not loosen. Every fail-closed behaviour is kept: unknown identifier widths, a heading that does not match the file name's identifier, an absent status line, a status line that is not `Accepted`, more than one status line in the preamble, and a malformed or unresolvable reference each continue to fail the readiness check with an actionable message naming the file and the expected form. Widening the accepted grammar never converts a failing check into a passing one by accident.

## Consequences and boundaries

The kit's own records keep their current form. `0014` and `0015` continue to validate unchanged, and this decision introduces no migration, rename, or rewrite of any existing record in any repository — including the kit's own. Repositories already carrying `YYYYMMDD-slug` records need no change either; their records become citable as they are, and their previously degraded `no-new-durable-decision` classifications can now resolve to the durable decision they already hold.

The change is grammar and validation only: no schema, protocol, enum, receipt, custody, or CLI-result change, and no version bump. The validator's messages keep naming the file and expected form; only the set of forms it accepts widens. No repository-declared naming pattern is consulted.

## Verification

The claim of this record is checked by both directions of the widened grammar. The kit's own `docs/decisions/0014-...md` and `docs/decisions/0015-...md` must keep passing each check unchanged, proving the widening did not disturb the existing house style. A `YYYYMMDD-slug` record with a plain `Status: Accepted` line must pass citation, heading, and status checks, proving the defect that motivated this record is closed. Negative cases must keep failing: an unknown identifier width, a heading whose prefix disagrees with its file name, a missing or non-`Accepted` status line, two status lines in the preamble, and a malformed reference.

## Follow-ups out of scope

- A repository-declared naming pattern in `.vibe/project.yaml` is explicitly out of this iteration. This decision accepts two fixed conventions; it does not add a configuration surface for arbitrary ones.
- Renaming, migrating, or rewriting any existing decision record, in the kit or in a consuming repository.
- Any relaxation of the status requirement beyond `Accepted`, or of the exactly-one-heading and exactly-one-status-line rules.