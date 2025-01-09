def fetch_nordpool_data(area: str = "EE"):
    """Fetch Nord Pool electricity prices for a specific area."""
    # Create an instance of the elspot API
    prices_spot = elspot.Prices()
    
    # Fetch hourly prices for today
    data = prices_spot.hourly(areas=[area])

    # Extract data for the specific area
    area_data = data["areas"].get(area, {})
    print(f"Prices for {area}: {area_data}")
    return area_data