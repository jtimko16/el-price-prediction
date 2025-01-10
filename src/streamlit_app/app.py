import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sys
from pathlib import Path

# Add the 'src' directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fun.api_f import fetch_nordpool_data, get_weather_forecast

# Dropdown for country selection
country_mapping = {
    "Estonia": "EE",
    "Finland": "FI",
    "Latvia": "LT",
}
selected_country_display = st.selectbox("Select a Country:", options=list(country_mapping.keys()))
selected_country = country_mapping[selected_country_display]

# Fetch and display Nordpool data
st.write(f"### Nordpool Day-Ahead Electricity Prices for {selected_country_display}")

try:
    df_nordpool = fetch_nordpool_data(area=selected_country)
    day_price = df_nordpool["hour"].dt.strftime("%B-%d").iloc[2]
    df_nordpool.insert(1,"day_time",df_nordpool["hour"].dt.strftime("%b-%d %H:%M"))
except:
    st.error("Failed to fetch Nordpool data. Please try again later.")
    st.stop()



## Split into two columns (first for Nordpool data and second for visualization)
col1, col2 = st.columns(2) 
with col1:
    st.write("**Nordpool Electricity Prices**")
    st.dataframe(df_nordpool[['day_time', 'electricity_price']]) # Display the data

with col2:
    fig, ax = plt.subplots()
    df_nordpool["electricity_price"] = df_nordpool["electricity_price"].astype(float)

    ## Extract the day prices only hour from hour field
    df_nordpool["hour"] = df_nordpool["hour"].dt.strftime("%H")
    df_nordpool = df_nordpool.set_index("hour")
    df_nordpool.plot(kind="bar", ax=ax)
    plt.xticks(rotation=90)
    ## Y label 
    plt.ylabel("Electricity Price (€/MWh)")

    plt.title(f"Nordpool Electricity Prices {selected_country_display} - {day_price}")

    # Use st.pyplot() to display the plot
    st.pyplot(fig)

# Input for custom latitude and longitude
st.sidebar.header("Weather Location:")
default_latitude = 59.437
default_longitude = 24.7535
latitude = st.sidebar.number_input("Enter Latitude:", value=default_latitude, format="%.2f")
longitude = st.sidebar.number_input("Enter Longitude:", value=default_longitude, format="%.2f")

weather_variable = st.sidebar.selectbox(
    "Select Weather Variable to innclude in Plot:",
    options=["wind_speed_10m", "temperature_2m", "direct_radiation"]
)

# Button to fetch weather data
if st.sidebar.button("Fetch Weather Data"):
    df_weather_forecast = get_weather_forecast(latitude, longitude)

    # Merge Nordpool and Weather data on hour
    df_merged = pd.merge(df_nordpool, df_weather_forecast, on="hour", how="inner")
    df_weather_forecast["hour"] = df_weather_forecast["hour"].dt.strftime("%b-%d %H:%M")

   
    st.write("### Merged Data")
    st.dataframe(df_merged) # Display the merged data
    

st.write("### Data Visualization")


if df_merged.empty:
    fig, ax = plt.subplots()
    df_nordpool["electricity_price"] = df_nordpool["electricity_price"].astype(float)

    ## Extract the day prices only hour from hour field
    df_nordpool["hour"] = df_nordpool["hour"].dt.strftime("%H")
    df_nordpool = df_nordpool.set_index("hour")
    df_nordpool.plot(kind="bar", ax=ax)
    plt.xticks(rotation=90)
    ## Y label 
    plt.ylabel("Electricity Price (€/MWh)")

    plt.title(f"Nordpool Electricity Prices {selected_country_display} - {day_price}")

    # Use st.pyplot() to display the plot
    st.pyplot(fig)

else:
    fig = px.line(df_merged, x="hour", y=weather_variable, title=f"{weather_variable} Forecast")
    st.plotly_chart(fig)