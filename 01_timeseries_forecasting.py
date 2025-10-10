#!/usr/bin/env python3.11
"""
PROJECT 1: TIME-SERIES FORECASTING FOR WEATHER & PEST TRENDS
=============================================================

Objective: Build ARIMA and Prophet models to predict weather variables and 
simulate automated alert systems for agricultural decision-making.

Resume Alignment:
"Built time-series forecasting models (ARIMA, Prophet) to predict weather and 
pest trends, enabling automated alerts that supported 1,000+ farmers in planning 
crops and pest management."

Author: Jae Mwangi
Date: October 2025
Data Source: MAWN Quality-Controlled Database (mawndb_qc)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Time series libraries
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from prophet import Prophet

# Evaluation metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10

print("="*80)
print("PROJECT 1: TIME-SERIES FORECASTING FOR WEATHER & PEST TRENDS")
print("="*80)

# ============================================================================
# SECTION 1: DATA LOADING AND PREPARATION
# ============================================================================

print("\n" + "="*80)
print("SECTION 1: DATA LOADING AND PREPARATION")
print("="*80)

print("\n[1.1] Loading MAWN Quality-Controlled Hourly Data")
print("-" * 80)

# Load the extracted hourly data
df_hourly = pd.read_csv('mawn_hourly_sample.csv', parse_dates=['datetime'])

print(f"✓ Loaded {len(df_hourly):,} hourly records")
print(f"✓ Date range: {df_hourly['datetime'].min()} to {df_hourly['datetime'].max()}")
print(f"✓ Stations: {', '.join(df_hourly['station'].unique())}")

print("\n[1.2] Data Quality Assessment")
print("-" * 80)

# Filter to single station for time-series analysis
station = 'aetna'
df_station = df_hourly[df_hourly['station'] == station].copy()
df_station = df_station.sort_values('datetime').reset_index(drop=True)

print(f"✓ Selected station: {station.upper()}")
print(f"✓ Records: {len(df_station):,}")
print(f"✓ Date range: {df_station['datetime'].min()} to {df_station['datetime'].max()}")

# Check data quality flags
print("\n✓ Data Quality Flags Distribution:")
print(f"  - Temperature (atmp_src): {df_station['atmp_src'].value_counts().to_dict()}")
print(f"  - Precipitation (pcpn_src): {df_station['pcpn_src'].value_counts().to_dict()}")

# Missing data analysis
missing_pct = (df_station[['atmp', 'relh', 'pcpn', 'lws0_pwet']].isnull().sum() / len(df_station) * 100)
print("\n✓ Missing Data Percentage:")
for col, pct in missing_pct.items():
    print(f"  - {col}: {pct:.2f}%")

print("\n[1.3] Aggregating to Daily Data")
print("-" * 80)
print("Rationale: Daily aggregation reduces noise and is appropriate for")
print("agricultural decision-making timescales (planting, pest management).")

# Aggregate to daily data
df_station['date'] = df_station['datetime'].dt.date

daily_agg = df_station.groupby('date').agg({
    'atmp': ['min', 'max', 'mean'],
    'relh': ['min', 'max', 'mean'],
    'dwpt': ['min', 'max', 'mean'],
    'pcpn': 'sum',  # Total daily precipitation
    'lws0_pwet': 'sum',  # Hours of leaf wetness
    'wspd': 'mean',
    'srad': 'sum',  # Total daily solar radiation
    'rpet': 'sum'  # Total daily evapotranspiration
}).reset_index()

# Flatten column names
daily_agg.columns = ['_'.join(col).strip('_') for col in daily_agg.columns.values]
daily_agg.rename(columns={'date': 'date'}, inplace=True)
daily_agg['date'] = pd.to_datetime(daily_agg['date'])

print(f"✓ Daily records created: {len(daily_agg):,}")
print(f"✓ Date range: {daily_agg['date'].min()} to {daily_agg['date'].max()}")

# Calculate Growing Degree Days (GDD) - Base 10°C
daily_agg['gdd'] = daily_agg['atmp_mean'].apply(lambda x: max(0, x - 10))

# Calculate temperature range
daily_agg['temp_range'] = daily_agg['atmp_max'] - daily_agg['atmp_min']

print("\n✓ Engineered Features:")
print("  - Growing Degree Days (GDD, base 10°C)")
print("  - Temperature Range (daily max - min)")
print("  - Daily precipitation sum")
print("  - Leaf wetness duration (hours)")

print("\n[1.4] Handling Missing Values")
print("-" * 80)

# Check for missing values in daily data
missing_daily = daily_agg.isnull().sum()
print("Missing values in daily data:")
print(missing_daily[missing_daily > 0])

# Forward fill small gaps (up to 3 days)
daily_agg = daily_agg.fillna(method='ffill', limit=3)

# Check remaining missing values
missing_after = daily_agg.isnull().sum()
print("\nMissing values after forward fill:")
print(missing_after[missing_after > 0])

# Drop rows with remaining missing values in key variables
key_vars = ['atmp_mean', 'relh_mean', 'pcpn_sum']
daily_agg = daily_agg.dropna(subset=key_vars)

print(f"\n✓ Final daily records: {len(daily_agg):,}")

print("\n[1.5] Train/Validation/Test Split")
print("-" * 80)
print("Split Strategy: Temporal split to respect time-series nature")
print("  - Train: 2019-2023 (model training)")
print("  - Validation: 2024 (hyperparameter tuning)")
print("  - Test: 2025 (final evaluation)")

# Create splits
train_end = '2023-12-31'
val_end = '2024-12-31'

train_data = daily_agg[daily_agg['date'] <= train_end].copy()
val_data = daily_agg[(daily_agg['date'] > train_end) & (daily_agg['date'] <= val_end)].copy()
test_data = daily_agg[daily_agg['date'] > val_end].copy()

print(f"\n✓ Train set: {len(train_data):,} days ({train_data['date'].min()} to {train_data['date'].max()})")
print(f"✓ Validation set: {len(val_data):,} days ({val_data['date'].min()} to {val_data['date'].max()})")
print(f"✓ Test set: {len(test_data):,} days ({test_data['date'].min()} to {test_data['date'].max()})")

# Save processed data
daily_agg.to_csv('daily_weather_aetna.csv', index=False)
print(f"\n✓ Saved processed daily data to: daily_weather_aetna.csv")

# ============================================================================
# SECTION 2: EXPLORATORY DATA ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("SECTION 2: EXPLORATORY DATA ANALYSIS")
print("="*80)

print("\n[2.1] Descriptive Statistics")
print("-" * 80)

print("\nTemperature Statistics (°C):")
print(train_data[['atmp_min', 'atmp_max', 'atmp_mean']].describe())

print("\nPrecipitation Statistics (mm):")
print(train_data['pcpn_sum'].describe())

print("\n[2.2] Creating Visualizations")
print("-" * 80)

# Create figure directory
import os
os.makedirs('figures', exist_ok=True)

# Plot 1: Temperature time series
fig, axes = plt.subplots(3, 1, figsize=(14, 10))

axes[0].plot(train_data['date'], train_data['atmp_mean'], label='Mean Temperature', alpha=0.7)
axes[0].fill_between(train_data['date'], train_data['atmp_min'], train_data['atmp_max'], 
                      alpha=0.3, label='Min-Max Range')
axes[0].set_ylabel('Temperature (°C)')
axes[0].set_title('Daily Temperature Patterns (Training Data: 2019-2023)', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].bar(train_data['date'], train_data['pcpn_sum'], width=1, alpha=0.7, label='Daily Precipitation')
axes[1].set_ylabel('Precipitation (mm)')
axes[1].set_title('Daily Precipitation', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

axes[2].plot(train_data['date'], train_data['relh_mean'], label='Mean Relative Humidity', 
             color='green', alpha=0.7)
axes[2].set_ylabel('Relative Humidity (%)')
axes[2].set_xlabel('Date')
axes[2].set_title('Daily Relative Humidity', fontsize=12, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/01_weather_timeseries_overview.png', dpi=300, bbox_inches='tight')
print("✓ Saved: figures/01_weather_timeseries_overview.png")
plt.close()

# Plot 2: Seasonal patterns
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Monthly temperature patterns
train_data['month'] = train_data['date'].dt.month
monthly_temp = train_data.groupby('month')['atmp_mean'].agg(['mean', 'std'])

axes[0, 0].plot(monthly_temp.index, monthly_temp['mean'], marker='o', linewidth=2)
axes[0, 0].fill_between(monthly_temp.index, 
                        monthly_temp['mean'] - monthly_temp['std'],
                        monthly_temp['mean'] + monthly_temp['std'],
                        alpha=0.3)
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Temperature (°C)')
axes[0, 0].set_title('Seasonal Temperature Pattern', fontweight='bold')
axes[0, 0].set_xticks(range(1, 13))
axes[0, 0].grid(True, alpha=0.3)

# Monthly precipitation
monthly_precip = train_data.groupby('month')['pcpn_sum'].sum()
axes[0, 1].bar(monthly_precip.index, monthly_precip.values, alpha=0.7, color='steelblue')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Total Precipitation (mm)')
axes[0, 1].set_title('Seasonal Precipitation Pattern', fontweight='bold')
axes[0, 1].set_xticks(range(1, 13))
axes[0, 1].grid(True, alpha=0.3)

# Temperature distribution
axes[1, 0].hist(train_data['atmp_mean'], bins=50, alpha=0.7, edgecolor='black')
axes[1, 0].set_xlabel('Temperature (°C)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('Temperature Distribution', fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# Growing Degree Days accumulation
train_data['gdd_cumsum'] = train_data['gdd'].cumsum()
axes[1, 1].plot(train_data['date'], train_data['gdd_cumsum'], linewidth=2)
axes[1, 1].set_xlabel('Date')
axes[1, 1].set_ylabel('Cumulative GDD')
axes[1, 1].set_title('Growing Degree Days Accumulation', fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/02_seasonal_patterns.png', dpi=300, bbox_inches='tight')
print("✓ Saved: figures/02_seasonal_patterns.png")
plt.close()

print("\n✓ EDA visualizations completed")

# ============================================================================
# SECTION 3: STATIONARITY TESTING
# ============================================================================

print("\n" + "="*80)
print("SECTION 3: STATIONARITY TESTING")
print("="*80)
print("Rationale: ARIMA models require stationary data (constant mean/variance)")

def test_stationarity(timeseries, variable_name):
    """
    Perform Augmented Dickey-Fuller test for stationarity
    """
    print(f"\n[{variable_name}]")
    print("-" * 80)
    
    # Perform ADF test
    result = adfuller(timeseries.dropna(), autolag='AIC')
    
    print(f"ADF Statistic: {result[0]:.6f}")
    print(f"p-value: {result[1]:.6f}")
    print(f"Critical Values:")
    for key, value in result[4].items():
        print(f"  {key}: {value:.3f}")
    
    if result[1] <= 0.05:
        print(f"✓ Result: STATIONARY (p-value = {result[1]:.6f} <= 0.05)")
        print("  → No differencing required")
        return True, 0
    else:
        print(f"✗ Result: NON-STATIONARY (p-value = {result[1]:.6f} > 0.05)")
        print("  → Differencing required")
        return False, 1

# Test temperature
temp_series = train_data.set_index('date')['atmp_mean']
is_stationary, d_temp = test_stationarity(temp_series, "Mean Temperature")

# Test differenced temperature if needed
if not is_stationary:
    print("\n  Testing first-order differencing...")
    temp_diff = temp_series.diff().dropna()
    is_stationary_diff, _ = test_stationarity(temp_diff, "Differenced Temperature")

# ============================================================================
# SECTION 4: ACF/PACF ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("SECTION 4: ACF/PACF ANALYSIS FOR ARIMA PARAMETER SELECTION")
print("="*80)
print("Purpose: Identify optimal (p, d, q) parameters for ARIMA model")
print("  - p: AR order (from PACF)")
print("  - d: Differencing order (from stationarity test)")
print("  - q: MA order (from ACF)")

# Create ACF/PACF plots
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Original series
plot_acf(temp_series.dropna(), lags=40, ax=axes[0, 0])
axes[0, 0].set_title('ACF: Original Temperature Series', fontweight='bold')

plot_pacf(temp_series.dropna(), lags=40, ax=axes[0, 1])
axes[0, 1].set_title('PACF: Original Temperature Series', fontweight='bold')

# Differenced series
temp_diff = temp_series.diff().dropna()
plot_acf(temp_diff, lags=40, ax=axes[1, 0])
axes[1, 0].set_title('ACF: Differenced Temperature Series', fontweight='bold')

plot_pacf(temp_diff, lags=40, ax=axes[1, 1])
axes[1, 1].set_title('PACF: Differenced Temperature Series', fontweight='bold')

plt.tight_layout()
plt.savefig('figures/03_acf_pacf_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: figures/03_acf_pacf_analysis.png")
plt.close()

print("\n✓ ACF/PACF analysis completed")
print("  Interpretation guide:")
print("  - PACF cuts off after lag p → AR(p)")
print("  - ACF cuts off after lag q → MA(q)")
print("  - Both decay gradually → ARIMA(p,d,q)")

print("\n" + "="*80)
print("CHECKPOINT: Data preparation and EDA completed")
print("="*80)
print(f"✓ Processed daily data: {len(daily_agg):,} records")
print(f"✓ Train/Val/Test split: {len(train_data)}/{len(val_data)}/{len(test_data)} days")
print(f"✓ Visualizations: 3 figures saved")
print(f"✓ Stationarity: Tested and documented")
print("\nReady to proceed to model building...")
print("="*80)

