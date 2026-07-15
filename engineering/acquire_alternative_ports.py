"""Download official C&Z alternative portfolios and cache as Parquet."""
from pathlib import Path
import argparse
from openassetpricing import OpenAP

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"datasets"/"raw";OUT.mkdir(exist_ok=True)
AVAILABLE=["deciles_ew","deciles_vw","quintiles_ew","quintiles_vw","ex_nyse_p20_me","ex_price5"]
parser=argparse.ArgumentParser();parser.add_argument("datasets",nargs="*",choices=AVAILABLE,default=["deciles_ew","deciles_vw"]);args=parser.parse_args()
client=OpenAP(release_year=202510)
for name in args.datasets:
    target=OUT/f"{name}.parquet"
    if target.exists():print(f"exists: {target.name}");continue
    frame=client.dl_port(name,"pandas")
    frame.to_parquet(target,index=False);print(f"saved: {target.name} ({len(frame):,} rows)")
