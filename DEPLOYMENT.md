# Deployment Guide

**Project**: Weather Forecasting & Agricultural Alert System 
**Author**: Jae Mwangi 
**Last Updated**: October 2025

---

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Running the Analysis](#running-the-analysis)
3. [Launching the Streamlit Dashboard](#launching-the-streamlit-dashboard)
4. [Deploying to Streamlit Cloud](#deploying-to-streamlit-cloud)
5. [Deploying to Other Platforms](#deploying-to-other-platforms)
6. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

- **Python 3.11+** installed on your system
- **pip** package manager
- **Git** (for version control)
- **8GB+ RAM** recommended (for Prophet model training)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Jae15/weather-forecasting-alerts.git
cd weather-forecasting-alerts
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: Prophet installation may take 5-10 minutes as it compiles C++ components.

### Step 4: Verify Installation

```bash
python -c "import pandas, prophet, streamlit; print('All packages installed successfully!')"
```

---

## Running the Analysis

The project consists of three main scripts that should be run in sequence:

### Script 1: Data Preparation & EDA

```bash
python 01_timeseries_forecasting.py
```

**What it does:**
- Loads and processes MAWN hourly data
- Aggregates to daily summaries
- Performs exploratory data analysis
- Tests for stationarity
- Generates ACF/PACF plots

**Outputs:**
- `daily_weather_aetna.csv` - Processed daily data
- `figures/01_weather_timeseries_overview.png`
- `figures/02_seasonal_patterns.png`
- `figures/03_acf_pacf_analysis.png`

**Runtime**: ~2-3 minutes

### Script 2: Model Building & Evaluation

```bash
python 02_model_building.py
```

**What it does:**
- Trains ARIMA model (grid search for optimal parameters)
- Trains Prophet model
- Generates forecasts on validation and test sets
- Compares models against baseline
- Performs residual analysis

**Outputs:**
- `model_comparison_results.csv` - Performance metrics
- `figures/04_forecast_comparison.png`
- `figures/05_residual_analysis.png`
- `figures/06_model_performance_comparison.png`

**Runtime**: ~5-10 minutes (ARIMA grid search is slow)

### Script 3: Alert System Simulation

```bash
python 03_alert_system.py
```

**What it does:**
- Trains Prophet models for temperature, humidity, precipitation
- Generates 14-day forecasts
- Evaluates alert thresholds
- Creates alert log with lead times
- Validates against actual conditions

**Outputs:**
- `generated_alerts.csv` - Alert log
- `figures/07_alert_system_overview.png`
- `figures/08_alert_timeline.png`
- `figures/09_alert_statistics.png`

**Runtime**: ~3-5 minutes

### Run All Scripts

```bash
# Run all scripts in sequence
python 01_timeseries_forecasting.py && \
python 02_model_building.py && \
python 03_alert_system.py
```

---

## Launching the Streamlit Dashboard

### Local Launch

```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Dashboard Features

- ** Overview**: Project summary, key metrics, temperature time series
- ** Model Performance**: Model comparison, metrics, methodology details
- ** Alert System**: Alert timeline, threshold configuration, recent alerts
- ** Data Explorer**: Interactive data visualization, statistics, raw data download

### Stopping the Dashboard

Press `Ctrl+C` in the terminal to stop the Streamlit server.

---

## Deploying to Streamlit Cloud

Streamlit Cloud provides **free hosting** for public Streamlit apps.

### Step 1: Prepare Your Repository

1. **Ensure all files are committed to Git**:
 ```bash
 git add .
 git commit -m "Prepare for deployment"
 git push origin main
 ```

2. **Verify `requirements.txt` is in the root directory**

3. **Ensure data files are included**:
 - `daily_weather_aetna.csv`
 - `model_comparison_results.csv`
 - `generated_alerts.csv`

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch (`main`), and main file (`app.py`)
5. Click "Deploy"

### Step 3: Wait for Deployment

- Initial deployment takes 5-10 minutes
- Streamlit Cloud will install dependencies and launch your app
- You'll receive a public URL (e.g., `https://your-app.streamlit.app`)

### Step 4: Update README

Add your live app URL to the README:

```markdown
**[ View Interactive Dashboard](https://your-app.streamlit.app)**
```

### Troubleshooting Streamlit Cloud

**Issue**: Deployment fails with "ModuleNotFoundError"
- **Solution**: Ensure all dependencies are in `requirements.txt`

**Issue**: App crashes with memory error
- **Solution**: Streamlit Cloud free tier has 1GB RAM limit. Consider:
 - Reducing data size
 - Using cached data loading (`@st.cache_data`)
 - Upgrading to paid tier

**Issue**: Data files not found
- **Solution**: Ensure CSV files are committed to Git (not in `.gitignore`)

---

## Deploying to Other Platforms

### Option 1: Heroku

1. **Create `Procfile`**:
 ```
 web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
 ```

2. **Create `setup.sh`**:
 ```bash
 mkdir -p ~/.streamlit/
 echo "[server]
 headless = true
 port = $PORT
 enableCORS = false
 " > ~/.streamlit/config.toml
 ```

3. **Deploy**:
 ```bash
 heroku create your-app-name
 git push heroku main
 ```

### Option 2: AWS EC2

1. **Launch EC2 instance** (t2.medium recommended)
2. **SSH into instance**:
 ```bash
 ssh -i your-key.pem ubuntu@your-ec2-ip
 ```
3. **Install dependencies**:
 ```bash
 sudo apt update
 sudo apt install python3.11 python3.11-venv
 ```
4. **Clone repo and run**:
 ```bash
 git clone https://github.com/Jae15/weather-forecasting-alerts.git
 cd weather-forecasting-alerts
 python3.11 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 streamlit run app.py --server.port=8501 --server.address=0.0.0.0
 ```
5. **Configure security group** to allow port 8501

### Option 3: Docker

1. **Create `Dockerfile`**:
 ```dockerfile
 FROM python:3.11-slim
 WORKDIR /app
 COPY requirements.txt .
 RUN pip install -r requirements.txt
 COPY . .
 EXPOSE 8501
 CMD ["streamlit", "run", "app.py"]
 ```

2. **Build and run**:
 ```bash
 docker build -t weather-forecasting-app .
 docker run -p 8501:8501 weather-forecasting-app
 ```

---

## Troubleshooting

### Common Issues

#### Issue: Prophet installation fails

**Error**: `ERROR: Failed building wheel for prophet`

**Solution**:
```bash
# Install build dependencies first
pip install pystan==2.19.1.1
pip install prophet
```

**On macOS**:
```bash
brew install gcc
pip install prophet
```

#### Issue: Streamlit not found

**Error**: `streamlit: command not found`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

# Reinstall streamlit
pip install streamlit
```

#### Issue: Data files not loading

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'daily_weather_aetna.csv'`

**Solution**:
```bash
# Ensure you're in the project directory
cd /path/to/weather-forecasting-alerts

# Verify data files exist
ls *.csv

# Run scripts in order to generate data files
python 01_timeseries_forecasting.py
python 02_model_building.py
python 03_alert_system.py
```

#### Issue: Matplotlib/Seaborn plots not displaying

**Error**: Blank figures or `RuntimeError: main thread is not in main loop`

**Solution**:
```bash
# Add to top of script
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
```

#### Issue: Out of memory errors

**Error**: `MemoryError` or `Killed`

**Solution**:
- Reduce data size (sample fewer stations)
- Use smaller forecast horizon
- Close other applications
- Upgrade to machine with more RAM

---

## Performance Optimization

### For Faster Model Training

1. **Reduce ARIMA grid search space**:
 ```python
 p_values = [1, 2, 3] # Instead of [0, 1, 2, 3, 5]
 q_values = [1, 2, 3]
 ```

2. **Use parallel processing for Prophet**:
 ```python
 from prophet import Prophet
 model = Prophet(mcmc_samples=0) # Disable MCMC for speed
 ```

3. **Cache Streamlit data loading**:
 ```python
 @st.cache_data
 def load_data():
 return pd.read_csv('daily_weather_aetna.csv')
 ```

### For Smaller File Sizes

1. **Compress figures**:
 ```python
 plt.savefig('figure.png', dpi=150) # Instead of dpi=300
 ```

2. **Use Parquet instead of CSV**:
 ```python
 df.to_parquet('data.parquet') # Smaller and faster
 ```

---

## Monitoring & Maintenance

### Updating the Model

To retrain models with new data:

1. **Update data files** with latest MAWN data
2. **Re-run analysis scripts**:
 ```bash
 python 01_timeseries_forecasting.py
 python 02_model_building.py
 python 03_alert_system.py
 ```
3. **Restart Streamlit app**:
 ```bash
 streamlit run app.py
 ```

### Monitoring Forecast Accuracy

Track model performance over time:

```python
# Add to monitoring script
actual = load_actual_data()
forecast = load_forecast_data()
mae = mean_absolute_error(actual, forecast)

if mae > 5.0: # Alert if accuracy degrades
 send_alert("Model accuracy degraded: MAE = {mae:.2f}")
```

---

## Support

For issues or questions:

- **GitHub Issues**: [Open an issue](https://github.com/Jae15/weather-forecasting-alerts/issues)
- **Email**: janomwangi@gmail.com
- **LinkedIn**: [Connect with me](https://www.linkedin.com/in/jae-m-9a492636/)

---

**Author**: Jae Mwangi 
**Last Updated**: October 2025

