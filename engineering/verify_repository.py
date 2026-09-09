from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engineering.argus_lab.integrity import verify_experiment_lifecycle, verify_manifest

errors=verify_manifest(ROOT/"datasets"/"manifest.json",ROOT/"datasets"/"raw")
errors.extend(verify_experiment_lifecycle(ROOT))
if errors:raise SystemExit("\n".join(errors))
print("dataset manifest and experiment lifecycle verified")
