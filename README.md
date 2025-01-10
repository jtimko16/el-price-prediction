## Nordpool Electricity Prices with Weather Visualization

This repository contains a simple Streamlit app that accesses one-day-ahead electricity prices (for selected countries: Finland, Estonia, or Latvia) and fetches the weather forecast for a specified location. The app visualizes the data for easy exploration.

It also includes a Python notebook for connecting to the API and performing data exploration.

#### Dependencies
The code was tested with Python 3.11 on a Windows machine. All dependencies are specified in the `requirements.txt` file.

#### Deployment

You can access the deployed version of the app at:

[https://nordpool-price-with-weather.streamlit.app/](https://nordpool-price-with-weather.streamlit.app/)

#### Running Locally

To run the app locally, use the following command in your terminal:

```bash
streamlit run src/streamlit_app/app.py

