#!/usr/bin/env python3.11
"""
INDEPENDENT PORTFOLIO PROJECT: TIME-SERIES FORECASTING - MODEL BUILDING & EVALUATION
====================================================================================

Author: Jae Mwangi
Project: Independent portfolio project (not affiliated with MSU/Enviroweather)
Data Source: MAWN (publicly available data, used with permission)

This script builds and evaluates ARIMA and Prophet models for temperature forecasting.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Time series libraries
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import itertools

# Evaluation metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10

print("="*80)
print("PROJECT 1: MODEL BUILDING & EVALUATION")
print("="*80)

# Load processed data
daily_data = pd.read_csv('daily_weather_aetna.csv', parse_dates=['date'])

# Create splits
train_end = '2023-12-31'
val_end = '2024-12-31'

train_data = daily_data[daily_data['date'] <= train_end].copy()
val_data = daily_data[(daily_data['date'] > train_end) & (daily_data['date'] <= val_end)].copy()
test_data = daily_data[daily_data['date'] > val_end].copy()

# ============================================================================
# SECTION 5: ARIMA MODEL DEVELOPMENT
# ============================================================================

print("\n" + "="*80)
print("SECTION 5: ARIMA MODEL DEVELOPMENT")
print("="*80)

print("\n[5.1] ARIMA Parameter Selection via Grid Search")
print("-" * 80)
print("Strategy: Test multiple (p,d,q) combinations and select based on AIC")

# Prepare time series
temp_train = train_data.set_index('date')['atmp_mean']
temp_val = val_data.set_index('date')['atmp_mean']
temp_test = test_data.set_index('date')['atmp_mean']

# Grid search for ARIMA parameters
p_values = [0, 1, 2, 3, 5]
d_values = [1]  # From stationarity test
q_values = [0, 1, 2, 3, 5]

best_aic = np.inf
best_params = None
results_grid = []

print("\nTesting parameter combinations...")
print("(This may take a few minutes...)")

for p, d, q in itertools.product(p_values, d_values, q_values):
    try:
        model = ARIMA(temp_train, order=(p, d, q))
        fitted_model = model.fit()
        aic = fitted_model.aic
        results_grid.append({'p': p, 'd': d, 'q': q, 'AIC': aic})
        
        if aic < best_aic:
            best_aic = aic
            best_params = (p, d, q)
        
        if (p + q) % 3 == 0:  # Print progress every few iterations
            print(f"  Tested ARIMA({p},{d},{q}): AIC = {aic:.2f}")
            
    except Exception as e:
        continue

print(f"\n Grid search completed")
print(f" Best parameters: ARIMA{best_params}")
print(f" Best AIC: {best_aic:.2f}")

# Show top 5 models
results_df = pd.DataFrame(results_grid).sort_values('AIC').head(10)
print("\nTop 10 ARIMA models by AIC:")
print(results_df.to_string(index=False))

print("\n[5.2] Training Final ARIMA Model")
print("-" * 80)

# Train final model with best parameters
arima_model = ARIMA(temp_train, order=best_params)
arima_fitted = arima_model.fit()

print(f" ARIMA{best_params} model trained")
print(f"\nModel Summary:")
print(arima_fitted.summary())

print("\n[5.3] ARIMA Forecasting - Validation Set")
print("-" * 80)

# Forecast on validation set
n_val = len(val_data)
arima_forecast_val = arima_fitted.forecast(steps=n_val)

# Calculate metrics
mae_val = mean_absolute_error(temp_val, arima_forecast_val)
rmse_val = np.sqrt(mean_squared_error(temp_val, arima_forecast_val))
mape_val = mean_absolute_percentage_error(temp_val, arima_forecast_val) * 100

print(f" Validation Set Performance:")
print(f"  - MAE:  {mae_val:.3f}degC")
print(f"  - RMSE: {rmse_val:.3f}degC")
print(f"  - MAPE: {mape_val:.2f}%")

print("\n[5.4] ARIMA Forecasting - Test Set")
print("-" * 80)

# Retrain on train+val for test set prediction
temp_train_full = pd.concat([temp_train, temp_val])
arima_model_full = ARIMA(temp_train_full, order=best_params)
arima_fitted_full = arima_model_full.fit()

# Forecast on test set
n_test = len(test_data)
arima_forecast_test = arima_fitted_full.forecast(steps=n_test)

# Calculate metrics
mae_test = mean_absolute_error(temp_test, arima_forecast_test)
rmse_test = np.sqrt(mean_squared_error(temp_test, arima_forecast_test))
mape_test = mean_absolute_percentage_error(temp_test, arima_forecast_test) * 100

print(f" Test Set Performance:")
print(f"  - MAE:  {mae_test:.3f}degC")
print(f"  - RMSE: {rmse_test:.3f}degC")
print(f"  - MAPE: {mape_test:.2f}%")

# ============================================================================
# SECTION 6: PROPHET MODEL DEVELOPMENT
# ============================================================================

print("\n" + "="*80)
print("SECTION 6: PROPHET MODEL DEVELOPMENT")
print("="*80)

print("\n[6.1] Preparing Data for Prophet")
print("-" * 80)
print("Prophet requires columns: 'ds' (date) and 'y' (value)")

# Prepare Prophet dataframes
prophet_train = train_data[['date', 'atmp_mean']].rename(columns={'date': 'ds', 'atmp_mean': 'y'})
prophet_val = val_data[['date', 'atmp_mean']].rename(columns={'date': 'ds', 'atmp_mean': 'y'})
prophet_test = test_data[['date', 'atmp_mean']].rename(columns={'date': 'ds', 'atmp_mean': 'y'})

print(f" Prophet training data: {len(prophet_train)} days")

print("\n[6.2] Training Prophet Model")
print("-" * 80)
print("Configuration:")
print("  - Yearly seasonality: Auto")
print("  - Weekly seasonality: Auto")
print("  - Daily seasonality: False (using daily data)")
print("  - Changepoint prior scale: 0.05 (default)")

# Initialize and train Prophet model
prophet_model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05,
    interval_width=0.95
)

prophet_model.fit(prophet_train)
print(" Prophet model trained")

print("\n[6.3] Prophet Forecasting - Validation Set")
print("-" * 80)

# Create future dataframe for validation
future_val = prophet_model.make_future_dataframe(periods=n_val, freq='D')
prophet_forecast_val = prophet_model.predict(future_val)

# Extract validation predictions
prophet_pred_val = prophet_forecast_val.iloc[-n_val:]['yhat'].values

# Calculate metrics
mae_prophet_val = mean_absolute_error(temp_val, prophet_pred_val)
rmse_prophet_val = np.sqrt(mean_squared_error(temp_val, prophet_pred_val))
mape_prophet_val = mean_absolute_percentage_error(temp_val, prophet_pred_val) * 100

print(f" Validation Set Performance:")
print(f"  - MAE:  {mae_prophet_val:.3f}degC")
print(f"  - RMSE: {rmse_prophet_val:.3f}degC")
print(f"  - MAPE: {mape_prophet_val:.2f}%")

print("\n[6.4] Prophet Forecasting - Test Set")
print("-" * 80)

# Retrain on train+val
prophet_train_full = pd.concat([prophet_train, prophet_val])
prophet_model_full = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05,
    interval_width=0.95
)
prophet_model_full.fit(prophet_train_full)

# Forecast test set
future_test = prophet_model_full.make_future_dataframe(periods=n_test, freq='D')
prophet_forecast_test = prophet_model_full.predict(future_test)

# Extract test predictions
prophet_pred_test = prophet_forecast_test.iloc[-n_test:]['yhat'].values

# Calculate metrics
mae_prophet_test = mean_absolute_error(temp_test, prophet_pred_test)
rmse_prophet_test = np.sqrt(mean_squared_error(temp_test, prophet_pred_test))
mape_prophet_test = mean_absolute_percentage_error(temp_test, prophet_pred_test) * 100

print(f" Test Set Performance:")
print(f"  - MAE:  {mae_prophet_test:.3f}degC")
print(f"  - RMSE: {rmse_prophet_test:.3f}degC")
print(f"  - MAPE: {mape_prophet_test:.2f}%")

# ============================================================================
# SECTION 7: BASELINE MODEL (PERSISTENCE)
# ============================================================================

print("\n" + "="*80)
print("SECTION 7: BASELINE MODEL (PERSISTENCE)")
print("="*80)
print("Persistence model: Tomorrow's temperature = Today's temperature")

# Validation set baseline
baseline_pred_val = temp_train.iloc[-1:].values[0]  # Last training value
baseline_pred_val = np.full(n_val, baseline_pred_val)

mae_baseline_val = mean_absolute_error(temp_val, baseline_pred_val)
rmse_baseline_val = np.sqrt(mean_squared_error(temp_val, baseline_pred_val))
mape_baseline_val = mean_absolute_percentage_error(temp_val, baseline_pred_val) * 100

print(f"\n Validation Set Performance:")
print(f"  - MAE:  {mae_baseline_val:.3f}degC")
print(f"  - RMSE: {rmse_baseline_val:.3f}degC")
print(f"  - MAPE: {mape_baseline_val:.2f}%")

# Test set baseline
baseline_pred_test = temp_train_full.iloc[-1:].values[0]
baseline_pred_test = np.full(n_test, baseline_pred_test)

mae_baseline_test = mean_absolute_error(temp_test, baseline_pred_test)
rmse_baseline_test = np.sqrt(mean_squared_error(temp_test, baseline_pred_test))
mape_baseline_test = mean_absolute_percentage_error(temp_test, baseline_pred_test) * 100

print(f"\n Test Set Performance:")
print(f"  - MAE:  {mae_baseline_test:.3f}degC")
print(f"  - RMSE: {rmse_baseline_test:.3f}degC")
print(f"  - MAPE: {mape_baseline_test:.2f}%")

# ============================================================================
# SECTION 8: MODEL COMPARISON
# ============================================================================

print("\n" + "="*80)
print("SECTION 8: MODEL COMPARISON")
print("="*80)

# Create comparison dataframe
comparison_results = pd.DataFrame({
    'Model': ['ARIMA', 'Prophet', 'Baseline (Persistence)'],
    'Val_MAE': [mae_val, mae_prophet_val, mae_baseline_val],
    'Val_RMSE': [rmse_val, rmse_prophet_val, rmse_baseline_val],
    'Val_MAPE': [mape_val, mape_prophet_val, mape_baseline_val],
    'Test_MAE': [mae_test, mae_prophet_test, mae_baseline_test],
    'Test_RMSE': [rmse_test, rmse_prophet_test, rmse_baseline_test],
    'Test_MAPE': [mape_test, mape_prophet_test, mape_baseline_test]
})

print("\nModel Performance Comparison:")
print(comparison_results.to_string(index=False))

# Save results
comparison_results.to_csv('model_comparison_results.csv', index=False)
print("\n Saved: model_comparison_results.csv")

# Determine best model
best_model_idx = comparison_results['Test_MAE'].idxmin()
best_model_name = comparison_results.loc[best_model_idx, 'Model']
print(f"\n Best Model (by Test MAE): {best_model_name}")

# ============================================================================
# SECTION 9: VISUALIZATION OF FORECASTS
# ============================================================================

print("\n" + "="*80)
print("SECTION 9: FORECAST VISUALIZATIONS")
print("="*80)

# Plot 1: Test set forecasts comparison
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Full view
axes[0].plot(test_data['date'], temp_test.values, label='Actual', linewidth=2, color='black')
axes[0].plot(test_data['date'], arima_forecast_test, label=f'ARIMA{best_params}', linewidth=2, alpha=0.8)
axes[0].plot(test_data['date'], prophet_pred_test, label='Prophet', linewidth=2, alpha=0.8)
axes[0].plot(test_data['date'], baseline_pred_test, label='Baseline', linewidth=2, alpha=0.6, linestyle='--')
axes[0].set_ylabel('Temperature (degC)')
axes[0].set_title('Temperature Forecast Comparison - Test Set (2025)', fontsize=12, fontweight='bold')
axes[0].legend(loc='best')
axes[0].grid(True, alpha=0.3)

# Zoomed view - first 30 days
zoom_days = 30
axes[1].plot(test_data['date'][:zoom_days], temp_test.values[:zoom_days], 
             label='Actual', linewidth=2, color='black', marker='o')
axes[1].plot(test_data['date'][:zoom_days], arima_forecast_test[:zoom_days], 
             label=f'ARIMA{best_params}', linewidth=2, alpha=0.8, marker='s')
axes[1].plot(test_data['date'][:zoom_days], prophet_pred_test[:zoom_days], 
             label='Prophet', linewidth=2, alpha=0.8, marker='^')
axes[1].set_ylabel('Temperature (degC)')
axes[1].set_xlabel('Date')
axes[1].set_title(f'Zoomed View - First {zoom_days} Days', fontsize=12, fontweight='bold')
axes[1].legend(loc='best')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/04_forecast_comparison.png', dpi=300, bbox_inches='tight')
print(" Saved: figures/04_forecast_comparison.png")
plt.close()

# Plot 2: Residual analysis
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ARIMA residuals
arima_residuals = temp_test.values - arima_forecast_test
axes[0, 0].plot(test_data['date'], arima_residuals, marker='o', linestyle='-', alpha=0.7)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_ylabel('Residual (degC)')
axes[0, 0].set_title(f'ARIMA{best_params} Residuals', fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(arima_residuals, bins=30, alpha=0.7, edgecolor='black')
axes[0, 1].axvline(x=0, color='r', linestyle='--')
axes[0, 1].set_xlabel('Residual (degC)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title(f'ARIMA{best_params} Residual Distribution', fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

# Prophet residuals
prophet_residuals = temp_test.values - prophet_pred_test
axes[1, 0].plot(test_data['date'], prophet_residuals, marker='o', linestyle='-', alpha=0.7, color='orange')
axes[1, 0].axhline(y=0, color='r', linestyle='--')
axes[1, 0].set_ylabel('Residual (degC)')
axes[1, 0].set_xlabel('Date')
axes[1, 0].set_title('Prophet Residuals', fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].hist(prophet_residuals, bins=30, alpha=0.7, edgecolor='black', color='orange')
axes[1, 1].axvline(x=0, color='r', linestyle='--')
axes[1, 1].set_xlabel('Residual (degC)')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Prophet Residual Distribution', fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/05_residual_analysis.png', dpi=300, bbox_inches='tight')
print(" Saved: figures/05_residual_analysis.png")
plt.close()

# Plot 3: Model performance comparison
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(comparison_results))
width = 0.25

ax.bar(x - width, comparison_results['Test_MAE'], width, label='MAE (degC)', alpha=0.8)
ax.bar(x, comparison_results['Test_RMSE'], width, label='RMSE (degC)', alpha=0.8)
ax.bar(x + width, comparison_results['Test_MAPE']/10, width, label='MAPE/10 (%)', alpha=0.8)

ax.set_xlabel('Model')
ax.set_ylabel('Error Metric')
ax.set_title('Model Performance Comparison - Test Set', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(comparison_results['Model'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('figures/06_model_performance_comparison.png', dpi=300, bbox_inches='tight')
print(" Saved: figures/06_model_performance_comparison.png")
plt.close()

print("\n" + "="*80)
print("CHECKPOINT: Model building and evaluation completed")
print("="*80)
print(f" ARIMA{best_params} model: MAE = {mae_test:.3f}degC")
print(f" Prophet model: MAE = {mae_prophet_test:.3f}degC")
print(f" Best model: {best_model_name}")
print(f" Visualizations: 3 additional figures saved")
print("\nReady to proceed to alert system simulation...")
print("="*80)

