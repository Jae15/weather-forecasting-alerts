# Enviroweather Portfolio Projects - Implementation Plan

## Overview
This document outlines three comprehensive data science projects based on Michigan Automated Weather Network (MAWN) data, designed to showcase experience with time-series forecasting, clustering, and classification models as described in the Enviroweather resume bullet points.

## Data Summary
- **Source**: MAWN Quality-Controlled Database (mawndb_qc)
- **Stations**: Aetna, Alpine (100,000 hourly records)
- **Date Range**: April 2019 - August 2025 (6+ years)
- **Key Variables**:
  - Temperature (atmp): -21°C to 34°C
  - Relative Humidity (relh): 14% to 100%
  - Precipitation (pcpn): Hourly accumulation
  - Leaf Wetness (lws0_pwet): 0-1 (binary/continuous)
  - Wind Speed (wspd), Solar Radiation (srad)
  - Soil Temperature & Moisture at multiple depths
  - Reference Evapotranspiration (rpet)

---

## Project 1: Time-Series Forecasting for Weather & Pest Trends

### Objective
Build ARIMA and Prophet models to predict weather variables and simulate automated alert systems for agricultural decision-making.

### Resume Alignment
> "Built time-series forecasting models (ARIMA, Prophet) to predict weather and pest trends, enabling automated alerts that supported 1,000+ farmers in planning crops and pest management."

### Key Components

#### 1.1 Data Preparation
- Aggregate hourly data to daily averages/min/max
- Create features: Growing Degree Days (GDD), Cumulative precipitation, Temperature ranges
- Handle missing values with forward-fill and interpolation
- Split data: Train (2019-2023), Validation (2024), Test (2025)

#### 1.2 Temperature Forecasting
- **ARIMA Model**:
  - Stationarity testing (ADF test)
  - ACF/PACF analysis for parameter selection
  - Grid search for optimal (p,d,q) parameters
  - 7-day and 14-day ahead forecasts
  
- **Prophet Model**:
  - Capture seasonality (yearly, weekly)
  - Include holidays and special events
  - Uncertainty intervals
  - Multi-step ahead forecasting

#### 1.3 Precipitation & Humidity Forecasting
- Similar approach for precipitation patterns
- Humidity forecasting for disease risk assessment

#### 1.4 Automated Alert System Simulation
- **Critical Thresholds**:
  - Temperature < 0°C (frost warning)
  - Temperature > 30°C (heat stress)
  - Humidity > 90% for 6+ hours (disease risk)
  - Precipitation > 25mm (flooding risk)
  
- **Alert Logic**:
  - Generate alerts when forecasts exceed thresholds
  - Calculate lead time (hours/days before event)
  - Simulate farmer notification system

#### 1.5 Model Evaluation
- Metrics: MAE, RMSE, MAPE
- Residual analysis
- Forecast accuracy by lead time
- Comparison: ARIMA vs Prophet vs Baseline (persistence model)

### Deliverables
- Jupyter notebook with full analysis
- Interactive visualizations (actual vs predicted)
- Alert system simulation results
- Model comparison report

---

## Project 2: Microclimate Segmentation Using Clustering

### Objective
Apply K-means and Hierarchical clustering to segment weather stations into microclimate zones, uncovering hidden risk patterns for targeted agricultural recommendations.

### Resume Alignment
> "Applied clustering (K-means, Hierarchical) and feature engineering to segment microclimates, uncovering hidden risk patterns and guiding targeted agricultural recommendations."

### Key Components

#### 2.1 Feature Engineering
Create comprehensive climate signatures for each station:

- **Temperature Features**:
  - Mean, min, max daily temperature
  - Temperature variability (std dev)
  - Growing Degree Days (GDD) - Base 10°C
  - Frost days count
  - Heat stress days (>30°C)
  
- **Moisture Features**:
  - Average relative humidity
  - Precipitation totals (seasonal)
  - Soil moisture patterns
  - Leaf wetness duration
  
- **Radiation & Wind**:
  - Average solar radiation
  - Wind speed patterns
  - Evapotranspiration rates
  
- **Temporal Patterns**:
  - Seasonal variations
  - Day-to-night temperature swings
  - Precipitation frequency vs intensity

#### 2.2 Clustering Analysis

**K-Means Clustering**:
- Elbow method for optimal K
- Silhouette score analysis
- 3-5 microclimate clusters expected
- Feature importance via cluster centers

**Hierarchical Clustering**:
- Dendrogram visualization
- Linkage methods comparison (ward, complete, average)
- Cophenetic correlation
- Compare with K-means results

#### 2.3 Risk Pattern Identification

For each cluster, identify:
- **Pest Risk Profiles**:
  - High humidity + moderate temp → fungal disease risk
  - Warm + dry → insect pest pressure
  - Cool + wet → bacterial disease risk
  
- **Crop Suitability**:
  - Match clusters to crop requirements
  - Identify optimal planting windows
  
- **Extreme Event Vulnerability**:
  - Frost risk zones
  - Drought-prone areas
  - Flood risk assessment

#### 2.4 Targeted Recommendations

Generate cluster-specific guidance:
- Recommended crop varieties
- Pest monitoring priorities
- Irrigation strategies
- Planting/harvesting timing

