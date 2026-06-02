from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_DIR = ROOT_DIR / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
REPORT_DIR = OUTPUT_DIR / "reports"
MODEL_DIR = ROOT_DIR / "models"

BASE_TARIFF_INR = 15.0
SURGE_UTIL_THRESHOLD = 0.80
DISCOUNT_UTIL_THRESHOLD = 0.30
MIN_TARIFF_INR = 9.0
MAX_TARIFF_INR = 30.0
RANDOM_STATE = 42

for path in [PROCESSED_DIR, FIGURE_DIR, REPORT_DIR, MODEL_DIR]:
    path.mkdir(parents=True, exist_ok=True)
