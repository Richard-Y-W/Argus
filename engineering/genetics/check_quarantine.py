"""Fail when genetics-owned machine artifacts contain PLEX-specific markers."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GENETICS_ROOTS = (
    REPO_ROOT / "engineering" / "genetics",
    REPO_ROOT / "experiments" / "EXP-028-modular-gene-repair",
    REPO_ROOT / "experiments" / "EXP-029-danger-routed-immune-controller",
    REPO_ROOT / "experiments" / "EXP-030-invariant-restoring-defense",
    REPO_ROOT / "experiments" / "EXP-031-surveillance-treatment-factorial",
)
SCANNED_SUFFIXES = {".py", ".json", ".toml", ".yaml", ".yml"}
FORBIDDEN_MARKERS = (
    "plex",
    "everef",
    "eve online",
    "19000001",
    "44992",
)


def quarantine_violations() -> list[str]:
    """Return path/marker pairs, excluding this enforcement module itself."""
    violations: list[str] = []
    for root in GENETICS_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path == Path(__file__) or not path.is_file():
                continue
            if path.suffix.lower() not in SCANNED_SUFFIXES:
                continue
            content = path.read_text(encoding="utf-8").lower()
            for marker in FORBIDDEN_MARKERS:
                if marker in content:
                    violations.append(f"{path.relative_to(REPO_ROOT)}: {marker}")
    return violations


def main() -> int:
    violations = quarantine_violations()
    if violations:
        print("Genetics/PLEX quarantine violations:")
        print("\n".join(violations))
        return 1
    print("Genetics/PLEX quarantine: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
