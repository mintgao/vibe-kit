#!/usr/bin/env python3
"""Verify and run the Vibe CLI from this Plugin's bundled release payload."""

import hashlib
import json
import os
from pathlib import Path
import sys


def main() -> int:
    plugin_root = Path(__file__).resolve().parents[3]
    payload_root = plugin_root / "payload"
    cli = payload_root / "bin/vibe"
    if not cli.is_file():
        print("error: Vibe Kit Plugin payload is missing; reinstall a verified Plugin artifact.", file=sys.stderr)
        return 2
    try:
        manifest = json.loads(
            (plugin_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        version = (payload_root / ".vibe/core/version").read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"error: Vibe Kit Plugin identity is unreadable: {error}", file=sys.stderr)
        return 2
    digest = hashlib.sha256()
    for path in sorted(item for item in payload_root.rglob("*") if item.is_file()):
        relative = path.relative_to(payload_root).as_posix()
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    if manifest.get("version") != version or manifest.get(
        "payload_tree_sha256"
    ) != digest.hexdigest():
        print(
            "error: Vibe Kit Plugin payload identity does not match its manifest; reinstall a verified Plugin artifact.",
            file=sys.stderr,
        )
        return 2
    os.execv(sys.executable, [sys.executable, str(cli), *sys.argv[1:]])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
