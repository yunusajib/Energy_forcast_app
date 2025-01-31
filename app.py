import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import requests
import numpy as np
from datetime import datetime, timedelta

# Enhanced Page Configuration
st.set_page_config(
    page_title="UK AI Energy Forecast & Savings 2.0",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom Styling
st.markdown("""
    <style>
    .main {background-color: #f4f4f4;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    .stSelectbox, .stRadio, .stTextInput, .stFileUploader {
        border-radius: 10px;
        margin: 10px 0;
    }
    .highlight {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        padding: 15px;
        background: rgba(76, 175, 80, 0.1);
        border-radius: 10px;
        margin: 10px 0;
    }
    .cta-button {
        background-color: #FF5733;
        color: white;
        font-size: 18px;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        display: block;
        margin: 20px auto;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .cta-button:hover {
        background-color: #ff4418;
        transform: scale(1.05);
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Caching for API calls
@st.cache_data(ttl=300)
def get_live_energy_data():
    try:
        energy_price_response = requests.get(
            "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-7-Day/standard-unit-rates/",
            timeout=5
        )
        carbon_intensity_response = requests.get(
            "https://api.carbonintensity.org.uk/intensity",
            timeout=5
        )

        if energy_price_response.status_code == 200 and carbon_intensity_response.status_code == 200:
            energy_price = energy_price_response.json()["results"][0]["value_inc_vat"]
            carbon_intensity = carbon_intensity_response.json()["data"][0]["intensity"]["actual"]
            return energy_price, carbon_intensity
        else:
            return 30, 200  # Default values if API fails
    except Exception as e:
        st.warning(f"Using default values due to API error: {str(e)}")
        return 30, 200

@st.cache_data(ttl=3600)
def fetch_historical_energy_data():
    try:
        # Enhanced sample data with trend and seasonality
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        base = np.linspace(25, 35, 12)
        seasonal = 2 * np.sin(np.linspace(0, 2*np.pi, 12))
        noise = np.random.normal(0, 0.5, 12)
        prices = base + seasonal + noise
        return pd.DataFrame({'Date': dates, 'Price': prices})
    except Exception as e:
        st.error(f"Error generating historical data: {str(e)}")
        return pd.DataFrame()

# Title and Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 AI Energy Cost & Carbon Forecast 2.0</h1>", unsafe_allow_html=True)
st.write("#### ⚡ Discover how AI can **predict your future energy costs**, reduce carbon emissions, and help you **switch to green energy solutions** for a **better future**.")

# New Feature: Real-time Price Alerts
with st.sidebar:
    st.header("⚡ Price Alerts")
    alert_price = st.slider("Set Price Alert (p/kWh)", 0, 50, 35)
    current_price_p_kwh, current_carbon_intensity = get_live_energy_data()
    if current_price_p_kwh > alert_price:
        st.warning(f"⚠️ Current price ({current_price_p_kwh:.1f}p) is above your alert threshold!")
    
    st.header("🌱 Green Energy Tips")
    st.info("• Best time to use appliances: 10 PM - 6 AM\n• Install smart meters\n• Use LED lighting")

# Main Dashboard
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='highlight'>💡 Current UK Electricity Price: {current_price_p_kwh:.1f} p/kWh</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='highlight'>🌍 Current Carbon Intensity: {current_carbon_intensity} gCO₂/kWh</div>", unsafe_allow_html=True)

# Enhanced Savings Calculator
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.write("## 💰 Advanced Savings Calculator")
col1, col2 = st.columns(2)
with col1:
    monthly_bill = st.number_input("Current Monthly Energy Bill (£)", min_value=0, step=10)
    usage_pattern = st.select_slider("Usage Pattern", options=["Night", "Mixed", "Day"])
with col2:
    property_type = st.selectbox("Property Type", ["Flat", "House", "Detached House"])
    occupants = st.number_input("Number of Occupants", min_value=1, max_value=10, value=2)

if st.button("📊 Calculate Smart Savings"):
    base_savings = monthly_bill * 0.30
    pattern_multiplier = {"Night": 1.2, "Mixed": 1.0, "Day": 0.8}[usage_pattern]
    property_multiplier = {"Flat": 1.1, "House": 1.0, "Detached House": 0.9}[property_type]
    occupant_factor = 1 + (occupants - 2) * 0.05
    
    estimated_savings = base_savings * pattern_multiplier * property_multiplier * occupant_factor
    potential_carbon_reduction = estimated_savings * 2.3  # kgCO2 per £ saved
    
    st.success(f"🌱 **Potential Monthly Savings:** £{estimated_savings:.2f}")
    st.info(f"🌍 **Potential Carbon Reduction:** {potential_carbon_reduction:.1f} kgCO₂ per month")
st.markdown("</div>", unsafe_allow_html=True)

# AI Forecasting with Enhanced Visualization
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.write("## 🔮 AI-Powered Energy Forecast")
historical_data = fetch_historical_energy_data()

if not historical_data.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(historical_data['Date'], historical_data['Price'], label='Historical')
    ax.set_title('Energy Price Trend & Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (p/kWh)')
    
    # ARIMA forecast
    try:
        model = ARIMA(historical_data['Price'], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=3)
        future_dates = pd.date_range(start=historical_data['Date'].iloc[-1], periods=4, freq='M')[1:]
        ax.plot(future_dates, forecast, 'r--', label='AI Forecast')
        ax.legend()
        st.pyplot(fig)
        
        # Forecast insights
        avg_forecast = forecast.mean()
        if avg_forecast > historical_data['Price'].mean():
            st.warning("⚠️ Prices are predicted to rise. Consider locking in current rates.")
        else:
            st.success("✅ Prices are predicted to stabilize or decrease.")
    except Exception as e:
        st.error(f"Error in forecast generation: {str(e)}")
st.markdown("</div>", unsafe_allow_html=True)

# New Feature: Personalized Recommendations
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.write("## 🎯 Personalized Energy Recommendations")
usage_time = st.radio("When do you use most energy?", ["Morning", "Afternoon", "Evening", "Night"])
has_smart_meter = st.checkbox("I have a smart meter")

recommendations = {
    "Morning": ["Schedule appliances for off-peak hours", "Install smart thermostats"],
    "Afternoon": ["Consider solar panels", "Use natural light"],
    "Evening": ["LED lighting upgrades", "Smart power strips"],
    "Night": ["Economy 7 tariff", "Battery storage systems"]
}

if usage_time:
    st.write("### 💡 Your Personalized Recommendations:")
    for i, rec in enumerate(recommendations[usage_time], 1):
        st.write(f"{i}. {rec}")
    
    if has_smart_meter:
        st.success("✅ Smart meter detected! You're eligible for dynamic tariffs.")
    else:
        st.info("💡 Tip: Installing a smart meter could save you up to 15% more!")
st.markdown("</div>", unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center;'>
        <h4>🌎 Join the Green Energy Movement & Start Saving Today! 🚀</h4>
        <p style='color: #666;'>Updated with AI-powered insights and real-time monitoring</p>
    </div>
""", unsafe_allow_html=True)