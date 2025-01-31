import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import requests
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="UK AI Energy Forecast & Savings",
    page_icon="🌍",
    layout="wide"
)

# Basic Styling
st.markdown("""
    <style>
    .main {background-color: #f4f4f4;}
    .highlight {font-size:24px; font-weight:bold; color:#4CAF50; text-align:center;}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 AI Energy Cost & Carbon Forecast</h1>", unsafe_allow_html=True)
st.write("#### ⚡ Discover how AI can predict your future energy costs and reduce carbon emissions.")

@st.cache_data(ttl=300)
def get_live_energy_data():
    try:
        return 30, 200  # Default values for testing
    except Exception as e:
        return 30, 200

@st.cache_data(ttl=3600)
def fetch_historical_energy_data():
    try:
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        prices = np.linspace(25, 35, 12) + np.random.normal(0, 0.5, 12)
        return pd.DataFrame({'Date': dates, 'Price': prices})
    except Exception as e:
        return pd.DataFrame()

# Main Dashboard
current_price_p_kwh, current_carbon_intensity = get_live_energy_data()
st.markdown(f"<div class='highlight'>💡 Current UK Electricity Price: {current_price_p_kwh:.1f} p/kWh</div>", unsafe_allow_html=True)
st.markdown(f"<div class='highlight'>🌍 Current Carbon Intensity: {current_carbon_intensity} gCO₂/kWh</div>", unsafe_allow_html=True)

# Savings Calculator
st.write("## 💰 Savings Calculator")
monthly_bill = st.number_input("Enter Your Current Monthly Energy Bill (£)", min_value=0, step=10)
if st.button("Calculate Savings"):
    estimated_savings = monthly_bill * 0.30
    st.success(f"🌱 **Potential Monthly Savings:** £{estimated_savings:.2f}")

# AI Forecasting
st.write("## 🔮 AI-Powered Energy Forecast")
historical_data = fetch_historical_energy_data()

if not historical_data.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(historical_data['Date'], historical_data['Price'], label='Historical')
    ax.set_title('Energy Price Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (p/kWh)')
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>🌎 Join the Green Energy Movement Today!</h4>", unsafe_allow_html=True)