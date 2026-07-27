"""Dependence diagnostics for factor-level publication-decay contrasts."""
from __future__ import annotations

from itertools import product

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform


def factor_contrasts(panel: pd.DataFrame) -> pd.DataFrame:
    """Return one post-publication-minus-in-sample contrast per factor, in pp/month."""
    means = panel.groupby(["name", "window"], observed=True).ret.mean().unstack()
    means = means.dropna(subset=["in_sample", "post_pub"])
    return means.assign(contrast_pct=(means.post_pub - means.in_sample) * 100)[
        ["contrast_pct"]
    ].reset_index()


def prepublication_correlation(
    panel: pd.DataFrame, min_overlap: int = 60, shrinkage: float = 0.10
) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    """Estimate and regularize pairwise correlation using no post-publication returns."""
    pre = panel[panel.window != "post_pub"].pivot(index="date", columns="name", values="ret")
    raw = pre.corr(min_periods=min_overlap)
    overlap = pre.notna().astype(int).T @ pre.notna().astype(int)
    names = raw.columns
    eligible_pairs = overlap.to_numpy()[np.triu_indices(len(names), 1)] >= min_overlap
    coverage = float(eligible_pairs.mean())

    matrix = raw.fillna(0.0).to_numpy()
    np.fill_diagonal(matrix, 1.0)
    matrix = (1.0 - shrinkage) * matrix + shrinkage * np.eye(len(matrix))
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    matrix = vectors @ np.diag(np.maximum(values, 1e-8)) @ vectors.T
    scale = np.sqrt(np.diag(matrix))
    matrix = matrix / np.outer(scale, scale)
    matrix = (matrix + matrix.T) / 2.0
    np.fill_diagonal(matrix, 1.0)
    return pd.DataFrame(matrix, index=names, columns=names), overlap, coverage


def effective_rank(correlation: pd.DataFrame) -> float:
    values = np.linalg.eigvalsh(correlation.to_numpy())
    return float(values.sum() ** 2 / np.square(values).sum())


def cluster_factors(correlation: pd.DataFrame, clusters: int = 13) -> pd.DataFrame:
    distance = np.sqrt(np.maximum(0.0, 0.5 * (1.0 - correlation.to_numpy())))
    distance = (distance + distance.T) / 2.0
    np.fill_diagonal(distance, 0.0)
    tree = linkage(squareform(distance, checks=True), method="average")
    labels = fcluster(tree, t=clusters, criterion="maxclust")
    return pd.DataFrame({"name": correlation.index, "cluster": labels.astype(int)})


def within_between_summary(correlation: pd.DataFrame, assignments: pd.DataFrame) -> dict:
    label = assignments.set_index("name").loc[correlation.index, "cluster"].to_numpy()
    upper = np.triu_indices(len(label), 1)
    values = correlation.to_numpy()[upper]
    same = label[upper[0]] == label[upper[1]]
    return {
        "within_median": float(np.median(values[same])),
        "between_median": float(np.median(values[~same])),
        "median_gap": float(np.median(values[same]) - np.median(values[~same])),
    }


def exact_sign_pvalue(values: pd.Series) -> float:
    """Enumerate the two-sided sign-randomization distribution."""
    observed = abs(float(values.mean()))
    array = values.to_numpy(dtype=float)
    permuted = np.fromiter(
        (abs(float(np.mean(array * signs))) for signs in product((-1.0, 1.0), repeat=len(array))),
        dtype=float,
        count=2 ** len(array),
    )
    return float(np.mean(permuted >= observed - 1e-12))
