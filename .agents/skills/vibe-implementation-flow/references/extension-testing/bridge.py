"""Test-only bridge to the production validator; not a public CLI API."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys


def cli_path():
    supplied = os.environ.get("VIBE_TEMPLATE_CLI")
    if supplied:
        return Path(supplied)
    for root in Path(__file__).absolute().parents:
        if (root / "bin/vibe").is_file():
            return root / "bin/vibe"
    raise RuntimeError("Set VIBE_TEMPLATE_CLI to the reviewed production CLI")


def validate(receipt, *args):
    path = cli_path()
    loader = importlib.machinery.SourceFileLoader("extension_production_validator", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return {"findings": module.validate_complete_verify_receipt(receipt),
            "origin": str(path), "arguments": list(args)}


if __name__ == "__main__":
    value = json.load(sys.stdin)
    print(json.dumps(validate(value, *sys.argv[1:]), sort_keys=True))
