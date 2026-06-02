# 📊 COMPREHENSIVE PROJECT REPORT

## **EV Dynamic Tariff Optimization for EV Charging Networks**

---

## **1. PROJECT OVERVIEW**

**Repository:** https://github.com/satyam9140/EV_DYNAMIC_TARIFF_OPTIMIZATION

**Project Status:** ✅ Completed

**Author:** Satyam Singh

**Domain:** Data Science & AI | Smart Energy Management

**Language:** Python (100% - 21,407 bytes)

**Created:** 10 hours ago

**Last Updated:** June 2, 2026

---

## **2. PROBLEM STATEMENT**

Traditional EV charging stations rely on **static pricing models** that fail to:
- ❌ Adapt to changing demand patterns
- ❌ Handle peak-hour congestion
- ❌ Balance charging loads efficiently
- ❌ Encourage off-peak charging behavior

This project introduces an **AI-powered, multi-agent system** that:
- ✅ Dynamically predicts EV charging demand
- ✅ Adjusts tariffs in real-time
- ✅ Reduces grid congestion
- ✅ Optimizes revenue efficiency
- ✅ Improves charging station utilization

---

## **3. SYSTEM ARCHITECTURE**

```
┌─────────────────────────────────────┐
│  EV Charging Raw Datasets           │
│  (UrbanEV, ACN Data)                │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Data Preprocessing │
        │ (01_*.py)          │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Exploratory Data   │
        │ Analysis (02_*.py) │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Demand Prediction  │
        │ Agent (03_*.py)    │
        │ [ML Model]         │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Dynamic Tariff     │
        │ Pricing Agent      │
        │ (04_*.py)          │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Monitoring &       │
        │ Learning Agent     │
        │ (05_*.py)          │
        └────────────────────┘
```

---

## **4. PROJECT STRUCTURE**

```
EV_DYNAMIC_TARIFF_OPTIMIZATION/
│
├── data/
│   ├── raw/                    # Raw datasets (7 CSV files)
│   │   ├── occupancy.csv
│   │   ├── duration.csv
│   │   ├── price.csv
│   │   ├── volume.csv
│   │   ├── stations.csv / information.csv
│   │   ├── distance.csv
│   │   └── time.csv
│   │
│   └── processed/              # Processed data (Parquet/CSV)
│       ├── urbanev_processed.parquet
│       ├── acn_sessions_processed.csv
│       └── hourly_model_table.csv
│
├── models/
│   └── demand_prediction_agent.joblib
│
├── outputs/
│   ├── figures/                 # Visualization outputs (PNG)
│   │   ├── 01_total_demand_trend.png
│   │   ├── 02_intraday_demand.png
│   │   ├── 03_intraday_utilization.png
│   │   └── 04_top_overloaded_stations.png
│   │
│   └── reports/                 # Analysis reports (CSV/JSON)
│       ├── station_level_eda_summary.csv
│       ├── hourly_behavior_summary.csv
│       ├── demand_predictions.csv
│       ├── demand_model_metrics.json
│       ├── dynamic_tariff_decisions.csv
│       ├── tariff_pricing_summary.json
│       ├── monitoring_learning_metrics.json
│       └── station_pricing_policy_summary.csv
│
├── src/
│   ├── 01_data_preprocessing.py      # [5,151 bytes]
│   ├── 02_eda.py                     # [2,882 bytes]
│   ├── 03_demand_prediction_agent.py # [4,549 bytes]
│   ├── 04_tariff_pricing_agent.py    # [3,215 bytes]
│   ├── 05_monitoring_learning_agent.py # [3,046 bytes]
│   └── config.py                     # [548 bytes]
│
├── app.py                      # Streamlit web interface
├── run_all.py                  # Complete pipeline orchestrator
├── requirements.txt            # Dependencies
├── Problem_Statement.pdf       # Original problem brief
└── README.md                   # Documentation
```

---

## **5. DATASETS USED**

| Dataset | Purpose | Details |
|---------|---------|---------|
| **occupancy.csv** | Station occupancy levels | Time-series charging station capacity utilization |
| **duration.csv** | Charging session duration | Average charging time per session |
| **price.csv** | Energy pricing signals | Raw pricing data for cost proxy |
| **volume.csv** | Charging volume (kWh) | Demand measurement across stations |
| **information.csv** | Station metadata | Charging capacities, locations, fast/slow chargers |
| **distance.csv** | Geographic distance analytics | Distance-based features |
| **time.csv** | Temporal patterns | Timestamps and temporal context |
| **acndata_sessions.json.xlsx** | ACN dataset (optional) | Alternative EV charging session data |

---

## **6. TECHNOLOGIES & DEPENDENCIES**

