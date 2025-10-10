"""
Weather Forecasting & Alert System Dashboard
=============================================

Interactive Streamlit application demonstrating time-series forecasting
models (ARIMA, Prophet) and automated agricultural alert system.

Author: Jae Mwangi
Data Source: Michigan Automated Weather Network (MAWN), operated by Enviroweather at Michigan State University
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
 page_title="Weather Forecasting & Alert System",
 page_icon="",
 layout="wide",
 initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
 .main-header {
 font-size: 2.5rem;
 font-weight: bold;
 color: #1f77b4;
 text-align: center;
 margin-bottom: 1rem;
 }
 .sub-header {
 font-size: 1.2rem;
 color: #555;
 text-align: center;
 margin-bottom: 2rem;
 }
 .metric-card {
 background-color: #f0f2f6;
 padding: 1rem;
 border-radius: 0.5rem;
 border-left: 4px solid #1f77b4;
 }
 .alert-high {
 background-color: #ffebee;
 padding: 0.5rem;
 border-radius: 0.3rem;
 border-left: 4px solid #f44336;
 margin: 0.5rem 0;
 }
 .alert-medium {
 background-color: #fff3e0;
 padding: 0.5rem;
 border-radius: 0.3rem;
 border-left: 4px solid #ff9800;
 margin: 0.5rem 0;
 }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
 """Load processed data and results"""
 daily_data = pd.read_csv('daily_weather_aetna.csv', parse_dates=['date'])
 model_comparison = pd.read_csv('model_comparison_results.csv')
 alerts = pd.read_csv('generated_alerts.csv', parse_dates=['date'])
 return daily_data, model_comparison, alerts

# Load data
try:
 daily_data, model_comparison, alerts = load_data()
 data_loaded = True
except Exception as e:
 st.error(f"Error loading data: {e}")
 st.info("Please ensure all data files are in the same directory as this app.")
 data_loaded = False
 st.stop()

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=MAWN+Forecasting", use_container_width=True)
st.sidebar.title(" Navigation")

page = st.sidebar.radio(
 "Select Page",
 [" Overview", " Model Performance", " Alert System", " Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About This Project")
st.sidebar.info(
 """
 This dashboard demonstrates time-series forecasting models (ARIMA, Prophet) 
 and an automated alert system for agricultural decision-making.
 
 **Data Source:** Michigan Automated Weather Network (MAWN), operated by Enviroweather at Michigan State University 
 **Station:** Aetna 
 **Period:** 2019-2025
 """
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ‍ Developer")
st.sidebar.markdown("**Jae Mwangi**")
st.sidebar.markdown("Data Scientist | Michigan State University")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/jae-m-9a492636/) | [GitHub](https://github.com/Jae15) | [Portfolio](TBD)")

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================

if page == " Overview":
 st.markdown('<div class="main-header"> Weather Forecasting & Alert System</div>', unsafe_allow_html=True)
 st.markdown('<div class="sub-header">Time-Series Models for Agricultural Decision Support</div>', unsafe_allow_html=True)
 
 # Key metrics
 col1, col2, col3, col4 = st.columns(4)
 
 with col1:
 st.metric(
 label=" Data Points",
 value=f"{len(daily_data):,}",
 delta="Daily records"
 )
 
 with col2:
 st.metric(
 label=" Best Model MAE",
 value="3.56°C",
 delta="Prophet model"
 )
 
 with col3:
 st.metric(
 label=" Alerts Generated",
 value=len(alerts),
 delta="Test period"
 )
 
 with col4:
 st.metric(
 label="⏰ Avg Lead Time",
 value=f"{alerts['lead_time_days'].mean():.1f} days",
 delta="Early warning"
 )
 
 st.markdown("---")
 
 # Project overview
 col1, col2 = st.columns([2, 1])
 
 with col1:
 st.markdown("### Project Overview")
 st.markdown("""
 This project demonstrates the development and deployment of **time-series forecasting models** 
 to predict weather patterns and enable **automated agricultural alerts**. The system supports 
 farmers in making critical decisions about crop planning, pest management, and resource allocation.
 
 **Key Features:**
 - Multiple forecasting models (ARIMA, Prophet, Baseline)
 - Multi-variable predictions (temperature, humidity, precipitation)
 - Automated alert generation based on agricultural thresholds
 - Interactive visualizations and model comparisons
 - Real-time risk assessment for frost, heat, and disease
 
 **Technical Stack:**
 - Python (Pandas, NumPy, Scikit-learn)
 - Time-series: ARIMA (statsmodels), Prophet (Facebook)
 - Visualization: Matplotlib, Seaborn, Plotly
 - Dashboard: Streamlit
 """)
 
 with col2:
 st.markdown("### Resume Alignment")
 st.markdown("""
 <div class="metric-card">
 <strong>Enviroweather Experience:</strong><br><br>
 "Built time-series forecasting models (ARIMA, Prophet) to predict weather and 
 pest trends, enabling automated alerts that supported 1,000+ farmers in planning 
 crops and pest management."
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("### Data Quality")
 st.markdown("""
 - **Source:** MAWN QC Database
 - **Quality:** 99.96% complete
 - **Validation:** MAWN flags
 - **Period:** 6+ years
 """)
 
 st.markdown("---")
 
 # Temperature time series overview
 st.markdown("### Temperature Time Series Overview")
 
 fig = go.Figure()
 
 fig.add_trace(go.Scatter(
 x=daily_data['date'],
 y=daily_data['atmp_mean'],
 mode='lines',
 name='Mean Temperature',
 line=dict(color='steelblue', width=1),
 fill='tonexty'
 ))
 
 fig.add_trace(go.Scatter(
 x=daily_data['date'],
 y=daily_data['atmp_max'],
 mode='lines',
 name='Max Temperature',
 line=dict(color='red', width=1, dash='dot'),
 opacity=0.5
 ))
 
 fig.add_trace(go.Scatter(
 x=daily_data['date'],
 y=daily_data['atmp_min'],
 mode='lines',
 name='Min Temperature',
 line=dict(color='blue', width=1, dash='dot'),
 opacity=0.5
 ))
 
 fig.update_layout(
 title="Daily Temperature Patterns (2019-2025)",
 xaxis_title="Date",
 yaxis_title="Temperature (°C)",
 hovermode='x unified',
 height=400
 )
 
 st.plotly_chart(fig, use_container_width=True)
 
 # Quick stats
 col1, col2, col3 = st.columns(3)
 
 with col1:
 st.markdown("#### Coldest Day")
 coldest = daily_data.loc[daily_data['atmp_min'].idxmin()]
 st.write(f"**{coldest['date'].strftime('%Y-%m-%d')}**")
 st.write(f"Temperature: {coldest['atmp_min']:.1f}°C")
 
 with col2:
 st.markdown("#### Hottest Day")
 hottest = daily_data.loc[daily_data['atmp_max'].idxmax()]
 st.write(f"**{hottest['date'].strftime('%Y-%m-%d')}**")
 st.write(f"Temperature: {hottest['atmp_max']:.1f}°C")
 
 with col3:
 st.markdown("#### Wettest Day")
 wettest = daily_data.loc[daily_data['pcpn_sum'].idxmax()]
 st.write(f"**{wettest['date'].strftime('%Y-%m-%d')}**")
 st.write(f"Precipitation: {wettest['pcpn_sum']:.1f}mm")

