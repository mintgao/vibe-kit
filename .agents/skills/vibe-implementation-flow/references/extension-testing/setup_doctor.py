"""Explicit test setup BEFORE the real Python/Node dispatcher, never a Kit API."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from bridge import cli_path

parser=argparse.ArgumentParser()
parser.add_argument('--state',choices=('absent','generated'),required=True)
parser.add_argument('--target',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
args.target.mkdir(parents=True,exist_ok=True)
args.output.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
if args.output.exists() or args.output.is_symlink():raise RuntimeError('Use a fresh owned fixture output; setup never overwrites it')
argv=None;code=None
if args.state=='generated':
    argv=[sys.executable,'-B',str(cli_path()),'doctor',str(args.target),'--format','json']
    result=subprocess.run(argv,text=True,capture_output=True)
    value=json.loads(result.stdout)
    if value['command']!='doctor':raise RuntimeError('Expected a real doctor result')
    descriptor=os.open(str(args.output),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(descriptor,'wb') as output:output.write(result.stdout.encode())
    code=result.returncode
raw=args.output.read_bytes() if args.output.is_file() else None
print(json.dumps({'setup':'before-child-dispatch','argv':argv,'doctor_exit':code,'actual_state':'generated' if raw is not None else 'absent','output_path_binding_sha256':hashlib.sha256(str(args.output.absolute()).encode()).hexdigest(),'output_sha256':hashlib.sha256(raw).hexdigest() if raw is not None else None,'output_mode':oct(args.output.stat().st_mode&0o777) if raw is not None else None},sort_keys=True))
