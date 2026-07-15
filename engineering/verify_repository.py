from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engineering.argus_lab.integrity import verify_manifest

errors=verify_manifest(ROOT/"datasets"/"manifest.json",ROOT/"datasets"/"raw")
if errors:raise SystemExit("\n".join(errors))
print("dataset manifest verified")