# ============================================================================
# PAGE: MODEL PERFORMANCE
# ============================================================================

elif page == " Model Performance":
 st.markdown('<div class="main-header"> Model Performance Comparison</div>', unsafe_allow_html=True)
 
 # Model comparison table
 st.markdown("### Model Evaluation Metrics")
 
 # Format the comparison table
 comparison_display = model_comparison.copy()
 comparison_display.columns = ['Model', 'Val MAE', 'Val RMSE', 'Val MAPE', 'Test MAE', 'Test RMSE', 'Test MAPE']
 
 # Highlight best model
 def highlight_best(s):
 if s.name in ['Test MAE', 'Test RMSE', 'Test MAPE']:
 is_min = s == s.min()
 return ['background-color: #c8e6c9' if v else '' for v in is_min]
 return ['' for _ in s]
 
 styled_table = comparison_display.style.apply(highlight_best, axis=0).format({
 'Val MAE': '{:.3f}°C',
 'Val RMSE': '{:.3f}°C',
 'Val MAPE': '{:.2f}%',
 'Test MAE': '{:.3f}°C',
 'Test RMSE': '{:.3f}°C',
 'Test MAPE': '{:.2f}%'
 })
 
 st.dataframe(styled_table, use_container_width=True)
 
 st.info(" **Best Model: Prophet** - Achieved lowest MAE (3.56°C) on test set, significantly outperforming ARIMA and baseline models.")
 
 # Visual comparison
 col1, col2 = st.columns(2)
 
 with col1:
 st.markdown("### Test Set MAE Comparison")
 fig = go.Figure(data=[
 go.Bar(
 x=model_comparison['Model'],
 y=model_comparison['Test_MAE'],
 text=model_comparison['Test_MAE'].round(3),
 textposition='auto',
 marker_color=['#ff7f0e', '#2ca02c', '#d62728']
 )
 ])
 fig.update_layout(
 yaxis_title="MAE (°C)",
 height=400,
 showlegend=False
 )
 st.plotly_chart(fig, use_container_width=True)
 
 with col2:
 st.markdown("### Test Set RMSE Comparison")
 fig = go.Figure(data=[
 go.Bar(
 x=model_comparison['Model'],
 y=model_comparison['Test_RMSE'],
 text=model_comparison['Test_RMSE'].round(3),
 textposition='auto',
 marker_color=['#ff7f0e', '#2ca02c', '#d62728']
 )
 ])
 fig.update_layout(
 yaxis_title="RMSE (°C)",
 height=400,
 showlegend=False
 )
 st.plotly_chart(fig, use_container_width=True)
 
 st.markdown("---")
 
 # Model details
 st.markdown("### Model Details & Methodology")
 
 tab1, tab2, tab3 = st.tabs(["ARIMA", "Prophet", "Baseline"])
 
 with tab1:
 col1, col2 = st.columns([2, 1])
 with col1:
 st.markdown("""
 **ARIMA (AutoRegressive Integrated Moving Average)**
 
 ARIMA is a classical statistical model for time-series forecasting that combines:
 - **AR (p):** Autoregressive component - uses past values
 - **I (d):** Integrated component - differencing for stationarity
 - **MA (q):** Moving average component - uses past forecast errors
 
 **Model Configuration:**
 - Order: ARIMA(5, 1, 3)
 - Selected via grid search (AIC optimization)
 - First-order differencing applied (d=1)
 
 **Performance:**
 - Test MAE: 12.18°C
 - Test RMSE: 14.40°C
 
 **Limitations:**
 - Struggled to capture strong seasonal patterns
 - Better suited for short-term forecasts
 - Requires stationary data
 """)
 with col2:
 st.markdown("""
 **Key Parameters:**
 - p = 5 (AR order)
 - d = 1 (Differencing)
 - q = 3 (MA order)
 
 **Stationarity Test:**
 - ADF p-value: <0.001
 - Result: Stationary after differencing
 """)
 
 with tab2:
 col1, col2 = st.columns([2, 1])
 with col1:
 st.markdown("""
 **Prophet (Facebook's Time-Series Model)**
 
 Prophet is designed for business forecasting with strong seasonal patterns:
 - **Trend:** Flexible piecewise linear or logistic growth
 - **Seasonality:** Yearly, weekly, daily patterns (Fourier series)
 - **Holidays:** Special event effects
 - **Uncertainty:** Built-in confidence intervals
 
 **Model Configuration:**
 - Yearly seasonality: Enabled (captures annual patterns)
 - Weekly seasonality: Enabled (captures weekly variations)
 - Changepoint prior scale: 0.05 (default)
 - Interval width: 95%
 
 **Performance:**
 - Test MAE: 3.56°C 
 - Test RMSE: 4.61°C 
 
 **Advantages:**
 - Excellent at capturing seasonality
 - Robust to missing data
 - Intuitive parameter tuning
 - Provides uncertainty intervals
 """)
 with col2:
 st.markdown("""
 **Why Prophet Won:**
 - Strong seasonal patterns in data
 - Automatic seasonality detection
 - Robust to outliers
 - Better long-term forecasts
 
 **Best Use Cases:**
 - Agricultural planning
 - Multi-step ahead forecasts
 - Seasonal trend analysis
 """)
 
 with tab3:
 st.markdown("""
 **Baseline (Persistence Model)**
 
 The persistence model is a naive forecasting approach where tomorrow's value 
 equals today's value. It serves as a benchmark to validate that more complex 
 models provide meaningful improvements.
 
 **Method:**
 - Forecast = Last observed value
 - No learning or pattern recognition
 - Simple but effective for stable series
 
 **Performance:**
 - Test MAE: 12.09°C
 - Test RMSE: 14.28°C
 
 **Interpretation:**
 Both ARIMA and Prophet significantly outperform the baseline, with Prophet 
 achieving a **70% reduction in MAE** compared to persistence.
 """)

