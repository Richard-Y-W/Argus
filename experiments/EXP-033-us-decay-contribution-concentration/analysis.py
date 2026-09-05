"""EXP-033: contribution concentration of archived US decay contrasts."""
import csv
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

    total_sum = sum(row["contrast_pct"] for row in rows)
    abs_sum = sum(abs(row["contrast_pct"]) for row in rows)
    full_mean = total_sum / len(rows)
    clusters = []
    for cluster in sorted({row["cluster"] for row in rows}):
        members = [row for row in rows if row["cluster"] == cluster]
        values = [row["contrast_pct"] for row in members]
        cluster_sum = sum(values)
        clusters.append({
            "cluster": cluster,
            "factors": len(values),
            "mean_pct": cluster_sum / len(values),
            "sum_pct": cluster_sum,
            "negative_factor_share": sum(value < 0 for value in values) / len(values),
            "signed_negative_total_share": cluster_sum / total_sum,
            "absolute_contribution_share": abs(cluster_sum) / abs_sum,
            "members": ";".join(sorted(row["name"] for row in members)),
        })
    leave_one = []
    for cluster in sorted({row["cluster"] for row in rows}):
        omitted = [row for row in rows if row["cluster"] == cluster]
        retained = [row for row in rows if row["cluster"] != cluster]
        leave_one.append({
            "omitted_cluster": cluster,
            "omitted_factors": len(omitted),
            "retained_mean_pct": sum(row["contrast_pct"] for row in retained) / len(retained),
        })
    max_signed = max(row["signed_negative_total_share"] for row in clusters)
    top_two_abs = sum(sorted((row["absolute_contribution_share"] for row in clusters), reverse=True)[:2])
    dominant_cluster = max(clusters, key=lambda row: row["signed_negative_total_share"])["cluster"]
    summary = [{
        "clusters": len(clusters),
        "factors": len(rows),
        "full_equal_factor_mean_pct": full_mean,
        "max_signed_negative_total_share": max_signed,
        "top_two_absolute_contribution_share": top_two_abs,
        "least_negative_leave_one_cluster_pct": max(row["retained_mean_pct"] for row in leave_one),
        "most_negative_leave_one_cluster_pct": min(row["retained_mean_pct"] for row in leave_one),
        "dominant_cluster": dominant_cluster,
        "P1": max_signed <= 0.40,
        "P2": top_two_abs <= 0.60,
        "P3": all(row["retained_mean_pct"] <= -0.10 for row in leave_one),
        "falsifier": max_signed >= 0.70,
    }]
    summary[0]["survives"] = summary[0]["P1"] and summary[0]["P2"] and summary[0]["P3"] and not summary[0]["falsifier"]
    OUT.mkdir(exist_ok=True)
    write_csv(OUT / "cluster_contributions.csv", clusters)
    write_csv(OUT / "leave_one_cluster.csv", leave_one)
    write_csv(OUT / "summary.csv", summary)
    log = ", ".join(f"{key}={value}" for key, value in summary[0].items())
    (OUT / "run_log.txt").write_text(log + "\n", encoding="utf-8")
    print(log)


if __name__ == "__main__":
    main()
