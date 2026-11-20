#!/usr/bin/env python3
"""Build installable zip packages and regenerate catalog.json."""
from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ROOT / "packages"
DIST = ROOT / "dist"


def main() -> int:
    DIST.mkdir(exist_ok=True)
    rows = []
    for src in sorted(p for p in PACKAGES.iterdir() if p.is_dir()):
        manifest = src / "plugin.json"
        if not manifest.is_file():
            continue
        raw = json.loads(manifest.read_text(encoding="utf-8"))
        block = raw.get("gantry") if isinstance(raw.get("gantry"), dict) else raw
        name = str(block.get("name") or raw.get("name") or src.name)
        version = str(block.get("version") or raw.get("version") or "0.1.0")
        out = DIST / f"{name}-{version}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(src.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    zf.write(path, path.relative_to(src).as_posix())
        data = out.read_bytes()
        rows.append({
            "name": name, "version": version,
            "description": str(block.get("description") or raw.get("description") or ""),
            "source": f"packages/{name}", "download": f"dist/{out.name}",
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
            "permissions": list(block.get("permissions") or []),
            "tools": list((block.get("contributes") or {}).get("tools") or []),
            "allow_uninstall": bool(block.get("allow_uninstall", False)),
            "default_enabled": bool(block.get("default_enabled", True)),
        })
    catalog = {"schema": 1,
               "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "gantry_compat": ">=0.11.0-beta.27", "packages": rows}
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"built {len(rows)} packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
