import importlib.util
from pathlib import Path
bridge=Path(__file__).absolute().parents[1]/"bridge.py"
spec=importlib.util.spec_from_file_location("extension_bridge",bridge)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def check(receipt,*args):
    return module.validate(receipt,*args)
