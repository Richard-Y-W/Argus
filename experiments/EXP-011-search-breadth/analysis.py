from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260716
RUNS = 20_000
K_GRID = (1, 5, 20, 50, 200)
CUTOFF = 1.6448536269514722
OUT = Path(__file__).parent / "results"


def main() -> None:
    rng = np.random.default_rng(SEED)
    train = rng.standard_normal((RUNS, max(K_GRID)))
    test = rng.standard_normal((RUNS, max(K_GRID)))
    rows = []
    for k in K_GRID:
        chosen = np.argmax(train[:, :k], axis=1)
        selected_train = train[np.arange(RUNS), chosen]
        selected_test = test[np.arange(RUNS), chosen]
        rows.append({
            "k": k,
            "selected_train_mean": selected_train.mean(),
            "selected_train_mc_se": selected_train.std(ddof=1) / np.sqrt(RUNS),
            "naive_train_pass_share": (selected_train > CUTOFF).mean(),
            "selected_test_mean": selected_test.mean(),
            "selected_test_mc_se": selected_test.std(ddof=1) / np.sqrt(RUNS),
            "selected_test_positive_share": (selected_test > 0).mean(),
            "selected_test_pass_share": (selected_test > CUTOFF).mean(),
        })
    summary = pd.DataFrame(rows)
    p1 = summary.selected_train_mean.is_monotonic_increasing and summary.selected_train_mean.is_unique
    p2 = (0.035 <= summary.iloc[0].naive_train_pass_share <= 0.065 and
          summary.iloc[-1].naive_train_pass_share > 0.95)
    p3 = ((summary.selected_test_mean.abs() < 0.05).all() and
          summary.selected_test_positive_share.between(0.47, 0.53).all())
    OUT.mkdir(exist_ok=True)
    summary.to_csv(OUT / "summary.csv", index=False)
    log = f"seed={SEED}\nruns={RUNS}\nP1={p1}\nP2={p2}\nP3={p3}\n"
    (OUT / "run_log.txt").write_text(log, encoding="utf-8")
    print(summary.round(4).to_string(index=False))
    print(log)


if __name__ == "__main__":
    main()
