from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260717
RUNS = 100_000
CANDIDATES = 100
CUTOFF = 1.6448536269514722
BATCH = 2_000
OUT = Path(__file__).parent / "results"


def main() -> None:
    rng = np.random.default_rng(SEED)
    leaky_count = confirmed_count = 0
    for start in range(0, RUNS, BATCH):
        n = min(BATCH, RUNS - start)
        train = rng.standard_normal((n, CANDIDATES))
        chosen = np.argmax(train, axis=1)
        validation = rng.standard_normal((n, CANDIDATES))[np.arange(n), chosen]
        confirmation = rng.standard_normal((n, CANDIDATES))[np.arange(n), chosen]
        leaky = validation > CUTOFF
        confirmed = leaky & (confirmation > CUTOFF)
        leaky_count += int(leaky.sum())
        confirmed_count += int(confirmed.sum())
    leaky_rate = leaky_count / RUNS
    confirmed_rate = confirmed_count / RUNS
    reduction = 1 - confirmed_rate / leaky_rate
    conditional = confirmed_count / leaky_count
    def mc_se(p: float) -> float:
        return float(np.sqrt(p * (1 - p) / RUNS))
    summary = pd.DataFrame([{
        "runs": RUNS,
        "candidates": CANDIDATES,
        "leaky_false_claim_rate": leaky_rate,
        "leaky_mc_se": mc_se(leaky_rate),
        "confirmed_false_claim_rate": confirmed_rate,
        "confirmed_mc_se": mc_se(confirmed_rate),
        "relative_reduction": reduction,
        "conditional_confirmation_share": conditional,
    }])
    p1 = 0.035 <= leaky_rate <= 0.065
    p2 = confirmed_rate < 0.005
    p3 = reduction >= 0.80
    p4 = conditional < 0.10
    OUT.mkdir(exist_ok=True)
    summary.to_csv(OUT / "summary.csv", index=False)
    log = f"seed={SEED}\nruns={RUNS}\nP1={p1}\nP2={p2}\nP3={p3}\nP4={p4}\n"
    (OUT / "run_log.txt").write_text(log, encoding="utf-8")
    print(summary.round(6).to_string(index=False))
    print(log)


if __name__ == "__main__":
    main()
