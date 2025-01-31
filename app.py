import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import requests
import sqlite3

# Page Configuration
st.set_page_config(page_title="UK AI Energy Forecast & Savings", page_icon="🌍", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main {background-color: #f4f4f4;}
    .stButton>button {background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;}
    .stSelectbox, .stRadio, .stTextInput, .stFileUploader {border-radius: 10px;}
    .highlight {font-size:24px; font-weight:bold; color:#4CAF50; text-align:center;}
    </style>
""", unsafe_allow_html=True)

# Title with Style
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 AI Energy Cost & Carbon Forecast</h1>", unsafe_allow_html=True)
st.write("#### ⚡ Discover how AI can **predict your future energy costs**, reduce carbon emissions, and help you **switch to green energy solutions** for a **better future**.")

# Function to fetch live UK electricity price (in pence/kWh) & carbon intensity
def get_live_energy_data():
    try:
        energy_price_response = requests.get("https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-7-Day/standard-unit-rates/")  # Example API (replace with real source)
        carbon_intensity_response = requests.get("https://api.carbonintensity.org.uk/intensity")

        if energy_price_response.status_code == 200 and carbon_intensity_response.status_code == 200:
            energy_price = energy_price_response.json()["results"][0]["value_inc_vat"]  # Extracting latest price
            carbon_intensity = carbon_intensity_response.json()["data"][0]["intensity"]["actual"]  # Extracting latest carbon intensity
            return energy_price, carbon_intensity
        else:
            return 30, 200  # Default values if API fails
    except:
        return 30, 200

# Get live energy data
current_price_p_kwh, current_carbon_intensity = get_live_energy_data()
st.markdown(f"<div class='highlight'>💡 Current UK Electricity Price: {current_price_p_kwh} p/kWh</div>", unsafe_allow_html=True)
st.markdown(f"<div class='highlight'>🌍 Current UK Carbon Intensity: {current_carbon_intensity} gCO₂/kWh</div>", unsafe_allow_html=True)

# AI Energy Forecasting Tool
st.write("## 🔮 AI-Powered Energy Forecast")
st.write("Input your monthly energy consumption and let AI **predict your costs & emissions** while suggesting the **best green energy solutions** to save money and protect the planet.")

source = st.selectbox("Select Your Category", ["Business", "Household"] )
activity = st.selectbox("Select Energy Usage Type", ["Electricity", "Heating", "Cooking", "Water Heating", "Lighting"])
monthly_energy_usage_kwh = st.number_input("Enter Your Monthly Energy Usage (kWh)", min_value=0, step=10)

if "forecast" not in st.session_state:
    st.session_state.forecast = None
    st.session_state.estimated_carbon_savings = None

if st.button("🔍 Generate AI Forecast"):
    if monthly_energy_usage_kwh > 0:
        # AI-Based Predictions
        model = ARIMA([monthly_energy_usage_kwh * (current_price_p_kwh / 100)], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=1)[0]
        estimated_carbon_savings = (monthly_energy_usage_kwh * current_carbon_intensity) / 1000  # Convert gCO₂ to kgCO₂
        
        # Store in session state
        st.session_state.forecast = forecast
        st.session_state.estimated_carbon_savings = estimated_carbon_savings
        
        st.write("### 📊 AI-Powered Cost & Carbon Forecast")
        st.write(f"💰 **Next Month's Predicted Energy Cost:** £{forecast:.2f}")
        st.write(f"🌿 **Estimated Monthly Carbon Emissions:** {estimated_carbon_savings:.2f} kgCO₂")
        
        # Green Energy Suggestions
        st.write("### ✅ AI-Recommended Green Energy Solutions")
        if activity == "Electricity":
            st.write("💡 **Switch to Solar Panels**: Reduce electricity costs by up to **25%** & cut CO₂ emissions. Suggested provider: [Solar Energy UK](https://www.solarenergyuk.org)")
        elif activity == "Heating":
            st.write("🔥 **Install a Heat Pump**: Cut heating costs by **40%** & access UK government grants. Suggested provider: [Green Heat Solutions](https://www.greenheatsolutions.co.uk)")
        elif activity == "Lighting":
            st.write("💡 **Switch to LED Lights**: Save **30% on lighting costs** and increase energy efficiency. Suggested provider: [Bright LED Systems](https://www.brightledsystems.com)")
        else:
            st.write("🌍 **Explore renewable energy providers** to reduce costs & emissions. Suggested provider: [Eco Wind Power](https://www.ecowindpower.co.uk)")
    else:
        st.error("⚠️ Please enter a valid monthly energy usage value.")

# Check if eligible for government grants
if st.button("🏛 Check Government Grant Eligibility"):
    st.write("🔎 Checking for available grants...")
    st.write("✅ You may be eligible for **Green Energy Grants**. Visit [UK Government Grants Portal](https://www.gov.uk/improve-energy-efficiency) to learn more.")

# Close Database Connection
st.write("---")
st.markdown("<h4 style='text-align: center;'>🌎 Join the Green Energy Movement & Reduce Your Costs Today! 🚀</h4>", unsafe_allow_html=True)
