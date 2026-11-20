#!/usr/bin/env python3
"""Verify package zips: root manifest, checksums, no local artifacts."""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
FORBIDDEN = ("__pycache__/", ".pyc", ".env", "EdgeProfile/", "data/")


def main() -> int:
    errors = []
    for pkg in CATALOG.get("packages") or []:
        zpath = ROOT / pkg["download"]
        if not zpath.is_file():
            errors.append(f"{pkg['name']}: missing {zpath}")
            continue
        data = zpath.read_bytes()
        if hashlib.sha256(data).hexdigest() != pkg["sha256"]:
            errors.append(f"{pkg['name']}: sha256 mismatch")
        with zipfile.ZipFile(zpath) as zf:
            names = zf.namelist()
            if "plugin.json" not in names:
                errors.append(f"{pkg['name']}: plugin.json is not at zip root")
            for name in names:
                if name.startswith("/") or ".." in Path(name).parts:
                    errors.append(f"{pkg['name']}: unsafe member {name}")
                if any(x in name for x in FORBIDDEN):
                    errors.append(f"{pkg['name']}: forbidden member {name}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"verified {len(CATALOG.get('packages') or [])} packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
