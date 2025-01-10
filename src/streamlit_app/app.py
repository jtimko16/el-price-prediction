import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
selected_country_display = st.selectbox(
    "Select a Country:", options=list(country_mapping.keys())
)
selected_country = country_mapping[selected_country_display]

# Fetch and display Nordpool data
st.write(f"### Nordpool Day-Ahead Electricity Prices for {selected_country_display}")

try:
    df_nordpool = fetch_nordpool_data(area=selected_country)
    day_price = (
        df_nordpool["datetime"].dt.strftime("%B-%d").iloc[2]
    )  ## Day of the day-ahead price
    df_nordpool.insert(
        1, "day_time", df_nordpool["datetime"].dt.strftime("%b-%d %H:%M")
    )
except:
    st.error("Failed to fetch Nordpool data. Please try again later.")
    st.stop()


## Split into two columns (first for Nordpool data and second for visualization)
col1, col2 = st.columns(2)
with col1:
    st.write("**Nordpool Electricity Prices**")
    st.dataframe(df_nordpool[["day_time", "electricity_price"]])  # Display the data

with col2:
    fig, ax = plt.subplots()
    df_nordpool["electricity_price"] = df_nordpool["electricity_price"].astype(float)

    ## Extract the day prices only hour from hour field
    df_nordpool["hour"] = df_nordpool["datetime"].dt.strftime("%H")
    df_nordpool = df_nordpool.set_index("hour")
    df_nordpool["electricity_price"].plot(kind="bar", ax=ax)
    plt.xticks(rotation=90)
    ## Y label
    plt.ylabel("Electricity Price (€/MWh)")

    plt.title(f"Nordpool Electricity Prices {selected_country_display} - {day_price}")

    # Use st.pyplot() to display the plot
    st.pyplot(fig)


##-----------Weather Data-----------------##

# Sidebar for user input
# Input for custom latitude and longitude
st.sidebar.header("Weather Location:")
default_latitude = 59.437
default_longitude = 24.7535
latitude = st.sidebar.number_input(
    "Enter Latitude:", value=default_latitude, format="%.2f"
)
longitude = st.sidebar.number_input(
    "Enter Longitude:", value=default_longitude, format="%.2f"
)

weather_variable = st.sidebar.selectbox(
    "Select Weather Variable to innclude in Plot:",
    options=["wind_speed_10m", "temperature_2m", "direct_radiation"],
)

# Button to fetch weather data
if st.sidebar.button("Fetch Weather Data"):
    try:
        df_weather_forecast = get_weather_forecast(latitude, longitude)

        # Merge Nordpool and Weather data on hour
        df_merged = pd.merge(
            df_nordpool, df_weather_forecast, on="datetime", how="inner"
        )
        df_weather_forecast["day_time"] = df_weather_forecast["datetime"].dt.strftime(
            "%b-%d %H:%M"
        )

        st.write("#### Electricity Price and Weather Visualization")
        # Create a figure and a set of subplots
        fig, ax1 = plt.subplots(figsize=(12, 6))  # Adjust size for clarity

        df_merged["hour"] = df_merged["datetime"].dt.strftime("%H")
        # Plot electricity prices as bars
        ax1.bar(
            df_merged["hour"],
            df_merged["electricity_price"],
            color="blue",
            alpha=0.7,
            label="Electricity Price",
        )
        ax1.set_xlabel("Hour")
        ax1.set_ylabel("Electricity Price (€/MWh)", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")
        plt.xticks(rotation=90)

        # Add a secondary y-axis for the weather variable
        ax2 = ax1.twinx()
        ax2.plot(
            df_merged["hour"],
            df_merged[weather_variable],  # Replace with the weather variable column
            color="red",
            label=weather_variable,
            marker="o",
        )
        ax2.set_ylabel(weather_variable, color="red")
        ax2.tick_params(axis="y", labelcolor="red")

        # Add title and legends
        plt.title(f"Electricity Price and Weather")
        fig.tight_layout()

        # Display the plot
        st.pyplot(fig)

        st.write("##### Merged Data")
        st.dataframe(df_merged)  # Display the merged data

    except:
        st.error("Failed to fetch weather data. Please try again later.")
