"""Dataset fingerprints and repository lifecycle integrity."""
from pathlib import Path
import hashlib,json

def sha256(path: Path):
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda:handle.read(1024*1024),b""):digest.update(block)
    return digest.hexdigest()

def verify_manifest(manifest_path: Path,raw_dir: Path):
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"));errors=[]
    files=dict(manifest["files"])
    for release in manifest.get("external_releases",{}).values():files.update(release.get("files",{}))
    for name,meta in files.items():
        path=raw_dir/name
        if not path.exists():errors.append(f"missing: {name}");continue
        actual=sha256(path)
        if actual.lower()!=meta["sha256"].lower():errors.append(f"hash mismatch: {name}")
    return errors


def verify_experiment_lifecycle(repo_root: Path) -> list[str]:
    """Require every completed experiment to have exactly one verdict record."""
    experiment_root = repo_root / "experiments"
    completed = {
        path.name.split("-", 2)[1]
        for path in experiment_root.glob("EXP-???-*")
        if path.is_dir() and (path / "results.md").exists()
    }
    successful = {
        path.name.split("-", 2)[1]
        for path in (repo_root / "successful_experiments").glob("EXP-???-*.md")
    }
    failed = {
        path.name.split("-", 2)[1]
        for path in (repo_root / "failed_experiments").glob("EXP-???-*.md")
    }

    errors: list[str] = []
    for experiment_id in sorted(completed):
        classifications = int(experiment_id in successful) + int(experiment_id in failed)
        if classifications == 0:
            errors.append(f"unclassified completed experiment: EXP-{experiment_id}")
        elif classifications > 1:
            errors.append(f"multiply classified experiment: EXP-{experiment_id}")
    for experiment_id in sorted((successful | failed) - completed):
        errors.append(f"verdict without completed experiment: EXP-{experiment_id}")
    return errors
