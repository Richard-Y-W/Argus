"""Dataset fingerprint verification."""
from pathlib import Path
import hashlib,json

def sha256(path: Path):
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda:handle.read(1024*1024),b""):digest.update(block)
    return digest.hexdigest()

def verify_manifest(manifest_path: Path,raw_dir: Path):
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"));errors=[]
    for name,meta in manifest["files"].items():
        path=raw_dir/name
        if not path.exists():errors.append(f"missing: {name}");continue
        actual=sha256(path)
        if actual.lower()!=meta["sha256"].lower():errors.append(f"hash mismatch: {name}")
    return errors
