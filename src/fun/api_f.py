from nordpool import elspot
import pandas as pd

def fetch_nordpool_data(area: str = "EE"):
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
    return area_df