```
Core Libraries:
- Python 3.11+
- pandas         : Data manipulation & analysis
- numpy          : Numerical computing
- scikit-learn   : Machine Learning algorithms
- joblib         : Model serialization
- matplotlib     : Data visualization
- openpyxl       : Excel file handling
- pyarrow        : Parquet file support
- streamlit      : Web UI framework
```

---

## **7. DETAILED MODULE BREAKDOWN**

### **Module 1: Data Preprocessing** `src/01_data_preprocessing.py`

**Purpose:** Transform raw datasets into ML-ready format

**Key Functions:**

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `read_csv_file()` | filename | DataFrame | Safe CSV reading with error handling |
| `build_timestamp_table()` | time.csv | DataFrame | Creates temporal features (date, hour, dayofweek, peak_hour) |
| `wide_to_long()` | CSV filename | Long-format DataFrame | Converts wide time-series to long format |
| `preprocess_urbanev()` | Raw CSVs | Processed Parquet/CSV | Main UrbanEV preprocessing pipeline |
| `preprocess_acn()` | ACN Excel | Processed CSV | ACN data preprocessing |

**Key Features Engineered:**
```
- capacity: Station charging capacity
- utilization_rate: occupancy / capacity
- queue_length_proxy: max(occupancy - capacity, 0)
- congestion_probability_proxy: (utilization >= 0.80)
- off_peak_low_utilization: (utilization < 0.30)
- baseline_tariff_inr: ₹15.0
- baseline_revenue: volume × tariff
- revenue_per_capacity: baseline_revenue / capacity
```

**Output Files:**
- `urbanev_processed.parquet` (optimized size)
- `acn_sessions_processed.csv`

---

### **Module 2: Exploratory Data Analysis** `src/02_eda.py`

**Purpose:** Understand demand patterns and station characteristics

**Visualizations Generated:**

1. **01_total_demand_trend.png**
   - Hourly demand aggregated across all stations
   - Identifies demand cyclicity and trend

2. **02_intraday_demand.png**
   - Average demand by hour of day
   - Shows peak and off-peak patterns

3. **03_intraday_utilization.png**
   - Average utilization rate by hour
   - Overlays surge (80%) and discount (30%) thresholds

4. **04_top_overloaded_stations.png**
   - Bar chart of 20 most congested stations
   - Prioritizes intervention areas

**Reports Generated:**
- `station_level_eda_summary.csv` (avg utilization, queue, volume per station)
- `hourly_behavior_summary.csv` (hourly volume and utilization patterns)

---

### **Module 3: Demand Prediction Agent** `src/03_demand_prediction_agent.py`

**Purpose:** Forecast charging demand using machine learning

**ML Models Trained:**
1. **HistGradientBoostingRegressor** (max_iter=250)
2. **RandomForestRegressor** (n_estimators=80, max_depth=16)

**Features Used (17 total):**
```
[
  'avg_occupancy', 'avg_duration', 'avg_raw_price', 
  'utilization_rate', 'queue_length_proxy', 'capacity',
  'hour', 'dayofweek', 'is_weekend', 'is_peak_hour',
  'CBD', 'dynamic_pricing',
  'lag_1h_demand', 'lag_24h_demand',
  'rolling_3h_demand', 'rolling_24h_demand',
  'lag_1h_utilization'
]
```

**Target Variable:** `demand_volume` (kWh)

**Data Split:** 80% train / 20% test (temporal split)

**Metrics Calculated:**
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score

**Output Files:**
- `demand_prediction_agent.joblib` (best trained model)
- `demand_predictions.csv` (test predictions + utilization rates)
- `demand_model_metrics.json` (performance metrics)

---

### **Module 4: Dynamic Tariff Pricing Agent** `src/04_tariff_pricing_agent.py`

**Purpose:** Generate intelligent pricing based on demand predictions

**Tariff Formula:**
```
multiplier = 1 + 0.35×utilization + 0.15×peak_hour + 0.20×congestion - 0.18×off_peak
tariff = ₹15.0 × multiplier
tariff = clip(tariff, ₹9.0, ₹30.0)  # Min/Max bounds
```

**Pricing Categories:**
- 🔴 **SURGE_PRICE**: utilization > 80% (high pricing to reduce demand)
- 🟡 **NORMAL_DYNAMIC_PRICE**: 30% ≤ utilization ≤ 80% (standard dynamic pricing)
- 🟢 **DISCOUNT_PRICE**: utilization < 30% (low pricing to encourage usage)

**Price Elasticity Model:**
```
elasticity = -0.25  # 1% price increase → 0.25% demand reduction
adjusted_volume = predicted_volume × (1 + elasticity × price_change_ratio)
```

**Revenue Calculation:**
```
old_revenue = predicted_demand × ₹15.0
new_revenue = adjusted_demand × dynamic_tariff
revenue_gain = new_revenue - old_revenue
revenue_gain_pct = 100 × revenue_gain / old_revenue
```

