import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "src/01_data_preprocessing.py",
    "src/02_eda.py",
    "src/03_demand_prediction_agent.py",
    "src/04_tariff_pricing_agent.py",
    "src/05_monitoring_learning_agent.py",
]

for script in SCRIPTS:
    print("\n" + "=" * 80)
    print(f"Running {script}")
    print("=" * 80)
    result = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(f"Pipeline stopped because {script} failed.")

print("\nComplete project pipeline finished successfully.")
