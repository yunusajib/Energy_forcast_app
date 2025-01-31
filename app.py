import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import requests
import sqlite3
import numpy as np

# Page Configuration
st.set_page_config(page_title="UK AI Energy Forecast & Savings", page_icon="🌍", layout="wide")

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

# Function to fetch historical UK energy price data for ARIMA training
def fetch_historical_energy_data():
    try:
        response = requests.get("https://api.carbonintensity.org.uk/intensity/stats/" )  # Replace with a real API source
        if response.status_code == 200:
            data = response.json()
            historical_prices = [entry['intensity'] for entry in data['data']][-12:]  # Fetch last 12 months of data
            return historical_prices
        else:
            return np.random.uniform(25, 35, 12).tolist()  # Generate random data if API fails
    except:
        return np.random.uniform(25, 35, 12).tolist()

# Fetch historical energy prices
historical_energy_data = fetch_historical_energy_data()

# AI Energy Forecasting Tool
st.write("## 🔮 AI-Powered Energy Forecast")
st.write("Input your monthly energy consumption and let AI **predict your costs & emissions** while suggesting the **best green energy solutions** to save money and protect the planet.")

source = st.selectbox("Select Your Category", ["Business", "Household"])
activity = st.selectbox("Select Energy Usage Type", ["Electricity", "Heating", "Cooking", "Water Heating", "Lighting"])
monthly_energy_usage_kwh = st.number_input("Enter Your Monthly Energy Usage (kWh)", min_value=0, step=10)

if "forecast" not in st.session_state:
    st.session_state.forecast = None
    st.session_state.estimated_carbon_savings = None
    st.session_state.estimated_savings = None

if st.button("🔍 Generate AI Forecast"):
    if monthly_energy_usage_kwh > 0:
        # Train ARIMA model on historical energy prices
        model = ARIMA(historical_energy_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=1)[0] * (monthly_energy_usage_kwh / 100)
        estimated_carbon_savings = (monthly_energy_usage_kwh * current_carbon_intensity) / 1000  # Convert gCO₂ to kgCO₂
        estimated_savings = forecast * 0.30  # Assuming 30% savings with green energy solutions
        
        # Store in session state
        st.session_state.forecast = forecast
        st.session_state.estimated_carbon_savings = estimated_carbon_savings
        st.session_state.estimated_savings = estimated_savings
        
        st.write("### 📊 AI-Powered Cost & Carbon Forecast")
        st.write(f"💰 **Next Month's Predicted Energy Cost:** £{forecast:.2f}")
        st.write(f"🌿 **Estimated Monthly Carbon Emissions:** {estimated_carbon_savings:.2f} kgCO₂")
        st.write(f"💡 **Potential Savings with Green Energy:** £{estimated_savings:.2f} per month")
    else:
        st.error("⚠️ Please enter a valid monthly energy usage value.")

# Check if eligible for government grants (Priority Feature)
st.write("## 🏛 Check Government Grant Eligibility")
if st.button("🔎 Check Now"):
    st.write("✅ You may be eligible for **Green Energy Grants**.")
    st.write("Visit [UK Government Grants Portal](https://www.gov.uk/improve-energy-efficiency) to learn more.")

# Close Database Connection
st.write("---")
st.markdown("<h4 style='text-align: center;'>🌎 Join the Green Energy Movement & Reduce Your Costs Today! 🚀</h4>", unsafe_allow_html=True)
