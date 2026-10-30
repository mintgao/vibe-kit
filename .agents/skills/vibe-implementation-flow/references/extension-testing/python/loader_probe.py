"""Observe the designated fixture file before the adapter imports any helper."""
import hashlib
import json
import os
from pathlib import Path
value=os.environ.get('VIBE_EXTENSION_DOCTOR_OUTPUT')
output=Path(value) if value else None
regular=bool(output is not None and not output.is_symlink() and output.is_file())
raw=output.read_bytes() if regular else None
SNAPSHOT={'state':'generated' if regular else 'absent' if output is None or not output.exists() else 'unavailable','exists':bool(output is not None and output.exists()),'sha256':hashlib.sha256(raw).hexdigest() if raw is not None else None,'path_binding_sha256':hashlib.sha256(str(output.absolute()).encode()).hexdigest() if output is not None else None,'loader_origin':__file__,'before_helper_import':True}
print('LOADER-START '+json.dumps(SNAPSHOT,sort_keys=True))
