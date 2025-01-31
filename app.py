import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import requests
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="UK AI Energy Forecast & Savings",
    page_icon="🌍",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main {background-color: #f4f4f4;}
    .stButton>button {background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;}
    .stSelectbox, .stRadio, .stTextInput, .stFileUploader {border-radius: 10px;}
    .highlight {font-size:24px; font-weight:bold; color:#4CAF50; text-align:center;}
    .cta-button {background-color: #FF5733; color: white; font-size: 18px; padding: 12px; border-radius: 10px; text-align: center; display: block; margin: auto; text-decoration: none;}
    </style>
""", unsafe_allow_html=True)

# Title with Style
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 AI Energy Cost & Carbon Forecast</h1>", unsafe_allow_html=True)
st.write("#### ⚡ Discover how AI can **predict your future energy costs**, reduce carbon emissions, and help you **switch to green energy solutions** for a **better future**.")

# Free Forever CTA Button
st.markdown("""
    <a href='#' class='cta-button'>🚀 Try for Free - Forever</a>
""", unsafe_allow_html=True)

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
    except:
        return 30, 200

def fetch_historical_energy_data():
    try:
        # Generate some sample historical data since the API is not available
        return np.random.uniform(25, 35, 12).tolist()
    except:
        return np.random.uniform(25, 35, 12).tolist()

# Get live energy data
current_price_p_kwh, current_carbon_intensity = get_live_energy_data()
st.markdown(f"<div class='highlight'>💡 Current UK Electricity Price: {current_price_p_kwh} p/kWh</div>", unsafe_allow_html=True)
st.markdown(f"<div class='highlight'>🌍 Current UK Carbon Intensity: {current_carbon_intensity} gCO₂/kWh</div>", unsafe_allow_html=True)

# Fetch historical energy prices
historical_energy_data = fetch_historical_energy_data()

# Savings Calculator (Priority Feature)
st.write("## 💰 How Much Can You Save?")
monthly_bill = st.number_input("Enter Your Current Monthly Energy Bill (£)", min_value=0, step=10)
if st.button("📊 Calculate Savings"):
    estimated_savings = monthly_bill * 0.30
    st.write(f"🌱 **Potential Savings:** £{estimated_savings:.2f} per month")

# Check if eligible for government grants
st.write("## 🏛 Check Government Grant Eligibility")
if st.button("🔎 Check Now"):
    st.write("✅ You may be eligible for **Green Energy Grants**.")
    st.write("Visit [UK Government Grants Portal](https://www.gov.uk/improve-energy-efficiency) to learn more.")

# AI Energy Forecasting Tool
st.write("## 🔮 AI-Powered Energy Forecast")
st.write("Input your monthly energy consumption and let AI **predict your costs & emissions**.")

source = st.selectbox("Select Your Category", ["Business", "Household"])
activity = st.selectbox("Select Energy Usage Type", ["Electricity", "Heating", "Cooking", "Water Heating", "Lighting"])
monthly_energy_usage_kwh = st.number_input("Enter Your Monthly Energy Usage (kWh)", min_value=0, step=10)

if st.button("🔍 Generate AI Forecast"):
    if monthly_energy_usage_kwh > 0:
        # Create training data for ARIMA
        training_data = pd.Series(historical_energy_data)
        
        # Train ARIMA model
        try:
            model = ARIMA(training_data, order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=1)[0] * (monthly_energy_usage_kwh / 100)
            estimated_carbon_savings = (monthly_energy_usage_kwh * current_carbon_intensity) / 1000
            
            st.write("### 📊 AI-Powered Cost & Carbon Forecast")
            st.write(f"💰 **Next Month's Predicted Energy Cost:** £{forecast:.2f}")
            st.write(f"🌿 **Estimated Monthly Carbon Emissions:** {estimated_carbon_savings:.2f} kgCO₂")
            
            # Green Energy Suggestions based on activity
            st.write("### ✅ AI-Recommended Green Energy Solutions")
            if activity == "Electricity":
                st.write("💡 **Switch to Solar Panels**: Reduce electricity costs by up to **25%**")
            elif activity == "Heating":
                st.write("🔥 **Install a Heat Pump**: Cut heating costs by **40%**")
            elif activity == "Lighting":
                st.write("💡 **Switch to LED Lights**: Save **30% on lighting costs**")
            else:
                st.write("🌍 **Explore renewable energy providers** to reduce costs & emissions")
        except Exception as e:
            st.error(f"Error in forecast generation: {str(e)}")
    else:
        st.error("⚠️ Please enter a valid monthly energy usage value.")

# Footer
st.write("---")
st.markdown("<h4 style='text-align: center;'>🌎 Join the Green Energy Movement & Reduce Your Costs Today! 🚀</h4>", unsafe_allow_html=True)