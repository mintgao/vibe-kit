#!/usr/bin/env python3
"""Run the Vibe CLI from this Plugin's bundled release payload."""

import os
from pathlib import Path
import sys


def main() -> int:
    plugin_root = Path(__file__).resolve().parents[3]
    cli = plugin_root / "payload/bin/vibe"
    if not cli.is_file():
        print("error: Vibe Kit Plugin payload is missing; reinstall a verified Plugin artifact.", file=sys.stderr)
        return 2
    os.execv(sys.executable, [sys.executable, str(cli), *sys.argv[1:]])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
