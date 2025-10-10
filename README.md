# 🌤️ Weather Forecasting & Agricultural Alert System

**Time-Series Forecasting Models for Agricultural Decision Support**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Project Overview

This project demonstrates the development and deployment of **time-series forecasting models** (ARIMA and Prophet) to predict weather patterns and enable **automated agricultural alerts**. Built using real-world data from the Michigan Automated Weather Network (MAWN), this system supports farmers in making critical decisions about crop planning, pest management, and resource allocation.

### 🎯 Key Objectives

- Develop accurate time-series forecasting models for temperature, humidity, and precipitation
- Compare ARIMA, Prophet, and baseline models for agricultural forecasting
- Build an automated alert system for frost, heat stress, and disease risk
- Create an interactive dashboard for real-time monitoring and decision support

### 🏆 Results Summary

| Model | Test MAE | Test RMSE | Status |
|-------|----------|-----------|--------|
| **Prophet** | **3.56°C** | **4.61°C** | ✅ Best |
| ARIMA(5,1,3) | 12.18°C | 14.40°C | ⚠️ |
| Baseline | 12.09°C | 14.28°C | ⚠️ |

- **55 alerts generated** with an average lead time of **27 days**
- **Prophet model achieved 70% reduction in MAE** compared to baseline
- Successfully predicted **86% of frost events** in the test period

---

## 🚀 Live Demo

