
# ⚡ AI-Driven Dynamic Tariff Optimization for EV Charging Networks

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Project-Completed-success?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Smart%20Energy-orange?style=for-the-badge)

### Intelligent demand prediction and adaptive pricing system for EV charging infrastructure

</div>

---

# 📌 Project Overview

This project develops an AI-powered tariff optimization framework for Electric Vehicle (EV) charging networks.

The system combines:
- 📊 Demand forecasting
- ⚡ Dynamic tariff optimization
- 🧠 Monitoring and learning agents
- 📈 EV charging utilization analytics

The primary goal is to reduce:
- Grid congestion
- Peak-hour overload
- Station imbalance

while improving:
- Revenue efficiency
- Charging station utilization
- User demand management

---

# 🎯 Problem Statement

Traditional EV charging stations often use static pricing models.

These static tariffs fail to:
- Adapt to changing demand
- Handle peak-hour congestion
- Balance charging loads efficiently
- Encourage off-peak charging behavior

This project introduces a multi-agent AI system that dynamically predicts charging demand and adjusts tariffs accordingly.

---

# 🧠 System Architecture

```text
┌────────────────────────────────────┐
│     EV Charging Raw Datasets       │
└────────────────┬───────────────────┘
                 │
                 ▼
      ┌────────────────────┐
      │ Data Preprocessing │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Exploratory Data   │
      │ Analysis (EDA)     │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Demand Prediction  │
      │ Agent (ML Model)   │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Dynamic Tariff     │
      │ Pricing Agent      │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │ Monitoring &       │
      │ Learning Agent     │
      └────────────────────┘
```

---

# 📂 Project Structure

```text
ev_tariff_project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── demand_prediction_agent.joblib
│
├── outputs/
│   ├── figures/
│   └── reports/
│
├── src/
│   ├── 01_data_preprocessing.py
│   ├── 02_eda.py
│   ├── 03_demand_prediction_agent.py
│   ├── 04_tariff_pricing_agent.py
│   ├── 05_monitoring_learning_agent.py
│   └── config.py
│
├── app.py
├── run_all.py
├── requirements.txt
└── README.md
```

---

# 📊 Datasets Used

The project uses multiple EV charging datasets:

| Dataset | Purpose |
|---|---|
| occupancy.csv | Charging station occupancy |
| duration.csv | Charging session duration |
| price.csv | Energy pricing |
| volume.csv | Charging volume |
| stations.csv | Station metadata |
| distance.csv | Distance analytics |
| time.csv | Time-based usage patterns |

---

# ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Matplotlib
- Machine Learning Regression Models

---

# 🚀 Workflow

## 1️⃣ Data Preprocessing
- Data cleaning
- Missing value handling
- Feature engineering
- Dataset merging

## 2️⃣ Exploratory Data Analysis
- Demand trend analysis
- Utilization analysis
- Overloaded station detection
- Intraday charging behavior analysis

## 3️⃣ Demand Prediction Agent
- Machine learning forecasting model
- Predicts charging demand patterns
- Stores trained model using Joblib

## 4️⃣ Dynamic Tariff Pricing Agent
- Generates adaptive charging tariffs
- Applies congestion-aware pricing
- Encourages balanced charging demand

## 5️⃣ Monitoring & Learning Agent
- Monitors tariff decisions
- Tracks prediction accuracy
- Updates pricing behavior

---

# 📈 Key Outputs

Generated outputs include:

- Demand prediction reports
- Dynamic tariff decisions
- Monitoring metrics
- Station pricing policy summaries
- Demand trend visualizations

Output files are stored inside:

```text
outputs/reports/
outputs/figures/
```

---

# 📊 Important Visualizations

The project generates:
- Total demand trends
- Intraday utilization graphs
- Station overload analysis
- Pricing policy summaries

---

# ▶️ How to Run the Project

## Step 1 — Create Virtual Environment

```bash
python -m venv .venv
```

## Step 2 — Activate Environment

### Windows
```bash
.venv\Scripts\activate
```

### Linux/Mac
```bash
source .venv/bin/activate
```

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4 — Run Complete Pipeline

```bash
python run_all.py
```

---

# 📌 Project Highlights

✅ Multi-agent AI system

✅ Dynamic tariff optimization

✅ Demand forecasting pipeline

✅ Real-world EV charging datasets

✅ Smart energy management approach

✅ Automated reporting system

---

# 🔮 Future Improvements

- Deep learning demand forecasting
- Reinforcement learning pricing strategies
- Real-time dashboard integration
- IoT-based charging station monitoring
- Cloud deployment

---

# 🏁 Conclusion

This project demonstrates how AI and machine learning can improve EV charging infrastructure through intelligent tariff optimization and demand-aware pricing systems.

The system provides:
- Better load balancing
- Smarter pricing strategies
- Improved utilization efficiency
- Reduced congestion risks

This work highlights the practical application of AI in sustainable smart-energy ecosystems.

---

# 👨‍💻 Author

**Satyam Singh**

CDC × Yhills Open Projects (2025–26)

Domain: Data Science & AI

