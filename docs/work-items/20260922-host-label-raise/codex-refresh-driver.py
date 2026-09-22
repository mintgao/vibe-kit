"""Codex-side refresh driver: existing-install admission of this repository (schema-4 five-stage record).

Host-neutral successor of the Hermes conformance driver: the admitting task's id
and the preparing task's id are supplied as arguments instead of being resolved
from a host-specific store. Run by the NEW Codex task over the manual-new-task
path (ADR 0018), from the repository root, after the preparing task has authored
`handoff-context.json` and `manual-transfer.json` in the conformance directory
(see codex-refresh-runbook.md).

It generates the receipt artifacts with --receipt, authors the host-side
artifacts, builds the schema-2 takeover object (receipt kind
existing-install-admission), validates it together with the minimal
manual-transfer payload using the installed bin/vibe validate-takeover, and
prints a SUMMARY block. It writes only under the conformance directory and a
disposable directory in the system temporary directory.
"""

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[3]
CLI = ROOT / "bin" / "vibe"
ORDER = [
    "source-resolved", "planned", "applied", "upgraded", "activated",
    "adapted", "verified", "re-evaluated", "ready",
]


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_cli(arguments, stdin_text=None):
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(ROOT), input=stdin_text, text=True, capture_output=True, check=False,
    )


