"""Controlled operation/CLI evidence; never actual host activation."""
import errno
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from tests.test_cli import ROOT, CLI, load_cli_module
from tests.test_next_iteration import snapshot_tree


class UpgradeMaintenanceTests(unittest.TestCase):
    def test_managed_projection_and_repair_scope_contract(self):
        text=(ROOT/'.vibe/core/upgrade-maintenance.md').read_text()
        for fragment in ('Target and installation facts','Stages','Evidence and gap','Owner','One next action','maintenance-required','review-maintenance-adaptation','two necessary','8 KiB','Protocol 4','source authentication','scope','recover-upgrade','spawnCount','not-started','actual successor'):
            self.assertIn(fragment,text)
        for skill in ('vibe-feature-flow','vibe-debug-flow','vibe-implementation-flow','vibe-project-onboarding','vibe-verification-flow'):
            self.assertIn('upgrade-maintenance.md',(ROOT/'.agents/skills'/skill/'SKILL.md').read_text())

    def test_controlled_unknown_partial_denied_conflict_and_precise_undo(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);a=root/'a';b=root/'b'
            a.write_bytes(b'A-before');b.write_bytes(b'B-before')
            before={p.name:(p.read_bytes(),p.stat().st_mode) for p in (a,b)}
            writes={'a':0,'b':0}
            def owned_write(p,old,new):
                if p.read_bytes()!=old:raise ValueError('old-line match failure')
                p.write_bytes(new);writes[p.name]+=1
            # Lost acknowledgement after a confirmed real write starts unknown.
            certainty='unknown'
            try:
                owned_write(a,b'A-before',b'A-after');raise ConnectionError('synthetic receipt loss')
            except ConnectionError:pass
            self.assertEqual(certainty,'unknown');self.assertEqual(a.read_bytes(),b'A-after')
            certainty='executed';self.assertEqual(writes['a'],1)
            # Read every item. Only the exact still-authorized missing item is filled.
            self.assertEqual(b.read_bytes(),b'B-before');owned_write(b,b'B-before',b'B-after')
            self.assertEqual(writes,{'a':1,'b':1})
            # Preserve ordinary cause; never relabel old-line mismatch as disconnection.
            with self.assertRaisesRegex(ValueError,'old-line match failure'):owned_write(b,b'WRONG',b'again')
            self.assertEqual(writes['b'],1)
            denied=mock.Mock(side_effect=PermissionError(errno.EACCES,'synthetic denied'))
            with self.assertRaises(PermissionError):denied()
            self.assertEqual(denied.call_count,1)  # no reconnect or alternative-tool retry
            # Strong process-creation failure proves no workload was started.
            start=mock.Mock(side_effect=OSError('synthetic before-create failure'))
            with self.assertRaises(OSError):start()
            self.assertEqual(writes,{'a':1,'b':1})
            # Concurrent user content is never overwritten by undo.
            b.write_bytes(b'user-change');self.assertNotEqual(b.read_bytes(),b'B-after')
            self.assertEqual(b.read_bytes(),b'user-change')
            self.assertEqual(a.read_bytes(),b'A-after');a.write_bytes(before['a'][0]);a.chmod(before['a'][1]&0o777)
            self.assertEqual(a.read_bytes(),b'A-before');self.assertEqual(b.read_bytes(),b'user-change')
            installed='B';admitted={'A'}
            self.assertNotIn(installed,admitted)  # undo does not downgrade the installed Kit

    def test_python_and_node_original_qa_readback_never_respawns_workload(self):
        node=os.environ.get('CODEX_TASK_WORKSPACE_NODE') or shutil.which('node')
        self.assertTrue(node,'Blocked: real Node unavailable')
        for language in ('python','node'):
            for status in (0,1):
                with self.subTest(language=language,status=status),tempfile.TemporaryDirectory() as temporary:
                    target=Path(temporary)
                    (target/'.vibe/local').mkdir(parents=True,mode=0o700)
                    (target/'.vibe/local/receipts').mkdir(mode=0o700)
                    count=target/'count'
                    if language=='python':
                        (target/'workload.py').write_text('from pathlib import Path\nimport sys\np=Path("count");p.write_text(str(int(p.read_text())+1) if p.exists() else "1")\nprint("controlled python workload")\nsys.exit('+str(status)+')\n')
                        command=shlex.quote(sys.executable)+' -B workload.py'
                    else:
                        (target/'workload.cjs').write_text('const fs=require("node:fs");fs.writeFileSync("count",String(fs.existsSync("count")?Number(fs.readFileSync("count"))+1:1));console.log("controlled node workload");process.exit('+str(status)+');\n')
                        (target/'package.json').write_text(json.dumps({'private':True,'scripts':{'test':'node workload.cjs'}}))
                        command=shlex.quote(node)+' --run test'
                    (target/'.vibe/project.yaml').write_text('schema_version: 1\ncommands:\n  lint: ""\n  typecheck: ""\n  test: '+json.dumps(command)+'\n  build: ""\n')
                    env=os.environ.copy();env['PATH']=str(Path(node).parent)+os.pathsep+env['PATH']
                    receipt=target/'.vibe/local/receipts/final.json'
                    result=subprocess.run([sys.executable,'-B',str(CLI),'verify',str(target),'--progress','--receipt',str(receipt),'--format','json'],env=env,text=True,capture_output=True)
                    evidence=os.environ.get('VIBE_MAINTENANCE_EVIDENCE_DIR')
                    if evidence:
                        destination=Path(evidence)/(language+'-'+str(status));destination.mkdir(parents=True,exist_ok=False)
                        (destination/'command.json').write_text(json.dumps({'argv':result.args,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'input_command':command,'evidence_level':'controlled-cli','candidate_cli_sha256':hashlib.sha256(CLI.read_bytes()).hexdigest()},indent=2)+'\n')
                        shutil.copytree(target,destination/'observed-fixture')
                    self.assertEqual(count.read_text(),'1')
                    original=receipt.read_bytes();m=load_cli_module();locator,errors=m.read_verify_locator(target);self.assertEqual(errors,[])
                    # The observer discarded its direct result. Recover only the original evidence.
                    before=snapshot_tree(target);probes=0
                    for _ in range(2):
                        probe=subprocess.run([sys.executable,'-B',str(CLI),'inspect-run',str(target),'--run-id',locator['run_id'],'--final-receipt',str(receipt),'--format','json'],env=env,text=True,capture_output=True)
                        probes+=1;self.assertEqual(probe.returncode,0,probe.stdout+probe.stderr)
                        facts=json.loads(probe.stdout)['inspection'];self.assertEqual(facts['historical_run_verdict'],'passed' if status==0 else 'not-passed')
                        self.assertEqual(facts['candidate_applicability'],'unproven');self.assertEqual(facts['project_origin'],'not-attested')
                    self.assertEqual(count.read_text(),'1');self.assertEqual(probes,2)
                    self.assertEqual(receipt.read_bytes(),original);self.assertEqual(snapshot_tree(target),before)
                    print('MAINTENANCE-READBACK '+json.dumps({'language':language,'actual_verify_exit':result.returncode,'workload_spawn_count':1,'read_only_probe_count':probes,'receipt_sha256':hashlib.sha256(original).hexdigest(),'evidence_level':'controlled-cli'}))

    def test_recover_without_active_transaction_is_blocked_not_downgrade(self):
        with tempfile.TemporaryDirectory() as temporary:
            target=Path(temporary);(target/'.vibe').mkdir()
            before=snapshot_tree(target)
            result=subprocess.run([sys.executable,'-B',str(CLI),'recover-upgrade',str(target),'--format','json'],text=True,capture_output=True)
            self.assertEqual(result.returncode,2)
            value=json.loads(result.stdout);self.assertEqual(value['status'],'blocked')
            self.assertEqual(snapshot_tree(target),before)
