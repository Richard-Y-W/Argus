"""EXP-032: equal dependence-cluster weighting of archived US decay contrasts."""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent / "results"
CONTRASTS = ROOT / "experiments/EXP-020-factor-balanced-us-decay/results/factor_contrasts.csv"
ASSIGNMENTS = ROOT / "experiments/EXP-022-effective-factor-breadth/results/assignments.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def median(values: list[float]) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def t_stat(values: list[float]) -> float:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    return mean / (math.sqrt(variance) / math.sqrt(len(values)))


def main() -> None:
    contrast_by_name = {
        row["name"]: float(row["postpub_minus_insample"])
        for row in read_csv(CONTRASTS)
    }
    rows = []
    for row in read_csv(ASSIGNMENTS):
        name = row["name"]
        if name in contrast_by_name:
            rows.append({
                "name": name,
                "cluster": int(row["cluster"]),
                "contrast_pct": contrast_by_name[name],
            })
    if len(rows) != len(contrast_by_name):
        raise ValueError("Assignment and contrast files do not match one-to-one.")

    clusters = []
    for cluster in sorted({row["cluster"] for row in rows}):
        values = [row["contrast_pct"] for row in rows if row["cluster"] == cluster]
        clusters.append({
            "cluster": cluster,
            "factors": len(values),
            "mean_pct": sum(values) / len(values),
            "median_pct": median(values),
            "negative_factor_share": sum(value < 0 for value in values) / len(values),
        })
    primary = [row["mean_pct"] for row in clusters]
    summary = [{
        "clusters": len(clusters),
        "factors": len(rows),
        "equal_cluster_mean_pct": sum(primary) / len(primary),
        "equal_cluster_median_pct": median(primary),
        "cluster_t": t_stat(primary),
        "negative_cluster_share": sum(value < 0 for value in primary) / len(primary),
        "minimum_cluster_pct": min(primary),
        "maximum_cluster_pct": max(primary),
        "P1": sum(primary) / len(primary) <= -0.10,
        "P2": bool(t_stat(primary) <= -1.65),
        "P3": sum(value < 0 for value in primary) / len(primary) >= 0.70,
        "falsifier": sum(primary) / len(primary) >= 0,
    }]
    summary[0]["survives"] = summary[0]["P1"] and summary[0]["P2"] and summary[0]["P3"] and not summary[0]["falsifier"]
    OUT.mkdir(exist_ok=True)
    write_csv(OUT / "cluster_contrasts.csv", clusters)
    write_csv(OUT / "summary.csv", summary)
    log = ", ".join(f"{key}={value}" for key, value in summary[0].items())
    (OUT / "run_log.txt").write_text(log + "\n", encoding="utf-8")
    print(log)


if __name__ == "__main__":
    main()