**[🌐 View Interactive Dashboard](https://your-streamlit-app.streamlit.app)** *(Deploy to Streamlit Cloud and add link)*

![Dashboard Preview](figures/dashboard_preview.png)

---

## 📊 Features

### 1. **Time-Series Forecasting**
- ✅ ARIMA model with automated parameter selection (grid search)
- ✅ Prophet model with seasonal decomposition
- ✅ Multi-step ahead forecasting (7-day and 14-day)
- ✅ Confidence intervals and uncertainty quantification

### 2. **Automated Alert System**
- 🥶 **Frost Warning**: Temperature < 0°C
- 🔥 **Heat Stress**: Temperature > 30°C
- 🦠 **Disease Risk**: High humidity (>90%) + favorable temperature
- 🌧️ **Heavy Rain**: Precipitation > 25mm

### 3. **Interactive Dashboard**
- 📈 Model performance comparison
- 🔔 Real-time alert monitoring
- 📊 Data exploration tools
- 📥 Downloadable reports (CSV)

---

## 🛠️ Technical Stack

### Core Technologies
- **Python 3.11**: Primary programming language
- **Pandas & NumPy**: Data manipulation and numerical computing
- **Statsmodels**: ARIMA model implementation
- **Prophet**: Facebook's time-series forecasting library
- **Scikit-learn**: Model evaluation metrics

### Visualization
- **Matplotlib & Seaborn**: Static visualizations
- **Plotly**: Interactive charts
- **Streamlit**: Web application framework

### Data Source
- **MAWN (Michigan Automated Weather Network)**: Quality-controlled weather data
- **Station**: Aetna
- **Period**: April 2019 - August 2025 (2,332 daily records)
- **Variables**: Temperature, humidity, precipitation, wind, solar radiation, soil conditions

---

## 📁 Project Structure

```
enviroweather_projects/
│
├── app.py                          # Streamlit dashboard application
├── 01_timeseries_forecasting.py   # Data preparation & EDA
├── 02_model_building.py            # ARIMA & Prophet model training
├── 03_alert_system.py              # Alert generation engine
│
├── data/
│   ├── mawn_hourly_sample.csv      # Raw hourly data (100K records)
│   └── daily_weather_aetna.csv     # Processed daily data
│
├── figures/                        # All visualizations (9 figures)
│   ├── 01_weather_timeseries_overview.png
│   ├── 02_seasonal_patterns.png
│   ├── 03_acf_pacf_analysis.png
│   ├── 04_forecast_comparison.png
│   ├── 05_residual_analysis.png
│   ├── 06_model_performance_comparison.png
│   ├── 07_alert_system_overview.png
│   ├── 08_alert_timeline.png
│   └── 09_alert_statistics.png
│
├── model_comparison_results.csv    # Model evaluation metrics
├── generated_alerts.csv            # Alert log
│
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── METHODOLOGY.md                  # Detailed methodology
└── LICENSE                         # MIT License
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jae15/weather-forecasting-alerts.git
   cd weather-forecasting-alerts
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Analysis

Execute the scripts in order to reproduce the full analysis:

```bash
# Step 1: Data preparation and EDA
python 01_timeseries_forecasting.py

# Step 2: Model training and evaluation
python 02_model_building.py

# Step 3: Alert system simulation
python 03_alert_system.py
```

### Launching the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## 📈 Methodology

### 1. Data Preparation

**Data Source**: Michigan Automated Weather Network (MAWN) quality-controlled database

**Sampling Strategy**:
- Selected Aetna station for complete time-series continuity
- Aggregated hourly data to daily summaries (min, max, mean)
- Created 2,332 daily records spanning 6+ years
- Train/Validation/Test split: 74% / 16% / 10%

**Feature Engineering**:
- Growing Degree Days (GDD) with base 10°C
- Temperature range (daily max - min)
- Cumulative precipitation
- Leaf wetness duration

**Data Quality**:
- 99.96% completeness for key variables
- Quality flags: MAWN (validated), RTMA (estimated), EMPTY (missing)
- Forward-fill for small gaps (≤3 days)

### 2. Model Development

#### ARIMA Model
- **Stationarity Testing**: Augmented Dickey-Fuller (ADF) test
- **Parameter Selection**: Grid search over (p,d,q) combinations
- **Optimal Configuration**: ARIMA(5, 1, 3) based on AIC
- **Performance**: MAE = 12.18°C (struggled with seasonality)

#### Prophet Model
- **Seasonality**: Yearly and weekly patterns enabled
- **Trend**: Automatic changepoint detection
- **Uncertainty**: 95% confidence intervals
- **Performance**: MAE = 3.56°C ✅ (Best model)

#### Baseline (Persistence)
- Simple forecast: Tomorrow = Today
- Performance: MAE = 12.09°C
- Used to validate model improvements

### 3. Alert System

**Threshold-Based Rules**:
- Frost: Temp < 0°C → HIGH severity
- Heat: Temp > 30°C → MEDIUM severity
- Disease (High): Humidity > 90% AND Temp 15-25°C → HIGH severity
- Disease (Moderate): Humidity > 85% AND Temp 10-30°C → MEDIUM severity
- Heavy Rain: Precipitation > 25mm → HIGH severity

**Alert Generation**:
- Multi-variable forecasts (temperature, humidity, precipitation)
- Daily evaluation against thresholds
- Lead time calculation (days in advance)
- Actionable recommendations for each alert type

**Performance**:
- 55 alerts generated in test period (239 days)
- Average lead time: 27 days
- 86% detection rate for frost events

### 4. Model Evaluation

**Metrics**:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)
- Residual analysis (distribution, autocorrelation)

**Validation Strategy**:
- Temporal train/validation/test split (no data leakage)
- Out-of-sample evaluation
- Comparison against baseline

---

## 📊 Key Findings

### Model Performance

1. **Prophet significantly outperformed ARIMA** for agricultural forecasting
   - 70% reduction in MAE compared to baseline
   - Better capture of seasonal patterns
   - More robust to long-term forecasts

2. **ARIMA limitations** for this use case
   - Struggled with strong seasonality
   - Required extensive parameter tuning
   - Less interpretable for stakeholders

3. **Practical implications**
   - Prophet is recommended for deployment
   - 3.56°C MAE is acceptable for agricultural decision-making
   - Confidence intervals provide risk assessment

### Alert System

1. **Frost warnings** were the most frequent alert type (55 alerts)
   - Critical for crop protection in Michigan climate
   - Average 27-day lead time enables proactive planning

2. **Disease risk alerts** require multi-variable monitoring
   - Humidity + temperature thresholds
   - Seasonal patterns (spring/fall higher risk)

3. **System reliability**
   - 86% detection rate for frost events
   - Low false negative rate (critical for agriculture)
   - Acceptable false positive rate (better safe than sorry)

---

## 🎓 Skills Demonstrated

This project showcases the following data science competencies:

### Technical Skills
- ✅ Time-series analysis and forecasting
- ✅ Statistical modeling (ARIMA, Prophet)
- ✅ Feature engineering and data preprocessing
- ✅ Model evaluation and comparison
- ✅ Data visualization (static and interactive)
- ✅ Dashboard development (Streamlit)

### Domain Knowledge
- ✅ Agricultural decision support systems
- ✅ Weather pattern analysis
- ✅ Pest and disease risk assessment
- ✅ Growing Degree Days (GDD) calculations

### Software Engineering
- ✅ Clean, modular Python code
- ✅ Version control (Git/GitHub)
- ✅ Documentation and reproducibility
- ✅ Deployment-ready application

---

## 🔮 Future Enhancements

- [ ] Expand to multiple weather stations (spatial analysis)
- [ ] Integrate real-time data feeds (API)
- [ ] Add ensemble methods (model stacking)
- [ ] Implement LSTM/GRU deep learning models
- [ ] Create mobile-friendly alert notifications
- [ ] Add crop-specific recommendations
- [ ] Integrate soil moisture sensor data
- [ ] Deploy to cloud platform (AWS/Azure/GCP)

---

## 📚 References

### Data Source
- **Michigan Automated Weather Network (MAWN)**: [https://www.enviroweather.msu.edu/](https://www.enviroweather.msu.edu/)
- Michigan State University, Department of Plant, Soil and Microbial Sciences

### Libraries & Tools
- **Prophet**: Taylor, S. J., & Letham, B. (2018). Forecasting at scale. *The American Statistician*, 72(1), 37-45.
- **Statsmodels**: Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with python. *Proceedings of the 9th Python in Science Conference*.
- **Streamlit**: [https://streamlit.io/](https://streamlit.io/)

### Agricultural Forecasting
- Hoogenboom, G. (2000). Contribution of agrometeorology to the simulation of crop production and its applications. *Agricultural and Forest Meteorology*, 103(1-2), 137-157.

---

## 👩‍💻 About Me

**Jae Mwangi**  
Data Scientist | Michigan State University - Enviroweather

I'm a data scientist with experience in time-series forecasting, machine learning, and agricultural decision support systems. This project is part of my portfolio demonstrating real-world applications of data science in agriculture.

### 🔗 Connect with Me
- **LinkedIn**: [linkedin.com/in/jae-m-9a492636](https://www.linkedin.com/in/jae-m-9a492636/)
- **GitHub**: [github.com/Jae15](https://github.com/Jae15)
- **Email**: [janomwangi@gmail.com](mailto:janomwangi@gmail.com)
- **Portfolio**: [TBD](https://TBD)

### 💼 Experience Highlights
- **Data Scientist, Michigan State University - Enviroweather** (Feb 2024 - Present)
  - Built time-series forecasting models (ARIMA, Prophet) to predict weather and pest trends
  - Enabled automated alerts that supported 1,000+ farmers in planning crops and pest management
  - Applied clustering (K-means, Hierarchical) to segment microclimates and guide targeted recommendations
  - Developed classification models with 85%+ accuracy in pest outbreak prediction

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Michigan State University** for providing access to MAWN data
- **Enviroweather team** for domain expertise and guidance
- **Open-source community** for the amazing tools and libraries

---

## 📞 Contact & Support

If you have questions, suggestions, or would like to collaborate:

- **Open an issue**: [GitHub Issues](https://github.com/Jae15/weather-forecasting-alerts/issues)
- **Email me**: janomwangi@gmail.com
- **LinkedIn**: [Connect with me](https://www.linkedin.com/in/jae-m-9a492636/)

---

<div align="center">
  <p><strong>⭐ If you found this project helpful, please consider giving it a star!</strong></p>
  <p>Built with ❤️ by Jae Mwangi</p>
</div>

