import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "outputs" / "reports"
FIGURE_DIR = ROOT / "outputs" / "figures"

st.set_page_config(page_title="EV Dynamic Tariff Optimization", layout="wide")
st.title("Agentic AI-Based Dynamic Tariff Optimization for EV Charging Networks")

metrics_path = REPORT_DIR / "monitoring_learning_metrics.json"
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text())
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue Gain %", f"{metrics['overall_revenue_gain_pct']:.2f}%")
    c2.metric("Congestion Reduction", f"{metrics['congestion_reduction_pct_points']:.2f} pp")
    c3.metric("Off-Peak Uplift", f"{metrics['off_peak_uplift_pct']:.2f}%")
    c4.metric("Pricing Efficiency", f"₹{metrics['pricing_efficiency_after_revenue_per_kwh']:.2f}/kWh")
else:
    st.warning("Run `python run_all.py` first to generate reports.")

st.header("EDA Visualizations")
for fig in sorted(FIGURE_DIR.glob("*.png")):
    st.image(str(fig), caption=fig.name, use_container_width=True)

st.header("Dynamic Tariff Decisions")
pricing_path = REPORT_DIR / "dynamic_tariff_decisions.csv"
if pricing_path.exists():
    df = pd.read_csv(pricing_path)
    st.dataframe(df.head(1000), use_container_width=True)
else:
    st.info("Dynamic tariff file not found yet.")
