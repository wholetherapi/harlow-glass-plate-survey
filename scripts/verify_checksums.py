"""Checksum verification for the Harlow Glass Plate Survey masters."""

import hashlib
import json
from pathlib import Path


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(manifest_path: str, masters_dir: str) -> int:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    failures = 0
    for item in manifest["items"]:
        master = Path(masters_dir) / item["derivative"]
        if not master.exists() or sha256_of(master) != item["sha256"]:
            failures += 1
            print(f"checksum mismatch: {master}")
    return failures


if __name__ == "__main__":
    raise SystemExit(verify("manifests/checksums.json", "masters"))
