import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import sys
from pathlib import Path

# Add the 'src' directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fun.api_f import fetch_nordpool_data, get_weather_forecast

# Define default latitude and longitude
default_latitude = 59.437
default_longitude = 24.7535

# Streamlit app
st.title("Electricity Prices and Weather Forecast Viewer")
st.write("Explore electricity prices and weather forecasts dynamically.")

# Input for custom latitude and longitude
st.sidebar.header("Input Parameters")
latitude = st.sidebar.number_input("Enter Latitude:", value=default_latitude, format="%.6f")
longitude = st.sidebar.number_input("Enter Longitude:", value=default_longitude, format="%.6f")

# Fetch data
st.write("### Nordpool Electricity Prices")
df_nordpool = fetch_nordpool_data(area="EE")
st.write(df_nordpool)

# Fetch weather forecast
df_weather_forecast = get_weather_forecast(latitude, longitude)
st.write("### Weather Forecast")
st.write(df_weather_forecast)

# Plot electricity prices
def plot_prices(data):
    fig, ax = plt.subplots()
    ax.plot(data["end"], data["price"], marker="o", label="Price (€/MWh)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (€/MWh)")
    ax.set_title("Nordpool Electricity Prices")
    ax.legend()
    st.pyplot(fig)

# Plot weather data
def plot_weather(data):
    fig, ax = plt.subplots()
    ax.plot(data["datetime"], data["temperature"], marker="o", label="Temperature (°C)")
    ax.plot(data["datetime"], data["wind_speed"], marker="x", label="Wind Speed (m/s)")
    ax.set_xlabel("Time")
    ax.set_title("Weather Forecast")
    ax.legend()
    st.pyplot(fig)

# Visualizations
plot_prices(df_nordpool)
plot_weather(df_weather_forecast)

st.write("### Input Summary")
st.write(f"Latitude: {latitude}, Longitude: {longitude}")