**Congestion Reduction:**
```
post_pricing_utilization = adjusted_volume / capacity
post_pricing_congestion = (post_pricing_utilization ≥ 0.80)
post_pricing_queue = max(post_pricing_utilization - 1.0, 0) × capacity
```

**Output Files:**
- `dynamic_tariff_decisions.csv` (all pricing decisions)
- `tariff_pricing_summary.json` (aggregate metrics)

---

### **Module 5: Monitoring & Learning Agent** `src/05_monitoring_learning_agent.py`

**Purpose:** Track system performance and calculate KPIs

**Key Metrics Calculated:**

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Revenue Gain %** | (new - old) / old × 100 | Overall pricing effectiveness |
| **Congestion Reduction** | (before_rate - after_rate) × 100 pp | Load balancing success |
| **Queue Reduction %** | (before_queue - after_queue) / before_queue × 100 | Waiting time improvement |
| **Off-Peak Uplift %** | Increased off-peak demand % | Demand shifting effectiveness |
| **Pricing Efficiency** | Total revenue / Total demand | Revenue per kWh |

**Station-Level Policy Summary:**
- Average dynamic tariff per station
- Average revenue gain % per station
- Surge/discount action counts
- Post-pricing utilization

**Output Files:**
- `monitoring_learning_metrics.json` (system-wide KPIs)
- `station_pricing_policy_summary.csv` (per-station metrics)

---

## **8. CONFIGURATION** `src/config.py`

```python
# Directory Structure
ROOT_DIR = Project root
RAW_DIR = data/raw
PROCESSED_DIR = data/processed
FIGURE_DIR = outputs/figures
REPORT_DIR = outputs/reports
MODEL_DIR = models/

# Pricing Parameters
BASE_TARIFF_INR = ₹15.0           # Default tariff
SURGE_UTIL_THRESHOLD = 0.80       # 80% capacity
DISCOUNT_UTIL_THRESHOLD = 0.30    # 30% capacity
MIN_TARIFF_INR = ₹9.0             # Floor price
MAX_TARIFF_INR = ₹30.0            # Ceiling price

# ML Parameters
RANDOM_STATE = 42                 # Reproducibility
```

---

## **9. MAIN ENTRY POINTS**

### **Pipeline Orchestrator** `run_all.py`

Executes all 5 modules sequentially:

```python
SCRIPTS = [
    "src/01_data_preprocessing.py",      # Step 1: Data prep
    "src/02_eda.py",                     # Step 2: Analysis
    "src/03_demand_prediction_agent.py", # Step 3: ML model
    "src/04_tariff_pricing_agent.py",    # Step 4: Pricing
    "src/05_monitoring_learning_agent.py" # Step 5: Monitoring
]
```

**Usage:**
```bash
python run_all.py
```

### **Web Dashboard** `app.py`

Streamlit application for interactive visualization

**Features:**
- Real-time KPI metrics display
- EDA visualizations
- Dynamic tariff decision table
- Responsive UI

**Usage:**
```bash
streamlit run app.py
```

---

## **10. EXECUTION WORKFLOW**

### **Step 1: Setup Environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Prepare Data**
- Place raw CSV files in `data/raw/`
- Ensure files: occupancy.csv, duration.csv, price.csv, volume.csv, time.csv, information.csv

### **Step 3: Run Pipeline**
```bash
python run_all.py
```

### **Step 4: View Results**
```bash
# Dashboard
streamlit run app.py

# Or inspect CSV/JSON outputs in outputs/ directory
```

---

## **11. KEY OUTPUTS & RESULTS**

### **Demand Predictions**
- Hourly forecast per station
- Predicted utilization rates
- Congestion probability

### **Dynamic Tariff Decisions**
- Individualized pricing per station-hour
- Pricing category (SURGE/NORMAL/DISCOUNT)
- Revenue impact analysis

### **System Metrics**
- Overall revenue optimization %
- Peak congestion reduction
- Off-peak demand increase
- Queue/waiting time reduction

### **Visualizations**
- Total demand trends over time
- Intraday demand patterns
- Station utilization profiles
- Top overloaded stations

---

## **12. TECHNOLOGIES & STACK**

```
┌─────────────────────────────────────┐
│        Python 3.11+ Stack           │
├─────────────────────────────────────┤
│ Data Processing: Pandas, NumPy      │
│ ML Algorithms: Scikit-learn         │
│ Visualization: Matplotlib           │
│ Model Storage: Joblib               │
│ File I/O: Parquet, CSV, Excel       │
│ Web UI: Streamlit                   │
│ Version Control: Git/GitHub         │
└─────────────────────────────────────┘
```

---

## **13. PROJECT HIGHLIGHTS**

✅ **Multi-Agent AI System** - Decomposed into specialized agents

✅ **Real-World Datasets** - UrbanEV + ACN charging data

