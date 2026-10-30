"""Focused execution of distributed templates via their actual dispatchers."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).absolute().parents[1]
BASE = ROOT / ".agents/skills/vibe-implementation-flow/references/extension-testing"


class ExtensionTestingTests(unittest.TestCase):
    def run_entry(self, runtime, state, extra=None, focused=True, actual_state=None):
        env=os.environ.copy(); env.update({"VIBE_TEMPLATE_CLI":str(ROOT/"bin/vibe"),"PYTHON":sys.executable,"EXTENSION_DOCTOR":state})
        if extra: env.update(extra)
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        fixture=Path(temporary.name);output=fixture/'observed/doctor.json'
        setup_command=[sys.executable,'-B',str(BASE/'setup_doctor.py'),'--state',actual_state or state,'--target',str(fixture/'doctor-target'),'--output',str(output)]
        setup=subprocess.run(setup_command,env=env,text=True,capture_output=True)
        self.assertEqual(setup.returncode,0,setup.stdout+setup.stderr)
        setup_observation=json.loads(setup.stdout)
        self.assertEqual(setup_observation['actual_state'],actual_state or state)
        env['VIBE_EXTENSION_DOCTOR_OUTPUT']=str(output)
        print('PRE-DISPATCH-SETUP '+json.dumps({'runtime':runtime,'argv':setup_command,'stdout':setup.stdout,'stderr':setup.stderr,'returncode':setup.returncode},sort_keys=True))
        if runtime=="python":
            command=[sys.executable,"-B","-m","unittest","discover","-s","tests"]+(["-p","test_contract.py"] if focused else [])+["-v"]
        else:
            node=env.get("CODEX_TASK_WORKSPACE_NODE") or shutil.which("node")
            self.assertTrue(node,"Blocked: real Node runtime unavailable")
            env["PATH"]=str(Path(node).parent)+os.pathsep+env["PATH"]
            command=[node,"--run","test"]+(["--","--focused"] if focused else [])
        direct_command=([sys.executable,"-B","-m","unittest","discover","-s","tests","-p","test_direct.py","-v"] if runtime=="python" else [node,"direct.cjs"])
        direct=subprocess.run(direct_command,cwd=BASE/runtime,env=env,text=True,capture_output=True)
        self.assertEqual(direct.returncode,0,direct.stdout+direct.stderr)
        print("DIRECT-HELPER-EVIDENCE "+json.dumps({"runtime":runtime,"argv":direct_command,"returncode":direct.returncode,"stdout":direct.stdout,"stderr":direct.stderr},sort_keys=True))
        result=subprocess.run(command,cwd=BASE/runtime,env=env,text=True,capture_output=True)
        for line in result.stdout.splitlines():
            if line.startswith('LOADER-START '):
                loaded=json.loads(line[len('LOADER-START '):])
                self.assertEqual(loaded['state'],actual_state or state)
                self.assertEqual(loaded['sha256'],setup_observation['output_sha256'])
                self.assertEqual(loaded['path_binding_sha256'],setup_observation['output_path_binding_sha256'])
                break
        else:self.fail('actual loader-start filesystem observation missing')
        print("TEMPLATE-EVIDENCE "+json.dumps({"runtime":runtime,"state":state,"argv":command,"returncode":result.returncode,"stdout":result.stdout,"stderr":result.stderr},sort_keys=True))
        return result

    def test_real_entries_both_lifecycles_and_negative_wiring(self):
        candidate_files=[ROOT/"bin/vibe"]+[path for path in BASE.rglob("*") if path.is_file()]
        def candidate():
            return {str(path.relative_to(ROOT)):{"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"mode":path.stat().st_mode&0o777} for path in candidate_files}
        candidate_before=candidate()
        for runtime in ("python","node"):
            history=BASE/runtime/("tests/test_historical.py" if runtime=="python" else "historical.cjs")
            historical_before=history.read_bytes()
            for state in ("absent","generated"):
                result=self.run_entry(runtime,state)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertIn('"state": "'+state+'"' if runtime=="python" else '"state":"'+state+'"',result.stdout)
                default=self.run_entry(runtime,state,focused=False)
                self.assertEqual(default.returncode,0,default.stdout+default.stderr)
            for variable,value in (("EXTENSION_ORIGIN","old"),("EXTENSION_ARGUMENT","WRONG")):
                result=self.run_entry(runtime,"absent",{variable:value})
                self.assertNotEqual(result.returncode,0)
            self.assertNotEqual(self.run_entry(runtime,"generated",actual_state="absent").returncode,0)
            self.assertEqual(self.run_entry(runtime,"generated").returncode,0)
            self.assertEqual(history.read_bytes(),historical_before)
            self.assertEqual(candidate(),candidate_before)
        print("FROZEN-SOURCE-INPUT "+json.dumps({"before":candidate_before,"after":candidate(),"same_candidate":True},sort_keys=True))
