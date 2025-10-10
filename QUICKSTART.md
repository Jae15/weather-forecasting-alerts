# Quick Start Guide
## Weather Forecasting & Agricultural Alert System

**Get up and running in 5 minutes!**

---

## Option 1: View the Dashboard (Fastest)

If the dashboard is already deployed:

🌐 **[View Live Dashboard](https://your-app.streamlit.app)**

---

## Option 2: Run Locally

### Step 1: Install Dependencies (2 minutes)

```bash
# Clone or download the project
cd weather-forecasting-alerts

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Launch Dashboard (30 seconds)

```bash
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`

---

## Option 3: Run Full Analysis

### Execute All Scripts (10-15 minutes total)

```bash
# Data preparation & EDA (~2 min)
python 01_timeseries_forecasting.py

# Model training (~5-10 min)
python 02_model_building.py

# Alert system (~3-5 min)
python 03_alert_system.py

# Launch dashboard
streamlit run app.py
```

---

## What You'll See

### Dashboard Pages:

1. **📊 Overview**
   - Project summary and key metrics
   - Temperature time series visualization
   - Data quality statistics

2. **📈 Model Performance**
   - Comparison of ARIMA, Prophet, and Baseline models
   - Accuracy metrics and visualizations
   - Model methodology details

3. **🔔 Alert System**
   - Active alerts and severity levels
   - Alert timeline and history
   - Threshold configuration

4. **🔍 Data Explorer**
   - Interactive data visualization
   - Custom date range selection
   - Downloadable datasets

---

## Key Files

- `app.py` - Streamlit dashboard (main application)
- `01_timeseries_forecasting.py` - Data prep & EDA
- `02_model_building.py` - Model training
- `03_alert_system.py` - Alert generation
- `README.md` - Full project documentation
- `RESULTS_SUMMARY.md` - Non-technical results explanation
- `METHODOLOGY.md` - Detailed technical methodology
- `DEPLOYMENT.md` - Deployment instructions

---

## Troubleshooting

**Issue**: `ModuleNotFoundError`
- **Fix**: `pip install -r requirements.txt`

**Issue**: `FileNotFoundError` for CSV files
- **Fix**: Run scripts 01, 02, 03 first to generate data files

**Issue**: Prophet installation fails
- **Fix**: `pip install pystan==2.19.1.1` then `pip install prophet`

---

## Next Steps

1. ✅ Explore the dashboard
2. ✅ Read `RESULTS_SUMMARY.md` for business impact
3. ✅ Review `METHODOLOGY.md` for technical details
4. ✅ Check `DEPLOYMENT.md` to deploy to cloud

---

**Questions?** 
- 📧 Email: janomwangi@gmail.com
- 💼 LinkedIn: [Jae Mwangi](https://www.linkedin.com/in/jae-m-9a492636/)
- 🐙 GitHub: [Open an issue](https://github.com/Jae15/weather-forecasting-alerts/issues)

---

**Author**: Jae Mwangi  
**Project**: Time-Series Forecasting for Agricultural Decision Support
