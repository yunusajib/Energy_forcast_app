import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import requests
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="UK AI Energy Forecast & Savings",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Move styles to a separate function for better organization
def load_custom_styles():
    return """
        <style>
        .main {background-color: #f4f4f4;}
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        }
        .stSelectbox, .stRadio, .stTextInput, .stFileUploader {
            border-radius: 10px;
        }
        .highlight {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            padding: 10px;
            margin: 10px 0;
        }
        </style>
    """

# Improved error handling for API calls
def get_live_energy_data():
    default_values = (30, 200)  # Default price and carbon intensity
    try:
        # Add timeout to prevent hanging
        energy_price_response = requests.get(
            "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-7-Day/standard-unit-rates/",
            timeout=5
        )
        carbon_intensity_response = requests.get(
            "https://api.carbonintensity.org.uk/intensity",
            timeout=5
        )

        if energy_price_response.status_code == 200 and carbon_intensity_response.status_code == 200:
            energy_data = energy_price_response.json()
            carbon_data = carbon_intensity_response.json()
            
            if "results" in energy_data and energy_data["results"]:
                price = energy_data["results"][0].get("value_inc_vat", default_values[0])
            else:
                price = default_values[0]
                
            if "data" in carbon_data and carbon_data["data"]:
                intensity = carbon_data["data"][0].get("intensity", {}).get("actual", default_values[1])
            else:
                intensity = default_values[1]
                
            return price, intensity
    except requests.RequestException as e:
        st.warning(f"Could not fetch live data: {str(e)}")
    return default_values

# Main application
def main():
    # Load custom styles
    st.markdown(load_custom_styles(), unsafe_allow_html=True)
    
    # Title
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 AI Energy Cost & Carbon Forecast</h1>", unsafe_allow_html=True)
    
    # Get live energy data
    current_price_p_kwh, current_carbon_intensity = get_live_energy_data()
    
    # Display current stats in columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='highlight'>💡 Current UK Electricity Price: {current_price_p_kwh:.2f} p/kWh</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='highlight'>🌍 Current Carbon Intensity: {current_carbon_intensity} gCO₂/kWh</div>", unsafe_allow_html=True)

    # Rest of your existing code...
    # (Keep the existing functionality but wrapped in the main function)

if __name__ == "__main__":
    main()