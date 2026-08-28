"""Deterministic controlled host for takeover contract scenarios.

This fixture keeps synthetic goal text in memory and always asks the installed
production ``bin/vibe validate-takeover`` command to judge result objects.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
from typing import Dict, List, Optional, Tuple


STAGES = (
    "source-resolved", "planned", "applied", "upgraded", "activated",
    "adapted", "verified", "re-evaluated", "ready",
)


class FakeTakeoverHost:
    def __init__(self, project: Path, synthetic_goal: str = "GOAL_SECRET_SENTINEL") -> None:
        self.project = project.resolve()
        self.cli = self.project / "bin/vibe"
        self.synthetic_goal = synthetic_goal
        self.successors: Dict[str, str] = {}
        self.create_attempts = 0
        doctor = subprocess.run(
            [str(self.cli), "doctor", str(self.project), "--format", "json"],
            cwd=str(self.project), text=True, capture_output=True, check=False,
        )
        if doctor.returncode != 0:
            raise AssertionError(doctor.stdout or doctor.stderr)
        receipt = json.loads(doctor.stdout)
        self.context = {
            "project_root": str(self.project),
            "manifest_sha256": receipt["manifest_sha256"],
            "activation_set_sha256": receipt["activation"]["actual_activation_set_sha256"],
            "target_fingerprint": receipt["target_fingerprint"],
        }

    def create_successor(self, idempotency_key: str, ambiguous: bool = False) -> Optional[str]:
        if idempotency_key in self.successors:
            return self.successors[idempotency_key]
        self.create_attempts += 1
        if ambiguous:
            return None
        task_id = f"successor-{len(self.successors) + 1}"
        self.successors[idempotency_key] = task_id
        return task_id

    def lookup_successor(self, idempotency_key: str) -> Optional[str]:
        return self.successors.get(idempotency_key)

    @staticmethod
    def _evidence(
        kind: str,
        ref: str,
        sequence: int,
        task_id: Optional[str],
        digest: Optional[str] = None,
    ) -> Dict[str, object]:
        return {
            "kind": kind,
            "ref": ref,
            "sha256": digest,
            "task_id": task_id,
            "sequence": sequence,
        }

    def ready(
        self,
        path: str = "manual-new-task",
        goal_kind: str = "unfinished",
        adaptation: str = "unchanged-complete",
    ) -> Dict[str, object]:
        source_task = "source-task"
        active_task = source_task if path == "same-task-reload" else "successor-task"
        receipt_kind = {
            "same-task-reload": "host-reload",
            "automatic-successor-handoff": "host-successor-start",
            "manual-new-task": "manual-task-start",
        }[path]
        handoff_key = "handoff-key" if path == "automatic-successor-handoff" else None
        sequence = 0
        history: List[Dict[str, object]] = []

        def custody(state: str, task_id: Optional[str]) -> None:
            nonlocal sequence
            history.append({"state": state, "task_id": task_id, "sequence": sequence})
            sequence += 1

        if goal_kind == "unfinished":
            custody("source-owned", source_task)

        evidence: Dict[str, List[Dict[str, object]]] = {name: [] for name in STAGES}

        def record(stage: str, kind: str, ref: str, task_id: Optional[str], digest: Optional[str] = None) -> None:
            nonlocal sequence
            evidence[stage].append(self._evidence(kind, ref, sequence, task_id, digest))
            sequence += 1

        record("source-resolved", "source-attestation", "source", source_task, "2" * 64)
        record("planned", "plan-receipt", "plan", source_task)
        record("applied", "apply-receipt", "apply", source_task)
        record("upgraded", "doctor-receipt", "upgrade-doctor", source_task)
        if goal_kind == "unfinished" and path == "automatic-successor-handoff":
            custody("automatic-transfer-pending", source_task)
        if goal_kind == "unfinished" and path == "manual-new-task":
            custody("manual-transfer-required", None)
            custody("manual-transfer-pending", active_task)
        activation_kind = "manual-task-start" if path == "manual-new-task" else "activation-receipt"
        record(
            "activated", activation_kind, "activation", active_task,
            self.context["activation_set_sha256"],
        )
        if path == "automatic-successor-handoff":
            record("activated", "handoff-claim", "handoff", active_task)
        if goal_kind == "unfinished" and path == "automatic-successor-handoff":
            custody("automatic-successor-owned", active_task)
        if goal_kind == "unfinished" and path == "manual-new-task":
            custody("manual-successor-owned", active_task)
        record("adapted", "onboarding-state", ".vibe/onboarding.json", active_task)
        record("adapted", "adaptation-review", "adaptation", active_task)
        record("verified", "doctor-receipt", "final-doctor", active_task)
        record("verified", "verify-receipt", "default-verify", active_task)
        record("re-evaluated", "routing-record", "routing", active_task)

        maintenance = goal_kind == "maintenance-only"
        custody_value = "none" if maintenance else history[-1]["state"]
        owner = None if maintenance else active_task
        continuation = "not-applicable" if maintenance else "ready-to-resume"
        transfer = None if maintenance or path == "same-task-reload" else "transfer-id"
        stages = {
            name: {"state": "satisfied", "outcome": None, "reason_code": None, "evidence": evidence[name]}
            for name in STAGES
        }
        stages["adapted"]["outcome"] = adaptation
        stages["re-evaluated"]["state"] = "not-applicable" if maintenance else "satisfied"
        stages["re-evaluated"]["outcome"] = "maintenance-only" if maintenance else "routable"
        return {
            "takeover_schema_version": 1,
            "takeover_id": "takeover-id",
            "evidence_origin": "controlled-fixture",
            "completion_owner_task_id": active_task,
            "project_root": str(self.project),
            "source": {
                "type": "local-payload", "ref": "controlled-local-payload",
                "artifact_sha256": None, "payload_tree_sha256": "2" * 64,
            },
            "versions": {"from": "0.5.0", "target": "0.6.0"},
            "target_fingerprint": copy.deepcopy(self.context["target_fingerprint"]),
            "overall_status": "ready",
            "last_completed_stage": "ready",
            "write_state": "project-files-written",
            "activation": {
                "path": path, "receipt_kind": receipt_kind, "receipt_id": "activation",
                "source_task_id": source_task, "active_task_id": active_task,
                "handoff_idempotency_key": handoff_key,
                "observed_manifest_sha256": self.context["manifest_sha256"],
                "observed_activation_set_sha256": self.context["activation_set_sha256"],
            },
            "goal": {
                "kind": goal_kind, "custody": custody_value,
                "continuation": continuation, "transfer_id": transfer,
                "owner_task_id": owner, "custody_history": history,
            },
            "stages": stages,
            "next_action": None,
        }

    def degraded_manual(self, unfinished: bool = True) -> Dict[str, object]:
        value = self.ready("manual-new-task", "unfinished" if unfinished else "maintenance-only")
        source_task = value["activation"]["source_task_id"]
        value["completion_owner_task_id"] = None
        value["overall_status"] = "degraded"
        value["last_completed_stage"] = "upgraded"
        value["activation"] = {
            "path": "none", "receipt_kind": None, "receipt_id": None,
            "source_task_id": source_task, "active_task_id": None,
            "handoff_idempotency_key": None, "observed_manifest_sha256": None,
            "observed_activation_set_sha256": None,
        }
        for name in STAGES[4:]:
            value["stages"][name] = {
                "state": "not-started", "outcome": None,
                "reason_code": None, "evidence": [],
            }
        value["stages"]["activated"] = {
            "state": "blocked", "outcome": None,
            "reason_code": "manual-new-task-required", "evidence": [],
        }
        if unfinished:
            value["goal"] = {
                "kind": "unfinished", "custody": "manual-transfer-required",
                "continuation": "paused", "transfer_id": "transfer-id",
                "owner_task_id": None,
                "custody_history": [
                    {"state": "source-owned", "task_id": source_task, "sequence": 0},
                    {"state": "manual-transfer-required", "task_id": None, "sequence": 5},
                ],
            }
        else:
            value["goal"] = {
                "kind": "maintenance-only", "custody": "none",
                "continuation": "not-applicable", "transfer_id": None,
                "owner_task_id": None, "custody_history": [],
            }
        value["next_action"] = {
            "code": "create-new-project-task",
            "detail": "Create one new task in this project.",
        }
        return value

    def block(self, value: Dict[str, object], stage: str, reason: str, action: str) -> Dict[str, object]:
        blocked = copy.deepcopy(value)
        index = STAGES.index(stage)
        blocked["overall_status"] = "blocked"
        blocked["completion_owner_task_id"] = None
        blocked["stages"][stage]["state"] = "blocked"
        blocked["stages"][stage]["reason_code"] = reason
        blocked["stages"][stage]["outcome"] = (
            "blocked" if stage == "adapted" else
            "blocked-by-target-rules" if stage == "re-evaluated" else None
        )
        for later in STAGES[index + 1:]:
            blocked["stages"][later] = {
                "state": "not-started", "outcome": None,
                "reason_code": None, "evidence": [],
            }
        blocked["last_completed_stage"] = STAGES[index - 1] if index else None
        blocked["next_action"] = {"code": action, "detail": "Resolve the controlled blocker."}
        if stage == "re-evaluated" and blocked["goal"]["kind"] == "unfinished":
            blocked["goal"]["continuation"] = "blocked"
        return blocked

    def validate(self, value: Dict[str, object]) -> Tuple[int, Dict[str, object], str]:
        result = subprocess.run(
            [str(self.cli), "validate-takeover", "--format", "json"],
            cwd=str(self.project), input=json.dumps(value), text=True,
            capture_output=True, check=False,
        )
        return result.returncode, json.loads(result.stdout), result.stderr
