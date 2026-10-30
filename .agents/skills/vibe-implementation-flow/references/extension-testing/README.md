# Extension contract test templates

Copy the Python or Node fixture with `bridge.py` and `receipt.json`. No package
installation is needed. The demonstration bridge calls Vibe's current production
`validate_complete_verify_receipt`; set `VIBE_TEMPLATE_CLI` to an explicitly
reviewed CLI when copying elsewhere. For another project, replace the bridge
with that project's original production validator and connect its real entry.
The bridge is test-only, not a public CLI or a substitute validator.

From `python/`: `python3 -B -m unittest discover -s tests -v`. Focused uses
the same discovery with `-p test_contract.py`. From `node/`: `node --run test`;
focused uses `node --run test -- --focused`. Provide the existing Node runtime
on the child process PATH; missing runtime is Blocked, never stubbed.
Before either real default/focused dispatcher starts, run the finite test setup
`python3 -B ../setup_doctor.py --state generated --target <owned-fixture>/target
--output <owned-fixture>/observed/doctor.json` from the Python or Node directory.
Use a fresh project-local owned fixture. Set `VIBE_EXTENSION_DOCTOR_OUTPUT` to
that exact output path and `EXTENSION_DOCTOR=generated` for the child dispatcher.
For absent use `--state absent` and `EXTENSION_DOCTOR=absent`; leave the same
designated leaf absent. Default absent can run without setup. Setup writes only
the requested fresh fixture output, never overwrites a file, and runs real doctor
without a complete verification pre-run. A broken doctor report is generated
output, not installation health. Loader probes stat/hash the actual path before
helper imports; a generated env label with a missing file must fail.
`EXTENSION_ORIGIN=old` and `EXTENSION_ARGUMENT=WRONG` intentionally make the
actual entry fail. Clear them to demonstrate the reviewed live wiring, while
retaining historical callers and assertions. Direct bridge success does not
prove dispatcher wiring. Record loaded origin, arguments and lifecycle state.

Receipt examples are complete default, valid reordered default and valid partial;
partial remains insufficient for default admission. The set-layer counterexample
deletes an unconfigured check and synchronizes summary; `$.checks` must reject
independently of summary. Missing/extra/type/coverage/flag/provenance/enum
mutations exercise the original validator. JavaScript JSON cannot represent a
distinct integral float: the Python template carries the `2.0` precision case.

Semantic variants freeze source/input and rebuild only their permitted output
index for absent/unindexed, malformed JSON, Fail and fake Pass. The valid
byte/hash/index consumer remains invariant; the deliberately bad semantic
consumer is detected. Reading/decoding is allowed. Separate integrity mutations
retain rejection for missing members, changed bytes, mode/executable bits and
undeclared files. Do not use semantic independence to bypass integrity guards.
These setup/dispatcher executions are outside compatibility/view/readback read
intervals. Static fixtures do not prove live host compliance or efficiency.
