from nordpool import elspot
import pandas as pd
import requests

def fetch_nordpool_data(area: str = "EE")->pd.DataFrame:
    """Fetch one day ahead electricity prices for a specific aread/country
    
    Args:
        area (str): Two letter country code"""
    # Create an instance of the elspot API
    prices_spot = elspot.Prices()
    
    # Fetch hourly prices for today
    data = prices_spot.hourly(areas=[area])

    # Extract data for the specific area
    area_data_dictionary = data["areas"].get(area, {})
    area_df = pd.DataFrame(area_data_dictionary["values"])

    ## Change timezone to CET (UTC+1)
    area_df["start"] = pd.to_datetime(area_df["start"]).dt.tz_convert("CET")
    
    ## Rename start column to hour and remove end
    area_df = area_df.rename(columns={"start": "hour"})
    area_df = area_df.drop(columns=["end"])

    ## Rename value to electricity_price
    area_df = area_df.rename(columns={"value": "electricity_price"})

    return area_df


def get_weather_forecast(latitude: float = 59.437, longitude: float = 24.7535)->pd.DataFrame:
    """Fetch weather forecast for a specific location
    
    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,direct_radiation,diffuse_radiation",
        "timezone": "CET"  # Directly request data in CET
    }

    # Fetch weather data
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    data = response.json()

    # Extract hourly data
    hourly_data = data.get("hourly", {})
    times = hourly_data.get("time", [])
    temperature_2m = hourly_data.get("temperature_2m", [])
    wind_speed_10m = hourly_data.get("wind_speed_10m", [])
    direct_radiation = hourly_data.get("direct_radiation", [])
    diffuse_radiation = hourly_data.get("diffuse_radiation", [])

    # Create a DataFrame
    df = pd.DataFrame({
        "hour": pd.to_datetime(times),  # Convert times to datetime
        "temperature_2m": temperature_2m,
        "wind_speed_10m": wind_speed_10m,
        "direct_radiation": direct_radiation,
        "diffuse_radiation": diffuse_radiation,
    })

    # Ensure timezone is CET
    df["hour"] = df["hour"].dt.tz_localize("CET")
    return df