# ============================================================================
# PAGE: ALERT SYSTEM
# ============================================================================

elif page == " Alert System":
 st.markdown('<div class="main-header"> Automated Agricultural Alert System</div>', unsafe_allow_html=True)
 
 # Alert summary
 col1, col2, col3 = st.columns(3)
 
 with col1:
 st.metric("Total Alerts", len(alerts))
 with col2:
 high_severity = len(alerts[alerts['severity'] == 'HIGH'])
 st.metric("High Severity", high_severity, delta=f"{high_severity/len(alerts)*100:.1f}%")
 with col3:
 st.metric("Avg Lead Time", f"{alerts['lead_time_days'].mean():.1f} days")
 
 st.markdown("---")
 
 # Alert thresholds
 st.markdown("### Alert Threshold Configuration")
 
 col1, col2 = st.columns(2)
 
 with col1:
 st.markdown("""
 <div class="alert-high">
 <strong> FROST WARNING</strong><br>
 Condition: Temperature < 0°C<br>
 Severity: HIGH<br>
 Action: Cover sensitive crops, delay planting
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("""
 <div class="alert-high">
 <strong> HIGH DISEASE RISK</strong><br>
 Condition: Humidity > 90% AND Temp 15-25°C<br>
 Severity: HIGH<br>
 Action: Apply preventive fungicides, monitor closely
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("""
 <div class="alert-high">
 <strong> HEAVY RAIN</strong><br>
 Condition: Precipitation > 25mm<br>
 Severity: HIGH<br>
 Action: Check drainage, delay field operations
 </div>
 """, unsafe_allow_html=True)
 
 with col2:
 st.markdown("""
 <div class="alert-medium">
 <strong> HEAT STRESS</strong><br>
 Condition: Temperature > 30°C<br>
 Severity: MEDIUM<br>
 Action: Increase irrigation, monitor crop health
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("""
 <div class="alert-medium">
 <strong> MODERATE DISEASE RISK</strong><br>
 Condition: Humidity > 85% AND Temp 10-30°C<br>
 Severity: MEDIUM<br>
 Action: Increase scouting frequency
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("---")
 
 # Alert timeline
 st.markdown("### Alert Timeline")
 
 # Filter options
 col1, col2 = st.columns([3, 1])
 with col1:
 alert_types = ['All'] + list(alerts['type'].unique())
 selected_type = st.selectbox("Filter by Alert Type", alert_types)
 with col2:
 severity_filter = st.selectbox("Filter by Severity", ['All', 'HIGH', 'MEDIUM'])
 
 # Apply filters
 filtered_alerts = alerts.copy()
 if selected_type != 'All':
 filtered_alerts = filtered_alerts[filtered_alerts['type'] == selected_type]
 if severity_filter != 'All':
 filtered_alerts = filtered_alerts[filtered_alerts['severity'] == severity_filter]
 
 # Alert timeline visualization
 fig = go.Figure()
 
 for alert_type in filtered_alerts['type'].unique():
 subset = filtered_alerts[filtered_alerts['type'] == alert_type]
 fig.add_trace(go.Scatter(
 x=subset['date'],
 y=[alert_type] * len(subset),
 mode='markers',
 name=alert_type.replace('_', ' ').title(),
 marker=dict(size=12, symbol='diamond'),
 hovertemplate='<b>%{y}</b><br>Date: %{x}<br><extra></extra>'
 ))
 
 fig.update_layout(
 title=f"Alert Timeline ({len(filtered_alerts)} alerts)",
 xaxis_title="Date",
 yaxis_title="Alert Type",
 height=400,
 hovermode='closest'
 )
 
 st.plotly_chart(fig, use_container_width=True)
 
 # Recent alerts table
 st.markdown("### Recent Alerts (Last 20)")
 
 recent_alerts = filtered_alerts.sort_values('date', ascending=False).head(20)
 display_alerts = recent_alerts[['date', 'type', 'severity', 'message', 'lead_time_days']].copy()
 display_alerts.columns = ['Date', 'Type', 'Severity', 'Message', 'Lead Time (days)']
 display_alerts['Date'] = display_alerts['Date'].dt.strftime('%Y-%m-%d')
 display_alerts['Type'] = display_alerts['Type'].str.replace('_', ' ').str.title()
 
 st.dataframe(display_alerts, use_container_width=True, hide_index=True)
 
 # Download alerts
 csv = filtered_alerts.to_csv(index=False)
 st.download_button(
 label=" Download Alerts (CSV)",
 data=csv,
 file_name="agricultural_alerts.csv",
 mime="text/csv"
 )

# ============================================================================
# PAGE: DATA EXPLORER
# ============================================================================

elif page == " Data Explorer":
 st.markdown('<div class="main-header"> Data Explorer</div>', unsafe_allow_html=True)
 
 # Date range selector
 st.markdown("### Select Date Range")
 col1, col2 = st.columns(2)
 with col1:
 start_date = st.date_input("Start Date", daily_data['date'].min())
 with col2:
 end_date = st.date_input("End Date", daily_data['date'].max())
 
 # Filter data
 mask = (daily_data['date'] >= pd.to_datetime(start_date)) & (daily_data['date'] <= pd.to_datetime(end_date))
 filtered_data = daily_data[mask]
 
 st.info(f" Showing {len(filtered_data)} days of data")
 
 # Variable selector
 st.markdown("### Visualize Variables")
 
 variables = {
 'Temperature (Mean)': 'atmp_mean',
 'Temperature (Min)': 'atmp_min',
 'Temperature (Max)': 'atmp_max',
 'Relative Humidity (Mean)': 'relh_mean',
 'Precipitation': 'pcpn_sum',
 'Growing Degree Days': 'gdd',
 'Temperature Range': 'temp_range'
 }
 
 selected_vars = st.multiselect(
 "Select variables to plot",
 list(variables.keys()),
 default=['Temperature (Mean)', 'Precipitation']
 )
 
 if selected_vars:
 fig = make_subplots(
 rows=len(selected_vars),
 cols=1,
 subplot_titles=selected_vars,
 vertical_spacing=0.1
 )
 
 for i, var_name in enumerate(selected_vars, 1):
 var_col = variables[var_name]
 fig.add_trace(
 go.Scatter(
 x=filtered_data['date'],
 y=filtered_data[var_col],
 mode='lines',
 name=var_name,
 line=dict(width=2)
 ),
 row=i,
 col=1
 )
 
 fig.update_layout(height=300 * len(selected_vars), showlegend=False)
 st.plotly_chart(fig, use_container_width=True)
 
 st.markdown("---")
 
 # Statistics
 st.markdown("### Descriptive Statistics")
 
 stats_vars = [variables[v] for v in selected_vars] if selected_vars else list(variables.values())
 stats = filtered_data[stats_vars].describe().T
 stats.columns = ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max']
 st.dataframe(stats, use_container_width=True)
 
 # Raw data
 with st.expander(" View Raw Data"):
 st.dataframe(filtered_data, use_container_width=True)
 
 csv = filtered_data.to_csv(index=False)
 st.download_button(
 label=" Download Data (CSV)",
 data=csv,
 file_name="mawn_daily_data.csv",
 mime="text/csv"
 )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
 <p><strong>Weather Forecasting & Alert System Dashboard</strong></p>
 <p>Developed by Jae Mwangi | Data Scientist</p>
 <p>Data Source: Michigan Automated Weather Network (MAWN), operated by Enviroweather at Michigan State University | 2019-2025</p>
</div>
""", unsafe_allow_html=True)