def load_vibe_module():
    loader = importlib.machinery.SourceFileLoader("vk_codex_ctx", str(CLI))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_artifact(directory, name, value):
    path = directory / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True, help="this admitting task's id")
    parser.add_argument("--source-task-id", required=True, help="the preparing task's id")
    parser.add_argument("--conf-dir", default=".vibe/local/codex-conformance")
    parser.add_argument("--predecessor-zip", required=True,
                        help="path to a v0.9.0 payload zip (public release asset)")
    parser.add_argument("--takeover-id", default=None)
    arguments = parser.parse_args()

    conf = (ROOT / arguments.conf_dir).resolve() if not Path(arguments.conf_dir).is_absolute() \
        else Path(arguments.conf_dir)
    conf.mkdir(parents=True, exist_ok=True)
    conf_rel = str(conf.relative_to(ROOT))
    task_id = arguments.task_id
    source_task = arguments.source_task_id
    takeover_id = arguments.takeover_id or f"vk-codex-admission-{task_id}"
    predecessor_zip = Path(arguments.predecessor_zip)

    print("== CODEX REFRESH DRIVER ==")
    print("project_root:", str(ROOT))
    print("admitting task:", task_id, "| preparing task:", source_task)

    handoff_path = conf / "handoff-context.json"
    transfer_path = conf / "manual-transfer.json"
    for required in (handoff_path, transfer_path, predecessor_zip):
        if not Path(required).exists():
            print(f"FATAL: required input missing: {required}")
            return 1
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    transfer = json.loads(transfer_path.read_text(encoding="utf-8"))
    if handoff.get("source_task_id") != source_task:
        print("FATAL: handoff-context.json source_task_id does not match --source-task-id")
        return 1
    if transfer.get("transfer_id") != handoff.get("transfer_id"):
        print("FATAL: manual-transfer.json transfer_id does not match handoff-context.json")
        return 1
    transfer_id = handoff["transfer_id"]

    steps = {}

    plan = run_cli([
        "plan", "upgrade", ".", "--source-type", "local-payload", "--source-ref", "0.10.0",
        "--format", "json", "--receipt", f"{conf_rel}/plan-receipt.json",
    ])
    steps["plan"] = plan.returncode
    print("plan rc:", plan.returncode)
    if plan.returncode != 0:
        print(plan.stdout[-2000:])
        print(plan.stderr[-2000:])
        return 1

    doctor = run_cli([
        "doctor", ".", "--format", "json", "--receipt", f"{conf_rel}/doctor-receipt.json",
    ])
    steps["doctor"] = doctor.returncode
    print("doctor rc:", doctor.returncode)
    if doctor.returncode != 0:
        print(doctor.stdout[-2000:])
        print(doctor.stderr[-2000:])
        return 1
    doctor_envelope = json.loads(doctor.stdout)

    verify = run_cli([
        "verify", ".", "--format", "json", "--receipt", f"{conf_rel}/verify-receipt.json",
    ])
    steps["verify"] = verify.returncode
    print("verify rc:", verify.returncode)
    if verify.returncode != 0:
        print(verify.stdout[-3000:])
        print(verify.stderr[-3000:])
        return 1
    verify_envelope = json.loads(verify.stdout)

    scratch = Path(tempfile.mkdtemp(prefix="vk-codex-refresh-"))
    regeneration = scratch / "regeneration"
    regeneration_result = run_cli([
        "init", str(regeneration), "--host", "codex,hermes", "--source-type", "local-payload",
        "--source-ref", "0.10.0", "--format", "json",
    ])
    steps["regeneration-init"] = regeneration_result.returncode
    print("regeneration init rc:", regeneration_result.returncode)
    if regeneration_result.returncode != 0:
        print(regeneration_result.stdout[-2000:])
        print(regeneration_result.stderr[-2000:])
        return 1
    manifest_equal = (
        (regeneration / ".vibe/manifest.json").read_bytes()
        == (ROOT / ".vibe/manifest.json").read_bytes()
    )
    print("regenerated manifest equals installed manifest (bytes):", manifest_equal)

    predecessor_payload = scratch / "predecessor-payload"
    predecessor_target = scratch / "predecessor-target"
    predecessor_payload.mkdir(parents=True)
    with zipfile.ZipFile(predecessor_zip) as archive:
        archive.extractall(predecessor_payload)
    pred_cli = predecessor_payload / "vibe-kit-0.9.0" / "bin" / "vibe"
    predecessor = subprocess.run(
        [sys.executable, str(pred_cli), "init", str(predecessor_target), "--format", "json"],
        text=True, capture_output=True, check=False,
    )
    steps["predecessor-init"] = predecessor.returncode
    print("predecessor (v0.9.0) init rc:", predecessor.returncode)
    if predecessor.returncode != 0:
        print(predecessor.stdout[-2000:])
        print(predecessor.stderr[-2000:])
        return 1
    upgrade = run_cli([
        "upgrade", str(predecessor_target), "--source-type", "local-payload",
        "--source-ref", "0.10.0", "--format", "json",
        "--receipt", f"{conf_rel}/historical-upgrade-receipt.json",
    ])
    steps["historical-upgrade"] = upgrade.returncode
    print("historical 0.9.0->0.10.0 upgrade rc:", upgrade.returncode)
    if upgrade.returncode != 0:
        print(upgrade.stdout[-2000:])
        print(upgrade.stderr[-2000:])
        return 1
    upgrade_envelope = json.loads(upgrade.stdout)

    module = load_vibe_module()
    context, context_errors = module.installed_takeover_contract_context(ROOT)
    if context_errors or context is None:
        print("FATAL: installed contract did not authenticate:", context_errors)
        return 1
    context_root = str(context["project_root"])
    manifest_sha = context["manifest_sha256"]
    activation_set_sha = context["activation_set_sha256"]
    print("context project_root:", context_root, "| equals repository root:", context_root == str(ROOT))
    print("context manifest_sha256:", manifest_sha)
    print("context activation_set_sha256:", activation_set_sha)

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest = json.loads((ROOT / ".vibe/manifest.json").read_text(encoding="utf-8"))
    source = manifest["source"]
    task_start_ref = f"{conf_rel}/task-start-record.json"

    write_artifact(conf, "source-attestation.json", {
        "artifact": "source-attestation",
        "task_id": task_id,
        "observed_at": now,
        "project_root": str(ROOT),
        "installed_manifest": ".vibe/manifest.json",
        "source": source,
        "note": "The installed manifest records this source; its payload tree digest is the "
                "installation-source identity presented in the takeover object.",
    })
    write_artifact(conf, "task-start-record.json", {
        "artifact": "task-start-record",
        "task_id": task_id,
        "started_at": now,
        "cwd": str(ROOT),
        "path": "manual-new-task",
        "receipt_kind": "existing-install-admission",
        "note": "A new Codex task started in this project and admitted the existing "
                "installation; it claims no upgrade transaction and writes no project files.",
        "receipt_artifacts": [
            f"{conf_rel}/plan-receipt.json",
            f"{conf_rel}/doctor-receipt.json",
            f"{conf_rel}/verify-receipt.json",
            f"{conf_rel}/historical-upgrade-receipt.json",
        ],
    })
    write_artifact(conf, "adaptation-review.json", {
        "artifact": "adaptation-review",
        "task_id": task_id,
        "outcome": "unchanged-complete",
        "reviewed": [".vibe/onboarding.json", ".vibe/manifest.json", "agent-install.json"],
        "note": "The installation is complete for its recorded selection ([codex, hermes]); "
                "the project-owned onboarding state is complete and preserved, and no "
                "adaptation change is required.",
    })
    write_artifact(conf, "routing-record.json", {
        "artifact": "routing-record",
        "task_id": task_id,
        "routing": "routable",
        "target_rules": "satisfied",
        "evidence": {
            "doctor_receipt": f"{conf_rel}/doctor-receipt.json",
            "verify_receipt": f"{conf_rel}/verify-receipt.json",
        },
        "note": "Target re-evaluation after the takeover: the installed contract "
                "authenticates, the default verification channel passed, and the target "
                "stays routable.",
    })

    def evidence(kind, ref, sha, task, sequence):
        return {"kind": kind, "ref": ref, "sha256": sha, "task_id": task, "sequence": sequence}

    def digest(relative):
        return sha256_file(ROOT / relative)

    stages = {
        "source-resolved": {
            "state": "satisfied", "outcome": None, "reason_code": None,
            "evidence": [evidence(
                "source-attestation", f"{conf_rel}/source-attestation.json",
                source["payload_tree_sha256"], source_task, 1,
            )],
        },
        "planned": {
            "state": "satisfied", "outcome": None, "reason_code": None,
            "evidence": [evidence(
                "plan-receipt", f"{conf_rel}/plan-receipt.json",
                digest(f"{conf_rel}/plan-receipt.json"), source_task, 2,
            )],
        },
        "applied": {
            "state": "satisfied", "outcome": None, "reason_code": None,
            "evidence": [evidence(
                "apply-receipt", f"{conf_rel}/historical-upgrade-receipt.json",
                digest(f"{conf_rel}/historical-upgrade-receipt.json"), source_task, 3,
            )],
        },
        "upgraded": {
            "state": "satisfied", "outcome": None, "reason_code": None,
            "evidence": [evidence(
                "doctor-receipt", f"{conf_rel}/doctor-receipt.json",
                digest(f"{conf_rel}/doctor-receipt.json"), source_task, 4,
            )],
        },
        "activated": {
            "state": "satisfied", "outcome": None, "reason_code": None,
            "evidence": [evidence(
                "manual-task-start", task_start_ref, activation_set_sha, task_id, 7,
            )],
        },
        "adapted": {
            "state": "satisfied", "outcome": "unchanged-complete", "reason_code": None,
            "evidence": [
                evidence(
                    "onboarding-state", ".vibe/onboarding.json",
                    digest(".vibe/onboarding.json"), task_id, 9,
                ),
                evidence(
                    "adaptation-review", f"{conf_rel}/adaptation-review.json",
                    digest(f"{conf_rel}/adaptation-review.json"), task_id, 10,
                ),
            ],
        },
        "verified": {
            "state": "satisfied", "outcome": None, "reason_code": None,
            "evidence": [
                evidence(
                    "doctor-receipt", f"{conf_rel}/doctor-receipt.json",
                    digest(f"{conf_rel}/doctor-receipt.json"), task_id, 11,
                ),
                evidence(
                    "verify-receipt", f"{conf_rel}/verify-receipt.json",
                    digest(f"{conf_rel}/verify-receipt.json"), task_id, 12,
                ),
            ],
        },
        "re-evaluated": {
            "state": "satisfied", "outcome": "routable", "reason_code": None,
            "evidence": [evidence(
                "routing-record", f"{conf_rel}/routing-record.json",
                digest(f"{conf_rel}/routing-record.json"), task_id, 13,
            )],
        },
        "ready": {"state": "satisfied", "outcome": None, "reason_code": None, "evidence": []},
    }

    fingerprint = doctor_envelope["target_fingerprint"]
    target_fingerprint = {
        "kit_version": fingerprint["kit_version"],
        "core_protocol": fingerprint["core_protocol"],
        "agent_install_schema": fingerprint["agent_install_schema"],
        "agent_install_protocol": fingerprint["agent_install_protocol"],
        "adapter_name": fingerprint["adapter_name"],
        "adapter_protocol": fingerprint["adapter_protocol"],
        "manifest_sha256": fingerprint.get("manifest_sha256"),
        "activation_set_sha256": fingerprint.get("activation_set_sha256"),
    }

    takeover = {
        "takeover_schema_version": 2,
        "takeover_id": takeover_id,
        "evidence_origin": "runtime",
        "completion_owner_task_id": task_id,
        "project_root": context_root,
        "source": {
            "type": source["type"],
            "ref": source["ref"],
            "artifact_sha256": source["artifact_sha256"],
            "payload_tree_sha256": source["payload_tree_sha256"],
        },
        "versions": {"from": handoff["versions"]["from"], "target": fingerprint["kit_version"]},
        "target_fingerprint": target_fingerprint,
        "overall_status": "ready",
        "last_completed_stage": "ready",
        "write_state": "none",
        "upgrade_transaction": {
            "schema_version": 1,
            "transaction_id": None,
            "outcome": "not-started",
            "commit_marker": "not-applicable",
            "installation_state": "target",
            "active_state_present": False,
        },
        "activation": {
            "path": "manual-new-task",
            "receipt_kind": "existing-install-admission",
            "receipt_id": task_start_ref,
            "source_task_id": source_task,
            "active_task_id": task_id,
            "handoff_idempotency_key": None,
            "observed_manifest_sha256": manifest_sha,
            "observed_activation_set_sha256": activation_set_sha,
        },
        "goal": {
            "kind": "unfinished",
            "custody": "manual-successor-owned",
            "continuation": "ready-to-resume",
            "transfer_id": transfer_id,
            "owner_task_id": task_id,
            "custody_history": [
                {"state": "source-owned", "task_id": source_task, "sequence": 0},
                {"state": "manual-transfer-required", "task_id": None, "sequence": 5},
                {"state": "manual-transfer-pending", "task_id": task_id, "sequence": 6},
                {"state": "manual-successor-owned", "task_id": task_id, "sequence": 8},
            ],
        },
        "stages": {name: stages[name] for name in ORDER},
        "next_action": None,
    }
    (conf / "takeover-object.json").write_text(
        json.dumps(takeover, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    validation = run_cli(
        [
            "validate-takeover", "--format", "json",
            "--manual-transfer", f"{conf_rel}/manual-transfer.json",
            "--receipt", f"{conf_rel}/validation-receipt.json",
        ],
        stdin_text=json.dumps(takeover),
    )
    steps["validate-takeover"] = validation.returncode
    print("validate-takeover rc:", validation.returncode)
    try:
        validation_envelope = json.loads(validation.stdout)
    except (ValueError, TypeError):
        validation_envelope = None
        print(validation.stdout[-2000:])
        print(validation.stderr[-2000:])
    status = (validation_envelope or {}).get("status")
    print("validation status:", status)
    if validation_envelope:
        print("validation errors:", json.dumps(validation_envelope.get("errors"), ensure_ascii=False))
        print("manual transfer status:", validation_envelope.get("manual_transfer_status"))

    artifacts = {}
    for path in sorted(conf.glob("*.json")):
        artifacts[path.name] = sha256_file(path)

    summary = {
        "task_id": task_id,
        "source_task_id": source_task,
        "transfer_id": transfer_id,
        "steps": steps,
        "envelope_statuses": {
            "plan": (json.loads(plan.stdout) or {}).get("status") if plan.stdout else None,
            "doctor": doctor_envelope.get("status"),
            "verify": verify_envelope.get("status"),
            "historical-upgrade": {
                "status": upgrade_envelope.get("status"),
                "from_version": upgrade_envelope.get("from_version"),
                "target_version": upgrade_envelope.get("target_version"),
                "transaction_outcome": (upgrade_envelope.get("transaction") or {}).get("outcome"),
            },
        },
        "regenerated_manifest_equal_bytes": manifest_equal,
        "context_root_matches": context_root == str(ROOT),
        "validation": {
            "rc": validation.returncode,
            "status": status,
            "errors": (validation_envelope or {}).get("errors"),
            "manual_transfer_status": (validation_envelope or {}).get("manual_transfer_status"),
        },
        "artifacts": artifacts,
    }
    (conf / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("== SUMMARY ==")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if status == "valid" else 1


if __name__ == "__main__":
    sys.exit(main())