✅ **Advanced ML Models** - HistGradientBoosting, RandomForest

✅ **Dynamic Pricing Engine** - Context-aware tariff optimization

✅ **Revenue Optimization** - Proven revenue increase potential

✅ **Congestion Reduction** - Load balancing through pricing

✅ **Automated Reporting** - JSON/CSV outputs for analysis

✅ **Web Dashboard** - Interactive Streamlit interface

✅ **Reproducible Pipeline** - Full end-to-end automation

---

## **14. FUTURE IMPROVEMENTS**

🚀 **Deep Learning** - LSTM/GRU for temporal forecasting

🚀 **Reinforcement Learning** - Optimal pricing strategy discovery

🚀 **Real-Time Dashboard** - WebSocket-based live updates

🚀 **IoT Integration** - Real charging station connectivity

🚀 **Cloud Deployment** - AWS/GCP for scalability

🚀 **A/B Testing** - Price experimentation framework

🚀 **Multi-Objective Optimization** - Balance revenue, sustainability, UX

---

## **15. KEY FORMULAS & ALGORITHMS**

### **Demand Prediction**
- **Algorithm:** HistGradientBoosting / RandomForest
- **Features:** 17 temporal + spatial + lagged features
- **Optimization:** Hyperparameter tuning via experimentation

### **Tariff Optimization**
- **Formula:** Dynamic = Base × (1 + 0.35×U + 0.15×P + 0.20×C - 0.18×O)
- **Constraints:** ₹9 ≤ Tariff ≤ ₹30
- **Categories:** 3-tier pricing (SURGE/NORMAL/DISCOUNT)

### **Price Elasticity**
- **Model:** Δ_Demand = Elasticity × (Δ_Price / Base_Price)
- **Coefficient:** -0.25 (inelastic demand)
- **Effect:** 10% price increase → 2.5% demand reduction

### **Revenue Optimization**
- **Old Model:** Volume × ₹15.0 (static)
- **New Model:** Elasticity_Volume × Dynamic_Tariff
- **Gain:** Revenue_Gain = New - Old

---

## **16. COMMIT HISTORY**

| Commit | Author | Date | Message |
|--------|--------|------|---------|
| 7814b9f | Satyam Singh | 2026-06-02 05:30:39 | Rename OP'26 Analytics.pdf to Problem_Statement.pdf |
| 45fcd54 | Satyam Singh | 2026-06-02 05:27:57 | project upload on github |

**Repository Stats:**
- Default Branch: `main`
- Total Commits: 2
- Watchers: 0
- Forks: 0
- Open Issues: 0
- Visibility: Public

---

## **17. CONTRIBUTIONS & TEAM**

| Contributor | Role | Affiliation |
|-------------|------|-------------|
| **Satyam Singh** | Project Lead & Developer | CDC × Yhills Open Projects (2025-26) |

**Domain:** Data Science & AI

**Program:** Open Projects Initiative

---

## **18. TECHNICAL SPECIFICATIONS**

| Aspect | Specification |
|--------|---------------|
| **Language** | Python 3.11+ |
| **Total Code Size** | 21,407 bytes |
| **Main Modules** | 5 sequential agents |
| **Key Models** | HistGradientBoosting, RandomForest |
| **Data Format** | Parquet (optimized) + CSV |
| **UI Framework** | Streamlit |
| **Reproducibility** | Full automation via run_all.py |

---

## **19. INSTALLATION & USAGE QUICK START**

```bash
# 1. Clone repository
git clone https://github.com/satyam9140/EV_DYNAMIC_TARIFF_OPTIMIZATION.git
cd EV_DYNAMIC_TARIFF_OPTIMIZATION

# 2. Setup environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place raw data in data/raw/

# 5. Run complete pipeline
python run_all.py

# 6. View results
# Check outputs/reports/ for CSV/JSON files
# View outputs/figures/ for visualizations

# 7. Launch dashboard (optional)
streamlit run app.py
```

---

## **20. CONCLUSION**

This project demonstrates a **production-ready AI system** for **dynamic EV charging tariff optimization**. It combines:

✨ **Data-driven decision making** through ML forecasting

✨ **Intelligent pricing** adapting to real-time demand

✨ **Revenue optimization** while improving user experience

✨ **Scalable architecture** ready for production deployment

The system delivers measurable value through:
- 📈 Revenue increase potential
- 📉 Congestion reduction
- ⚡ Load balancing
- 💰 Pricing efficiency

**This work exemplifies how AI and machine learning drive innovation in sustainable smart-energy ecosystems.**

---

**Generated on:** June 2, 2026  
**Repository:** https://github.com/satyam9140/EV_DYNAMIC_TARIFF_OPTIMIZATION  
**Status:** ✅ Complete & Production-Ready

---

**END OF REPORT**
