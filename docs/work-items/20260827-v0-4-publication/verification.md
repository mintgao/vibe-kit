# Verification: Publish Vibe Kit v0.4.0 GitHub prerelease

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | README, changelog, release notes and product/architecture context consistently identify 0.4.0 as a GitHub Pre-release and exclude stable, Plugin Directory and package-manager publication. | Pass |
| AC-2 | Workspace Python and macOS Python 3.9.6 each pass 21/21 tests; `vibe verify`, `doctor`, bytecode compilation and official Skill/Plugin validators pass. Independent QA reran `doctor`, bytecode compilation and diff checks. | Pass |
| AC-3–AC-8 | Require the clean release commit, rebuilt prerelease artifacts and GitHub publication/read-back. | Pending |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `python3 -m unittest discover -s tests -v` | Pass | 21/21 on workspace Python. |
| `/usr/bin/python3 -m unittest discover -s tests -v` | Pass | 21/21 on Python 3.9.6. |
| `python3 bin/vibe verify .` | Pass | Configured test gate passed, 21/21. |
| `python3 bin/vibe doctor .` | Pass | Version integrity 0.4.0; zero warnings. |
| `python3 -m py_compile bin/vibe tests/test_cli.py` | Pass | Release source compiles. |
| Official Skill/Plugin validators | Pass | Managed feedback Skill and source Plugin accepted using the system Python runtime. |
| Independent QA prep gate | Pass to commit | Dirty-tree prerelease packaging correctly fails; current unpublished artifact must not be uploaded. |

## Manual scenarios

- Independent QA confirmed that the existing ignored `dist/vibe-kit-0.4.0` belongs to the dirty-tree unpublished candidate and must be moved aside before the clean prerelease build.
- Remote publication, digest read-back and isolated download verification remain pending.

## Limitations and follow-ups

- Linux CI, signatures/provenance and stable promotion are out of scope.