#### 2.5 Visualization
- Geographic map of clusters (if coordinates available)
- Radar charts for cluster characteristics
- Heatmaps of feature distributions
- Time-series overlays by cluster

### Deliverables
- Clustering analysis notebook
- Microclimate profile cards (one per cluster)
- Risk assessment matrix
- Interactive visualizations

---

## Project 3: Pest Outbreak Classification Models

### Objective
Develop Random Forest, Logistic Regression, and Naïve Bayes classifiers to predict pest outbreak risk with 85%+ accuracy, validated through ROC-AUC, confusion matrix, and cross-validation.

### Resume Alignment
> "Developed classification models (Random Forest, Logistic Regression, Naïve Bayes) with 85%+ accuracy in pest outbreak prediction, validated through ROC-AUC, confusion matrix and cross-validation."

### Key Components

#### 3.1 Target Variable Creation

**Pest Outbreak Risk Indicators** (based on environmental conditions):

- **Fungal Disease Risk** (e.g., Late Blight, Powdery Mildew):
  - Leaf wetness > 6 hours
  - Temperature 15-25°C
  - Humidity > 85%
  - Label: 1 (High Risk), 0 (Low Risk)
  
- **Insect Pest Risk** (e.g., Aphids, Corn Borer):
  - Temperature 20-30°C
  - Low precipitation (< 5mm/week)
  - Growing season months
  - Label: 1 (High Risk), 0 (Low Risk)

#### 3.2 Feature Engineering

**Weather-Based Features**:
- Current conditions: temp, humidity, precipitation, leaf wetness
- Rolling averages: 3-day, 7-day, 14-day
- Cumulative values: GDD, precipitation sum
- Lagged features: previous 1, 3, 7 days
- Rate of change: temperature delta, humidity trend

**Temporal Features**:
- Month, day of year
- Growing season indicator
- Days since last rain
- Consecutive days with favorable conditions

#### 3.3 Model Development

**Random Forest Classifier**:
- Hyperparameter tuning (n_estimators, max_depth, min_samples_split)
- Feature importance analysis
- Out-of-bag error estimation
- Target: 85%+ accuracy

**Logistic Regression**:
- Feature scaling (StandardScaler)
- Regularization (L1/L2)
- Coefficient interpretation
- Probability calibration

**Naïve Bayes**:
- Gaussian Naïve Bayes for continuous features
- Prior probability estimation
- Conditional independence assumption validation

#### 3.4 Model Validation

**Cross-Validation**:
- 5-fold stratified CV
- Time-series split (respect temporal order)
- Ensure balanced classes in each fold

**Performance Metrics**:
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC curve
- Confusion Matrix
- Classification Report
- Precision-Recall curve (for imbalanced data)

**Threshold Optimization**:
- Adjust decision threshold for optimal recall (minimize false negatives)
- Cost-sensitive learning (false negatives more costly than false positives)

#### 3.5 Model Comparison & Ensemble

- Compare all three models
- Ensemble methods: Voting classifier, Stacking
- Feature importance across models
- Model interpretability (SHAP values for Random Forest)

#### 3.6 Practical Application

**Early Warning System**:
- Real-time risk scoring
- Alert generation when risk > threshold
- Lead time analysis (how many days in advance can we predict?)
- False alarm rate vs detection rate trade-off

### Deliverables
- Classification modeling notebook
- Model comparison report with metrics
- ROC curves and confusion matrices
- Feature importance visualizations
- Pest risk prediction dashboard (interactive)
- Model deployment guide

---

## Technical Stack

### Languages & Core Libraries
- Python 3.11
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly

### Time-Series
- statsmodels (ARIMA)
- Prophet (Facebook Prophet)

### Machine Learning
- scikit-learn (clustering, classification)
- imbalanced-learn (SMOTE for class imbalance)

### Evaluation & Visualization
- scikit-learn metrics
- yellowbrick (ML visualizations)
- SHAP (model interpretability)

---

## Success Criteria

### Project 1 (Forecasting)
- ✅ ARIMA and Prophet models implemented
- ✅ 7-day and 14-day forecasts generated
- ✅ MAE < 2°C for temperature forecasts
- ✅ Automated alert system simulated
- ✅ Model comparison with clear winner

### Project 2 (Clustering)
- ✅ K-means and Hierarchical clustering applied
- ✅ 3-5 distinct microclimate clusters identified
- ✅ Silhouette score > 0.5
- ✅ Risk patterns documented for each cluster
- ✅ Actionable recommendations generated

### Project 3 (Classification)
- ✅ Three models (RF, LR, NB) trained and evaluated
- ✅ Accuracy ≥ 85% on test set
- ✅ ROC-AUC ≥ 0.85
- ✅ Confusion matrix and cross-validation results
- ✅ Feature importance analysis completed
- ✅ Early warning system demonstrated

---

## Timeline

- **Phase 1**: Data preparation & EDA (Complete)
- **Phase 2**: Time-series forecasting project (Next)
- **Phase 3**: Clustering project
- **Phase 4**: Classification project
- **Phase 5**: Documentation & portfolio assembly

---

## Notes

- All models will be documented with clear methodology
- Code will be modular and well-commented
- Visualizations will be publication-quality
- Results will be reproducible
- Portfolio will include README with project descriptions

