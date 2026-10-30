# Focused evidence through the actual entry

When a shared helper or adapter changes, a direct unit test cannot prove that the
configured default entry reaches it. Record a finite slice, with actual loaded
origin and arguments, before canonical QA. Keep intentionally historical tests.

| Configured check | Actual default entry | Live caller/helper | Observed origin/arguments | Focused execution | Historical caller |
|---|---|---|---|---|---|
| Python unittest discovery | `python3 -m unittest discover -s tests -v` | `test_live.py` → `adapter.py` → `new_helper.py` | helper module/file and actual argument tuple | same discovery with `-p test_live.py` | unchanged `test_historical.py` → old helper |
| Node package script | `node --run test` (`package.json` test script) | `observer.cjs` → `adapter.cjs` → `new.cjs` | `require.resolve`/module origin and `process.argv` | `node --run test -- --focused` | unchanged legacy assertion |

A useful negative fixture makes the new helper's direct test pass while the live
adapter still imports the old helper. The real focused entry must fail on that
origin; a second negative must detect wrong arguments. Change only the reviewed
live wiring, then rerun those focused entries and the unchanged historical test.
Record the commands, observations and expected negative/positive results separately
from static caller inspection.

Use an existing project runtime and script dispatcher. The repository tests accept
`CODEX_TASK_WORKSPACE_NODE`, otherwise discover `node` on PATH; they install
nothing and embed no host-specific runtime path in the core. A missing runtime or
dispatcher is unavailable evidence, not a passing Node scenario. This aid is
applicable only to affected shared entries; S work has no mandatory table. It
never asks RD to pre-run QA's complete default matrix.

Runnable [extension-testing templates](extension-testing/README.md) exercise strict receipt shape, set-layer rejection, semantic/integrity separation and real doctor lifecycles through Python discovery and Node package scripts.
